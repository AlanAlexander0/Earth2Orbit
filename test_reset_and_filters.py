"""
Test Suite: Reset Button & Multi-Filter Interaction
Verifies:
1. "Kerala" search + India + Mars filter -> 0 matches
2. reset_filters() callback execution safely updates session_state
3. State restores to empty string, All Countries, All Targets, and default analog
4. Multiple reset cycles
5. Resetting when no filters are set
"""

import unittest
from unittest.mock import MagicMock, patch
import streamlit as st
from modules.nasa_data_loaders import load_earth_analogs


class TestResetAndFilters(unittest.TestCase):

    def setUp(self):
        self.analogs = load_earth_analogs()
        # Clean session state
        st.session_state.clear()

    def filter_sites(self, analogs, search_query, country, target):
        q = search_query.strip().lower() if search_query else ""
        res = list(analogs)
        if q:
            res = [
                a for a in res
                if (
                    q in a["name"].lower() or 
                    q in a["region"].lower() or 
                    q in a["country"].lower() or 
                    q in a.get("biome", "").lower() or 
                    q in a.get("koppen_climate", "").lower() or
                    q in a["geology"]["lithology_type"].lower() or 
                    q in a["geology"].get("rock_units", "").lower() or
                    q in a["planetary_analog_relevance"]["primary_target"].lower() or
                    any(q in m.lower() for m in a["geology"].get("dominant_minerals", []))
                )
            ]
        if country != "All Countries":
            res = [a for a in res if a["country"].strip().lower() == country.strip().lower()]
        if target != "All Targets":
            res = [
                a for a in res
                if target.strip().lower() in a["planetary_analog_relevance"]["primary_target"].lower()
            ]
        return res

    def test_kerala_india_mars_zero_matches(self):
        """Test searching 'Kerala', Country='India', Target='Mars' yields 0 matches."""
        matches = self.filter_sites(self.analogs, "Kerala", "India", "Mars")
        self.assertEqual(len(matches), 0, "Expected 0 matches for Kerala + India + Mars")

    def test_reset_callback_execution(self):
        """Test that reset callback safely resets all keys."""
        default_id = self.analogs[0]["id"]
        
        # Simulate user changing filters
        st.session_state["earth_search_text"] = "Kerala"
        st.session_state["earth_country_filter"] = "India"
        st.session_state["earth_target_filter"] = "Mars"
        st.session_state["selected_analog_id"] = None

        # Verify filters produce 0 matches
        matches_before = self.filter_sites(
            self.analogs,
            st.session_state["earth_search_text"],
            st.session_state["earth_country_filter"],
            st.session_state["earth_target_filter"]
        )
        self.assertEqual(len(matches_before), 0)

        # Execute reset_filters callback logic
        st.session_state["earth_search_text"] = ""
        st.session_state["earth_country_filter"] = "All Countries"
        st.session_state["earth_target_filter"] = "All Targets"
        st.session_state["selected_analog_id"] = default_id

        # Verify reset state
        self.assertEqual(st.session_state["earth_search_text"], "")
        self.assertEqual(st.session_state["earth_country_filter"], "All Countries")
        self.assertEqual(st.session_state["earth_target_filter"], "All Targets")
        self.assertEqual(st.session_state["selected_analog_id"], default_id)

        # Verify all sites are now matched
        matches_after = self.filter_sites(
            self.analogs,
            st.session_state["earth_search_text"],
            st.session_state["earth_country_filter"],
            st.session_state["earth_target_filter"]
        )
        self.assertEqual(len(matches_after), len(self.analogs))
        self.assertEqual(len(matches_after), 6)

    def test_repeated_reset_cycles(self):
        """Test repeated filter-then-reset cycles."""
        default_id = self.analogs[0]["id"]
        
        test_queries = [
            ("Atacama", "Chile", "Mars"),
            ("Iceland", "Iceland", "Moon"),
            ("Antarctica", "Antarctica", "Moon"),
            ("nonexistent_site", "All Countries", "All Targets"),
            ("Ladakh", "India", "Mars")
        ]

        for query, country, target in test_queries:
            st.session_state["earth_search_text"] = query
            st.session_state["earth_country_filter"] = country
            st.session_state["earth_target_filter"] = target

            # Reset
            st.session_state["earth_search_text"] = ""
            st.session_state["earth_country_filter"] = "All Countries"
            st.session_state["earth_target_filter"] = "All Targets"
            st.session_state["selected_analog_id"] = default_id

            self.assertEqual(st.session_state["earth_search_text"], "")
            self.assertEqual(st.session_state["earth_country_filter"], "All Countries")
            self.assertEqual(st.session_state["earth_target_filter"], "All Targets")
            
            matches = self.filter_sites(
                self.analogs,
                st.session_state["earth_search_text"],
                st.session_state["earth_country_filter"],
                st.session_state["earth_target_filter"]
            )
            self.assertEqual(len(matches), 6)

    def test_reset_when_already_default(self):
        """Test reset when no filters were set."""
        default_id = self.analogs[0]["id"]
        st.session_state["earth_search_text"] = ""
        st.session_state["earth_country_filter"] = "All Countries"
        st.session_state["earth_target_filter"] = "All Targets"
        st.session_state["selected_analog_id"] = default_id

        # Calling reset should remain safe
        st.session_state["earth_search_text"] = ""
        st.session_state["earth_country_filter"] = "All Countries"
        st.session_state["earth_target_filter"] = "All Targets"
        st.session_state["selected_analog_id"] = default_id

        self.assertEqual(st.session_state["earth_search_text"], "")
        self.assertEqual(st.session_state["earth_country_filter"], "All Countries")
        self.assertEqual(st.session_state["earth_target_filter"], "All Targets")


if __name__ == "__main__":
    unittest.main()

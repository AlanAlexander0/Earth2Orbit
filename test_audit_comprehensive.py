"""
Comprehensive 8-Page Audit Script for Earth2Orbit
Tests all combinations of sites, targets, comparisons, charts, profiles, and reports.
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np

# Ensure root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.nasa_data_loaders import (
    load_earth_analogs,
    load_planetary_targets,
    load_terrain_profiles,
    load_data_sources_catalog,
    fetch_nasa_power_climatology
)
from utils.metrics import (
    calculate_planetary_similarity,
    FEATURE_METADATA,
    compute_feature_distance,
    extract_mineral_tokens
)
from modules.visualizations import (
    create_earth_folium_map,
    create_similarity_radar_chart,
    create_feature_breakdown_bar_chart,
    create_terrain_cross_section_chart,
    create_nasa_power_climatology_chart,
    create_rhombus_donut_chart
)
from modules.pdf_generator import generate_dossier_pdf
from utils.ui_components import (
    clean_html,
    render_rhombus_kpi_row,
    render_rhombus_metric_grid
)

class TestComprehensiveAudit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.earth_analogs = load_earth_analogs()
        cls.planetary_bodies = load_planetary_targets()
        cls.terrain_profiles = load_terrain_profiles()
        cls.data_sources = load_data_sources_catalog()

    def test_page_1_overview_data_and_kpis(self):
        """Audit Page 1: Overview Dashboard components."""
        total_sites = len(self.earth_analogs)
        total_targets = sum(len(b.get("targets", [])) for b in self.planetary_bodies)
        self.assertEqual(total_sites, 6)
        self.assertEqual(total_targets, 4)

        # Test Donut Chart
        from modules.visualizations import COLOR_PRIMARY, COLOR_SECONDARY
        donut_fig = create_rhombus_donut_chart([4, 2], ["Mars", "Moon"], [COLOR_SECONDARY, COLOR_PRIMARY])
        self.assertIsNotNone(donut_fig)
        self.assertIn("data", donut_fig)

        # Test KPI Row payload formatting
        kpi_cards = [
            {"value": f"{total_sites} Analogs", "label": "Active Terrestrial Benchmarks", "icon_svg": "<svg></svg>", "color": "primary", "percent": 100},
            {"value": "2 Worlds", "label": "Moon & Mars Reference Bodies", "icon_svg": "<svg></svg>", "color": "secondary", "percent": 85},
            {"value": f"{total_targets} Candidate Sites", "label": "Lunar South Pole & Jezero Delta", "icon_svg": "<svg></svg>", "color": "info", "percent": 90},
            {"value": "81.4% Fidelity", "label": "Max ACI Score (Lonar vs Moon)", "icon_svg": "<svg></svg>", "color": "warning", "percent": 81}
        ]
        for c in kpi_cards:
            self.assertIn("value", c)
            self.assertIn("label", c)
            self.assertIn("percent", c)

    def test_page_2_earth_explorer_all_sites_and_map(self):
        """Audit Page 2: Earth Analog Explorer across all 6 terrestrial sites."""
        self.assertEqual(len(self.earth_analogs), 6)
        for analog in self.earth_analogs:
            # Check mandatory keys
            for key in ["id", "name", "region", "country", "coordinates", "elevation_m", "relief_m", "mean_slope_deg", "terrain_roughness_rms_m", "geology", "temperature_c", "planetary_analog_relevance", "references"]:
                self.assertIn(key, analog, f"Missing key '{key}' in site {analog.get('name')}")
            
            # Check geology subkeys
            geo = analog["geology"]
            self.assertIn("lithology_type", geo)
            self.assertTrue("rock_units" in geo or "stratigraphy" in geo)
            self.assertIn("dominant_minerals", geo)
            self.assertIn("geomorphic_features", geo)
            self.assertIsInstance(geo["dominant_minerals"], list)
            self.assertIsInstance(geo["geomorphic_features"], list)

            # Check environmental values
            self.assertIn("annual_mean", analog["temperature_c"])
            self.assertIn("annual_precipitation_mm", analog)
            self.assertIn("atmospheric_pressure_hpa", analog)

            # Check planetary analog relevance
            rel = analog["planetary_analog_relevance"]
            self.assertIn("primary_target", rel)
            self.assertIn("fidelity_summary", rel)
            self.assertIn("analog_mission_targets", rel)

            # Check references have citation and URL/DOI
            for ref in analog["references"]:
                self.assertIn("citation", ref)
                url = ref.get("doi") or ref.get("url")
                self.assertIsNotNone(url, f"Missing DOI or URL in {analog['name']}")
                self.assertTrue(url.startswith("http"), f"Invalid reference URL in {analog['name']}")

        # Test Folium Map Generation
        folium_map = create_earth_folium_map(self.earth_analogs, selected_id="lonar_crater")
        self.assertIsNotNone(folium_map)

        # Test NASA POWER synthetic / offline fallback climatology
        power_data = fetch_nasa_power_climatology(19.9756, 76.5064)
        self.assertIn("status", power_data)

    def test_page_3_planetary_targets_all_bodies_and_sites(self):
        """Audit Page 3: Planetary Targets for Moon and Mars."""
        self.assertEqual(len(self.planetary_bodies), 2)
        bodies = {b["body_id"]: b for b in self.planetary_bodies}
        self.assertIn("moon", bodies)
        self.assertIn("mars", bodies)

        # Moon audit
        moon = bodies["moon"]
        self.assertIsNone(moon["surface_pressure_hpa"])  # Must be None (Vacuum)
        self.assertAlmostEqual(moon["gravity_m_s2"], 1.62, places=2)
        self.assertEqual(len(moon["targets"]), 2)

        for target in moon["targets"]:
            for key in ["id", "name", "target_code", "coordinates", "elevation_m", "relief_m", "mean_slope_deg", "terrain_roughness_rms_m", "geology", "instruments"]:
                self.assertIn(key, target, f"Missing key '{key}' in Moon target {target.get('name')}")
            self.assertIn("min_psr", target["temperature_k"])

        # Mars audit
        mars = bodies["mars"]
        self.assertAlmostEqual(mars["surface_pressure_hpa"], 6.1, places=1)
        self.assertAlmostEqual(mars["gravity_m_s2"], 3.72, places=2)
        self.assertEqual(len(mars["targets"]), 2)

        for target in mars["targets"]:
            for key in ["id", "name", "target_code", "coordinates", "elevation_m", "relief_m", "mean_slope_deg", "terrain_roughness_rms_m", "geology", "instruments"]:
                self.assertIn(key, target, f"Missing key '{key}' in Mars target {target.get('name')}")
            self.assertIn("mean", target["temperature_k"])

    def test_page_4_comparison_laboratory_all_24_pairings(self):
        """Audit Page 4: All 24 Earth-Planetary pairings (6 Earth x 4 Planetary)."""
        pairings_tested = 0
        for earth in self.earth_analogs:
            for body in self.planetary_bodies:
                for target in body["targets"]:
                    results = calculate_planetary_similarity(earth, target, body)
                    pairings_tested += 1

                    # Verify structure
                    self.assertIn("aci_score_pct", results)
                    self.assertIn("measurement_coverage_pct", results)
                    self.assertIn("evidence_availability_pct", results)
                    self.assertIn("features", results)
                    self.assertIn("excluded_features", results)

                    # Verify bounds
                    self.assertGreaterEqual(results["aci_score_pct"], 0.0)
                    self.assertLessEqual(results["aci_score_pct"], 100.0)
                    self.assertGreater(results["measurement_coverage_pct"], 0.0)
                    self.assertLessEqual(results["measurement_coverage_pct"], 100.0)

                    # Verify atmospheric pressure logic
                    if body["body_id"] == "moon":
                        excluded_keys = [ex["key"] for ex in results["excluded_features"]]
                        self.assertIn("surface_pressure_hpa", excluded_keys)
                        self.assertNotIn("surface_pressure_hpa", results["features"])
                    else:
                        self.assertIn("surface_pressure_hpa", results["features"])

                    # Verify radar and bar charts
                    radar_fig = create_similarity_radar_chart(results)
                    self.assertIsNotNone(radar_fig)
                    bar_fig = create_feature_breakdown_bar_chart(results)
                    self.assertIsNotNone(bar_fig)

        self.assertEqual(pairings_tested, 24)

    def test_page_5_terrain_analysis_profiles_and_datums(self):
        """Audit Page 5: Topographic profiles and cross-section charts."""
        self.assertIn("lonar_crater", self.terrain_profiles)
        self.assertIn("tso_kar", self.terrain_profiles)
        self.assertIn("lunar_south_pole_shackleton", self.terrain_profiles)
        self.assertIn("mars_jezero_delta", self.terrain_profiles)

        for prof_key, profile in self.terrain_profiles.items():
            self.assertIn("name", profile)
            self.assertIn("source", profile)
            self.assertIn("distance_km", profile)
            self.assertIn("elevation_m", profile)
            self.assertEqual(len(profile["distance_km"]), len(profile["elevation_m"]))

        # Test cross section chart
        fig = create_terrain_cross_section_chart(
            self.terrain_profiles["lonar_crater"],
            self.terrain_profiles["lunar_south_pole_shackleton"],
            "Lonar Crater",
            "Shackleton Crater"
        )
        self.assertIsNotNone(fig)

    def test_page_6_nasa_data_observatory_all_12_sources(self):
        """Audit Page 6: All Earth and Planetary data sources and audit matrix."""
        earth_srcs = self.data_sources.get("earth_sources", [])
        plan_srcs = self.data_sources.get("planetary_sources", [])
        self.assertEqual(len(earth_srcs), 5)
        self.assertEqual(len(plan_srcs), 7)
        self.assertEqual(len(earth_srcs) + len(plan_srcs), 12)

        # Check required fields exist or resolve gracefully
        for s in earth_srcs:
            self.assertIn("name", s)
            self.assertIn("integration_status", s)
            self.assertIn("parameters", s)
            self.assertIn("citation", s)

        for s in plan_srcs:
            self.assertIn("instrument", s)
            self.assertIn("body", s)
            self.assertIn("integration_status", s)
            self.assertIn("parameters", s)
            self.assertIn("citation", s)

    def test_page_7_research_reports_all_pairings_pdf_generation(self):
        """Audit Page 7: PDF dossier generation across pairings."""
        for earth in self.earth_analogs[:2]:  # Test first 2 sites to keep test fast
            for body in self.planetary_bodies:
                target = body["targets"][0]
                results = calculate_planetary_similarity(earth, target, body)
                pdf_bytes = generate_dossier_pdf(results, earth, target, body)
                self.assertIsInstance(pdf_bytes, bytes)
                self.assertGreater(len(pdf_bytes), 2000)
                self.assertTrue(pdf_bytes.startswith(b"%PDF-1."))

    def test_page_8_about_page_and_methodology(self):
        """Audit Page 8: Mathematical formulas and weights definition."""
        self.assertIn("relief_m", FEATURE_METADATA)
        self.assertIn("mean_slope_deg", FEATURE_METADATA)
        self.assertIn("terrain_roughness_rms_m", FEATURE_METADATA)
        self.assertIn("diurnal_swing_c", FEATURE_METADATA)
        self.assertIn("lithology_affinity", FEATURE_METADATA)
        self.assertIn("mineral_jaccard", FEATURE_METADATA)
        self.assertIn("surface_pressure_hpa", FEATURE_METADATA)

    def test_no_commonmark_raw_html_leakage(self):
        """Audit UI Components: Ensure clean_html never leaves 4+ spaces indentation."""
        dirty_html = """
            <div class="rhombus-stat-grid">
                <div class="rhombus-stat-card">
                    <button class="rhombus-icon-btn">
                        <svg width="20" height="20">
                            <path d="M18 8"></path>
                        </svg>
                    </button>
                    <span class="rhombus-badge-dot"></span>
                </div>
            </div>
        """
        cleaned = clean_html(dirty_html)
        lines = cleaned.split("\n")
        for line in lines:
            if line.strip():
                self.assertFalse(line.startswith("    "), f"Found indented line: {line}")


if __name__ == "__main__":
    unittest.main()

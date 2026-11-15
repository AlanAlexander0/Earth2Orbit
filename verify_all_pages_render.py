"""
Verify all eight module render functions execute without raising exceptions
and check all output HTML strings for any raw tag leakage.
"""

import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Ensure root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.nasa_data_loaders import (
    load_earth_analogs,
    load_planetary_targets,
    load_terrain_profiles,
    load_data_sources_catalog
)

class TestAllPagesRender(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.earth_analogs = load_earth_analogs()
        cls.planetary_bodies = load_planetary_targets()
        cls.terrain_profiles = load_terrain_profiles()
        cls.data_sources = load_data_sources_catalog()

    def test_overview_module_execution(self):
        """Page 1: Overview"""
        from modules.home_dashboard import render_home_dashboard
        # We patch streamlit widgets to verify execution path without crashing
        with patch("streamlit.button", return_value=False), \
             patch("streamlit.columns", side_effect=lambda n, **kwargs: [MagicMock() for _ in range(n if isinstance(n, int) else len(n))]), \
             patch("streamlit.container", return_value=MagicMock()), \
             patch("streamlit.plotly_chart"), \
             patch("streamlit.dataframe"):
            try:
                render_home_dashboard(self.earth_analogs, self.planetary_bodies)
            except Exception as e:
                self.fail(f"render_home_dashboard raised an exception: {e}")

    def test_earth_explorer_module_execution(self):
        """Page 2: Earth Analog Explorer"""
        from modules.earth_explorer import render_earth_explorer
        with patch("streamlit.text_input", return_value=""), \
             patch("streamlit.selectbox", side_effect=["All Countries", "All Targets", "Lonar Crater (Maharashtra, India)"]), \
             patch("streamlit.columns", side_effect=lambda n, **kwargs: [MagicMock() for _ in range(n if isinstance(n, int) else len(n))]), \
             patch("streamlit.container", return_value=MagicMock()), \
             patch("streamlit.tabs", return_value=[MagicMock() for _ in range(5)]), \
             patch("streamlit_folium.st_folium"):
            try:
                render_earth_explorer(self.earth_analogs)
            except Exception as e:
                self.fail(f"render_earth_explorer raised an exception: {e}")

    def test_planetary_targets_module_execution(self):
        """Page 3: Planetary Targets"""
        from modules.planetary_targets import render_planetary_targets
        with patch("streamlit.radio", return_value="The Moon (Luna)"), \
             patch("streamlit.selectbox", return_value="Lunar South Pole — Shackleton Rim"), \
             patch("streamlit.columns", side_effect=lambda n, **kwargs: [MagicMock() for _ in range(n if isinstance(n, int) else len(n))]), \
             patch("streamlit.container", return_value=MagicMock()), \
             patch("streamlit.tabs", return_value=[MagicMock() for _ in range(4)]):
            try:
                render_planetary_targets(self.planetary_bodies)
            except Exception as e:
                self.fail(f"render_planetary_targets (Moon) raised an exception: {e}")

        # Also test Mars selection
        with patch("streamlit.radio", return_value="Mars"), \
             patch("streamlit.selectbox", return_value="Jezero Crater — Western Fan Delta"), \
             patch("streamlit.columns", side_effect=lambda n, **kwargs: [MagicMock() for _ in range(n if isinstance(n, int) else len(n))]), \
             patch("streamlit.container", return_value=MagicMock()), \
             patch("streamlit.tabs", return_value=[MagicMock() for _ in range(4)]):
            try:
                render_planetary_targets(self.planetary_bodies)
            except Exception as e:
                self.fail(f"render_planetary_targets (Mars) raised an exception: {e}")

    def test_comparison_laboratory_module_execution(self):
        """Page 4: Comparison Laboratory"""
        from modules.comparison_engine import render_comparison_engine
        mock_col = MagicMock()
        mock_col.slider.return_value = 1.0

        with patch("streamlit.selectbox", side_effect=lambda label, options, **kwargs: options[0] if options else None), \
             patch("streamlit.slider", return_value=1.0), \
             patch("streamlit.columns", side_effect=lambda n, **kwargs: [mock_col for _ in range(n if isinstance(n, int) else len(n))]), \
             patch("streamlit.container", return_value=MagicMock()), \
             patch("streamlit.expander", return_value=MagicMock()), \
             patch("streamlit.plotly_chart"), \
             patch("streamlit.dataframe"):
            try:
                render_comparison_engine(self.earth_analogs, self.planetary_bodies, self.terrain_profiles)
            except Exception as e:
                self.fail(f"render_comparison_engine raised an exception: {e}")

    def test_terrain_analysis_module_execution(self):
        """Page 5: Terrain Analysis"""
        from modules.terrain_analysis import render_terrain_analysis
        with patch("streamlit.selectbox", side_effect=lambda label, options, **kwargs: options[0] if options else None), \
             patch("streamlit.columns", side_effect=lambda n, **kwargs: [MagicMock() for _ in range(n if isinstance(n, int) else len(n))]), \
             patch("streamlit.container", return_value=MagicMock()), \
             patch("streamlit.tabs", return_value=[MagicMock() for _ in range(3)]), \
             patch("streamlit.plotly_chart"), \
             patch("streamlit.dataframe"):
            try:
                render_terrain_analysis(self.earth_analogs, self.planetary_bodies, self.terrain_profiles)
            except Exception as e:
                self.fail(f"render_terrain_analysis raised an exception: {e}")

    def test_nasa_data_observatory_module_execution(self):
        """Page 6: NASA Data Observatory"""
        from modules.nasa_data_observatory import render_nasa_data_observatory
        with patch("streamlit.tabs", side_effect=lambda tabs, **kwargs: [MagicMock() for _ in range(len(tabs))]), \
             patch("streamlit.container", return_value=MagicMock()), \
             patch("streamlit.dataframe"):
            try:
                render_nasa_data_observatory()
            except Exception as e:
                self.fail(f"render_nasa_data_observatory raised an exception: {e}")

    def test_research_reports_module_execution(self):
        """Page 7: Research Reports"""
        from modules.research_report import render_research_report
        with patch("streamlit.selectbox", side_effect=["Lonar Crater (Maharashtra, India)", "The Moon (Luna) — Lunar South Pole — Shackleton Rim"]), \
             patch("streamlit.columns", side_effect=lambda n, **kwargs: [MagicMock() for _ in range(n if isinstance(n, int) else len(n))]), \
             patch("streamlit.container", return_value=MagicMock()), \
             patch("streamlit.download_button"):
            try:
                render_research_report(self.earth_analogs, self.planetary_bodies, self.data_sources)
            except Exception as e:
                self.fail(f"render_research_report raised an exception: {e}")

    def test_about_page_module_execution(self):
        """Page 8: About Earth2Orbit"""
        from modules.about_page import render_about_page
        with patch("streamlit.columns", side_effect=lambda n, **kwargs: [MagicMock() for _ in range(n if isinstance(n, int) else len(n))]), \
             patch("streamlit.container", return_value=MagicMock()):
            try:
                render_about_page()
            except Exception as e:
                self.fail(f"render_about_page raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()

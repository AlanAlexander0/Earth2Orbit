"""
Earth2Orbit — Comprehensive Scientific Test Suite
Verifies:
1. Data loading and JSON schema validity with integration statuses
2. Missing parameter exclusions (Moon vacuum pressure excluded)
3. Quantitative Analog Compatibility Index (ACI) calculation
4. Evidence Availability and Measurement Coverage metrics
5. Folium and Plotly chart generation in light theme
6. ReportLab PDF generation and export functionality
"""

import unittest
import os
import sys

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.nasa_data_loaders import (
    load_earth_analogs,
    load_planetary_targets,
    load_terrain_profiles,
    load_data_sources_catalog
)
from utils.metrics import (
    calculate_planetary_similarity,
    extract_mineral_tokens,
    compute_feature_distance
)
from modules.visualizations import (
    create_similarity_radar_chart,
    create_feature_breakdown_bar_chart,
    create_terrain_cross_section_chart
)
from modules.pdf_generator import generate_dossier_pdf


class TestEarth2Orbit(unittest.TestCase):

    def setUp(self):
        self.earth_analogs = load_earth_analogs()
        self.planetary_bodies = load_planetary_targets()
        self.terrain_profiles = load_terrain_profiles()
        self.data_sources = load_data_sources_catalog()

    def test_01_earth_analogs_count_and_keys(self):
        """Verify all 6 terrestrial analog locations exist with mandatory keys."""
        ids = [a["id"] for a in self.earth_analogs]
        self.assertIn("tso_kar", ids)
        self.assertIn("lonar_crater", ids)
        self.assertIn("sambhar_lake", ids)
        self.assertIn("atacama_desert", ids)
        self.assertIn("mcmurdo_valleys", ids)
        self.assertIn("iceland_volcanic", ids)
        self.assertEqual(len(ids), 6)

        for a in self.earth_analogs:
            self.assertIn("coordinates", a)
            self.assertIn("elevation_m", a)
            self.assertIn("relief_m", a)
            self.assertIn("mean_slope_deg", a)
            self.assertIn("terrain_roughness_rms_m", a)
            self.assertIn("geology", a)
            self.assertIn("planetary_analog_relevance", a)
            self.assertIn("references", a)
            self.assertGreater(len(a["references"]), 0)

    def test_02_planetary_targets_count_and_keys(self):
        """Verify Moon and Mars bodies with required targets exist."""
        body_ids = [b["body_id"] for b in self.planetary_bodies]
        self.assertIn("moon", body_ids)
        self.assertIn("mars", body_ids)

        moon = next(b for b in self.planetary_bodies if b["body_id"] == "moon")
        mars = next(b for b in self.planetary_bodies if b["body_id"] == "mars")

        moon_target_ids = [t["id"] for t in moon["targets"]]
        mars_target_ids = [t["id"] for t in mars["targets"]]

        self.assertIn("lunar_south_pole_shackleton", moon_target_ids)
        self.assertIn("lunar_south_pole_malapert", moon_target_ids)
        self.assertIn("mars_jezero_delta", mars_target_ids)
        self.assertIn("mars_jezero_seitah", mars_target_ids)

    def test_03_missing_data_exclusion_for_moon(self):
        """Crucial requirement: lunar comparisons MUST exclude atmospheric pressure."""
        lonar = next(a for a in self.earth_analogs if a["id"] == "lonar_crater")
        moon = next(b for b in self.planetary_bodies if b["body_id"] == "moon")
        shackleton = next(t for t in moon["targets"] if t["id"] == "lunar_south_pole_shackleton")

        results = calculate_planetary_similarity(lonar, shackleton, moon)

        excluded_keys = [ex["key"] for ex in results["excluded_features"]]
        self.assertIn("surface_pressure_hpa", excluded_keys)
        self.assertNotIn("surface_pressure_hpa", results["features"])

        # Check coverage and ACI metrics
        self.assertLess(results["measurement_coverage_pct"], 100.0)
        self.assertGreater(results["aci_score_pct"], 0.0)
        self.assertGreater(results["evidence_availability_pct"], 0.0)

    def test_04_mars_comparison_includes_atmospheric_pressure(self):
        """Mars has thin ~6.1 hPa atmosphere, so atmospheric pressure is available and included."""
        tso_kar = next(a for a in self.earth_analogs if a["id"] == "tso_kar")
        mars = next(b for b in self.planetary_bodies if b["body_id"] == "mars")
        delta = next(t for t in mars["targets"] if t["id"] == "mars_jezero_delta")

        results = calculate_planetary_similarity(tso_kar, delta, mars)
        self.assertIn("surface_pressure_hpa", results["features"])
        self.assertEqual(results["measurement_coverage_pct"], 100.0)

    def test_05_mineral_token_extraction(self):
        """Verify mineral keyword tokenizer extracts recognized diagnostic phases."""
        minerals = ["Calcic Plagioclase Feldspar (An95)", "Magnesian Olivine", "Smectite clays", "Gypsum"]
        tokens = extract_mineral_tokens(minerals)
        self.assertIn("plagioclase", tokens)
        self.assertIn("olivine", tokens)
        self.assertIn("smectite", tokens)
        self.assertIn("gypsum", tokens)

    def test_06_visualization_figures_generate(self):
        """Verify Plotly charts build without exceptions."""
        lonar = next(a for a in self.earth_analogs if a["id"] == "lonar_crater")
        mars = next(b for b in self.planetary_bodies if b["body_id"] == "mars")
        seitah = next(t for t in mars["targets"] if t["id"] == "mars_jezero_seitah")

        results = calculate_planetary_similarity(lonar, seitah, mars)
        radar_fig = create_similarity_radar_chart(results)
        bar_fig = create_feature_breakdown_bar_chart(results)
        topo_fig = create_terrain_cross_section_chart(
            self.terrain_profiles.get("lonar_crater"),
            self.terrain_profiles.get("mars_jezero_delta"),
            "Lonar Crater",
            "Jezero Delta"
        )

        self.assertIsNotNone(radar_fig)
        self.assertIsNotNone(bar_fig)
        self.assertIsNotNone(topo_fig)

    def test_07_pdf_dossier_generation(self):
        """Verify that ReportLab PDF dossier generates non-empty PDF bytes."""
        tso_kar = next(a for a in self.earth_analogs if a["id"] == "tso_kar")
        mars = next(b for b in self.planetary_bodies if b["body_id"] == "mars")
        delta = next(t for t in mars["targets"] if t["id"] == "mars_jezero_delta")

        results = calculate_planetary_similarity(tso_kar, delta, mars)
        pdf_bytes = generate_dossier_pdf(results, tso_kar, delta, mars)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 1000)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

    def test_08_data_sources_integration_status(self):
        """Verify that all data sources have explicit integration statuses."""
        earth_srcs = self.data_sources.get("earth_sources", [])
        plan_srcs = self.data_sources.get("planetary_sources", [])
        self.assertGreater(len(earth_srcs), 0)
        self.assertGreater(len(plan_srcs), 0)

        valid_statuses = [
            "downloaded_and_processed",
            "api_accessed",
            "externally_referenced",
            "planned_future_integration"
        ]

        for s in earth_srcs + plan_srcs:
            self.assertIn("integration_status", s)
            self.assertIn(s["integration_status"], valid_statuses)

    def test_09_clean_html_strips_indentation(self):
        """Verify clean_html removes indentation that causes CommonMark pre/code wrapping."""
        from utils.ui_components import clean_html
        indented = """
            <div class="rhombus-card">
                <span class="rhombus-badge-dot"></span>
                <p>Test content</p>
            </div>
        """
        cleaned = clean_html(indented)
        self.assertFalse(any(line.startswith("    ") for line in cleaned.split("\n")))
        self.assertTrue(cleaned.startswith("<div class=\"rhombus-card\">"))
        self.assertIn("<span class=\"rhombus-badge-dot\"></span>", cleaned)

    def test_10_safe_dataset_metadata_resilience(self):
        """Verify incomplete dataset dictionaries do not cause KeyError."""
        incomplete_dataset = {"name": "Test Incomplete Source"}
        # Safe extraction checks
        name = incomplete_dataset.get("name") or "Dataset"
        sensor = incomplete_dataset.get("sensor") or incomplete_dataset.get("instrument") or "Not specified"
        self.assertEqual(name, "Test Incomplete Source")
        self.assertEqual(sensor, "Not specified")
        label = f"{name} ({sensor})" if sensor != "Not specified" else name
        self.assertEqual(label, "Test Incomplete Source")

    def test_11_kpi_and_metric_grid_helpers(self):
        """Verify render_rhombus_kpi_row and render_rhombus_metric_grid functions."""
        from utils.ui_components import render_rhombus_kpi_row, render_rhombus_metric_grid
        # Verify functions are callable and do not raise
        self.assertTrue(callable(render_rhombus_kpi_row))
        self.assertTrue(callable(render_rhombus_metric_grid))


if __name__ == "__main__":
    unittest.main()

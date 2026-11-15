"""
Earth2Orbit — Comparison Laboratory Module
Calculates transparent, weighted, normalized analog compatibility between terrestrial analogs
and extraterrestrial reference environments adapted to the Rhombus Design System:
- Rhombus Page Header and Dual Pairing Selectors
- High-Contrast ACI Score Card and Methodology Details
- Rhombus-themed Radar and Feature Breakdown Charts
- Topographic Cross-Section Transects
- Clean Parameter Comparison Matrix and Interpretation Cards
"""

import streamlit as st
import pandas as pd
from utils.metrics import calculate_planetary_similarity, FEATURE_METADATA
from modules.visualizations import (
    create_similarity_radar_chart,
    create_feature_breakdown_bar_chart,
    create_terrain_cross_section_chart
)
from utils.ui_components import (
    render_rhombus_page_header,
    render_rhombus_card_header,
    render_scientific_notice,
    render_warning_notice,
    render_html
)


def render_comparison_engine(earth_analogs: list, planetary_bodies: list, terrain_profiles: dict):
    """Renders the transparent multi-parameter scientific comparison laboratory."""

    render_rhombus_page_header(
        title="Comparison Laboratory",
        subtitle="Quantitative multi-parameter evaluation between terrestrial analogs and planetary reference regions"
    )

    # Dual Selectors in bordered containers
    col_e, col_p = st.columns(2)

    with col_e:
        with st.container(border=True):
            render_rhombus_card_header("1. Terrestrial Analog Field Site", "Select candidate field location")
            earth_names = [a["name"] for a in earth_analogs]
            def_idx = 0
            if "selected_analog_id" in st.session_state:
                ids = [a["id"] for a in earth_analogs]
                if st.session_state.selected_analog_id in ids:
                    def_idx = ids.index(st.session_state.selected_analog_id)

            sel_earth_name = st.selectbox("Earth Analog Site:", options=earth_names, index=def_idx, label_visibility="collapsed")
            selected_earth = next((a for a in earth_analogs if a["name"] == sel_earth_name), earth_analogs[0])
            render_html(f"<div style='font-size: 0.8rem; color: #555555; margin-top: 6px;'>Region: {selected_earth['region']}, {selected_earth['country']}</div>")

    with col_p:
        with st.container(border=True):
            render_rhombus_card_header("2. Planetary Reference Region", "Select lunar or Martian target")
            target_options = []
            target_map = {}
            for body in planetary_bodies:
                for t in body.get("targets", []):
                    label = f"{body['body_name']} — {t['name']}"
                    target_options.append(label)
                    target_map[label] = (body, t)

            default_target_pair = (planetary_bodies[0], planetary_bodies[0]["targets"][0]) if planetary_bodies and planetary_bodies[0].get("targets") else (None, None)
            sel_target_label = st.selectbox("Planetary Target:", options=target_options, label_visibility="collapsed")
            selected_body, selected_target = target_map.get(sel_target_label, default_target_pair)
            render_html(f"<div style='font-size: 0.8rem; color: #555555; margin-top: 6px;'>Datum: {selected_target.get('elevation_reference', 'PDS Standard')}</div>")

    # Domain Weight Adjustment Expander
    with st.expander("Customize Domain Sensitivity Weights (Research Hypothesis Testing)", expanded=False):
        st.caption(
            "Adjust relative importance weights (w_j) to evaluate specific research hypotheses "
            "(e.g., emphasizing lithological concordance over atmospheric pressure):"
        )
        w_cols = st.columns(5)
        w_topo = w_cols[0].slider("Topographic Relief", 0.1, 3.0, 1.0, 0.1)
        w_slope = w_cols[1].slider("Slope & Roughness", 0.1, 3.0, 1.0, 0.1)
        w_therm = w_cols[2].slider("Thermal Regime", 0.1, 3.0, 1.0, 0.1)
        w_litho = w_cols[3].slider("Lithology Affinity", 0.1, 3.0, 1.5, 0.1)
        w_miner = w_cols[4].slider("Mineral Concordance", 0.1, 3.0, 1.5, 0.1)

        custom_weights = {
            "relief_m": w_topo,
            "mean_slope_deg": w_slope,
            "terrain_roughness_rms_m": w_slope,
            "diurnal_swing_c": w_therm,
            "lithology_affinity": w_litho,
            "mineral_jaccard": w_miner,
            "surface_pressure_hpa": 0.8
        }

    # Execute Similarity Calculation
    results = calculate_planetary_similarity(
        earth_data=selected_earth,
        target_data=selected_target,
        planetary_body=selected_body,
        custom_weights=custom_weights
    )

    aci = results["aci_score_pct"]
    cov = results["measurement_coverage_pct"]
    evidence = results["evidence_availability_pct"]

    # Rhombus Score Card and Methodology Explanation
    sc_col1, sc_col2 = st.columns([1.1, 1.9])

    with sc_col1:
        with st.container(border=True):
            render_html(
                f"""
                <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: #555555; font-weight: 600;">
                    Analog Compatibility Index (ACI)
                </div>
                <div style="font-size: 2.75rem; font-weight: 700; color: #775da6; line-height: 1.1; margin: 0.5rem 0;">
                    {aci:.1f}%
                </div>
                <div style="font-size: 0.8125rem; color: #555555; margin-bottom: 1rem;">
                    Pairing: <strong>{selected_earth['name']}</strong> ⟷ <strong>{selected_target['name'].split(':')[0]} ({selected_body['body_name']})</strong>
                </div>
                <div style="display: flex; gap: 1.5rem; border-top: 1px solid var(--border-color-subtle); padding-top: 0.75rem;">
                    <div>
                        <div style="font-size: 0.7rem; color: #666666; text-transform: uppercase; font-weight: 600;">Coverage</div>
                        <div style="font-size: 1.1rem; font-weight: 700; color: #202020;">{cov:.1f}%</div>
                        <div style="font-size: 0.7rem; color: #775da6;">{results['available_count']} / {results['total_potential_count']} params</div>
                    </div>
                    <div>
                        <div style="font-size: 0.7rem; color: #666666; text-transform: uppercase; font-weight: 600;">Evidence</div>
                        <div style="font-size: 1.1rem; font-weight: 700; color: #202020;">{evidence:.1f}%</div>
                        <div style="font-size: 0.7rem; color: #70b6c1;">PDS Verified</div>
                    </div>
                </div>
                """
            )

    with sc_col2:
        with st.container(border=True):
            render_rhombus_card_header("Scientific Evaluation Summary", "Key geological and environmental alignment")
            render_html(
                f"""
                <p style="font-size: 0.9rem; color: #202020; line-height: 1.6; margin: 0 0 0.75rem 0;">
                    {results['scientific_interpretation']}
                </p>
                <div style="font-size: 0.8rem; color: #555555;">
                    <strong>Candidate Pairing:</strong> Terrestrial study of <strong>{selected_earth['name']}</strong> informs mission operations, instrument calibration, and sample return protocols for <strong>{selected_target['name'].split(':')[0]}</strong>.
                </div>
                """
            )
            with st.expander("Scoring Methodology & Formula Details", expanded=False):
                st.caption(
                    "The Analog Compatibility Index (ACI) evaluates normalized distance across available parameters: "
                    "d_j = min(1.0, |x_Earth,j - x_Target,j| / R_j), where ACI = 100 * (1 - Σ(w_j * d_j) / Σ(w_j)). "
                    "Parameters without physical planetary counterparts (e.g. atmospheric pressure on the Moon) are strictly excluded."
                )

    # Excluded Features Notice (if any)
    if results["excluded_features"]:
        ex_names = ", ".join(ex["name"] for ex in results["excluded_features"])
        st.caption(f"ℹ️ **Excluded Inapplicable Parameters:** {ex_names} (omitted from denominator to prevent mathematical distortion).")

    # Graphical Visualizations in bordered containers
    v_col1, v_col2 = st.columns(2)

    with v_col1:
        with st.container(border=True):
            render_rhombus_card_header("Multi-Dimensional Compatibility Radar", "Normalized feature compatibility across available parameters")
            radar_fig = create_similarity_radar_chart(results)
            st.plotly_chart(radar_fig, use_container_width=True)

    with v_col2:
        with st.container(border=True):
            render_rhombus_card_header("Parameter Compatibility Breakdown", "Individual normalized score and assigned domain weighting")
            bar_fig = create_feature_breakdown_bar_chart(results)
            st.plotly_chart(bar_fig, use_container_width=True)

    # Topographic Transects in bordered container
    with st.container(border=True):
        render_rhombus_card_header("Topographic Elevation Transects (Illustrative Comparison)", "Local elevation profiles across distinct planetary datums and horizontal spans")
        e_prof = terrain_profiles.get(selected_earth["id"])
        t_prof = terrain_profiles.get(selected_target["id"])
        
        topo_fig = create_terrain_cross_section_chart(
            earth_profile=e_prof,
            target_profile=t_prof,
            earth_name=selected_earth["name"],
            target_name=selected_target["name"]
        )
        st.plotly_chart(topo_fig, use_container_width=True)
        st.caption(
            "ℹ️ **Geodetic Note:** Profiles represent separate local morphological transects with distinct horizontal lengths "
            "(km) and vertical datums (Earth EGM96 Mean Sea Level vs Lunar 1,737.4 km radius sphere vs Mars Areoid)."
        )

    # Side-by-Side Detailed Parameter Comparison Table (In Expandable Section)
    with st.expander("📋 Detailed Parameter Compatibility Matrix & Distance Values (d_j)", expanded=False):
        table_rows = []
        for key, feat in results["features"].items():
            sim_pct = feat["similarity"] * 100.0
            table_rows.append({
                "Parameter Domain": feat["name"],
                "Earth Analog Value": feat["earth_val"],
                "Planetary Target Value": feat["target_val"],
                "Distance (d_j)": f"{feat['norm_distance']:.2f}",
                "Compatibility Score": f"{sim_pct:.1f}%",
                "Weight (w_j)": f"{feat['weight']:.1f}",
                "Status": "Included"
            })

        for ex in results["excluded_features"]:
            table_rows.append({
                "Parameter Domain": ex["name"],
                "Earth Analog Value": f"{selected_earth.get(ex['key'], 'N/A')}",
                "Planetary Target Value": "Not Available (Excluded)",
                "Distance (d_j)": "N/A",
                "Compatibility Score": "Excluded",
                "Weight (w_j)": "0.0",
                "Status": "Insufficient Data"
            })

        df_matrix = pd.DataFrame(table_rows)
        st.dataframe(df_matrix, use_container_width=True)

    # Expandable Limitations Section
    with st.expander("Physical & Environmental Constraints for this Pairing", expanded=False):
        st.markdown("**Documented Physical Disparities (Gravity, Atmosphere, Radiation):**")
        for lim in results["limitations"]:
            st.markdown(f"- ⚠️ {lim}")
        st.caption("Complete comparative dossiers and formal citations are available in the Research Reports module.")

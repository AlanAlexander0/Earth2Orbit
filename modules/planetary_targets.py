"""
Earth2Orbit — Planetary Reference Targets Module
Editorial planetary research experience adapted to the Rhombus Design System:
- Rhombus Page Header and Body Controls
- 4-Column Planetary Physical Metric Cards with high-contrast labels
- Rhombus Showcase Panels with authentic NASA Public Domain Photography
- Tabbed Dossiers for Lithology, Thermal Regimes, PDS Sensors, and Science Questions
"""

import streamlit as st
import pandas as pd
from utils.ui_components import (
    render_rhombus_page_header,
    render_rhombus_card_header,
    render_rhombus_metric_grid,
    render_scientific_notice,
    render_warning_notice,
    render_html
)


def render_planetary_targets(planetary_bodies: list):
    """Renders the dedicated Moon and Mars planetary reference regions module."""

    render_rhombus_page_header(
        title="Planetary Reference Regions",
        subtitle="Validated lunar and Martian candidate exploration environments mapped by NASA and international missions"
    )

    # Body selector: Moon vs Mars in container
    with st.container(border=True):
        render_rhombus_card_header("Select Planetary Body", "Choose between the Moon (Luna) and Mars")
        body_names = [b["body_name"] for b in planetary_bodies]
        selected_body_name = st.radio(
            "Select Planetary Body:",
            options=body_names,
            horizontal=True,
            label_visibility="collapsed"
        )

    selected_body = next((b for b in planetary_bodies if b["body_name"] == selected_body_name), planetary_bodies[0])

    # Planetary Macro Properties (Responsive High-Contrast Rhombus Metric Cards)
    p_val = f"{selected_body['surface_pressure_hpa']} hPa" if selected_body['surface_pressure_hpa'] is not None else "Vacuum (< 10⁻¹² hPa)"
    macro_metrics = [
        {"label": "Mean Radius", "value": f"{selected_body['radius_km']:,} km", "delta": None},
        {"label": "Surface Gravity", "value": f"{selected_body['gravity_m_s2']} m/s²", "delta": f"{(selected_body['gravity_m_s2']/9.81)*100:.1f}% Earth g"},
        {"label": "Atmospheric Pressure", "value": p_val, "delta": None},
        {"label": "Radiation Shielding", "value": "None / Thin", "delta": "High Cosmic Ray Flux"}
    ]
    render_rhombus_metric_grid(macro_metrics)

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    # Environmental Context & Candidacy Distinction
    if selected_body["surface_pressure_hpa"] is None:
        render_scientific_notice(
            "The Lunar South Pole features candidate landing regions for NASA's Artemis program, "
            "preserving permanently shadowed cold traps (< 100 K) and water ice in a lunar vacuum environment.",
            strong_prefix="Lunar Exploration Context:"
        )
    else:
        render_scientific_notice(
            "Jezero Crater is the operational landing site of NASA's Mars 2020 Perseverance Rover, "
            "preserving an ancient Late Noachian lacustrine delta under a thin 6.1 hPa CO₂ atmosphere.",
            strong_prefix="Martian Exploration Context:"
        )

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    # Target Site Selector
    targets = selected_body.get("targets", [])
    target_names = [t["name"] for t in targets]

    selected_target_name = st.selectbox(
        f"Select {selected_body['body_name']} Reference Region:",
        options=target_names
    )
    selected_target = next((t for t in targets if t["name"] == selected_target_name), targets[0] if targets else {})

    # Deep Space Observatory Photographic Showcase Panel in Rhombus Card
    is_moon = selected_body["body_id"] == "moon"
    img_url = "https://images-assets.nasa.gov/image/PIA14011/PIA14011~orig.jpg" if is_moon else "https://images-assets.nasa.gov/image/PIA23962/PIA23962~orig.jpg"
    badge_cls = "rhombus-badge-primary" if is_moon else "rhombus-badge-secondary"
    body_label = "The Moon (Luna)" if is_moon else "Mars"

    render_html(
        f"""
        <div class="rhombus-card" style="padding: 1.25rem 1.5rem; margin-top: 0.5rem; margin-bottom: 1.25rem; width: 100%; box-sizing: border-box;">
            <div style="display: flex; gap: 1.5rem; align-items: flex-start; flex-wrap: wrap;">
                <div style="flex: 2 1 280px; min-width: 0;">
                    <div style="margin-bottom: 0.5rem;">
                        <span class="rhombus-badge {badge_cls}">{body_label}</span>
                        <span style="font-size: 0.78rem; color: #555555; margin-left: 8px;">Target Code: {selected_target.get('target_code', 'N/A')}</span>
                    </div>
                    <h3 style="font-size: 1.5rem; font-weight: 700; color: #202020; margin: 0 0 0.5rem 0; word-wrap: break-word;">{selected_target['name']}</h3>
                    <p style="font-size: 0.875rem; color: #333333; line-height: 1.6; margin: 0;">{selected_target['geology']['stratigraphy']}</p>
                </div>
                <div style="flex: 1 1 200px; max-width: 260px; border-radius: 8px; overflow: hidden; border: 1px solid var(--border-color-default);">
                    <img src="{img_url}" alt="{selected_target['name']}" style="width: 100%; height: 150px; object-fit: cover; display: block;" />
                </div>
            </div>
        </div>
        """
    )

    # Sub-target Metrics (Responsive High-Contrast Rhombus Metric Cards)
    coords = selected_target["coordinates"]
    lat_str = f"{abs(coords['latitude']):.2f}° {'N' if coords['latitude'] >= 0 else 'S'}"
    lon_str = f"{abs(coords['longitude']):.2f}° {'E' if coords['longitude'] >= 0 else 'W'}"
    elev_ref = selected_target.get("elevation_reference", "Datum")

    target_metrics = [
        {"label": "Orbital Coordinates", "value": f"{lat_str}, {lon_str}", "delta": None},
        {"label": "Elevation & Datum", "value": f"{selected_target['elevation_m']} m", "delta": f"Ref: {elev_ref}"},
        {"label": "Mean Regional Slope", "value": f"{selected_target['mean_slope_deg']}°", "delta": f"Relief: {selected_target['relief_m']} m"},
        {"label": "Terrain Roughness", "value": f"{selected_target['terrain_roughness_rms_m']} m RMS", "delta": None}
    ]
    render_rhombus_metric_grid(target_metrics)

    # Key Thermal Environment Cards
    temp_k = selected_target.get("temperature_k", {})
    temp_c = selected_target.get("temperature_c", {})
    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)
    th1, th2, th3 = st.columns(3)
    th1.metric(
        "Minimum Temperature",
        f"{temp_k.get('min_psr', temp_k.get('min_diurnal', 'N/A'))} K",
        f"{temp_c.get('min_psr', temp_c.get('min_diurnal', 'N/A'))} °C"
    )
    th2.metric(
        "Mean Surface Temp",
        f"{temp_k.get('mean', 'N/A')} K",
        f"{temp_c.get('mean', 'N/A')} °C"
    )
    th3.metric(
        "Max Temperature",
        f"{temp_k.get('max_illuminated', temp_k.get('max_diurnal', 'N/A'))} K",
        f"{temp_c.get('max_illuminated', temp_c.get('max_diurnal', 'N/A'))} °C"
    )

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Expandable Details for Deep Geological Stratigraphy & Sensors
    with st.expander("🔬 Detailed Lithology, Mineralogy, Instruments & Scientific Questions", expanded=False):
        tab_geo, tab_therm, tab_instr, tab_science = st.tabs([
            "Lithology & Geomorphology",
            "Thermal Regimes & Illumination",
            "NASA Mission Instruments",
            "Priority Scientific Questions"
        ])

        with tab_geo:
            geo = selected_target["geology"]
            with st.container(border=True):
                render_rhombus_card_header("Lithological Stratigraphy", "Rock classification and stratigraphic context")
                render_html(
                    f"""
                    <div style="font-size: 0.95rem; color: #202020; margin-bottom: 0.5rem;">
                        <strong>Classification:</strong> <code style="background-color: var(--color-primary-lighter); color: var(--color-primary-dark); padding: 2px 6px; border-radius: 4px;">{geo['lithology_type']}</code>
                    </div>
                    <div style="font-size: 0.875rem; color: #555555; line-height: 1.5;">
                        <strong>Stratigraphic Context:</strong> {geo['stratigraphy']}
                    </div>
                    """
                )

            c_m, c_g = st.columns(2)
            with c_m:
                with st.container(border=True):
                    render_rhombus_card_header("Confirmed Diagnostic Mineral Phases", "")
                    for m in geo["dominant_minerals"]:
                        st.markdown(f"- **{m}**")

            with c_g:
                with st.container(border=True):
                    render_rhombus_card_header("Geomorphic Features & Surface Morphology", "")
                    for f in geo["geomorphic_features"]:
                        st.markdown(f"- {f}")

        with tab_therm:
            th1, th2, th3 = st.columns(3)
            th1.metric(
                "Minimum Temperature",
                f"{temp_k.get('min_psr', temp_k.get('min_diurnal', 'N/A'))} K",
                f"{temp_c.get('min_psr', temp_c.get('min_diurnal', 'N/A'))} °C"
            )
            th2.metric(
                "Mean Surface Temp",
                f"{temp_k.get('mean', 'N/A')} K",
                f"{temp_c.get('mean', 'N/A')} °C"
            )
            th3.metric(
                "Max Temperature",
                f"{temp_k.get('max_illuminated', temp_k.get('max_diurnal', 'N/A'))} K",
                f"{temp_c.get('max_illuminated', temp_c.get('max_diurnal', 'N/A'))} °C"
            )
            st.caption("Derived from NASA LRO Diviner bolometric thermal radiometry & Mars Odyssey THEMIS thermal infrared.")

        with tab_instr:
            with st.container(border=True):
                render_rhombus_card_header("Primary Orbital & In-Situ Instrumentation", "NASA Planetary Data System (PDS) instruments")
                instruments = selected_target.get("instruments", [])
                for instr in instruments:
                    render_html(
                        f"""
                        <div style="padding: 0.85rem 1rem; margin-bottom: 0.6rem; background: var(--background-color-subtle); border-radius: 6px; border: 1px solid var(--border-color-subtle);">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <strong style="color: #202020; font-size: 0.95rem;">{instr['instrument']}</strong>
                                <span class="rhombus-badge rhombus-badge-primary">{instr['spacecraft']}</span>
                            </div>
                            <div style="font-size: 0.84rem; color: #333333; margin-top: 0.25rem;">
                                <strong>Measured Properties:</strong> {instr['measurement']}
                            </div>
                            <div style="font-size: 0.75rem; color: #666666; font-family: monospace; margin-top: 0.2rem;">
                                PDS Product ID: {instr['dataset_id']}
                            </div>
                        </div>
                        """
                    )

        with tab_science:
            with st.container(border=True):
                render_rhombus_card_header("Priority Scientific Questions", "")
                for q in selected_target.get("key_scientific_questions", []):
                    st.markdown(f"- ❓ *{q}*")

                st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)
                conf = selected_target.get("data_confidence", {})
                render_html(
                    f"""
                    <div style="padding: 0.75rem; background: var(--background-color-subtle); border-radius: 6px; border-left: 3px solid var(--color-info);">
                        <strong>Evidence Provenance:</strong> {conf.get('confidence_notes', '')}
                    </div>
                    """
                )

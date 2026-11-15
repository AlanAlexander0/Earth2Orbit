"""
Earth2Orbit — Terrain Analysis Module
Scientific topographic analysis, elevation cross-sections, slope distributions,
and vertical datum reconciliation adapted to the Rhombus Design System:
- Rhombus Page Header and Geodetic Notice
- Interactive Cross-Sectional Transects in native bordered containers
- Comparative Geomorphic Metric Bar Charts
- Sensor Resolving Limits and Geodetic Reference Matrices
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from modules.visualizations import (
    create_terrain_cross_section_chart,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_INFO,
    COLOR_WARNING,
    COLOR_TEXT,
    COLOR_MUTED
)
from utils.ui_components import (
    render_rhombus_page_header,
    render_rhombus_card_header,
    render_scientific_notice,
    render_html
)


def render_terrain_analysis(earth_analogs: list, planetary_bodies: list, terrain_profiles: dict):
    """Renders the comprehensive scientific terrain analysis module in Rhombus style."""

    render_rhombus_page_header(
        title="Terrain & Topographic Analysis",
        subtitle="Quantitative relief evaluation, slope distributions, and vertical datum reconciliation"
    )

    # Scientific Requirement: Vertical Datum & Resolution Clarification (Concise)
    render_scientific_notice(
        "Topographic evaluations compare scale-invariant relative relief (Δh), slope gradients, "
        "and sub-kilometer RMS roughness across Earth, Lunar, and Martian vertical reference datums.",
        strong_prefix="Geodetic Principle:"
    )

    tab_profiles, tab_metrics, tab_geodesy = st.tabs([
        "Topographic Elevation Profiles",
        "Comparative Slope & Ruggedness Distributions",
        "Geodetic Datums & Sensor Specifications"
    ])

    with tab_profiles:
        with st.container(border=True):
            render_rhombus_card_header("Illustrative Topographic Elevation Transects", "Compare morphological cross-sections across separate planetary datums and horizontal spans")

            c1, c2 = st.columns(2)
            earth_avail_profiles = [k for k in terrain_profiles.keys() if any(a["id"] == k for a in earth_analogs)]
            target_avail_profiles = [k for k in terrain_profiles.keys() if not any(a["id"] == k for a in earth_analogs)]

            with c1:
                sel_e_prof = st.selectbox(
                    "Terrestrial Transect (NASA SRTM 30m):",
                    options=earth_avail_profiles,
                    format_func=lambda x: terrain_profiles[x]["name"]
                )
            with c2:
                sel_t_prof = st.selectbox(
                    "Planetary Transect (NASA LOLA / MOLA):",
                    options=target_avail_profiles,
                    format_func=lambda x: terrain_profiles[x]["name"]
                )

            e_prof_data = terrain_profiles.get(sel_e_prof, {})
            t_prof_data = terrain_profiles.get(sel_t_prof, {})
            e_name = e_prof_data.get("name", "Terrestrial Transect").split(" - ")[0]
            t_name = t_prof_data.get("name", "Planetary Transect").split(" - ")[0]

            prof_fig = create_terrain_cross_section_chart(
                earth_profile=e_prof_data if e_prof_data else None,
                target_profile=t_prof_data if t_prof_data else None,
                earth_name=e_name,
                target_name=t_name
            )
            st.plotly_chart(prof_fig, use_container_width=True)
            st.caption(
                "ℹ️ **Scientific Geodetic Notice:** These elevation profiles possess separate horizontal extents (e.g., 3 km vs 25 km) "
                "and distinct vertical datums (Earth EGM96 Geoid vs Lunar 1,737.4 km radius sphere vs Mars Areoid). They illustrate "
                "relative landform morphology (rim-to-floor crater relief, delta scarps) rather than direct absolute elevation comparisons."
            )

            e_desc = e_prof_data.get("description", "High-resolution DEM elevation transect")
            t_desc = t_prof_data.get("description", "Planetary laser altimetry elevation profile")
            render_html(
                f"""
                <div style="font-size: 0.85rem; line-height: 1.55; color: #202020; border-top: 1px solid var(--border-color-subtle); padding-top: 0.75rem; margin-top: 0.5rem;">
                    <p style="margin: 0 0 0.5rem 0;"><strong>Terrestrial Transect:</strong> {e_desc}</p>
                    <p style="margin: 0;"><strong>Planetary Reference:</strong> {t_desc}</p>
                </div>
                """
            )

    with tab_metrics:
        with st.container(border=True):
            render_rhombus_card_header("Comparative Geomorphic Metrics Across Sites", "Relative relief, slope angles, and surface roughness across Earth, Moon, and Mars")

            all_sites_data = []
            for a in earth_analogs:
                all_sites_data.append({
                    "Body": "Earth",
                    "Site": a["name"],
                    "Relative Relief (m)": a["relief_m"],
                    "Mean Slope (deg)": a["mean_slope_deg"],
                    "Roughness RMS (m)": a["terrain_roughness_rms_m"]
                })

            for b in planetary_bodies:
                for t in b.get("targets", []):
                    all_sites_data.append({
                        "Body": b["body_name"],
                        "Site": t["name"],
                        "Relative Relief (m)": t["relief_m"],
                        "Mean Slope (deg)": t["mean_slope_deg"],
                        "Roughness RMS (m)": t["terrain_roughness_rms_m"]
                    })

            df_all = pd.DataFrame(all_sites_data)

            metric_select = st.selectbox(
                "Select Metric to Compare:",
                options=["Relative Relief (m)", "Mean Slope (deg)", "Roughness RMS (m)"]
            )

            fig_bar = px.bar(
                df_all,
                x="Site",
                y=metric_select,
                color="Body",
                color_discrete_map={"Earth": COLOR_INFO, "The Moon (Luna)": COLOR_PRIMARY, "Mars": COLOR_SECONDARY},
                title=f"Comparative {metric_select}"
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='#FFFFFF',
                font=dict(color=COLOR_TEXT, size=10),
                xaxis=dict(gridcolor='#ececec', tickangle=-20),
                yaxis=dict(gridcolor='#ececec'),
                margin=dict(l=20, r=20, t=50, b=50),
                legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center")
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    with tab_geodesy:
        with st.container(border=True):
            render_rhombus_card_header("Planetary Geodetic Systems & Sensor Resolving Limits", "Documenting orbital sensor resolutions, precision, and vertical datums")

            geodesy_table = [
                {
                    "Planetary Body": "Earth",
                    "Primary Topographic Sensor": "NASA SRTM (Shuttle Radar Topography Mission)",
                    "Vertical Datum": "EGM96 Geoid (Mean Sea Level)",
                    "Spatial Resolution": "1 arc-second (~30 meters)",
                    "Vertical Accuracy": "±16 meters absolute linear"
                },
                {
                    "Planetary Body": "Earth",
                    "Primary Topographic Sensor": "NASA / METI ASTER GDEM v3",
                    "Vertical Datum": "WGS84 / EGM96 Geoid",
                    "Spatial Resolution": "1 arc-second (~30 meters)",
                    "Vertical Accuracy": "±12 meters linear error"
                },
                {
                    "Planetary Body": "The Moon (Luna)",
                    "Primary Topographic Sensor": "NASA LOLA (Lunar Orbiter Laser Altimeter)",
                    "Vertical Datum": "Lunar Mean Radius Reference Sphere (R = 1,737.4 km)",
                    "Spatial Resolution": "5 to 20 meters/pixel at South Pole (polar GDRs)",
                    "Vertical Accuracy": "±1 meter vertical precision"
                },
                {
                    "Planetary Body": "Mars",
                    "Primary Topographic Sensor": "NASA MOLA (Mars Orbiter Laser Altimeter)",
                    "Vertical Datum": "MOLA Areoid (Equipotential 6.1 mbar gravity surface)",
                    "Spatial Resolution": "128 pixels/degree (~463 meters at equator)",
                    "Vertical Accuracy": "±1 meter precision; ±30 m absolute geodetic"
                },
                {
                    "Planetary Body": "Mars",
                    "Primary Topographic Sensor": "NASA HiRISE Stereo Digital Terrain Models",
                    "Vertical Datum": "MOLA Areoid (tied to MOLA tracks)",
                    "Spatial Resolution": "1.0 to 2.0 meters/pixel post spacing",
                    "Vertical Accuracy": "Sub-meter relative elevation precision"
                }
            ]
            df_geo = pd.DataFrame(geodesy_table)
            st.dataframe(df_geo, use_container_width=True)

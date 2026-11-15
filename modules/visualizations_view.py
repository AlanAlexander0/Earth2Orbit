"""
Planetary Analog Explorer - Interactive Visualizations Module
Deep-dive visualization suite: Feature distribution histograms,
overlaid terrain profiles, and cross-body environmental parameter scatter comparisons.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from modules.visualizations import create_terrain_cross_section_chart


def render_visualizations_view(earth_analogs: list, planetary_bodies: list, terrain_profiles: dict):
    """Renders the comprehensive visualization laboratory."""
    
    st.markdown("## 📈 Planetary Geospatial Visualizations")
    st.markdown(
        "Interactive graphical analytics comparing morphometry, thermal swings, "
        "and topographic profiles across terrestrial and planetary environments."
    )

    tab_profiles, tab_dist, tab_scatter = st.tabs([
        "🏔️ Topographic Transect Comparison",
        "📊 Parameter Distributions Across Sites",
        "🌌 Earth vs Mars vs Moon Environmental Scatter"
    ])

    with tab_profiles:
        st.markdown("### Calibrated Topographic Elevation Profiles")
        st.caption("Select an Earth analog transect (NASA SRTM 30m) and planetary transect (NASA LOLA / MOLA) to compare cross-sectional relief:")
        
        c1, c2 = st.columns(2)
        earth_avail_profiles = [k for k in terrain_profiles.keys() if any(a["id"] == k for a in earth_analogs)]
        target_avail_profiles = [k for k in terrain_profiles.keys() if not any(a["id"] == k for a in earth_analogs)]

        with c1:
            sel_e_prof = st.selectbox(
                "Select Earth Transect:",
                options=earth_avail_profiles,
                format_func=lambda x: terrain_profiles[x]["name"]
            )
        with c2:
            sel_t_prof = st.selectbox(
                "Select Planetary Transect:",
                options=target_avail_profiles,
                format_func=lambda x: terrain_profiles[x]["name"]
            )

        prof_fig = create_terrain_cross_section_chart(
            earth_profile=terrain_profiles.get(sel_e_prof),
            target_profile=terrain_profiles.get(sel_t_prof),
            earth_name=terrain_profiles[sel_e_prof]["name"].split(" - ")[0],
            target_name=terrain_profiles[sel_t_prof]["name"].split(" - ")[0]
        )
        st.plotly_chart(prof_fig, use_container_width=True)

        st.info(
            f"**Earth Profile Description:** {terrain_profiles[sel_e_prof]['description']}\n\n"
            f"**Planetary Profile Description:** {terrain_profiles[sel_t_prof]['description']}"
        )

    with tab_dist:
        st.markdown("### Terrestrial Analog Parameter Distributions")
        st.caption("Comparative distribution of morphometric and environmental metrics across the 6 curated field sites:")

        e_records = []
        for a in earth_analogs:
            e_records.append({
                "Site": a["name"],
                "Elevation (m)": a["elevation_m"],
                "Relief (m)": a["relief_m"],
                "Slope (deg)": a["mean_slope_deg"],
                "Roughness RMS (m)": a["terrain_roughness_rms_m"],
                "Diurnal Swing (°C)": a["temperature_c"]["diurnal_swing"],
                "Annual Rain (mm)": a["annual_precipitation_mm"],
                "Atmospheric Pressure (hPa)": a["atmospheric_pressure_hpa"]
            })
        df_e = pd.DataFrame(e_records)

        metric_choice = st.selectbox(
            "Select Metric to Visualize:",
            options=["Elevation (m)", "Relief (m)", "Slope (deg)", "Roughness RMS (m)", "Diurnal Swing (°C)", "Annual Rain (mm)", "Atmospheric Pressure (hPa)"]
        )

        fig_bar = px.bar(
            df_e,
            x="Site",
            y=metric_choice,
            color=metric_choice,
            color_continuous_scale="Viridis",
            title=f"Distribution of {metric_choice} Across Terrestrial Field Sites"
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(13, 24, 51, 0.5)',
            font=dict(color="#f1f5f9"),
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with tab_scatter:
        st.markdown("### Cross-World Environmental Scatter: Relief vs Thermal Swing")
        st.caption("Plotting all Earth, Lunar, and Martian sites on a single comparative domain space:")

        scatter_data = []
        for a in earth_analogs:
            scatter_data.append({
                "World": "Earth",
                "Site Name": a["name"],
                "Topographic Relief (m)": a["relief_m"],
                "Diurnal Swing (K / °C)": a["temperature_c"]["diurnal_swing"],
                "Mean Slope (deg)": a["mean_slope_deg"]
            })

        for b in planetary_bodies:
            for t in b.get("targets", []):
                scatter_data.append({
                    "World": b["body_name"],
                    "Site Name": t["name"],
                    "Topographic Relief (m)": t["relief_m"],
                    "Diurnal Swing (K / °C)": t["temperature_c"]["diurnal_swing"],
                    "Mean Slope (deg)": t["mean_slope_deg"]
                })

        df_scatter = pd.DataFrame(scatter_data)

        fig_scatter = px.scatter(
            df_scatter,
            x="Topographic Relief (m)",
            y="Diurnal Swing (K / °C)",
            color="World",
            size="Mean Slope (deg)",
            hover_name="Site Name",
            color_discrete_map={"Earth": "#10b981", "The Moon (Luna)": "#c8d6e5", "Mars": "#ff6b4a"},
            title="Environmental Stress Space (Relief vs Thermal Cycling, Bubble Size = Mean Slope)"
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(13, 24, 51, 0.5)',
            font=dict(color="#f1f5f9"),
            xaxis=dict(gridcolor='rgba(255,255,255,0.08)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.08)'),
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

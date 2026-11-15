"""
Earth2Orbit — Earth Analog Explorer Module
Geospatial Intelligence centrepiece adapted to the Rhombus Design System:
- Rhombus Page Header and Search/Filter Controls
- Interactive Folium multi-layer map enclosed in a native bordered container
- High-contrast site metrics with guaranteed readability
- Tabbed dossiers for Geological Stratigraphy, Environmental Extremes, Analog Missions, and NASA POWER API
"""

import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from modules.visualizations import create_earth_folium_map, create_nasa_power_climatology_chart
from modules.nasa_data_loaders import fetch_nasa_power_climatology
from utils.ui_components import (
    render_rhombus_page_header,
    render_rhombus_card_header,
    render_rhombus_metric_grid,
    render_scientific_notice,
    render_warning_notice,
    render_html
)


def render_earth_explorer(earth_analogs: list):
    """Renders the Earth Analog Explorer interactive map and profile views."""

    render_rhombus_page_header(
        title="Earth Analog Explorer",
        subtitle="Geospatial intelligence map and scientific evaluation dossiers for terrestrial planetary analogs"
    )

    # Default analog site
    default_analog_id = earth_analogs[0]["id"] if earth_analogs else "tso_kar"

    # State initialization for filters
    if "earth_search_text" not in st.session_state:
        st.session_state["earth_search_text"] = ""
    if "earth_country_filter" not in st.session_state:
        st.session_state["earth_country_filter"] = "All Countries"
    if "earth_target_filter" not in st.session_state:
        st.session_state["earth_target_filter"] = "All Targets"
    if "selected_analog_id" not in st.session_state:
        st.session_state["selected_analog_id"] = default_analog_id

    def reset_filters():
        st.session_state["earth_search_text"] = ""
        st.session_state["earth_country_filter"] = "All Countries"
        st.session_state["earth_target_filter"] = "All Targets"
        st.session_state["selected_analog_id"] = default_analog_id

    # Search and Filter Controls in native container
    with st.container(border=True):
        render_rhombus_card_header("Filter & Search Analogs", "Search by site name, region, country, geology, or planetary target affinity")
        f_col1, f_col2, f_col3, f_col4 = st.columns([1.8, 1.1, 1.1, 0.8])
        with f_col1:
            search_query = st.text_input(
                "Search field sites:",
                key="earth_search_text",
                placeholder="e.g. Ladakh, Lonar, Sambhar, Atacama, India, basalt..."
            )
        with f_col2:
            country_options = ["All Countries"] + sorted(list(set(a["country"] for a in earth_analogs)))
            sel_country = st.selectbox("Country:", country_options, key="earth_country_filter")
        with f_col3:
            target_options = ["All Targets", "Mars", "Moon"]
            sel_target_filter = st.selectbox("Planetary Target:", target_options, key="earth_target_filter")
        with f_col4:
            st.markdown("<div style='height: 1.7rem;'></div>", unsafe_allow_html=True)
            st.button(
                "↺ Reset",
                key="reset_earth_filters",
                on_click=reset_filters,
                use_container_width=True,
                help="Reset all search queries and filters"
            )

    # Filter analogs list with robust multi-field matching
    filtered_analogs = list(earth_analogs)
    q = search_query.strip().lower() if search_query else ""
    if q:
        filtered_analogs = [
            a for a in filtered_analogs 
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
    if sel_country != "All Countries":
        filtered_analogs = [a for a in filtered_analogs if a["country"].strip().lower() == sel_country.strip().lower()]
    if sel_target_filter != "All Targets":
        filtered_analogs = [
            a for a in filtered_analogs 
            if sel_target_filter.strip().lower() in a["planetary_analog_relevance"]["primary_target"].lower()
        ]

    # Handle zero matching results gracefully without falling back to unrelated sites
    if not filtered_analogs:
        # Clear selected location so unrelated sites are never shown
        st.session_state["selected_analog_id"] = None

        render_html(
            """
            <div class="rhombus-card" style="border-left: 4px solid var(--color-warning); padding: 1.5rem; margin-top: 1rem; margin-bottom: 1.25rem;">
                <h3 style="font-size: 1.25rem; font-weight: 700; color: #202020; margin: 0 0 0.5rem 0;">
                    No matching analog sites found.
                </h3>
                <p style="font-size: 0.875rem; color: #555555; line-height: 1.6; margin: 0;">
                    No configured terrestrial planetary analog research locations match your current search terms and filter criteria.<br>
                    <strong>Scientific Integrity:</strong> Earth2Orbit does not display unverified or unrelated sites as fallbacks. Refine your query or click <strong>Reset Filters</strong> below to browse all 6 verified terrestrial analog locations.
                </p>
            </div>
            """
        )

        col_rst, _ = st.columns([1.5, 2.5])
        with col_rst:
            st.button(
                "↺ Reset Filters & Show All Sites",
                key="btn_reset_empty",
                on_click=reset_filters,
                use_container_width=True
            )

        with st.container(border=True):
            render_rhombus_card_header("Geospatial Intelligence Map", "0 locations match current filters")
            folium_map = create_earth_folium_map([])
            st_folium(folium_map, width="100%", height=380, returned_objects=[])

        return

    # Site Selection from filtered results only
    site_names = [a["name"] for a in filtered_analogs]
    site_ids = [a["id"] for a in filtered_analogs]

    if st.session_state.get("selected_analog_id") not in site_ids:
        st.session_state.selected_analog_id = site_ids[0]

    current_idx = site_ids.index(st.session_state.selected_analog_id)

    col_sel, col_stat = st.columns([2.5, 1.5])
    with col_sel:
        match_suffix = f" ({len(filtered_analogs)} of {len(earth_analogs)} matching)" if len(filtered_analogs) < len(earth_analogs) else ""
        selected_name = st.selectbox(
            f"Selected Analog Field Site{match_suffix}:",
            options=site_names,
            index=current_idx
        )
        selected_analog = next((a for a in filtered_analogs if a["name"] == selected_name), filtered_analogs[0])
        st.session_state.selected_analog_id = selected_analog["id"]

    with col_stat:
        is_primary = selected_analog["id"] in ["tso_kar", "lonar_crater", "sambhar_lake"]
        badge_cls = "rhombus-badge-primary" if is_primary else "rhombus-badge-info"
        badge_txt = "Primary Research Candidate (India)" if is_primary else "Global Planetary Benchmark"
        render_html(
            f"""
            <div style="padding-top: 1.6rem;">
                <span class="rhombus-badge {badge_cls}" style="font-size: 0.8rem; padding: 6px 12px;">
                    {badge_txt}
                </span>
            </div>
            """
        )

    # Interactive Geospatial Map inside container showing active matching sites
    with st.container(border=True):
        map_subtitle = (
            f"Displaying {len(filtered_analogs)} matching analog locations • OpenStreetMap Basemap"
            if len(filtered_analogs) < len(earth_analogs)
            else "OpenStreetMap Default, Esri High-Resolution Satellite, and OpenTopoMap layers"
        )
        render_rhombus_card_header("Geospatial Intelligence Map", map_subtitle)
        folium_map = create_earth_folium_map(filtered_analogs, selected_id=selected_analog["id"])
        st_folium(folium_map, width="100%", height=440, returned_objects=[])

    # Comprehensive Location Dossier (High-Contrast Rhombus Card)
    coords = selected_analog["coordinates"]
    lat_str = f"{abs(coords['latitude']):.4f}° {'N' if coords['latitude'] >= 0 else 'S'}"
    lon_str = f"{abs(coords['longitude']):.4f}° {'E' if coords['longitude'] >= 0 else 'W'}"

    render_html(
        f"""
        <div style="margin: 1.5rem 0 1rem 0;">
            <h2 style="font-size: 1.5rem; font-weight: 700; color: #202020; margin: 0 0 0.25rem 0;">
                Site Dossier: {selected_analog['name']}
            </h2>
            <p style="font-size: 0.875rem; color: #555555; margin: 0;">
                {selected_analog['region']}, {selected_analog['country']} • Target: {selected_analog['planetary_analog_relevance']['primary_target']}
            </p>
        </div>
        """
    )

    # High-Contrast Key Metrics Grid (Responsive Rhombus Metric Cards)
    site_metrics = [
        {"label": "Geographic Coordinates", "value": f"{lat_str}, {lon_str}", "delta": None},
        {"label": "Elevation a.s.l.", "value": f"{selected_analog['elevation_m']} m", "delta": f"Relief: {selected_analog['relief_m']} m (SRTM)"},
        {"label": "Köppen Biome", "value": selected_analog["koppen_climate"], "delta": selected_analog["biome"]},
        {"label": "Slope & Roughness", "value": f"{selected_analog['mean_slope_deg']}°", "delta": f"RMS: {selected_analog['terrain_roughness_rms_m']} m"}
    ]
    render_rhombus_metric_grid(site_metrics)

    # Concise Site Summary Card (Terrain Description & Planetary Relevance)
    rel = selected_analog["planetary_analog_relevance"]
    render_html(
        f"""
        <div class="rhombus-card" style="padding: 1rem 1.25rem; margin-top: 1rem; margin-bottom: 1rem; border-left: 4px solid var(--color-primary);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
                <div style="flex: 1 1 300px;">
                    <div style="font-size: 0.72rem; text-transform: uppercase; color: var(--color-primary); font-weight: 700; letter-spacing: 0.5px;">Planetary Target Affinity</div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #202020; margin: 2px 0 6px 0;">{rel['primary_target']}</div>
                    <div style="font-size: 0.85rem; color: #444444; line-height: 1.5;">{rel['fidelity_summary']}</div>
                </div>
                <div style="flex: 1 1 250px; background-color: var(--background-color-subtle); border-radius: 6px; padding: 10px 12px; border: 1px solid var(--border-color-subtle);">
                    <div style="font-size: 0.72rem; text-transform: uppercase; color: #555555; font-weight: 600; letter-spacing: 0.5px;">Terrain Classification</div>
                    <div style="font-size: 0.85rem; color: #202020; margin-top: 3px; line-height: 1.5;">
                        <strong>{selected_analog['biome']}</strong> ({selected_analog['koppen_climate']}) with {selected_analog['elevation_m']} m elevation, {selected_analog['relief_m']} m local relief, and {selected_analog['mean_slope_deg']}° slope.
                    </div>
                </div>
            </div>
        </div>
        """
    )

    # Expandable Detailed Scientific Documentation
    with st.expander("🔬 Detailed Scientific Documentation & In-Situ Parameters", expanded=False):
        tab_geo, tab_env, tab_rel, tab_nasa, tab_refs = st.tabs([
            "Lithological Stratigraphy & Minerals",
            "Extended Environmental Regimes",
            "Exploration Campaigns & Processes",
            "NASA POWER Climatology API",
            "Peer-Reviewed References & Citations"
        ])

        with tab_geo:
            geology = selected_analog["geology"]
            with st.container(border=True):
                render_rhombus_card_header("Lithological Stratigraphy", "Rock types and formation context")
                render_html(
                    f"""
                    <div style="font-size: 0.95rem; color: #202020; margin-bottom: 0.5rem;">
                        <strong>Classification:</strong> <code style="background-color: var(--color-primary-lighter); color: var(--color-primary-dark); padding: 2px 6px; border-radius: 4px;">{geology['lithology_type']}</code>
                    </div>
                    <div style="font-size: 0.875rem; color: #555555; line-height: 1.5;">
                        <strong>Rock Units:</strong> {geology.get('rock_units') or geology.get('stratigraphy', 'Not specified')}
                    </div>
                    """
                )

            c_min, c_geom = st.columns(2)
            with c_min:
                with st.container(border=True):
                    render_rhombus_card_header("Diagnostic Mineral Phases", "")
                    for mineral in geology["dominant_minerals"]:
                        st.markdown(f"- **{mineral}**")

            with c_geom:
                with st.container(border=True):
                    render_rhombus_card_header("Geomorphic Features", "")
                    for feat in geology["geomorphic_features"]:
                        st.markdown(f"- {feat}")

        with tab_env:
            temp = selected_analog["temperature_c"]
            c_t1, c_t2, c_t3, c_t4 = st.columns(4)
            c_t1.metric("Annual Mean Temp", f"{temp['annual_mean']} °C")
            c_t2.metric("Summer Peak", f"{temp['summer_max']} °C")
            c_t3.metric("Winter Minimum", f"{temp['winter_min']} °C")
            c_t4.metric("Diurnal Thermal Swing", f"Δ {temp['diurnal_swing']} °C")

            st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)
            e1, e2, e3, e4 = st.columns(4)
            e1.metric("Annual Precipitation", f"{selected_analog['annual_precipitation_mm']} mm/yr")
            e2.metric("Surface Pressure", f"{selected_analog['atmospheric_pressure_hpa']} hPa")
            e3.metric("Solar UV Index Peak", f"{selected_analog['uv_index_max']} / 15")
            e4.metric("Aqueous Chemistry", f"pH {selected_analog['ph_level']}", f"{selected_analog['salinity_ppt']} ppt salinity")

        with tab_rel:
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                with st.container(border=True):
                    render_rhombus_card_header("Target Exploration Campaigns", "")
                    for mis in rel["analog_mission_targets"]:
                        st.markdown(f"- 🎯 **{mis}**")

            with r_col2:
                with st.container(border=True):
                    render_rhombus_card_header("Planetary Processes Investigated", "")
                    for proc in rel["analog_processes"]:
                        st.markdown(f"- 🔬 {proc}")

        with tab_nasa:
            with st.container(border=True):
                render_rhombus_card_header("NASA POWER Climatology API Integration", f"Live solar insolation and surface temperatures at {coords['latitude']:.4f}°, {coords['longitude']:.4f}°")

                if st.button("📡 Ingest NASA POWER API Data", key="btn_power_query"):
                    with st.spinner("Connecting to NASA Langley Research Center POWER REST API..."):
                        power_result = fetch_nasa_power_climatology(coords["latitude"], coords["longitude"])
                        if power_result.get("status") == "success":
                            st.success(f"✓ {power_result.get('message')}")
                            params = power_result.get("parameters", {})
                            fig_clim = create_nasa_power_climatology_chart(params, selected_analog["name"])
                            st.plotly_chart(fig_clim, use_container_width=True)

                            st.markdown("**Monthly Climatological Parameter Matrix:**")
                            df_power = pd.DataFrame(params)
                            st.dataframe(df_power.style.format("{:.2f}"), use_container_width=True)
                        else:
                            st.warning(f"⚠️ {power_result.get('message')}")
                            st.info("Displaying local calibrated baseline climatology.")

        with tab_refs:
            with st.container(border=True):
                render_rhombus_card_header("Peer-Reviewed Citations & Mission Reports", "Verified academic and space agency publications")
                for ref in selected_analog.get("references", []):
                    url = ref.get("doi") or ref.get("url", "#")
                    render_html(
                        f"""
                        <div style="padding: 0.75rem 1rem; margin-bottom: 0.5rem; background: var(--background-color-subtle); border-radius: 6px; border-left: 3px solid var(--color-primary); border: 1px solid var(--border-color-subtle);">
                            <div style="font-size: 0.85rem; color: #202020; line-height: 1.5;">{ref['citation']}</div>
                            <a href="{url}" target="_blank" style="font-size: 0.78rem; color: var(--color-primary); font-weight: 600; display: inline-block; margin-top: 0.35rem;">🔗 Access Source Publication</a>
                        </div>
                        """
                    )

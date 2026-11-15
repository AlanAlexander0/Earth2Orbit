"""
Earth2Orbit — NASA Data Observatory Module
Organizes mission datasets across Lunar, Martian, and Earth systems with rigorous
4-level integration status attribution adapted to the Rhombus Design System:
- Rhombus Page Header and Data Provenance Standards
- Dataset Cards with Rhombus Badges and high-contrast parameter specifications
- Official NASA PDS and Earthdata Node Archive Links
- Comprehensive Technical Integration Status Audit Matrix
"""

import streamlit as st
import pandas as pd
from modules.nasa_data_loaders import load_data_sources_catalog
from utils.ui_components import (
    render_rhombus_page_header,
    render_scientific_notice,
    render_html,
    render_rhombus_card_header
)


def render_nasa_data_observatory():
    """Renders the comprehensive NASA Data Observatory directory."""

    render_rhombus_page_header(
        title="NASA Data Observatory",
        subtitle="Formal scientific registry of NASA Planetary Data System (PDS) and Earth Observation datasets"
    )

    # Scientific Rigor Notice on Integration Status (Concise)
    render_scientific_notice(
        "Earth2Orbit registers official NASA Planetary Data System (PDS) and Earth Observation products "
        "with transparent integration tiers, technical specifications, and direct archive gateways.",
        strong_prefix="Data Provenance & Registry:"
    )

    catalog = load_data_sources_catalog()
    earth_sources = catalog.get("earth_sources", [])
    planetary_sources = catalog.get("planetary_sources", [])

    def safe_str(d: dict, *keys, fallback: str = "Not specified") -> str:
        """Safely extracts the first non-empty string for the given keys, or fallback."""
        if not isinstance(d, dict):
            return fallback
        for k in keys:
            v = d.get(k)
            if v is not None and str(v).strip():
                return str(v).strip()
        return fallback

    def safe_list(d: dict, *keys) -> list:
        """Safely extracts the first non-empty list for the given keys, or empty list."""
        if not isinstance(d, dict):
            return []
        for k in keys:
            v = d.get(k)
            if isinstance(v, list) and v:
                return v
        return []

    # Status Badge Helper matching Rhombus badge classes
    def get_status_badge(status_code: str, label: str) -> str:
        color_map = {
            "downloaded_and_processed": "rhombus-badge-primary",
            "api_accessed": "rhombus-badge-info",
            "externally_referenced": "rhombus-badge-secondary",
            "planned_future_integration": "rhombus-badge-warning"
        }
        cls = color_map.get(status_code, "rhombus-badge-primary")
        return f'<span class="rhombus-badge {cls}">{label}</span>'

    # Scientific Use dictionary mapping instruments to clear 1-sentence scientific uses
    scientific_uses = {
        "NASA LOLA": "Orbital laser altimetry mapping surface elevation, slope angles, and roughness across lunar candidate landing areas.",
        "NASA LROC": "Sub-meter narrow-angle and wide-angle imaging for lunar polar illumination and boulder distribution analysis.",
        "NASA Diviner": "Bolometric infrared radiometry measuring diurnal surface temperatures and cryogenic PSR cold traps (< 100 K).",
        "NASA MOLA": "Global pulse laser altimetry establishing the Martian vertical datum (Areoid) and basin relief benchmarks.",
        "NASA Odyssey THEMIS": "Thermal infrared multi-band imaging estimating surface regolith grain size and bedrock thermal inertia.",
        "NASA MRO CRISM": "Targeted hyperspectral VNIR/SWIR reflectance mapping clay, phyllosilicate, and carbonate aqueous mineralogy.",
        "NASA MRO HiRISE": "Sub-meter per pixel stereo imaging resolving fine-scale stratigraphy, inverted channels, and boulder fields.",
        "NASA POWER": "Live programmatic retrieval of solar insolation, surface air temperatures, and barometric pressure.",
        "NASA SRTM": "Global 30-meter radar DEM providing baseline orthometric elevation and relief for terrestrial field sites.",
        "NASA ASTER GDEM": "Stereo optical DEM modeling complex alpine terrain and regional surface reflectance.",
        "NASA MODIS": "Moderate-resolution thermal and vegetative radiometry for regional land surface temperature monitoring.",
        "ESA Copernicus Sentinel-2": "Multispectral 10m-20m BOA surface reflectance tracking evaporite salt boundaries and mineral indices."
    }

    tab_moon, tab_mars, tab_earth = st.tabs([
        "The Moon (LOLA, LROC, Diviner)",
        "Mars (MOLA, THEMIS, CRISM, HiRISE)",
        "Earth (SRTM, NASA POWER, Sentinel-2)"
    ])

    with tab_moon:
        render_html(
            """
            <div style="margin: 0.5rem 0 1rem 0;">
                <h3 style="font-size: 1.25rem; font-weight: 700; color: #202020; margin: 0 0 0.25rem 0;">
                    Lunar Reconnaissance Orbiter (LRO) Instruments
                </h3>
                <p style="font-size: 0.85rem; color: #555555; margin: 0;">
                    Topography, imaging, and bolometric thermal radiometry for the Lunar South Pole
                </p>
            </div>
            """
        )
        lunar_sources = [s for s in planetary_sources if s.get("body") == "Moon"]
        for src in lunar_sources:
            badge_html = get_status_badge(
                safe_str(src, "integration_status", fallback="externally_referenced"),
                safe_str(src, "status_label", fallback="Referenced")
            )
            inst = safe_str(src, "instrument", "name", fallback="Lunar Instrument")
            full_n = safe_str(src, "full_name", fallback="")
            title_text = f"{inst} — {full_n}" if full_n else inst
            craft = safe_str(src, "spacecraft", "mission", fallback="Lunar Reconnaissance Orbiter")
            pds_node = safe_str(src, "pds_node", "agency", "provider", fallback="NASA PDS Node")
            ds_id = safe_str(src, "dataset_id", fallback="PDS Standard")
            params = safe_list(src, "parameters")
            params_str = ", ".join(params) if params else "Calibrated orbital measurements"
            res = safe_str(src, "resolution", "spatial_resolution", fallback="Calibrated variable resolution")
            units = safe_str(src, "units", fallback="Standard physical units")
            citation = safe_str(src, "citation", fallback="NASA Planetary Data System Documentation")
            url = safe_str(src, "archive_url", "source_url", "endpoint_url", fallback="#")
            sc_use = scientific_uses.get(inst, "Calibrated planetary observation and characterization.")

            render_html(
                f"""
                <div class="rhombus-card" style="border-left: 4px solid var(--color-primary); margin-bottom: 1rem;">
                    <div class="rhombus-card-header" style="margin-bottom: 0.5rem;">
                        <div>
                            <div class="rhombus-card-title">{title_text}</div>
                            <p class="rhombus-card-subtitle">{craft}</p>
                        </div>
                        <div>{badge_html}</div>
                    </div>
                    <div style="font-size: 0.85rem; color: #202020; line-height: 1.5; margin-bottom: 0.5rem;">
                        <strong>Scientific Use:</strong> {sc_use}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color-subtle); padding-top: 0.5rem; margin-top: 0.5rem;">
                        <a href="{url}" target="_blank" style="color: var(--color-primary); font-weight: 600; font-size: 0.82rem;">🔗 Official NASA PDS Archive</a>
                        <details style="font-size: 0.78rem; color: #555555; text-align: right;">
                            <summary style="cursor: pointer; color: #666666; font-weight: 500;">Technical Specifications</summary>
                            <div style="text-align: left; padding-top: 0.4rem; font-size: 0.78rem; color: #444444;">
                                <div><strong>PDS Node:</strong> {pds_node}</div>
                                <div><strong>Dataset ID:</strong> <code>{ds_id}</code></div>
                                <div><strong>Resolution:</strong> {res} | <strong>Units:</strong> {units}</div>
                                <div><strong>Measured Parameters:</strong> {params_str}</div>
                                <div><strong>Citation:</strong> <em>{citation}</em></div>
                            </div>
                        </details>
                    </div>
                </div>
                """
            )

    with tab_mars:
        render_html(
            """
            <div style="margin: 0.5rem 0 1rem 0;">
                <h3 style="font-size: 1.25rem; font-weight: 700; color: #202020; margin: 0 0 0.25rem 0;">
                    Mars Exploration Orbital & In-Situ Instrumentation
                </h3>
                <p style="font-size: 0.85rem; color: #555555; margin: 0;">
                    Orbital altimetry, thermal emission imaging, VNIR hyperspectral data, and sub-meter stereo models
                </p>
            </div>
            """
        )
        mars_sources = [s for s in planetary_sources if s.get("body") == "Mars"]
        for src in mars_sources:
            badge_html = get_status_badge(
                safe_str(src, "integration_status", fallback="externally_referenced"),
                safe_str(src, "status_label", fallback="Referenced")
            )
            inst = safe_str(src, "instrument", "name", fallback="Mars Instrument")
            full_n = safe_str(src, "full_name", fallback="")
            title_text = f"{inst} — {full_n}" if full_n else inst
            craft = safe_str(src, "spacecraft", "mission", fallback="Mars Exploration Spacecraft")
            pds_node = safe_str(src, "pds_node", "agency", "provider", fallback="NASA PDS Node")
            ds_id = safe_str(src, "dataset_id", fallback="PDS Standard")
            params = safe_list(src, "parameters")
            params_str = ", ".join(params) if params else "Calibrated orbital measurements"
            res = safe_str(src, "resolution", "spatial_resolution", fallback="Calibrated variable resolution")
            units = safe_str(src, "units", fallback="Standard physical units")
            citation = safe_str(src, "citation", fallback="NASA Planetary Data System Documentation")
            url = safe_str(src, "archive_url", "source_url", "endpoint_url", fallback="#")
            sc_use = scientific_uses.get(inst, "Calibrated Martian surface observation and analysis.")

            render_html(
                f"""
                <div class="rhombus-card" style="border-left: 4px solid var(--color-secondary); margin-bottom: 1rem;">
                    <div class="rhombus-card-header" style="margin-bottom: 0.5rem;">
                        <div>
                            <div class="rhombus-card-title">{title_text}</div>
                            <p class="rhombus-card-subtitle">{craft}</p>
                        </div>
                        <div>{badge_html}</div>
                    </div>
                    <div style="font-size: 0.85rem; color: #202020; line-height: 1.5; margin-bottom: 0.5rem;">
                        <strong>Scientific Use:</strong> {sc_use}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color-subtle); padding-top: 0.5rem; margin-top: 0.5rem;">
                        <a href="{url}" target="_blank" style="color: var(--color-secondary); font-weight: 600; font-size: 0.82rem;">🔗 Official NASA PDS Archive</a>
                        <details style="font-size: 0.78rem; color: #555555; text-align: right;">
                            <summary style="cursor: pointer; color: #666666; font-weight: 500;">Technical Specifications</summary>
                            <div style="text-align: left; padding-top: 0.4rem; font-size: 0.78rem; color: #444444;">
                                <div><strong>PDS Node:</strong> {pds_node}</div>
                                <div><strong>Dataset ID:</strong> <code>{ds_id}</code></div>
                                <div><strong>Resolution:</strong> {res} | <strong>Units:</strong> {units}</div>
                                <div><strong>Measured Parameters:</strong> {params_str}</div>
                                <div><strong>Citation:</strong> <em>{citation}</em></div>
                            </div>
                        </details>
                    </div>
                </div>
                """
            )

    with tab_earth:
        render_html(
            """
            <div style="margin: 0.5rem 0 1rem 0;">
                <h3 style="font-size: 1.25rem; font-weight: 700; color: #202020; margin: 0 0 0.25rem 0;">
                    Terrestrial Remote Sensing & Atmospheric Feeds
                </h3>
                <p style="font-size: 0.85rem; color: #555555; margin: 0;">
                    NASA SRTM elevation, NASA POWER solar climatology, and ESA Copernicus Sentinel-2 multispectral imagery
                </p>
            </div>
            """
        )
        for src in earth_sources:
            badge_html = get_status_badge(
                safe_str(src, "integration_status", fallback="externally_referenced"),
                safe_str(src, "status_label", fallback="Referenced")
            )
            name = safe_str(src, "name", fallback="Terrestrial Feed")
            full_n = safe_str(src, "full_name", fallback="")
            title_text = f"{name} — {full_n}" if full_n else name
            agency = safe_str(src, "agency", "provider", fallback="Earth Observation Agency")
            protocol = safe_str(src, "access_protocol", fallback="Public Web / REST")
            res = safe_str(src, "spatial_resolution", "resolution", fallback="Variable")
            temporal = safe_str(src, "temporal_coverage", fallback="Standard Mission Duration")
            params = safe_list(src, "parameters")
            params_str = ", ".join(params) if params else "Terrestrial surface parameters"
            citation = safe_str(src, "citation", fallback="Technical documentation")
            url = safe_str(src, "endpoint_url", "source_url", "url", fallback="#")
            sc_use = scientific_uses.get(name, "Calibrated Earth observation and field site characterization.")

            render_html(
                f"""
                <div class="rhombus-card" style="border-left: 4px solid var(--color-info); margin-bottom: 1rem;">
                    <div class="rhombus-card-header" style="margin-bottom: 0.5rem;">
                        <div>
                            <div class="rhombus-card-title">{title_text}</div>
                            <p class="rhombus-card-subtitle">{agency}</p>
                        </div>
                        <div>{badge_html}</div>
                    </div>
                    <div style="font-size: 0.85rem; color: #202020; line-height: 1.5; margin-bottom: 0.5rem;">
                        <strong>Scientific Use:</strong> {sc_use}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color-subtle); padding-top: 0.5rem; margin-top: 0.5rem;">
                        <a href="{url}" target="_blank" style="color: var(--color-info-dark); font-weight: 600; font-size: 0.82rem;">🔗 Access Data Gateway</a>
                        <details style="font-size: 0.78rem; color: #555555; text-align: right;">
                            <summary style="cursor: pointer; color: #666666; font-weight: 500;">Technical Specifications</summary>
                            <div style="text-align: left; padding-top: 0.4rem; font-size: 0.78rem; color: #444444;">
                                <div><strong>Protocol:</strong> {protocol} | <strong>Resolution:</strong> {res}</div>
                                <div><strong>Temporal:</strong> {temporal}</div>
                                <div><strong>Measured Parameters:</strong> {params_str}</div>
                                <div><strong>Citation:</strong> <em>{citation}</em></div>
                            </div>
                        </details>
                    </div>
                </div>
                """
            )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Closed Expandable Integration Audit Matrix
    with st.expander("📊 Complete Dataset Integration Status Audit Matrix", expanded=False):
        all_sources = []
        for s in planetary_sources:
            inst = safe_str(s, "instrument", "name", fallback="Planetary Instrument")
            craft = safe_str(s, "spacecraft", "mission", fallback="")
            dataset_label = f"{inst} ({craft})" if craft else inst
            all_sources.append({
                "Body": safe_str(s, "body", fallback="Planetary"),
                "Dataset / Sensor": dataset_label,
                "Technical Status": safe_str(s, "status_label", fallback="Referenced"),
                "Resolution": safe_str(s, "resolution", "spatial_resolution", fallback="Variable"),
                "PDS Node / Source": safe_str(s, "pds_node", "provider", "agency", fallback="NASA PDS Node")
            })
        for s in earth_sources:
            name = safe_str(s, "name", fallback="Terrestrial Dataset")
            sensor = safe_str(s, "sensor", "instrument", "full_name", fallback="")
            dataset_label = f"{name} ({sensor})" if sensor and sensor != name else name
            all_sources.append({
                "Body": "Earth",
                "Dataset / Sensor": dataset_label,
                "Technical Status": safe_str(s, "status_label", fallback="Referenced"),
                "Resolution": safe_str(s, "spatial_resolution", "resolution", fallback="Variable"),
                "PDS Node / Source": safe_str(s, "provider", "agency", fallback="NASA Earthdata")
            })

        df_audit = pd.DataFrame(all_sources)
        st.dataframe(df_audit, use_container_width=True)

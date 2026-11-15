"""
Planetary Analog Explorer - NASA & ESA Planetary Data Integration Catalog
Modular viewer for official NASA & ESA planetary and Earth observation datasets.
"""

import streamlit as st
import pandas as pd
from modules.nasa_data_loaders import load_data_sources_catalog, fetch_nasa_power_climatology
from utils.ui_components import render_scientific_notice


def render_data_catalog():
    """Renders the comprehensive NASA and ESA planetary data integration directory."""
    
    st.markdown("## 🛰️ NASA Planetary Data System (PDS) & Earthdata Integration")
    st.markdown(
        "Explore official NASA Planetary Data System (PDS) and Earth Science data products used "
        "to characterize terrestrial analogs and extraterrestrial landing sites. "
        "All products are cited with dataset IDs, spatial resolution, physical units, and official archive links."
    )

    render_scientific_notice(
        "To ensure sustainable bandwidth and local execution speed without massive multi-gigabyte downloads, "
        "this platform uses calibrated regional samples and direct REST API endpoints (e.g. NASA POWER) "
        "alongside official NASA PDS Geosciences and Imaging Node metadata schemas.",
        strong_prefix="DATA INGESTION ARCHITECTURE:"
    )

    catalog = load_data_sources_catalog()
    earth_sources = catalog.get("earth_sources", [])
    planetary_sources = catalog.get("planetary_sources", [])

    tab_earth, tab_moon, tab_mars = st.tabs([
        "🌍 Earth Observation Archives (NASA & ESA)",
        "🌕 Lunar Instruments (NASA LOLA, LROC, Diviner)",
        "🔴 Martian Instruments (NASA MOLA, CRISM, THEMIS, HiRISE)"
    ])

    with tab_earth:
        st.markdown("### Terrestrial Remote Sensing & Climatology Datasets")
        for src in earth_sources:
            st.markdown(
                f"""
                <div class="sc-card" style="border-left: 4px solid #10b981; margin-bottom: 1.2rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <h4 style="margin: 0; color: #ffffff;">{src['name']} — {src['full_name']}</h4>
                        <span class="sc-badge badge-earth">{src['agency']}</span>
                    </div>
                    <div style="margin-top: 0.6rem; font-size: 0.85rem; color: #cbd5e1; line-height: 1.6;">
                        <p style="margin: 2px 0;"><strong>Measured Parameters:</strong> {', '.join(src['parameters'])}</p>
                        <p style="margin: 2px 0;"><strong>Spatial Resolution:</strong> {src['spatial_resolution']}</p>
                        <p style="margin: 2px 0;"><strong>Temporal Coverage:</strong> {src['temporal_coverage']}</p>
                        <p style="margin: 2px 0;"><strong>Access Protocol:</strong> {src['access_protocol']}</p>
                    </div>
                    <div style="margin-top: 0.6rem; padding-top: 0.5rem; border-top: 1px solid rgba(255,255,255,0.06); font-size: 0.8rem; color: #94a3b8;">
                        <strong>Citation:</strong> <em>{src['citation']}</em><br>
                        <a href="{src['endpoint_url']}" target="_blank" style="color: #38bdf8;">🔗 Official Archive / Endpoint URL</a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with tab_moon:
        st.markdown("### Lunar Reconnaissance Orbiter (LRO) Instruments")
        lunar_sources = [s for s in planetary_sources if s.get("body") == "Moon"]
        for src in lunar_sources:
            st.markdown(
                f"""
                <div class="sc-card" style="border-left: 4px solid #c8d6e5; margin-bottom: 1.2rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <h4 style="margin: 0; color: #ffffff;">{src['instrument']} — {src['full_name']}</h4>
                        <span class="sc-badge badge-moon">{src['spacecraft']}</span>
                    </div>
                    <div style="margin-top: 0.6rem; font-size: 0.85rem; color: #cbd5e1; line-height: 1.6;">
                        <p style="margin: 2px 0;"><strong>PDS Node:</strong> {src['pds_node']}</p>
                        <p style="margin: 2px 0;"><strong>Standard Dataset ID:</strong> <code>{src['dataset_id']}</code></p>
                        <p style="margin: 2px 0;"><strong>Parameters:</strong> {', '.join(src['parameters'])}</p>
                        <p style="margin: 2px 0;"><strong>Spatial Resolution:</strong> {src['resolution']}</p>
                        <p style="margin: 2px 0;"><strong>Physical Units:</strong> {src['units']}</p>
                    </div>
                    <div style="margin-top: 0.6rem; padding-top: 0.5rem; border-top: 1px solid rgba(255,255,255,0.06); font-size: 0.8rem; color: #94a3b8;">
                        <strong>Citation:</strong> <em>{src['citation']}</em><br>
                        <a href="{src['archive_url']}" target="_blank" style="color: #38bdf8;">🔗 Access NASA PDS Geosciences / Imaging Node Archive</a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with tab_mars:
        st.markdown("### Mars Exploration Orbital & In-Situ Instrumentation")
        mars_sources = [s for s in planetary_sources if s.get("body") == "Mars"]
        for src in mars_sources:
            st.markdown(
                f"""
                <div class="sc-card" style="border-left: 4px solid #ff6b4a; margin-bottom: 1.2rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <h4 style="margin: 0; color: #ffffff;">{src['instrument']} — {src['full_name']}</h4>
                        <span class="sc-badge badge-mars">{src['spacecraft']}</span>
                    </div>
                    <div style="margin-top: 0.6rem; font-size: 0.85rem; color: #cbd5e1; line-height: 1.6;">
                        <p style="margin: 2px 0;"><strong>PDS Node:</strong> {src['pds_node']}</p>
                        <p style="margin: 2px 0;"><strong>Standard Dataset ID:</strong> <code>{src['dataset_id']}</code></p>
                        <p style="margin: 2px 0;"><strong>Parameters:</strong> {', '.join(src['parameters'])}</p>
                        <p style="margin: 2px 0;"><strong>Spatial Resolution:</strong> {src['resolution']}</p>
                        <p style="margin: 2px 0;"><strong>Physical Units:</strong> {src['units']}</p>
                    </div>
                    <div style="margin-top: 0.6rem; padding-top: 0.5rem; border-top: 1px solid rgba(255,255,255,0.06); font-size: 0.8rem; color: #94a3b8;">
                        <strong>Citation:</strong> <em>{src['citation']}</em><br>
                        <a href="{src['archive_url']}" target="_blank" style="color: #38bdf8;">🔗 Access NASA Planetary Data System Node</a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

"""
Earth2Orbit — About Module
Project mission, scientific objectives, empirical methodology, technology stack,
limitations, and future roadmap adapted to the Rhombus Design System:
- Rhombus Page Header and Specification Panel
- High-contrast typography and clean tabbed cards
- Rigorous scientific caveats and academic independence disclaimers
"""

import streamlit as st
from utils.ui_components import (
    render_rhombus_page_header,
    render_scientific_notice,
    render_html,
    render_rhombus_card_header
)


def render_about_page():
    """Renders the comprehensive About Earth2Orbit scientific dossier."""

    render_rhombus_page_header(
        title="About Earth2Orbit",
        subtitle="NASA Space Apps Challenge 2026 // Developed by Team: QuantumBoyzz"
    )

    # Core Identity Card
    render_html(
        """
        <div class="rhombus-card" style="border-top: 4px solid var(--color-primary); padding: 1.5rem; margin-bottom: 1.25rem;">
            <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: var(--color-primary); font-weight: 700;">
                Project Specification
            </div>
            <h2 style="font-size: 1.75rem; font-weight: 700; color: #202020; margin: 0.4rem 0 0.2rem 0;">
                Earth2Orbit — Planetary Analog Explorer
            </h2>
            <div style="font-size: 0.95rem; font-weight: 600; color: var(--color-secondary-dark); margin-bottom: 0.8rem;">
                Connecting Earth's Landscapes to Other Worlds.
            </div>
            <div style="font-size: 0.875rem; color: #333333; line-height: 1.6;">
                <strong>Challenge Theme:</strong> Identify Earth Locations that Analog the Permanent Moon Base Locations and Mars.<br>
                <strong>Team:</strong> QuantumBoyzz<br>
                <strong>Event:</strong> NASA Space Apps Challenge 2026
            </div>
        </div>
        """
    )

    # Simplified Core Content: Motivation, Objectives, and Physical Constraints
    c_left, c_right = st.columns(2)

    with c_left:
        with st.container(border=True):
            render_rhombus_card_header("Project Motivation & Objectives", "Why terrestrial analogs matter")
            st.markdown(
                """
                Extraterrestrial exploration is constrained by extreme cost and operational risk. 
                Before space agency hardware, drilling systems, and instruments are deployed to the Moon or Mars, 
                they must be evaluated in terrestrial testbeds that mirror specific physical and geochemical processes.

                **Core Objectives:**
                1. **Curate Terrestrial Analog Testbeds:** Focus on Indian geological sites (**Lonar Crater**, **Tso Kar Basin**, **Sambhar Salt Lake**) alongside international benchmarks (**Atacama**, **McMurdo**, **Iceland**).
                2. **Transparent Multi-Criteria Evaluation:** Provide an empirical, normalized similarity metric (ACI) across relief, slope, roughness, thermal cycling, lithology, and mineralogy.
                3. **Scientific Integrity:** Emphasize that analogs represent process-level models, not identical planetary duplicates.
                """
            )

    with c_right:
        with st.container(border=True):
            render_rhombus_card_header("Physical Constraints & Scientific Boundaries", "Accounting for environmental disparities")
            st.markdown(
                """
                - **Gravity Disparity:** Earth (1.0 g / 9.81 m/s²) vs Moon (0.166 g / 1.62 m/s²) and Mars (0.379 g / 3.72 m/s²) fundamentally alters sediment transport and slope stability.
                - **Atmospheric Regimes:** The Moon is an ultra-high vacuum (< 10⁻¹² hPa); Mars has a thin 6.1 hPa CO₂ atmosphere. Liquid water is thermodynamically unstable on both surfaces today.
                - **Radiation & Shielding:** Earth's magnetosphere blocks solar particle events and cosmic rays that strike extraterrestrial surfaces unattenuated.
                - **Biosphere Overprint:** All terrestrial sites possess microbial life and organic chemistry absent from pristine regolith.
                """
            )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Planned Future Capabilities (Clearly labeled as planned, not implemented)
    with st.expander("🚀 Planned Future Enhancements (Roadmap — Not Yet Implemented)", expanded=False):
        st.markdown(
            """
            *Note: The following capabilities are planned conceptual roadmap milestones and are not yet implemented in the current release:*
            - **Cloud Raster Ingestion:** Streaming integration with AWS Registry of Open Data for full-resolution NASA LOLA polar DEM tiles.
            - **Spectral Angle Mapper (SAM):** Real-time spectral matching between laboratory reflectance spectra and orbital CRISM hyperspectral cubes.
            - **ISRO Planetary Feeds:** Incorporating Chandrayaan-1 Moon Mineralogy Mapper (M³) and Chandrayaan-2/3 TMC-2 terrain datasets.
            - **Field Data Upload Portal:** Capability for field scientists to upload in-situ GPS, geochemical assays, and XRD mineral counts.
            """
        )

    # Open-Source Licenses & Software Credits
    with st.expander("📄 Open-Source Licenses & Software Credits", expanded=False):
        st.markdown(
            """
            - **UI Framework Components:** Adapted under MIT License (Copyright © Hummingbird UI).
            - **Core Scientific Libraries:** Python 3.12, Streamlit, Folium, Streamlit-Folium, Plotly, NumPy, Pandas, Scikit-learn, ReportLab.
            - **Geodetic & Space Agency Data:** NASA Planetary Data System (PDS), NASA POWER API, USGS, and ESA Copernicus Open Access Hub.
            """
        )

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    render_scientific_notice(
        "Earth2Orbit was developed independently by Team QuantumBoyzz for the NASA Space Apps Challenge 2026. "
        "It utilizes public scientific data provided by NASA, ESA, USGS, and peer-reviewed literature. "
        "This educational platform does not claim official endorsement or validation by NASA.",
        strong_prefix="Academic Independence & Data Attribution:"
    )

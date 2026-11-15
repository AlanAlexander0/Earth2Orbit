"""
Earth2Orbit — Planetary Analog Explorer
NASA Space Apps Challenge 2026 // Geospatial Research Platform

A professional geospatial research platform adapted to the Rhombus Dashboard Design System.
Compares terrestrial planetary analog environments (Tso Kar, Lonar Crater, Sambhar Lake, Atacama, McMurdo, Iceland)
with lunar (South Pole, Artemis candidates) and Martian (Jezero Crater) environments using transparent, evidence-based methodology.

Developed by Team: QuantumBoyzz
"""

import os
import streamlit as st

# Streamlit Page Configuration - Rhombus Dashboard Theme
st.set_page_config(
    page_title="Earth2Orbit — Planetary Analog Explorer",
    page_icon="⊛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and inject Rhombus CSS
STYLE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "style.css")
if os.path.exists(STYLE_PATH):
    with open(STYLE_PATH, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Import Data Loaders
from modules.nasa_data_loaders import (
    load_earth_analogs,
    load_planetary_targets,
    load_terrain_profiles,
    load_data_sources_catalog
)

# Import Module Views
from modules.home_dashboard import render_home_dashboard
from modules.earth_explorer import render_earth_explorer
from modules.planetary_targets import render_planetary_targets
from modules.comparison_engine import render_comparison_engine
from modules.terrain_analysis import render_terrain_analysis
from modules.nasa_data_observatory import render_nasa_data_observatory
from modules.research_report import render_research_report
from modules.about_page import render_about_page
from utils.ui_components import render_rhombus_topbar, render_html


def main():
    # Load cached datasets
    earth_analogs = load_earth_analogs()
    planetary_bodies = load_planetary_targets()
    terrain_profiles = load_terrain_profiles()
    data_sources = load_data_sources_catalog()

    # Navigation Module List (Rhombus Navigation Style)
    nav_options = [
        "Overview",
        "Earth Analog Explorer",
        "Planetary Targets",
        "Comparison Laboratory",
        "Terrain Analysis",
        "NASA Data Observatory",
        "Research Reports",
        "About Earth2Orbit"
    ]

    # Initialize or synchronize session navigation state
    if "nav_module" not in st.session_state:
        st.session_state["nav_module"] = nav_options[0]

    if st.session_state["nav_module"] not in nav_options:
        st.session_state["nav_module"] = nav_options[0]

    # Sidebar Navigation & Branding (Rhombus Sidebar Pattern)
    with st.sidebar:
        # Rhombus Logo + Brand Header
        render_html(
            """
            <div class="rhombus-sidebar-brand">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="11.5" y="0.893372" width="15" height="15" transform="rotate(45 11.5 0.893372)" fill="white" stroke="#202020" stroke-width="1.5" stroke-linejoin="round"/>
                    <rect x="11.5" y="10.0147" width="8" height="8" transform="rotate(45 11.5 10.0147)" fill="#775da6" stroke="#775da6" stroke-linejoin="round"/>
                    <rect x="11.5" y="7.25739" width="6" height="6" transform="rotate(45 11.5 7.25739)" fill="#f9837c" stroke="#202020" stroke-width="0.5" stroke-linejoin="round"/>
                </svg>
                <div>
                    <div class="rhombus-sidebar-title">Earth2Orbit</div>
                    <div class="rhombus-sidebar-tagline">Planetary Analogs</div>
                </div>
            </div>
            """
        )

        st.caption("NAVIGATION")

        # Navigation Radio (Styled as Rhombus list-group items)
        nav_index = nav_options.index(st.session_state["nav_module"])
        selected_nav = st.radio(
            "Navigation Menu:",
            options=nav_options,
            index=nav_index,
            label_visibility="collapsed"
        )

        if selected_nav != st.session_state["nav_module"]:
            st.session_state["nav_module"] = selected_nav
            st.rerun()

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # Rhombus Sidebar Footer Card
        render_html(
            """
            <div class="rhombus-sidebar-footer">
                <h4>Earth2Orbit Research Kit</h4>
                <p>NASA Space Apps 2026<br>Team: QuantumBoyzz<br>
                <a href="#about" onclick="window.location.reload();">Documentation & Specs</a>
                </p>
            </div>
            """
        )

    # Top Application Header Bar (Rhombus Topbar)
    render_rhombus_topbar()

    # Route to Selected Module
    current_module = st.session_state["nav_module"]

    if current_module == "Overview":
        render_home_dashboard(earth_analogs, planetary_bodies)
    elif current_module == "Earth Analog Explorer":
        render_earth_explorer(earth_analogs)
    elif current_module == "Planetary Targets":
        render_planetary_targets(planetary_bodies)
    elif current_module == "Comparison Laboratory":
        render_comparison_engine(earth_analogs, planetary_bodies, terrain_profiles)
    elif current_module == "Terrain Analysis":
        render_terrain_analysis(earth_analogs, planetary_bodies, terrain_profiles)
    elif current_module == "NASA Data Observatory":
        render_nasa_data_observatory()
    elif current_module == "Research Reports":
        render_research_report(earth_analogs, planetary_bodies, data_sources)
    elif current_module == "About Earth2Orbit":
        render_about_page()


if __name__ == "__main__":
    main()

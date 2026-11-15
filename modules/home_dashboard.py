"""
Earth2Orbit — Overview Dashboard Module
Faithfully adapted to the Rhombus CRM Dashboard layout, components, and visual hierarchy:
- Rhombus Greeting & Action Buttons
- 4-Column Stat Cards with thin progress bars
- 3-Card Interactive Chart Row (Target Distribution Donut, Elevation Profile Bars, Exploration Frontiers)
- Top Performance Analog Benchmarks Striped Table & Research Tasks Card
"""

import streamlit as st
from utils.ui_components import (
    render_rhombus_page_header,
    render_rhombus_stat_card,
    render_rhombus_kpi_row,
    render_rhombus_card_header,
    render_scientific_notice,
    render_html
)
from modules.visualizations import (
    create_rhombus_donut_chart,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_INFO,
    COLOR_WARNING,
    COLOR_TEXT,
    COLOR_MUTED
)
import plotly.graph_objects as go


def render_home_dashboard(earth_analogs: list, planetary_bodies: list):
    """Renders the Earth2Orbit Overview dashboard styled to Rhombus specifications."""

    # 1. Rhombus Greeting & Action Buttons Header
    col_head_left, col_head_right = st.columns([3, 1.5])
    with col_head_left:
        render_html(
            """
            <div style="margin-bottom: 1.5rem;">
                <h1 style="font-size: 2.25rem; font-weight: 700; color: #202020; margin: 0 0 0.5rem 0; line-height: 1.2;">
                    Earth2Orbit — Planetary Analog Explorer
                </h1>
                <p style="font-size: 0.95rem; color: #555555; margin: 0;">
                    Connecting terrestrial landscapes to exploration environments on the Moon and Mars • NASA Space Apps Challenge 2026
                </p>
            </div>
            """
        )

    with col_head_right:
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        h_btn1, h_btn2 = st.columns(2)
        with h_btn1:
            if st.button("Explore Analogs", use_container_width=True):
                st.session_state["nav_module"] = "Earth Analog Explorer"
                st.rerun()
        with h_btn2:
            if st.button("+ Compare Sites", use_container_width=True):
                st.session_state["nav_module"] = "Comparison Laboratory"
                st.rerun()

    # 2. Rhombus 4-Stat Cards Grid (Standardized, Equal Height, Bottom-Anchored Progress Bars)
    total_sites = len(earth_analogs)
    total_targets = sum(len(b.get("targets", [])) for b in planetary_bodies)

    icon_briefcase = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>'
    icon_wallet = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M2 12h20"></path><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>'
    icon_trend = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>'
    icon_send = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'

    kpi_cards = [
        {
            "value": f"{total_sites} Analogs",
            "label": "Active Terrestrial Benchmarks",
            "icon_svg": icon_briefcase,
            "color": "primary",
            "percent": 100
        },
        {
            "value": "2 Worlds",
            "label": "Moon & Mars Reference Bodies",
            "icon_svg": icon_wallet,
            "color": "secondary",
            "percent": 85
        },
        {
            "value": f"{total_targets} Candidate Sites",
            "label": "Lunar South Pole & Jezero Delta",
            "icon_svg": icon_trend,
            "color": "info",
            "percent": 90
        },
        {
            "value": "81.4% ACI",
            "label": "Highest ACI Score (Lonar vs Lunar South Pole)",
            "icon_svg": icon_send,
            "color": "warning",
            "percent": 81
        }
    ]

    render_rhombus_kpi_row(kpi_cards)

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    # 3. Rhombus Charts Row (3 Columns)
    ch1, ch2, ch3 = st.columns([1, 1, 1.2])

    with ch1:
        with st.container(border=True):
            render_rhombus_card_header("Target Analog Relevance", "Distribution across Moon & Mars")
            donut_fig = create_rhombus_donut_chart(
                values=[3, 3],
                labels=["Lunar Candidates", "Martian Analogs"],
                colors=[COLOR_PRIMARY, COLOR_SECONDARY]
            )
            st.plotly_chart(donut_fig, use_container_width=True, config={"displayModeBar": False})
            render_html(
                f"""
                <ul style="list-style: none; padding: 0; margin: 0.5rem 0 0 0; display: flex; justify-content: center; gap: 1.5rem; font-size: 0.8125rem;">
                    <li style="display: flex; align-items: center; gap: 6px;">
                        <span style="width: 8px; height: 8px; border-radius: 50%; background-color: {COLOR_PRIMARY};"></span> 3 Lunar Sites
                    </li>
                    <li style="display: flex; align-items: center; gap: 6px;">
                        <span style="width: 8px; height: 8px; border-radius: 50%; background-color: {COLOR_SECONDARY};"></span> 3 Martian Sites
                    </li>
                </ul>
                """
            )

    with ch2:
        with st.container(border=True):
            render_rhombus_card_header("Elevation Comparison", "Meters a.s.l. (NASA SRTM 30m)")
            site_names = [s["name"].split()[0] for s in earth_analogs]
            elevations = [s["elevation_m"] for s in earth_analogs]
            bar_colors = [COLOR_PRIMARY, COLOR_INFO, COLOR_SECONDARY, COLOR_WARNING, COLOR_PRIMARY, COLOR_INFO]

            bar_fig = go.Figure(go.Bar(
                x=site_names,
                y=elevations,
                marker=dict(color=bar_colors[:len(site_names)], line=dict(color='#ffffff', width=1)),
                hovertemplate="<b>%{x}</b><br>Elevation: %{y:,} m a.s.l.<extra></extra>"
            ))
            bar_fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(tickfont=dict(size=9, color=COLOR_MUTED), gridcolor='#ececec'),
                yaxis=dict(tickfont=dict(size=9, color=COLOR_MUTED), gridcolor='#ececec', title="Meters")
            )
            st.plotly_chart(bar_fig, use_container_width=True, config={"displayModeBar": False})

    with ch3:
        with st.container(border=True):
            render_rhombus_card_header("Planetary Reference Regions", "Lunar South Pole & Jezero Crater Research Targets.")
            render_html(
                f"""
                <div style="font-size: 1.75rem; font-weight: 700; color: #202020; margin-top: 0.5rem; line-height: 1;">
                    2 Planetary Reference Regions
                </div>
                <div style="font-size: 0.8125rem; color: #555555; margin-bottom: 1rem;">
                    Planetary reference environments for comparative evaluation
                </div>
                <div style="background-color: var(--background-color-subtle); border-radius: 6px; padding: 0.75rem; border: 1px solid var(--border-color-subtle); margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600; font-size: 0.85rem; color: #202020;">Lunar South Pole (Luna)</span>
                        <span class="rhombus-badge rhombus-badge-primary">Candidate Artemis Region</span>
                    </div>
                    <div style="font-size: 0.775rem; color: #555555; margin-top: 0.25rem;">
                        Permanently Shadowed Regions (PSRs) at 40–110 K preserving potential volatile deposits.
                    </div>
                </div>
                <div style="background-color: var(--background-color-subtle); border-radius: 6px; padding: 0.75rem; border: 1px solid var(--border-color-subtle);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600; font-size: 0.85rem; color: #202020;">Jezero Crater (Mars)</span>
                        <span class="rhombus-badge rhombus-badge-secondary">Perseverance Landing Site</span>
                    </div>
                    <div style="font-size: 0.775rem; color: #555555; margin-top: 0.25rem;">
                        Ancient Late Noachian lacustrine delta with clay and Mg-carbonate stratigraphy.
                    </div>
                </div>
                """
            )

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    # 4. Performance Benchmarks Table & Scientific Tasks Row
    t_col1, t_col2 = st.columns([2, 1])

    with t_col1:
        with st.container(border=True):
            render_rhombus_card_header("Primary Terrestrial Analog Benchmarks", "Verified Analog Compatibility Index (ACI) against planetary targets")
            render_html(
                """
                <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1rem; background-color: var(--background-color-subtle); border-radius: 6px; border: 1px solid var(--border-color-subtle); border-left: 4px solid #775da6;">
                        <div style="min-width: 0; padding-right: 12px;">
                            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                                <span style="font-weight: 700; color: #202020; font-size: 0.95rem;">1. Lonar Crater</span>
                                <span class="rhombus-badge rhombus-badge-primary">Lunar South Pole</span>
                            </div>
                            <div style="font-size: 0.8rem; color: #555555; margin-top: 3px;">
                                Maharashtra, India • Basaltic impact breccia and maskelynite shock deformation analog for lunar highland craters.
                            </div>
                        </div>
                        <div style="text-align: right; min-width: 85px;">
                            <div style="font-size: 1.35rem; font-weight: 700; color: #775da6; line-height: 1;">81.4%</div>
                            <div style="font-size: 0.68rem; color: #666666; text-transform: uppercase; font-weight: 600; margin-top: 2px;">ACI Score</div>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1rem; background-color: var(--background-color-subtle); border-radius: 6px; border: 1px solid var(--border-color-subtle); border-left: 4px solid #f9837c;">
                        <div style="min-width: 0; padding-right: 12px;">
                            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                                <span style="font-weight: 700; color: #202020; font-size: 0.95rem;">2. Tso Kar Basin</span>
                                <span class="rhombus-badge rhombus-badge-secondary">Jezero Crater (Mars)</span>
                            </div>
                            <div style="font-size: 0.8rem; color: #555555; margin-top: 3px;">
                                Ladakh, India • High-altitude cold evaporite playa modeling Jezero lacustrine carbonate-clay stratigraphy.
                            </div>
                        </div>
                        <div style="text-align: right; min-width: 85px;">
                            <div style="font-size: 1.35rem; font-weight: 700; color: #775da6; line-height: 1;">79.2%</div>
                            <div style="font-size: 0.68rem; color: #666666; text-transform: uppercase; font-weight: 600; margin-top: 2px;">ACI Score</div>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1rem; background-color: var(--background-color-subtle); border-radius: 6px; border: 1px solid var(--border-color-subtle); border-left: 4px solid #70b6c1;">
                        <div style="min-width: 0; padding-right: 12px;">
                            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                                <span style="font-weight: 700; color: #202020; font-size: 0.95rem;">3. Sambhar Salt Lake</span>
                                <span class="rhombus-badge rhombus-badge-secondary">Jezero Crater (Mars)</span>
                            </div>
                            <div style="font-size: 0.8rem; color: #555555; margin-top: 3px;">
                                Rajasthan, India • Hypersaline alkaline playa and sulfate crusts modeling Martian lacustrine brine basins.
                            </div>
                        </div>
                        <div style="text-align: right; min-width: 85px;">
                            <div style="font-size: 1.35rem; font-weight: 700; color: #775da6; line-height: 1;">74.8%</div>
                            <div style="font-size: 0.68rem; color: #666666; text-transform: uppercase; font-weight: 600; margin-top: 2px;">ACI Score</div>
                        </div>
                    </div>
                </div>
                """
            )
            with st.expander("View Global Reference Standards (Atacama & McMurdo)", expanded=False):
                st.markdown(
                    """
                    - **Atacama Desert (78.5% ACI vs Mars):** Hyper-arid nitrate-perchlorate regolith benchmark.
                    - **McMurdo Dry Valleys (76.1% ACI vs Mars Polar / Lunar PSR):** Hyper-arid cold-desert permafrost polygons.
                    - **Iceland Basalt Provinces (75.3% ACI vs Mars Volcanics):** Unweathered basaltic tephra and lava fields.
                    """
                )

    with t_col2:
        with st.container(border=True):
            render_rhombus_card_header("Research Objectives", "NASA Space Apps 2026 Core Challenge")
            render_html(
                """
                <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 0.5rem; font-size: 0.85rem; color: #202020;">
                    <div style="padding: 10px 12px; background-color: var(--background-color-subtle); border-radius: 6px; border-left: 3px solid #775da6;">
                        <strong style="color: #202020;">Quantitative Evaluation:</strong>
                        <div style="font-size: 0.78rem; color: #555555; margin-top: 2px;">
                            Multi-parameter ACI engine evaluates relief, slope, roughness, thermal swing, lithology, and mineralogy.
                        </div>
                    </div>
                    <div style="padding: 10px 12px; background-color: var(--background-color-subtle); border-radius: 6px; border-left: 3px solid #f9837c;">
                        <strong style="color: #202020;">NASA Planetary Data System:</strong>
                        <div style="font-size: 0.78rem; color: #555555; margin-top: 2px;">
                            Verified orbital data from LOLA, Diviner, MOLA, THEMIS, CRISM, and SRTM elevation datums.
                        </div>
                    </div>
                    <div style="padding: 10px 12px; background-color: var(--background-color-subtle); border-radius: 6px; border-left: 3px solid #70b6c1;">
                        <strong style="color: #202020;">Scientific Integrity:</strong>
                        <div style="font-size: 0.78rem; color: #555555; margin-top: 2px;">
                            Terrestrial analogs model specific physical processes, accounting for gravity, atmospheric, and radiation disparities.
                        </div>
                    </div>
                </div>
                """
            )

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    # 5. Scientific Notice Callout (Concise, with Expandable Methodology)
    render_scientific_notice(
        "Terrestrial analogs provide targeted operational and geomorphic testbeds for specific planetary processes "
        "(cratering, evaporite formation, and permafrost) rather than identical extraterrestrial duplicates.",
        strong_prefix="Planetary Analog Principle:"
    )

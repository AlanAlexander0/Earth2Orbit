"""
Earth2Orbit — Rhombus UI Component Library
Reproduces the exact visual patterns, typography, and layout of the Rhombus CRM Dashboard.
Guarantees ZERO raw HTML leakage by stripping line indentation before Markdown parsing.
"""

import streamlit as st
import textwrap


def clean_html(html_str: str) -> str:
    """
    Cleans an HTML string by stripping indentation and whitespace on every line.
    Prevents CommonMark from interpreting indented HTML lines as code blocks (<pre><code>).
    """
    lines = [line.strip() for line in textwrap.dedent(html_str).splitlines() if line.strip()]
    return "".join(lines)


def render_html(html_str: str):
    """Safely renders HTML in Streamlit without code-block escaping."""
    st.markdown(clean_html(html_str), unsafe_allow_html=True)


def render_rhombus_topbar():
    """
    Renders the exact 72px Rhombus topbar with search bar, help icon,
    notification bell with coral badge, and Team QuantumBoyzz profile pill.
    """
    html = """
    <div class="rhombus-topbar">
        <div class="rhombus-search-box">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#767676" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input type="text" placeholder="Search analog sites, craters, datasets..." />
        </div>
        <div class="rhombus-topbar-right">
            <button class="rhombus-icon-btn" title="Help & Documentation">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                    <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
            </button>
            <button class="rhombus-icon-btn" title="Updates Available">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                    <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                </svg>
                <span class="rhombus-badge-dot"></span>
            </button>
            <div class="rhombus-user-pill">
                <div class="rhombus-user-avatar">QB</div>
                <div class="rhombus-user-info">
                    <div class="rhombus-user-name">Team QuantumBoyzz</div>
                    <div class="rhombus-user-role">NASA Space Apps 2026</div>
                </div>
            </div>
        </div>
    </div>
    """
    render_html(html)


def render_rhombus_page_header(title: str, subtitle: str, badge_text: str = None, badge_color: str = "primary"):
    """
    Renders Rhombus page header with 30px bold text-default title,
    muted descriptive subtitle, and optional status badge.
    """
    badge_html = ""
    if badge_text:
        badge_html = f'<span class="rhombus-badge rhombus-badge-{badge_color}" style="margin-left: 10px; vertical-align: middle;">{badge_text}</span>'

    html = f"""
    <div class="rhombus-page-header">
        <div>
            <h1 class="rhombus-page-title">{title} {badge_html}</h1>
            <p class="rhombus-page-subtitle">{subtitle}</p>
        </div>
    </div>
    """
    render_html(html)


def render_rhombus_stat_card(value: str, label: str, icon_svg: str, color: str = "primary", percent: int = 75):
    """
    Renders the signature Rhombus stat card:
    - Bold 22px-24px value (#202020)
    - Muted high-contrast label (#555555)
    - Color-tinted icon on the top right
    - 4px progress bar with colored fill and percentage indicator anchored at the bottom
    """
    cleaned_icon = clean_html(icon_svg)
    html = f"""
    <div class="rhombus-stat-card">
        <div class="rhombus-stat-top">
            <div class="rhombus-stat-info">
                <div class="rhombus-stat-value">{value}</div>
                <div class="rhombus-stat-label">{label}</div>
            </div>
            <div class="rhombus-stat-icon-wrapper bg-{color}-subtle">
                {cleaned_icon}
            </div>
        </div>
        <div class="rhombus-progress-container">
            <div class="rhombus-progress-track">
                <div class="rhombus-progress-fill bg-{color}-fill" style="width: {percent}%;"></div>
            </div>
            <div class="rhombus-progress-percent">{percent}%</div>
        </div>
    </div>
    """
    render_html(html)


def render_rhombus_kpi_row(cards: list):
    """
    Renders a unified responsive 4-column KPI row with identical heights,
    aligned typography, identical icon dimensions, and bottom-anchored progress bars.
    """
    cards_html = []
    for c in cards:
        val = c.get("value", "")
        lbl = c.get("label", "")
        icon = clean_html(c.get("icon_svg", ""))
        color = c.get("color", "primary")
        pct = c.get("percent", 75)
        snippet = f"""
        <div class="rhombus-stat-card">
            <div class="rhombus-stat-top">
                <div class="rhombus-stat-info">
                    <div class="rhombus-stat-value">{val}</div>
                    <div class="rhombus-stat-label">{lbl}</div>
                </div>
                <div class="rhombus-stat-icon-wrapper bg-{color}-subtle">
                    {icon}
                </div>
            </div>
            <div class="rhombus-progress-container">
                <div class="rhombus-progress-track">
                    <div class="rhombus-progress-fill bg-{color}-fill" style="width: {pct}%;"></div>
                </div>
                <div class="rhombus-progress-percent">{pct}%</div>
            </div>
        </div>
        """
        cards_html.append(snippet)

    grid_html = f"""
    <div class="rhombus-stat-grid">
        {''.join(cards_html)}
    </div>
    """
    render_html(grid_html)


def render_rhombus_metric_grid(metrics: list):
    """
    Renders a clean, responsive metric grid (4 cols on desktop, 2 on medium, 1 on mobile)
    with guaranteed equal heights, high-contrast labels, and no horizontal overflow.
    """
    cards_html = []
    for m in metrics:
        lbl = m.get("label", "")
        val = m.get("value", "")
        delta = m.get("delta")
        delta_html = f'<div class="rhombus-metric-delta">{delta}</div>' if delta else ''
        snippet = f"""
        <div class="rhombus-metric-card">
            <div class="rhombus-metric-label">{lbl}</div>
            <div class="rhombus-metric-value">{val}</div>
            {delta_html}
        </div>
        """
        cards_html.append(snippet)

    grid_html = f"""
    <div class="rhombus-metric-grid">
        {''.join(cards_html)}
    </div>
    """
    render_html(grid_html)


def render_rhombus_card_header(title: str, subtitle: str = ""):
    """Renders a standard Rhombus card header with title, subtitle, and menu dots."""
    sub_html = f'<p class="rhombus-card-subtitle">{subtitle}</p>' if subtitle else ''
    html = f"""
    <div class="rhombus-card-header">
        <div>
            <div class="rhombus-card-title">{title}</div>
            {sub_html}
        </div>
        <div class="rhombus-card-menu">•••</div>
    </div>
    """
    render_html(html)


def render_scientific_notice(text: str, strong_prefix: str = "Scientific Methodology Note:"):
    """Renders a restrained high-contrast scientific callout card in Rhombus style."""
    html = f"""
    <div class="rhombus-notice-card" style="border-left: 4px solid var(--color-primary);">
        <div style="font-size: 0.875rem; color: #202020; line-height: 1.5;">
            <strong style="color: var(--color-primary-dark); font-weight: 600;">{strong_prefix}</strong> {text}
        </div>
    </div>
    """
    render_html(html)


def render_warning_notice(text: str, strong_prefix: str = "Data Limitation & Boundary:"):
    """Renders a coral/secondary-accented limitation note in Rhombus style."""
    html = f"""
    <div class="rhombus-notice-card" style="border-left: 4px solid var(--color-secondary);">
        <div style="font-size: 0.875rem; color: #202020; line-height: 1.5;">
            <strong style="color: var(--color-secondary-dark); font-weight: 600;">{strong_prefix}</strong> {text}
        </div>
    </div>
    """
    render_html(html)


# Backward-compatible aliases
def render_app_header():
    render_rhombus_topbar()

def render_editorial_hero(title: str, subtitle: str, kicker: str = "Planetary Geospatial Research Platform", badges: list = None):
    render_rhombus_page_header(title, subtitle)

def render_metric_card(label: str, value: str, subtext: str = "", border_color: str = "#775da6"):
    html = f"""
    <div class="rhombus-card" style="border-top: 3px solid {border_color}; padding: 1.25rem;">
        <div class="rhombus-stat-label">{label}</div>
        <div class="rhombus-stat-value" style="margin-top: 0.25rem;">{value}</div>
        <div style="font-size: 0.775rem; color: var(--text-color-muted); margin-top: 0.25rem;">{subtext}</div>
    </div>
    """
    render_html(html)

def render_space_showcase_card(title: str, subtitle: str, badge_text: str, badge_type: str, image_url: str = None, description: str = "", meta_items: list = None):
    badge_class = f"rhombus-badge-{badge_type}" if badge_type in ["primary", "secondary", "info", "warning"] else "rhombus-badge-primary"
    meta_html = ""
    if meta_items:
        meta_html = "<div style='display: flex; gap: 1.5rem; flex-wrap: wrap; margin-top: 1rem; border-top: 1px solid var(--border-color-subtle); padding-top: 0.75rem;'>"
        for label, val in meta_items:
            meta_html += f"<div><div style='font-size: 0.72rem; color: #666666; text-transform: uppercase; font-weight: 600;'>{label}</div><div style='font-size: 1.1rem; font-weight: 700; color: #202020; font-family: monospace;'>{val}</div></div>"
        meta_html += "</div>"

    img_html = ""
    if image_url:
        img_html = f"<div style='flex: 1; min-width: 200px; max-width: 260px; border-radius: 8px; overflow: hidden; border: 1px solid var(--border-color-default);'><img src='{image_url}' alt='{title}' style='width: 100%; height: 150px; object-fit: cover; display: block;' /></div>"

    html = f"""
    <div class="rhombus-card">
        <div style="display: flex; gap: 1.5rem; align-items: flex-start; flex-wrap: wrap;">
            <div style="flex: 2; min-width: 260px;">
                <div style="margin-bottom: 0.5rem;">
                    <span class="rhombus-badge {badge_class}">{badge_text}</span>
                </div>
                <div style="font-size: 1.35rem; font-weight: 700; color: #202020; margin-bottom: 0.25rem;">{title}</div>
                <div style="font-size: 0.85rem; color: #666666; margin-bottom: 0.6rem;">{subtitle}</div>
                <p style="margin: 0; font-size: 0.875rem; color: #333333; line-height: 1.55;">{description}</p>
                {meta_html}
            </div>
            {img_html}
        </div>
    </div>
    """
    render_html(html)

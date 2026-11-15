"""
Earth2Orbit — Geospatial & Interactive Visualization Engine
Builds Plotly charts, Folium maps, radar graphs, and topographic cross-sections
styled in the Rhombus CRM Design System (Purple #775da6, Coral #f9837c, Teal #70b6c1, Gold #f3cc5c).
"""

from typing import Dict, Any, List, Optional
import folium
from folium import plugins
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# Rhombus Palette Tokens
COLOR_PRIMARY = "#775da6"       # Purple
COLOR_PRIMARY_DARK = "#634c8d"
COLOR_PRIMARY_LIGHT = "#efecf4"
COLOR_SECONDARY = "#f9837c"     # Coral
COLOR_INFO = "#70b6c1"          # Teal
COLOR_WARNING = "#f3cc5c"       # Gold
COLOR_TEXT = "#202020"          # Dark Charcoal
COLOR_MUTED = "#555555"         # High-Contrast Gray
COLOR_GRID = "#ececec"          # Light Border Gray


def create_earth_folium_map(analogs: List[Dict[str, Any]], selected_id: Optional[str] = None) -> folium.Map:
    """
    Builds an interactive global Folium map showcasing terrestrial planetary analog sites
    with OpenStreetMap (default), Esri Satellite, and OpenTopoMap basemaps styled with Rhombus tokens.
    """
    if analogs and selected_id:
        target = next((a for a in analogs if a["id"] == selected_id), None)
        if target:
            center_lat = target["coordinates"]["latitude"]
            center_lon = target["coordinates"]["longitude"]
            zoom_start = 6
        else:
            center_lat = analogs[0]["coordinates"]["latitude"]
            center_lon = analogs[0]["coordinates"]["longitude"]
            zoom_start = 4
    elif analogs:
        center_lat = analogs[0]["coordinates"]["latitude"]
        center_lon = analogs[0]["coordinates"]["longitude"]
        zoom_start = 4
    else:
        center_lat, center_lon, zoom_start = 20.0, 0.0, 2

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles=None,
        control_scale=True
    )

    # 1. Primary Default Basemap: OpenStreetMap Standard (Fast, reliable, compliant)
    folium.TileLayer(
        tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr='&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors',
        name="OpenStreetMap (Default Research Basemap)",
        overlay=False,
        control=True,
        max_zoom=19
    ).add_to(m)

    # 2. Satellite Imagery Layer: Esri World Imagery
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community",
        name="Esri High-Resolution Satellite",
        overlay=False,
        control=True,
        max_zoom=18
    ).add_to(m)

    # 3. Topographic Layer: OpenTopoMap
    folium.TileLayer(
        tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org" target="_blank">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org" target="_blank">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank">CC-BY-SA</a>)',
        name="OpenTopoMap Topographic Relief",
        overlay=False,
        control=True,
        max_zoom=17
    ).add_to(m)

    # Plot analog locations with Rhombus colored pins
    for a in analogs:
        lat = a["coordinates"]["latitude"]
        lon = a["coordinates"]["longitude"]
        name = a["name"]
        region = f"{a['region']}, {a['country']}"
        is_selected = (a["id"] == selected_id)
        is_primary = a["id"] in ["tso_kar", "lonar_crater", "sambhar_lake"]

        marker_bg = COLOR_PRIMARY if is_selected else (COLOR_INFO if is_primary else "#767676")
        border_col = "#ffffff"

        popup_html = f"""
        <div style="font-family: 'Inter', -apple-system, sans-serif; min-width: 230px; color: #202020; padding: 4px;">
            <div style="border-bottom: 2px solid {COLOR_PRIMARY}; padding-bottom: 6px; margin-bottom: 8px;">
                <span style="font-size: 10px; font-weight: 700; text-transform: uppercase; color: {COLOR_INFO if is_primary else COLOR_PRIMARY};">
                    {'Primary Research Candidate' if is_primary else 'Global Benchmark'}
                </span>
                <div style="font-size: 14px; font-weight: 700; color: #202020; margin-top: 2px;">{name}</div>
                <div style="font-size: 11px; color: #555555;">{region}</div>
            </div>
            <div style="font-size: 11px; line-height: 1.5; color: #333333;">
                <div><strong>Elevation:</strong> {a['elevation_m']} m a.s.l.</div>
                <div><strong>Geology:</strong> {a['geology']['lithology_type']}</div>
                <div><strong>Target Analog:</strong> {a['planetary_analog_relevance']['primary_target']}</div>
                <div style="color: {COLOR_PRIMARY}; font-weight: 600; margin-top: 4px;">Coords: {lat:.4f}° N, {lon:.4f}° E</div>
            </div>
        </div>
        """

        div_icon = folium.DivIcon(
            html=f"""
            <div style="
                background: {marker_bg};
                width: {'22px' if is_selected else '16px'};
                height: {'22px' if is_selected else '16px'};
                border-radius: 50%;
                border: 2px solid {border_col};
                box-shadow: 0 1px 4px rgba(0, 0, 0, 0.25);
                cursor: pointer;
            "></div>
            """,
            icon_size=(22 if is_selected else 16, 22 if is_selected else 16),
            icon_anchor=(11 if is_selected else 8, 11 if is_selected else 8)
        )

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{name} ({region})",
            icon=div_icon
        ).add_to(m)

        if is_selected:
            folium.Circle(
                location=[lat, lon],
                radius=30000,
                color=COLOR_PRIMARY,
                weight=2,
                fill=True,
                fill_color=COLOR_PRIMARY,
                fill_opacity=0.15
            ).add_to(m)

    plugins.Fullscreen(position="topright").add_to(m)
    folium.LayerControl(position="topleft", collapsed=False).add_to(m)
    return m


def create_similarity_radar_chart(results: Dict[str, Any]) -> go.Figure:
    """
    Builds a Plotly radar chart displaying multi-dimensional similarity scores
    in the Rhombus purple palette.
    """
    categories = []
    scores = []
    
    for key, feat in results.get("features", {}).items():
        categories.append(feat["name"])
        scores.append(feat["similarity"] * 100.0)

    if categories:
        categories.append(categories[0])
        scores.append(scores[0])

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        fillcolor='rgba(119, 93, 166, 0.22)',
        line=dict(color=COLOR_PRIMARY, width=2.5),
        marker=dict(size=6, color=COLOR_PRIMARY_DARK),
        name='Analog Compatibility (%)',
        hovertemplate='%{theta}<br><b>Fidelity: %{r:.1f}%</b><extra></extra>'
    ))

    if categories:
        fig.add_trace(go.Scatterpolar(
            r=[100] * len(categories),
            theta=categories,
            mode='lines',
            line=dict(color=COLOR_GRID, width=1, dash='dash'),
            name='100% Benchmark',
            hoverinfo='skip'
        ))

    fig.update_layout(
        polar=dict(
            bgcolor='#FFFFFF',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color=COLOR_MUTED, size=9),
                gridcolor=COLOR_GRID,
                linecolor='#dcdcdc'
            ),
            angularaxis=dict(
                tickfont=dict(color=COLOR_TEXT, size=10, family='Inter, sans-serif'),
                gridcolor=COLOR_GRID,
                linecolor='#dcdcdc'
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=30, r=30, t=30, b=30),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color=COLOR_MUTED, size=10)
        )
    )
    return fig


def create_feature_breakdown_bar_chart(results: Dict[str, Any]) -> go.Figure:
    """
    Renders a Plotly horizontal bar chart using Rhombus colors.
    """
    data = []
    for key, feat in results.get("features", {}).items():
        data.append({
            "Feature": feat["name"],
            "Similarity (%)": feat["similarity"] * 100.0,
            "Weight": feat["weight"],
            "Earth Value": feat["earth_val"],
            "Target Value": feat["target_val"]
        })

    df = pd.DataFrame(data)
    if df.empty:
        return go.Figure()

    df = df.sort_values(by="Similarity (%)", ascending=True)

    fig = go.Figure(go.Bar(
        x=df["Similarity (%)"],
        y=df["Feature"],
        orientation='h',
        marker=dict(
            color=df["Similarity (%)"],
            colorscale=[[0, COLOR_SECONDARY], [0.5, COLOR_WARNING], [1, COLOR_PRIMARY]],
            line=dict(color='#dcdcdc', width=1)
        ),
        customdata=list(zip(df["Earth Value"], df["Target Value"], df["Weight"])),
        hovertemplate="<b>%{y}</b><br>Score: %{x:.1f}%<br>Earth: %{customdata[0]}<br>Target: %{customdata[1]}<br>Weight: %{customdata[2]}<extra></extra>"
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=10, r=20, t=15, b=20),
        xaxis=dict(
            title="Analog Compatibility (%)",
            range=[0, 105],
            gridcolor=COLOR_GRID,
            tickfont=dict(color=COLOR_MUTED, size=9),
            title_font=dict(color=COLOR_TEXT, size=10)
        ),
        yaxis=dict(
            tickfont=dict(color=COLOR_TEXT, size=10),
            gridcolor=COLOR_GRID
        )
    )
    return fig


def create_terrain_cross_section_chart(
    earth_profile: Optional[Dict[str, Any]],
    target_profile: Optional[Dict[str, Any]],
    earth_name: str,
    target_name: str
) -> go.Figure:
    """
    Renders dual-panel illustrative topographic transects showing separate horizontal spans and planetary vertical datums.
    """
    from plotly.subplots import make_subplots

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            f"Earth Analog: {earth_name} (NASA SRTM 30m • EGM96 Geoid)",
            f"Planetary Reference: {target_name} (NASA Orbital Datum)"
        ),
        horizontal_spacing=0.12
    )

    if earth_profile:
        dist_e = earth_profile.get("distance_km", [])
        elev_e = earth_profile.get("elevation_m", [])
        fig.add_trace(
            go.Scatter(
                x=dist_e,
                y=elev_e,
                mode='lines+markers',
                fill='tozeroy',
                fillcolor='rgba(112, 182, 193, 0.18)',
                line=dict(color=COLOR_INFO, width=2),
                marker=dict(size=4, color=COLOR_PRIMARY_DARK),
                name=f"{earth_name} (m MSL)",
                hovertemplate="Dist: %{x} km<br>Elev: %{y} m MSL<extra></extra>"
            ),
            row=1, col=1
        )
    else:
        fig.add_annotation(
            text="DEM transect not available for this site",
            xref="x1", yref="y1", showarrow=False, font=dict(color=COLOR_MUTED),
            row=1, col=1
        )

    if target_profile:
        dist_t = target_profile.get("distance_km", [])
        elev_t = target_profile.get("elevation_m", [])
        is_mars = "Mars" in target_profile.get("name", "") or "Jezero" in target_name
        color_t = COLOR_SECONDARY if is_mars else COLOR_PRIMARY
        fill_t = 'rgba(249, 131, 124, 0.18)' if is_mars else 'rgba(119, 93, 166, 0.18)'
        datum_label = "MOLA Areoid" if is_mars else "LOLA R=1,737.4km Datum"

        fig.add_trace(
            go.Scatter(
                x=dist_t,
                y=elev_t,
                mode='lines+markers',
                fill='tozeroy',
                fillcolor=fill_t,
                line=dict(color=color_t, width=2),
                marker=dict(size=4, color=COLOR_PRIMARY_DARK),
                name=f"{target_name} ({datum_label})",
                hovertemplate=f"Dist: %{{x}} km<br>Elev: %{{y}} m ({datum_label})<extra></extra>"
            ),
            row=1, col=2
        )
    else:
        fig.add_annotation(
            text="Planetary laser altimetry transect not available",
            xref="x2", yref="y2", showarrow=False, font=dict(color=COLOR_MUTED),
            row=1, col=2
        )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=30, r=30, t=50, b=40),
        showlegend=False
    )
    fig.update_xaxes(title_text="Profile Distance (km)", gridcolor=COLOR_GRID, tickfont=dict(color=COLOR_MUTED, size=9))
    fig.update_yaxes(title_text="Elevation (meters)", gridcolor=COLOR_GRID, tickfont=dict(color=COLOR_MUTED, size=9))

    return fig


def create_nasa_power_climatology_chart(power_params: Dict[str, Any], location_name: str) -> go.Figure:
    """
    Renders monthly climatological temperature cycle and solar radiation from NASA POWER in Rhombus style.
    """
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    t2m_dict = power_params.get("T2M", {})
    t2m_vals = [t2m_dict.get(m, 0.0) for m in ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]]

    solar_dict = power_params.get("ALLSKY_SFC_SW_DWN", {})
    solar_vals = [solar_dict.get(m, 0.0) for m in ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=months,
        y=t2m_vals,
        name="Mean Surface Temp (°C)",
        mode="lines+markers",
        line=dict(color=COLOR_PRIMARY, width=2.5),
        marker=dict(size=6, color=COLOR_PRIMARY_DARK),
        yaxis="y1"
    ))

    fig.add_trace(go.Bar(
        x=months,
        y=solar_vals,
        name="Solar Irradiance (kW-hr/m²/day)",
        marker=dict(color="rgba(243, 204, 92, 0.45)", line=dict(color=COLOR_WARNING, width=1.5)),
        yaxis="y2"
    ))

    fig.update_layout(
        title=dict(
            text=f"NASA POWER Monthly Climatology: {location_name}",
            font=dict(color=COLOR_TEXT, size=13, family="Inter, sans-serif")
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(gridcolor=COLOR_GRID, tickfont=dict(color=COLOR_MUTED)),
        yaxis=dict(
            title="Temperature (°C)",
            titlefont=dict(color=COLOR_PRIMARY, size=10),
            tickfont=dict(color=COLOR_PRIMARY),
            gridcolor=COLOR_GRID
        ),
        yaxis2=dict(
            title="Solar Irradiance (kW-hr/m²/day)",
            titlefont=dict(color="#dcb33f", size=10),
            tickfont=dict(color="#dcb33f"),
            overlaying="y",
            side="right",
            gridcolor='rgba(0,0,0,0)'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=COLOR_MUTED, size=9)
        )
    )
    return fig


def create_rhombus_donut_chart(values: List[float], labels: List[str], colors: List[str], title: str = "") -> go.Figure:
    """
    Renders signature Rhombus donut chart (like the Email Sent Total chart in Rhombus index.html).
    """
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.68,
        marker=dict(colors=colors, line=dict(color='#ffffff', width=2)),
        textinfo='percent',
        textposition='inside',
        insidetextfont=dict(family='Inter, sans-serif', size=12, color='#ffffff', weight=600),
        hoverinfo='label+value+percent'
    )])

    fig.update_layout(
        title=dict(text=title, font=dict(color=COLOR_TEXT, size=13)) if title else None,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color=COLOR_MUTED, size=10)
        )
    )
    return fig

"""
Planetary Analog Explorer - Modular NASA & Planetary Data Loaders
Provides structured loaders for Earth analogs, lunar & Martian targets,
terrain profiles, dataset specifications, and live NASA POWER API integration.
"""

import json
import os
from typing import Dict, Any, List, Optional
import requests
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


@st.cache_data
def load_earth_analogs() -> List[Dict[str, Any]]:
    """Loads curated terrestrial planetary analog sites."""
    path = os.path.join(DATA_DIR, "earth_analogs.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("analogs", [])


@st.cache_data
def load_planetary_targets() -> List[Dict[str, Any]]:
    """Loads Moon and Mars reference target sites and orbital instrument metadata."""
    path = os.path.join(DATA_DIR, "planetary_targets.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("bodies", [])


@st.cache_data
def load_terrain_profiles() -> Dict[str, Any]:
    """Loads calibrated cross-sectional topographic profiles (SRTM, LOLA, MOLA)."""
    path = os.path.join(DATA_DIR, "terrain_profiles.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("profiles", {})


@st.cache_data
def load_data_sources_catalog() -> Dict[str, Any]:
    """Loads the formal NASA and ESA instrument catalog, PDS nodes, and citations."""
    path = os.path.join(DATA_DIR, "data_sources.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


@st.cache_data(ttl=3600)
def fetch_nasa_power_climatology(lat: float, lon: float) -> Dict[str, Any]:
    """
    Queries official NASA POWER (Prediction Of Worldwide Energy Resources) API
    for climatological monthly solar radiation, surface temperature, and atmospheric pressure.
    Returns live API data or structured offline notice with status.
    """
    url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
    params = {
        "parameters": "T2M,T2M_MAX,T2M_MIN,ALLSKY_SFC_SW_DWN,PRECTOTCORR,PS,RH2M",
        "community": "AG",
        "longitude": round(lon, 4),
        "latitude": round(lat, 4),
        "format": "JSON"
    }
    
    try:
        response = requests.get(url, params=params, timeout=5.0)
        if response.status_code == 200:
            payload = response.json()
            properties = payload.get("properties", {})
            parameter_data = properties.get("parameter", {})
            return {
                "status": "success",
                "source": "NASA POWER Climatology API v2.0 (Live Endpoint)",
                "coordinates": {"lat": lat, "lon": lon},
                "parameters": parameter_data,
                "elevation": payload.get("geometry", {}).get("coordinates", [0, 0, None])[2],
                "message": "Live Earth Observation data successfully retrieved from NASA Langley Research Center."
            }
        else:
            return {
                "status": "http_error",
                "source": "NASA POWER API",
                "status_code": response.status_code,
                "message": f"NASA API returned HTTP {response.status_code}. Using local verified scientific profile."
            }
    except requests.exceptions.RequestException as e:
        return {
            "status": "offline",
            "source": "NASA POWER API (Offline Fallback)",
            "error_detail": str(e),
            "message": "Live NASA POWER endpoint unreachable or timed out. Utilizing local peer-reviewed climatological baseline."
        }

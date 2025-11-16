from astronomy_dashboard.services.weather_api import get_weather_api

import requests
import streamlit as st
from typing import List, Dict, Any
from PIL import Image
from io import BytesIO

ICON_URL = "https://openweathermap.org/img/wn"

#Warsaw coordinates
LAT = "52"
LON = "21"

#temp, przejrzystosc, zachmurzenie
def get_weather(days : int, include_today : bool, lon : str, lat : str) -> List[Dict[str, Any]]:
    """
    Return weather at 00:00:00 in night for specific number of days (max 4 days).

    Args:
        days (int) : Number of days that is returned. Max is 4.
        include_today (bool) : specify if return today's weather
        lon (str) : longituide of location
        lat (str) : latitude of location

    Returns:
        List[Dict[str, Any]] with basic weather information

    Raises:
        ValueError if days higher than 4

    """

    if days > 4:
        raise ValueError("Number of days can't be higher than 4.")

    start_idx = 0 if include_today else 1
    end_idx = start_idx + days


    weather = [item for item in get_weather_api(lat = lat, lon = lon, units = "metric")
                        if (item["part_of_day"] == 'n' and "00:00:00" in item["dt_txt"])][start_idx : end_idx]

    return weather

@st.cache_data
def get_weather_icon(icon_cd : str) -> Image.Image:
    """
    Return icon_cd as Image.Image from OpenWeather

    Args:
        icon_cd (str) : code of icon
    
    Returns:
        Image.Image : icon
    
    Raises:
        ConnectionError - if icon can't be retrieved
    """

    url = f"{ICON_URL}/{icon_cd}@2x.png"

    try:
        response = requests.get(url, timeout = 5)

        if response.status_code != 200:
            raise ConnectionError(f"Could not fetch icon {icon_cd}")

    except Exception as e:
        raise ConnectionError(f"Failed to fetch icon {icon_cd}: {e}")
    
    return Image.open(BytesIO(response.content))

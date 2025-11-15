import requests
import streamlit as st
from urllib.parse import urlencode
from typing import Any, Dict, List


URL_BASE = "https://api.openweathermap.org/data/2.5/forecast"

LAT = '52.252440'
LON = '21.037042'



def get_weather(lat : str, lon : str, **params) -> List[Dict[str, Any]]:
    """Get weather forecast data from the OpenWeather API. Return data as list of dictionaries"""

    api_key = st.secrets["OPEN_WEATHER_API"]

    try:
        url = build_url(lat = lat, lon = lon, appid = api_key, **params)
        response = requests.get(url, timeout=10)

    except Exception as exc:
        raise TimeoutError(f"Connection to weather API is not successful. {exc}")

    return parse_response(response)


def parse_response(response : requests.models.Response) -> list:
    """Validate the API response, extract and return basic weather information."""
    
    if response.status_code != 200:
        raise ConnectionError(
            f"Connection do weather API is not succesful. Response code is {response.status_code}"
        )
    
    res : List[Dict[str, Any]] = []

    for item in response.json()["list"]:
        res.append(
            {
                "dt_txt"        : item["dt_txt"]
                ,"temp"         : item["main"]["temp"]
                ,"weather"      : item["weather"][0]["main"]
                ,"weather_desc" : item["weather"][0]["description"]
                ,"cloudiness_%" : item["clouds"]["all"]
                ,"wind_speed"   : item["wind"]["speed"]
                ,"visibility"   : item["visibility"]
                ,"part_of_day"  : item["sys"]["pod"]
            }
        )
    
    return res

def build_url( **params) -> str:
    """Build URL for API request"""
    
    return f"{URL_BASE}?{urlencode(params)}"

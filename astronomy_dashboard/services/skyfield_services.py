from skyfield.api import load, wgs84
from skyfield.framelib import ecliptic_frame
from functools import lru_cache
from typing import List
import datetime


PLANET_KEYS = [
        ("Mercury",  "mercury"),
        ("Venus",    "venus"),
        ("Mars",     "mars"),
        ("Jupiter",  "jupiter barycenter"),
        ("Saturn",   "saturn barycenter"),
        ("Uranus",   "uranus barycenter"),
        ("Neptune",  "neptune barycenter"),
    ]

#min altitude for planet to be visible
PLANET_ALT_LIMIT = 5.0

# ----------------------------- CACHING -----------------------------

@lru_cache()
def load_timescale():
    """Return cached Skyfield timescale object"""
    return load.timescale()



@lru_cache()
def get_ephemeris():
    """Return cached Skyfield ephemeris de421.bsp"""
    return load("de421.bsp")


# ----------------------------- MOON PHASE -----------------------------

def get_moon_phase(year : int, month : int, day : int) -> tuple[str, float]:
    """
    Calculate moon phase on specific date at 23:59 UTC time.

    Args:
        year (int) : date year
        month (int) : date month
        day (int) : date day

    Return:
        (phase_name, phase_deg):
            str - name of Moon phase
            float - phase in deg
    Raises:

    """
    validate_date(year, month, day)

    ts = load_timescale()
    t = ts.utc(year, month, day, 23, 59)

    eph = get_ephemeris()
    sun, moon, earth = eph["sun"], eph["moon"], eph["earth"]

    e = earth.at(t)
    s, m = e.observe(sun).apparent(), e.observe(moon).apparent()

    _, slon, _ = s.frame_latlon(ecliptic_frame)
    _, mlon, _ = m.frame_latlon(ecliptic_frame)

    phase = (mlon.degrees - slon.degrees) % 360.0

    return(get_phase_name(phase), phase)


def get_phase_name(phase : float) -> str:
    """
    Return the name of phase based on phase in deg.

    Args:
        phase (float) : phase of the moon in deg, expected valu is between 0 and 360

    Returns:
        phase_name(str) - name of the phase

    Raises:
        ValueError: if phase is outside the expected range
    """


    if phase < 22.5 or phase >= 337.5:
        return "New Moon"
    elif phase < 67.5:
        return "Waxing Crescent"
    elif phase < 112.5:
        return "First Quarter"
    elif phase < 157.5:
        return "Waxing Gibbous"
    elif phase < 202.5:
        return "Full Moon"
    elif phase < 247.5:
        return "Waning Gibbous"
    elif phase < 292.5:
        return "Last Quarter"
    else:
        return "Waning Crescent"

# ----------------------------- VISIBLE PLANET -----------------------------

def get_visible_planets(
        year : int, 
        month : int, 
        day : int, 
        lat: float, 
        lng : float
    ) -> List[str]:
    """
    Returns list of visible planets on given date at 23:59 UTC and location. 
    
    Args:
        year (int) : date year
        month (int) : date month
        day (int) : date day
        lat (float) : latitude in deg
        lng (float) : longitude in deg

    Returns:
        List[str]: names of visible planets

    """
    validate_date(year, month, day)
    validate_coordinates(lat, lng)

    ts = load_timescale()
    t = ts.utc(year, month, day, 23, 59)

    eph = get_ephemeris()

    observer = eph['earth'] + wgs84.latlon(lat, lng)
    visible = []

    for name, key in PLANET_KEYS:
        planet = eph[key]
        alt, az, _ = observer.at(t).observe(planet).apparent().altaz()

        if alt.degrees >= PLANET_ALT_LIMIT:
            visible.append(name)
    
    return visible

#---------------------------------- VALIDATION ------------------------------

def validate_date(year : int, month : int, day : int):
    """Date validator"""
    try:
        datetime.date(year, month, day)
    except Exception as e:
        raise ValueError(f"Invalid date {day}-{month}-{year}")


def validate_coordinates(lat : float, lon : float):
    """Coordinates validator"""
    if not (-90 <= lat <= 90):
        raise ValueError(f"Invalid latitude: {lat}")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Invalid longitude: {lon}")

"""
weather_tool.py
Handles communication with the Open-Meteo public APIs:
1. Geocoding API - converts a city name into latitude/longitude
2. Forecast API - fetches current temperature for given coordinates
"""

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def geocode_city(city_name: str) -> dict:
    """
    Converts a city name into latitude/longitude using Open-Meteo's geocoding API.
    Returns a dict with city name, lat, lon, and country - or raises an error if not found.
    """
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
    response = requests.get(GEOCODING_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        raise ValueError(f"City '{city_name}' not found.")

    result = data["results"][0]
    return {
        "name": result["name"],
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "country": result.get("country", "Unknown"),
    }


def get_current_temperature(latitude: float, longitude: float) -> float:
    """
    Fetches the current temperature (in Celsius) for given coordinates
    using Open-Meteo's forecast API.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m",
    }
    response = requests.get(FORECAST_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    return data["current"]["temperature_2m"]


def get_city_temperature(city_name: str) -> dict:
    """
    Combines geocoding + forecast lookup into a single convenient function.
    This is the function the agent will call as its 'tool'.
    """
    location = geocode_city(city_name)
    temperature = get_current_temperature(location["latitude"], location["longitude"])

    return {
        "city": location["name"],
        "country": location["country"],
        "temperature_celsius": temperature,
    }


# Quick manual test - run this file directly to check it works
if __name__ == "__main__":
    result = get_city_temperature("Budapest")
    print(result)
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import requests

load_dotenv()


mcp = FastMCP("implementation")

realtime_weather_url = "https://api.tomorrow.io/v4/weather/realtime?location={city}&apikey={weather_api_key}"
hourly_weather_url = "https://api.tomorrow.io/v4/weather/history/recent?location={city}&apikey={weather_api_key}"
pin_to_place_url = "https://api.postalpincode.in/pincode/{pincode}"


@mcp.tool()
def pintoplace(pincode: int):
    """
    Gets the place name for the given pincode.

    Args:
        pincode (str): The pincode to get the place name for.

    Returns:
        dict: The place data.
    """
    pincode = str(pincode)
    try:
        response = requests.get(pin_to_place_url.format(pincode=pincode))
        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@mcp.tool()
def realtime_weather(city: str):
    """
    Get the realtime weather forecasts for the location.

    Args:
        city (str): The city to get the weather for.

    Returns:
        dict: The weather data.
    """
    headers = {
        "accept": "application/json",
        "accept-encoding": "deflate, gzip, br"
    }

    try:
        response = requests.get(realtime_weather_url.format(city=city, weather_api_key=os.getenv("weather_api_key")), headers=headers)
        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}



@mcp.tool()
def hourly_weather(city: str):
    """
    Get the historical weather forecasts for the location, including hourly history for the last 24 hours, and daily history for the last day.

    Args:
        city (str): The city to get the weather for.

    Returns:
        dict: The weather data.
    """
    headers = {
        "accept": "application/json",
        "accept-encoding": "deflate, gzip, br"
    }
    try:
        response = requests.get(hourly_weather_url.format(city=city, weather_api_key=os.getenv("weather_api_key")), headers=headers)
        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")

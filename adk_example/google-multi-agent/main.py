import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

import requests
import os

def get_current_time() -> str:
    """Returns the current time in UTC."""
    now = datetime.datetime.now(ZoneInfo("UTC"))
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")

def get_weather(city: str) -> dict:
    # Hardcoded weather data instead of API call
    hardcoded_weather_data = {
        "london": {"weather": "partly cloudy", "temp_c": 18.5},
        "paris": {"weather": "sunny", "temp_c": 22.3},
        "new york": {"weather": "clear", "temp_c": 25.1},
        "tokyo": {"weather": "overcast", "temp_c": 19.7},
        "sydney": {"weather": "light rain", "temp_c": 16.2},
        "default": {"weather": "partly cloudy", "temp_c": 20.0}
    }
    
    # Get weather data for the city (case insensitive)
    city_lower = city.lower()
    weather_data = hardcoded_weather_data.get(city_lower, hardcoded_weather_data["default"])
    
    weather = weather_data["weather"].capitalize()
    temp_c = weather_data["temp_c"]
    temp_f = (temp_c * 9/5) + 32

    report = (
        f"The weather in {city.title()} is {weather} with a temperature of "
        f"{temp_c:.1f}°C ({temp_f:.1f}°F)."
    )
    return {"status": "success", "report": report}

    
def book_theme_park_ticket(weather_report: str) -> dict:
    """Books a theme park ticket only if the weather is suitable.

    Args:
        weather_report (str): Weather description from `get_weather`.

    Returns:
        dict: status and booking confirmation or reason for failure.
    """
    safe_conditions = [
        "sunny", "clear", "partly cloudy", "mostly sunny", "fair", 
        "light clouds", "few clouds", "scattered clouds", "overcast",
        "dry", "pleasant", "mild", "warm", "cool", "calm", "light wind"
    ]
    if any(cond in weather_report.lower() for cond in safe_conditions):
        return {
            "status": "success",
            "message": "Ticket booked! The weather is suitable for visiting the theme park."
        }
    else:
        return {
            "status": "error",
            "error_message": (
                "Cannot book ticket. The weather is not ideal for outdoor activities."
            )
        }


root_agent = Agent(
    name="weather_themepark_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent that provides current weather in a city and books theme park tickets if weather is suitable."
    ),
    instruction=(
        "You are a helpful agent that provides weather updates and can book theme park tickets "
        "only if the weather is favorable for outdoor activities (e.g., sunny or partly cloudy)."
    ),
    tools=[get_weather, book_theme_park_ticket],
)

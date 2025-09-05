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

    
def create_travel_itinerary(weather_report: str, city: str = "the destination") -> dict:
    """Creates a travel itinerary based on weather conditions.

    Args:
        weather_report (str): Weather description from `get_weather`.
        city (str): The destination city for the travel itinerary.

    Returns:
        dict: status and itinerary details.
    """
    # Weather-based activity recommendations
    outdoor_activities = ["city walking tours", "outdoor sightseeing", "park visits", "outdoor dining"]
    indoor_activities = ["museum visits", "shopping centers", "indoor attractions", "spa treatments"]
    rainy_activities = ["art galleries", "indoor markets", "cultural centers", "cozy cafes"]
    
    weather_lower = weather_report.lower()
    
    # Determine activities based on weather
    if any(cond in weather_lower for cond in ["sunny", "clear", "partly cloudy"]):
        recommended_activities = outdoor_activities + ["beach activities", "rooftop dining"]
        itinerary_focus = "outdoor exploration and leisure"
        recommended_hotel_type = "beachfront resort or outdoor pool hotel"
    elif any(cond in weather_lower for cond in ["rain", "storm", "heavy"]):
        recommended_activities = rainy_activities + ["room service dining", "indoor entertainment"]
        itinerary_focus = "indoor comfort and relaxation"
        recommended_hotel_type = "luxury spa hotel or indoor entertainment hotel"
    elif any(cond in weather_lower for cond in ["overcast", "cloudy", "mild"]):
        recommended_activities = indoor_activities + outdoor_activities[:2]  # Mix of both
        itinerary_focus = "flexible indoor/outdoor activities"
        recommended_hotel_type = "city center hotel"
    else:
        recommended_activities = outdoor_activities + indoor_activities
        itinerary_focus = "general sightseeing"
        recommended_hotel_type = "business hotel"
    
    # Create itinerary
    itinerary = {
        "destination": city.title(),
        "weather_conditions": weather_report,
        "recommended_activities": recommended_activities[:4],  # Top 4 activities
        "itinerary_focus": itinerary_focus,
        "recommended_hotel_type": recommended_hotel_type
    }
    
    return {
        "status": "success",
        "message": f"Travel itinerary created for {city.title()}!",
        "itinerary": itinerary
    }


def book_hotel(city: str, hotel_type: str = "standard hotel") -> dict:
    """Books hotel accommodation for a specific city.

    Args:
        city (str): The destination city for hotel booking.
        hotel_type (str): Type of hotel to book (e.g., "luxury spa hotel", "beachfront resort").

    Returns:
        dict: status and booking confirmation details.
    """
    # Available hotel types and their features
    hotel_options = {
        "beachfront resort": {
            "amenities": ["private beach access", "outdoor pool", "spa services", "water sports"],
            "price_range": "$200-400/night"
        },
        "luxury spa hotel": {
            "amenities": ["full-service spa", "indoor pool", "fine dining", "room service"],
            "price_range": "$180-350/night"
        },
        "city center hotel": {
            "amenities": ["central location", "business center", "fitness center", "restaurant"],
            "price_range": "$120-250/night"
        },
        "business hotel": {
            "amenities": ["meeting rooms", "wifi", "fitness center", "airport shuttle"],
            "price_range": "$100-200/night"
        },
        "outdoor pool hotel": {
            "amenities": ["outdoor pool", "sun deck", "poolside service", "garden area"],
            "price_range": "$150-280/night"
        },
        "boutique hotel": {
            "amenities": ["unique design", "personalized service", "local art", "gourmet breakfast"],
            "price_range": "$140-300/night"
        }
    }
    
    # Normalize hotel type for lookup
    hotel_type_lower = hotel_type.lower()
    selected_hotel = None
    
    # Find matching hotel type
    for hotel_name, details in hotel_options.items():
        if hotel_name in hotel_type_lower or any(word in hotel_type_lower for word in hotel_name.split()):
            selected_hotel = hotel_name
            break
    
    # Default to city center hotel if no match found
    if not selected_hotel:
        selected_hotel = "city center hotel"
    
    hotel_details = hotel_options[selected_hotel]
    booking_confirmation = f"HTL-{hash(f'{city.lower()}-{selected_hotel}') % 10000:04d}"
    
    booking_info = {
        "destination": city.title(),
        "hotel_type": selected_hotel,
        "amenities": hotel_details["amenities"],
        "price_range": hotel_details["price_range"],
        "booking_confirmation": booking_confirmation,
        "check_in": "3:00 PM",
        "check_out": "11:00 AM"
    }
    
    return {
        "status": "success",
        "message": f"{selected_hotel.title()} successfully booked in {city.title()}!",
        "booking": booking_info
    }


root_agent = Agent(
    name="travel_weather_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent that provides weather information, creates travel itineraries, and books hotel accommodations based on weather conditions and preferences."
    ),
    instruction=(
        "You are a helpful travel agent that provides weather updates, creates personalized travel itineraries, "
        "and books hotel accommodations. You can suggest activities based on current weather conditions and "
        "help users find the perfect hotel for their stay. Use the get_weather tool first to check conditions, "
        "then create_travel_itinerary for activity recommendations, and finally book_hotel for accommodations."
    ),
    tools=[get_weather, create_travel_itinerary, book_hotel],
)

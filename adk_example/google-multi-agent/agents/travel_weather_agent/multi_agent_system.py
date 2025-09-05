import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent, LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search

import requests
import os

# MODEL configuration
MODEL = "gemini-2.0-flash"

# ===== UTILITY FUNCTIONS =====
def get_current_time() -> str:
    """Returns the current time in UTC."""
    now = datetime.datetime.now(ZoneInfo("UTC"))
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")

# ===== SPECIALIZED SUB-AGENTS =====

def get_weather(city: str) -> dict:
    """Weather data retrieval function."""
    hardcoded_weather_data = {
        "london": {"weather": "partly cloudy", "temp_c": 18.5},
        "paris": {"weather": "sunny", "temp_c": 22.3},
        "new york": {"weather": "clear", "temp_c": 25.1},
        "tokyo": {"weather": "overcast", "temp_c": 19.7},
        "sydney": {"weather": "light rain", "temp_c": 16.2},
        "default": {"weather": "partly cloudy", "temp_c": 20.0}
    }
    
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

# 1. Weather Specialist Agent
weather_agent = Agent(
    name="weather_specialist",
    model=MODEL,
    description="Specialist agent that provides accurate weather information for any city worldwide.",
    instruction=(
        "You are a weather specialist. Provide accurate, detailed weather information including "
        "temperature in both Celsius and Fahrenheit, weather conditions, and any relevant details "
        "for travel planning. Always be precise and helpful."
    ),
    tools=[google_search],
)

def create_travel_itinerary(weather_report: str, city: str = "the destination") -> dict:
    """Creates detailed travel itinerary based on weather conditions."""
    outdoor_activities = ["city walking tours", "outdoor sightseeing", "park visits", "outdoor dining"]
    indoor_activities = ["museum visits", "shopping centers", "indoor attractions", "spa treatments"]
    rainy_activities = ["art galleries", "indoor markets", "cultural centers", "cozy cafes"]
    
    weather_lower = weather_report.lower()
    
    if any(cond in weather_lower for cond in ["sunny", "clear", "partly cloudy"]):
        recommended_activities = outdoor_activities + ["beach activities", "rooftop dining"]
        itinerary_focus = "outdoor exploration and leisure"
        recommended_hotel_type = "beachfront resort or outdoor pool hotel"
    elif any(cond in weather_lower for cond in ["rain", "storm", "heavy"]):
        recommended_activities = rainy_activities + ["room service dining", "indoor entertainment"]
        itinerary_focus = "indoor comfort and relaxation"
        recommended_hotel_type = "luxury spa hotel or indoor entertainment hotel"
    elif any(cond in weather_lower for cond in ["overcast", "cloudy", "mild"]):
        recommended_activities = indoor_activities + outdoor_activities[:2]
        itinerary_focus = "flexible indoor/outdoor activities"
        recommended_hotel_type = "city center hotel"
    else:
        recommended_activities = outdoor_activities + indoor_activities
        itinerary_focus = "general sightseeing"
        recommended_hotel_type = "business hotel"
    
    itinerary = {
        "destination": city.title(),
        "weather_conditions": weather_report,
        "recommended_activities": recommended_activities[:4],
        "itinerary_focus": itinerary_focus,
        "recommended_hotel_type": recommended_hotel_type
    }
    
    return {
        "status": "success",
        "message": f"Travel itinerary created for {city.title()}!",
        "itinerary": itinerary
    }

# 2. Itinerary Specialist Agent
itinerary_agent = Agent(
    name="itinerary_specialist",
    model=MODEL,
    description="Expert travel planner that creates personalized itineraries based on weather conditions and preferences.",
    instruction=(
        "You are an expert travel planner. Create detailed, personalized itineraries that match "
        "the current weather conditions. Recommend activities, dining options, and experiences "
        "that are appropriate for the weather. Always consider the traveler's comfort and safety."
    ),
    tools=[create_travel_itinerary],
    #tools=[google_search],
)

def book_hotel(city: str, hotel_type: str = "standard hotel") -> dict:
    """Books hotel accommodation with detailed amenities."""
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
    
    hotel_type_lower = hotel_type.lower()
    selected_hotel = None
    
    for hotel_name, details in hotel_options.items():
        if hotel_name in hotel_type_lower or any(word in hotel_type_lower for word in hotel_name.split()):
            selected_hotel = hotel_name
            break
    
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

# 3. Hotel Booking Specialist Agent
hotel_agent = Agent(
    name="hotel_specialist",
    model=MODEL,
    description="Expert accommodation specialist that finds and books the perfect hotels based on traveler needs and preferences.",
    instruction=(
        "You are a hotel booking expert. Find and book the most suitable accommodations based on "
        "the traveler's needs, budget, and preferences. Provide detailed information about amenities, "
        "pricing, and booking confirmations. Always ensure the best value and experience for guests."
    ),
    tools=[book_hotel],
)

# ===== COORDINATING LLM AGENT =====

travel_coordinator = LlmAgent(
    name="travel_coordinator",
    model=MODEL,
    description=(
        "Master travel coordinator that orchestrates specialized agents to provide comprehensive "
        "travel planning services including weather analysis, itinerary creation, and hotel booking. "
        "Guides users through a structured process to plan the perfect trip."
    ),
    instruction=(
        "You are a master travel coordinator managing a team of specialist agents. "
        "Your role is to:\n\n"
        "1. **Weather Analysis**: Use the weather specialist to get current conditions\n"
        "2. **Itinerary Planning**: Coordinate with the itinerary specialist to create weather-appropriate activities\n"
        "3. **Accommodation Booking**: Work with the hotel specialist to find perfect accommodations\n\n"
        "**Process Flow:**\n"
        "- Start by getting weather information for the destination\n"
        "- Create a detailed itinerary based on weather conditions\n"
        "- Book appropriate hotel accommodations\n"
        "- Provide a comprehensive travel plan summary\n\n"
        "Always ensure all aspects work together seamlessly and provide exceptional travel experiences. "
        "Coordinate between specialists to ensure recommendations are consistent and complementary."
    ),
    output_key="travel_coordinator_output",
    tools=[
        AgentTool(agent=weather_agent),
        AgentTool(agent=itinerary_agent),
        AgentTool(agent=hotel_agent),
    ],
)

# ===== ROOT AGENT =====
root_agent = travel_coordinator

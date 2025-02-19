import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import db

load_dotenv()

# Load API keys
JCDECAUX_API_KEY = os.getenv("JCDECAUX_API_KEY")
CONTRACT_NAME = os.getenv("JCDECAUX_CONTRACT_NAME")
JCDECAUX_URL = "https://api.jcdecaux.com/vls/v1/stations"

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY_NAME = os.getenv("CITY_NAME")
WEATHER_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={OPENWEATHER_API_KEY}&units=metric"

def fetch_bike_data():
    """Fetch and store bike availability data from JCDecaux API."""
    try:
        response = requests.get(JCDECAUX_URL, params={"apiKey": JCDECAUX_API_KEY, "contract": CONTRACT_NAME})
        data = response.json()

        for station in data:
            db.insert_bike_data(
                station_id=station["number"],
                available_bikes=station["available_bikes"],
                available_stands=station["available_bike_stands"],
                last_update=datetime.utcfromtimestamp(station["last_update"] / 1000).isoformat(),
                status=station["status"]
            )
        print("Bike data updated.")
    except Exception as e:
        print("Error fetching bike data:", e)

def fetch_weather_data():
    """Fetch and store weather data from OpenWeatherMap API."""
    try:
        response = requests.get(WEATHER_URL)
        data = response.json()

        db.insert_weather_data(
            city=data["name"],
            temperature=data["main"]["temp"],
            humidity=data["main"]["humidity"],
            description=data["weather"][0]["description"],
            timestamp=datetime.utcnow().isoformat()
        )
        print("Weather data updated.")
    except Exception as e:
        print("Error fetching weather data:", e)

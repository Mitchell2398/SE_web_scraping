import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def insert_bike_data(station_id, available_bikes, available_stands, last_update, status):
    """Insert bike data into Supabase and print errors."""
    url = f"{SUPABASE_URL}/rest/v1/availability"
    data = {
        "number": station_id,
        "available_bikes": available_bikes,
        "available_bike_stands": available_stands,
        "last_update": last_update,
        "status": status
    }
    response = requests.post(url, json=data, headers=HEADERS)
    
    # Print full response for debugging
    print("Bike Data Insert Response:", response.status_code, response.text)

    if response.status_code != 201:  # 201 = Successfully created
        print("⚠️ ERROR: Failed to insert bike data:", response.text)


def insert_weather_data(city, temperature, humidity, description, timestamp):
    """Insert weather data into Supabase, handling empty responses."""
    url = f"{SUPABASE_URL}/rest/v1/weather"
    data = {
        "city": city,
        "temperature": temperature,
        "humidity": humidity,
        "weather_description": description,
        "timestamp": timestamp
    }
    response = requests.post(url, json=data, headers=HEADERS)

    try:
        response_data = response.json() if response.text else {}
        print("🌤 Weather Data Insert Response:", response.status_code, response_data)
    except ValueError:
        print("⚠️ Warning: Supabase returned an empty response, but data was likely inserted.")

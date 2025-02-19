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

def insert_bike_data_bulk(stations):
    """Bulk insert bike data into Supabase while preventing duplicates."""
    url = f"{SUPABASE_URL}/rest/v1/availability"

    for station in stations:
        # First, check if the record already exists
        check_url = f"{SUPABASE_URL}/rest/v1/availability?number=eq.{station['number']}&last_update=eq.{station['last_update']}&select=number"
        check_response = requests.get(check_url, headers=HEADERS)

        if check_response.status_code == 200 and check_response.json():
            print(f"Skipping duplicate: Station {station['number']} at {station['last_update']}")
            continue  # Skip if it already exists

        #Insert only if no duplicate found
        response = requests.post(url, json=station, headers=HEADERS)
        print("Bike Data Insert Response:", response.status_code, response.text)

        if response.status_code != 201:
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
        print("Weather Data Insert Response:", response.status_code, response_data)
    except ValueError:
        print("⚠️ Warning: Supabase returned an empty response, but data was likely inserted.")

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

    if not isinstance(stations, list):
        stations = [stations]

    for station in stations:
        # Prepare data to match exact schema column names
        formatted_station = {
            'number': station['number'],
            'available_bikes': station['available_bikes'],
            'available_bike_stands': station['available_stands'],  # Fix the field name
            'last_update': station['last_update'],
            'status': station['status']
        }

        # First, check if the record already exists
        check_url = f"{SUPABASE_URL}/rest/v1/availability?number=eq.{formatted_station['number']}&last_update=eq.{formatted_station['last_update']}&select=number"
        check_response = requests.get(check_url, headers=HEADERS)

        if check_response.status_code == 200 and check_response.json():
            print(f"Skipping duplicate: Station {formatted_station['number']} at {formatted_station['last_update']}")
            continue

        # Insert only if no duplicate found
        response = requests.post(url, json=formatted_station, headers=HEADERS)
        
        if response.status_code == 201:
            print(f"Successfully inserted data for station {formatted_station['number']}")
        else:
            print(f"⚠️ ERROR: Failed to insert bike data for station {formatted_station['number']}:", response.text)

def insert_weather_data(city, temperature, humidity, description, timestamp):
    """Insert weather data into Supabase, handling empty responses and preventing duplicates."""
    url = f"{SUPABASE_URL}/rest/v1/weather"
    
    # Check for existing record with same timestamp
    check_url = f"{SUPABASE_URL}/rest/v1/weather?timestamp=eq.{timestamp}&select=id"
    check_response = requests.get(check_url, headers=HEADERS)
    
    if check_response.status_code == 200 and check_response.json():
        print(f"Skipping duplicate weather record for {city} at {timestamp}")
        return
    
    data = {
        "city": city,
        "temperature": temperature,
        "humidity": humidity,
        "weather_description": description,
        "timestamp": timestamp
    }
    
    try:
        response = requests.post(url, json=data, headers=HEADERS)
        response.raise_for_status()
        
        if response.status_code == 201:
            print(f"Successfully inserted weather data for {city} at {timestamp}")
        else:
            print(f"⚠️ ERROR: Failed to insert weather data: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️ ERROR: Failed to insert weather data: {str(e)}")
    except ValueError as e:
        if response.status_code == 201:
            print("Weather data inserted successfully (empty response)")
        else:
            print(f"⚠️ ERROR: Invalid response format: {str(e)}")

import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

test_data = {
    "number": 42,
    "available_bikes": 5,
    "available_bike_stands": 10,
    "last_update": "2025-02-19T10:58:32",
    "status": "OPEN"
}

response = requests.post(f"{SUPABASE_URL}/rest/v1/availability", json=test_data, headers=HEADERS)
print(response.status_code, response.text)

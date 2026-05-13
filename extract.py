import requests
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")


def fetch_weather_data() -> List[Dict[str, Any]]:
    """
    fetch weather data from weather API
    """
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q=Nairobi&aqi=yes"

    try:
        response = requests.get(url)
        response.raise_for_status()

        raw_data = response.json()

        with open("nairobi_weather_data.json", "w") as file:
            json.dump(raw_data, file, indent=4)

        print("Weather data fetched and saved to nairobi_weather_data.json")
        return raw_data
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        raise
    
if __name__ == "__main__":
    fetch_weather_data()
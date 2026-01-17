import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from backend.utils.config import OPENWEATHER_API_KEY
from backend.utils.helpers import setup_logger, log_step, mock_weather_data

logger = setup_logger(__name__)

class OpenWeatherIngestion:
    """Fetch current and historical weather data from OpenWeather API."""
    
    def __init__(self):
        self.api_key = OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.geo_url = "https://api.openweathermap.org/geo/1.0/direct"

    def geocode(self, state, district):
        """Resolve coordinates for a district using OpenWeather geocoding API."""
        try:
            q = f"{district},{state},IN"
            params = {"q": q, "limit": 1, "appid": self.api_key}
            resp = requests.get(self.geo_url, params=params, timeout=5)
            if resp.status_code == 200:
                results = resp.json()
                if results:
                    item = results[0]
                    return item.get("lat"), item.get("lon")
        except Exception as e:
            logger.warning(f"Geocoding failed for {district}, {state}: {e}")
        return None, None
    
    def fetch_current_weather(self, lat, lon):
        """Fetch current weather for coordinates."""
        try:
            url = f"{self.base_url}/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                log_step("OpenWeather API - Current", "success")
                return {
                    'temperature': data['main']['temp'],
                    'rainfall': data['rain'].get('1h', 0) if 'rain' in data else 0,
                    'humidity': data['main']['humidity']
                }
        except Exception as e:
            logger.warning(f"OpenWeather API failed: {e}. Using mock data.")
        
        return mock_weather_data("Unknown", "Unknown")
    
    def fetch_historical_weather(self, state, district):
        """Fetch historical weather patterns (mock implementation)."""
        log_step("OpenWeather - Historical", "success (mock)")
        
        # In production, integrate with weatherapi.com or similar for historical data
        return mock_weather_data(state, district)

def get_weather_data(state, district):
    """Public interface for weather data."""
    ingestion = OpenWeatherIngestion()
    # Try live geocoding for ANY district
    lat, lon = ingestion.geocode(state, district)
    if lat is not None and lon is not None:
        return ingestion.fetch_current_weather(lat, lon)
    # Fallback
    return ingestion.fetch_historical_weather(state, district)

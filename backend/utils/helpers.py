import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_logger(name):
    """Create a logger for a module."""
    return logging.getLogger(name)

def mock_ndvi_data(district, crop, season):
    """Generate realistic NDVI time-series mock data."""
    dates = pd.date_range(start=datetime.now() - timedelta(days=120), periods=8, freq='16D')
    # NDVI typically ranges from -1 to 1, vegetation usually 0.2-0.8
    base_ndvi = random.uniform(0.4, 0.7)
    trend = random.uniform(-0.02, 0.02)
    
    ndvi_values = [base_ndvi + (i * trend) + random.uniform(-0.05, 0.05) for i in range(8)]
    ndvi_values = np.clip(ndvi_values, 0.1, 0.9)
    
    return {
        'dates': dates.tolist(),
        'values': ndvi_values,
        'mean': np.mean(ndvi_values),
        'trend': trend,
        'variance': np.var(ndvi_values)
    }

def mock_weather_data(state, district):
    """Generate realistic weather data."""
    return {
        'temperature': random.uniform(20, 35),
        'rainfall': random.uniform(10, 100),
        'humidity': random.uniform(40, 80),
        'temperature_anomaly': random.uniform(-5, 5),
        'rainfall_deviation': random.uniform(-30, 30)
    }

def mock_soil_data(district):
    """Generate realistic soil data."""
    soil_types = ['Sandy Loam', 'Clay Loam', 'Silt Loam', 'Clay', 'Loam']
    return {
        'soil_type': random.choice(soil_types),
        'soil_moisture': random.uniform(20, 80),
        'organic_carbon': random.uniform(0.3, 1.5),
        'soil_depth': random.uniform(30, 100),
        'soil_moisture_index': random.uniform(0.2, 1.0)
    }

def mock_pest_data(district, season):
    """Generate realistic pest incident data."""
    return {
        'pest_count': random.randint(0, 10),
        'major_pests': random.sample(['Aphids', 'Armyworm', 'Whiteflies', 'Grasshoppers', 'Beetles'], k=random.randint(1, 3)),
        'pest_frequency': random.uniform(0.1, 0.8)
    }

def log_step(step_name, status="success", details=""):
    """Log pipeline steps."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{timestamp}] {step_name} - Status: {status} {details}")

def ensure_dir_exists(directory):
    """Create directory if it doesn't exist."""
    import os
    os.makedirs(directory, exist_ok=True)
    return directory

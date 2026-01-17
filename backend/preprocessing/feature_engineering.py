import numpy as np
import pandas as pd
from backend.utils.helpers import setup_logger, log_step
from backend.ingestion.openweather import get_weather_data
from backend.ingestion.modis import get_ndvi_data, extract_ndvi_features
from backend.ingestion.gldas import get_soil_moisture
from backend.ingestion.soil import get_soil_data
from backend.ingestion.pest import get_pest_data

logger = setup_logger(__name__)

class FeatureEngineer:
    """Create features from raw data sources."""
    
    @staticmethod
    def engineer_features(state, district, crop, season):
        """
        Aggregate all 7 data sources into ML-ready feature vector.
        Returns: dict with all features
        """
        
        log_step("Feature Engineering - Start", "in_progress")
        
        # 1. NDVI features (NASA MODIS)
        ndvi_data = get_ndvi_data(district, crop, season)
        ndvi_features = extract_ndvi_features(ndvi_data)
        
        # 2. Weather features (OpenWeather API)
        weather_data = get_weather_data(state, district)
        
        # 3. Soil moisture (NASA GLDAS)
        soil_moisture_data = get_soil_moisture(district)
        
        # 4. Static soil properties (NBSS&LUP)
        soil_props = get_soil_data(district)
        
        # 5. Pest incidents (State Agricultural Dept)
        pest_data = get_pest_data(district, season)
        
        # Combine all features
        features = {
            # NDVI features
            'ndvi_mean': ndvi_features['ndvi_mean'],
            'ndvi_trend': ndvi_features['ndvi_trend'],
            'ndvi_variance': ndvi_features['ndvi_variance'],
            
            # Weather features
            'rainfall_deviation': weather_data.get('rainfall_deviation', 0),
            'temperature_anomaly': weather_data.get('temperature_anomaly', 0),
            
            # Soil moisture
            'soil_moisture_index': soil_moisture_data['soil_moisture_index'],
            
            # Static soil features
            'soil_type_encoded': soil_props['soil_type_encoded'],
            
            # Pest features
            'pest_frequency': pest_data['pest_frequency'],
            
            # Categorical features
            'crop': crop,
            'season': season
        }
        
        log_step("Feature Engineering - Complete", "success")
        return features

def prepare_feature_vector(state, district, crop, season):
    """
    Prepare normalized feature vector for model input.
    """
    engineer = FeatureEngineer()
    raw_features = engineer.engineer_features(state, district, crop, season)
    
    # Normalize features to 0-1 range
    normalized_features = {
        'ndvi_mean': np.clip(raw_features['ndvi_mean'], 0, 1),
        'ndvi_trend': np.clip((raw_features['ndvi_trend'] + 0.1) / 0.2, 0, 1),
        'ndvi_variance': np.clip(raw_features['ndvi_variance'], 0, 0.1) * 10,
        'rainfall_deviation': np.clip((raw_features['rainfall_deviation'] + 50) / 100, 0, 1),
        'temperature_anomaly': np.clip((raw_features['temperature_anomaly'] + 10) / 20, 0, 1),
        'soil_moisture_index': np.clip(raw_features['soil_moisture_index'] / 100, 0, 1),
        'soil_type_encoded': raw_features['soil_type_encoded'] / 5,
        'pest_frequency': np.clip(raw_features['pest_frequency'], 0, 1)
    }
    
    return normalized_features, raw_features

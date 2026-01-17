import numpy as np
import pandas as pd
from backend.utils.helpers import setup_logger, log_step

logger = setup_logger(__name__)

class LabelGenerator:
    """Generate labels from yield/failure data with realistic correlations."""
    
    @staticmethod
    def generate_labels(features):
        """
        Generate realistic training labels based on feature correlations.
        Uses domain knowledge to create realistic failure patterns.
        
        Args:
            features: numpy array of shape (n_samples, 8) with features:
                [ndvi_mean, ndvi_trend, ndvi_variance, rainfall_dev, 
                 temp_anom, soil_moisture, soil_type, pest_freq]
        
        Returns:
            labels: numpy array of 0 (no failure) or 1 (failure)
        """
        n_samples = features.shape[0]
        labels = np.zeros(n_samples, dtype=int)
        
        for i in range(n_samples):
            ndvi_mean = features[i, 0]
            ndvi_trend = features[i, 1]
            ndvi_variance = features[i, 2]
            rainfall_dev = features[i, 3]
            temp_anom = features[i, 4]
            soil_moisture = features[i, 5]
            soil_type = features[i, 6]
            pest_freq = features[i, 7]
            
            # Calculate failure probability based on realistic thresholds
            failure_score = 0
            
            # NDVI-based risk (vegetation health)
            if ndvi_mean < 0.3:
                failure_score += 0.35  # Critical vegetation stress
            elif ndvi_mean < 0.5:
                failure_score += 0.15  # Moderate stress
            
            # Negative NDVI trend (declining health)
            if ndvi_trend < -0.05:
                failure_score += 0.20
            elif ndvi_trend < -0.02:
                failure_score += 0.10
            
            # High NDVI variance (inconsistent growth)
            if ndvi_variance > 0.07:
                failure_score += 0.12
            
            # Rainfall deviation
            if abs(rainfall_dev) > 30:
                failure_score += 0.25  # Severe drought or flood
            elif abs(rainfall_dev) > 15:
                failure_score += 0.12
            
            # Temperature anomaly
            if abs(temp_anom) > 5:
                failure_score += 0.20  # Extreme heat or cold
            elif abs(temp_anom) > 2.5:
                failure_score += 0.10
            
            # Soil moisture
            if soil_moisture < 0.25:
                failure_score += 0.25  # Severe water stress
            elif soil_moisture < 0.4:
                failure_score += 0.12
            
            # Pest frequency
            if pest_freq > 0.7:
                failure_score += 0.25  # High pest pressure
            elif pest_freq > 0.5:
                failure_score += 0.12
            
            # Interaction effects (compounding risks)
            if ndvi_mean < 0.4 and soil_moisture < 0.3:
                failure_score += 0.15  # Drought + poor vegetation
            
            if abs(rainfall_dev) > 20 and abs(temp_anom) > 3:
                failure_score += 0.15  # Climate extremes
            
            if pest_freq > 0.6 and ndvi_mean < 0.5:
                failure_score += 0.12  # Pests + weak plants
            
            # Add small random noise for realism
            failure_score += np.random.uniform(-0.05, 0.05)
            
            # Clip to [0, 1] range
            failure_score = np.clip(failure_score, 0, 1)
            
            # Convert to binary label (threshold at 0.5)
            labels[i] = 1 if failure_score > 0.5 else 0
        
        failure_rate = np.mean(labels)
        logger.info(f"Generated labels with {failure_rate:.1%} failure rate")
        log_step("Label Generation", "success")
        
        return labels

def create_training_dataset(X, y):
    """Create DataFrame for training."""
    feature_names = [
        'ndvi_mean', 'ndvi_trend', 'ndvi_variance',
        'rainfall_deviation', 'temperature_anomaly',
        'soil_moisture_index', 'soil_type_encoded',
        'pest_frequency'
    ]
    
    df = pd.DataFrame(X, columns=feature_names)
    df['failure_label'] = y
    
    return df

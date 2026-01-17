"""
Yield Prediction Model
Estimates crop yield based on current conditions
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

def train_yield_model():
    """Train a yield prediction model"""
    # Generate training data (2000 samples)
    np.random.seed(42)
    n_samples = 2000
    
    # Features: NDVI, rainfall_deviation, soil_moisture, temp_anomaly, pest_frequency
    ndvi = np.random.uniform(0.2, 0.9, n_samples)
    rainfall_dev = np.random.uniform(-40, 40, n_samples)
    soil_moisture = np.random.uniform(0.2, 0.9, n_samples)
    temp_anomaly = np.random.uniform(-8, 8, n_samples)
    pest_freq = np.random.uniform(0, 1, n_samples)
    
    # Generate realistic yield (quintals/hectare) with correlations
    # Base yield: 40-60 quintals/hectare
    base_yield = np.random.uniform(40, 60, n_samples)
    
    # NDVI impact (higher NDVI = higher yield)
    ndvi_impact = (ndvi - 0.5) * 30  # ±15 quintals
    
    # Rainfall impact
    rainfall_impact = -abs(rainfall_dev) * 0.2  # Extreme rain/drought reduces yield
    
    # Soil moisture impact
    moisture_impact = (soil_moisture - 0.5) * 15
    
    # Temperature impact
    temp_impact = -abs(temp_anomaly) * 1.5  # Extreme temps reduce yield
    
    # Pest impact
    pest_impact = -pest_freq * 10
    
    # Calculate final yield
    yield_values = base_yield + ndvi_impact + rainfall_impact + moisture_impact + temp_impact + pest_impact
    yield_values = np.clip(yield_values, 10, 80)  # Realistic bounds
    
    # Create features array
    X = np.column_stack([ndvi, rainfall_dev, soil_moisture, temp_anomaly, pest_freq])
    
    # Train Random Forest Regressor
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X, yield_values)
    
    # Save model
    os.makedirs('backend/model/saved', exist_ok=True)
    with open('backend/model/saved/yield_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Yield model trained with R² score: {model.score(X, yield_values):.3f}")
    return model

def load_yield_model():
    """Load the trained yield model"""
    model_path = 'backend/model/saved/yield_model.pkl'
    
    if not os.path.exists(model_path):
        print("Yield model not found. Training new model...")
        return train_yield_model()
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    return model

def predict_yield(ndvi, rainfall_deviation, soil_moisture, temp_anomaly, pest_frequency, crop_type='Rice'):
    """Predict yield for given conditions"""
    model = load_yield_model()
    
    # Create feature vector
    features = np.array([[ndvi, rainfall_deviation, soil_moisture, temp_anomaly, pest_frequency]])
    
    # Predict
    yield_estimate = model.predict(features)[0]
    
    # Calculate confidence interval (±10%)
    confidence_margin = yield_estimate * 0.1
    yield_low = max(10, yield_estimate - confidence_margin)
    yield_high = min(80, yield_estimate + confidence_margin)
    
    # Historical average for comparison (by crop type)
    crop_averages = {
        'Rice': 45,
        'Wheat': 40,
        'Cotton': 35,
        'Sugarcane': 600,  # Different unit
        'Corn': 50
    }
    
    historical_avg = crop_averages.get(crop_type, 45)
    comparison_pct = ((yield_estimate - historical_avg) / historical_avg) * 100
    
    return {
        'yield_estimate': round(yield_estimate, 1),
        'yield_low': round(yield_low, 1),
        'yield_high': round(yield_high, 1),
        'unit': 'quintals/hectare',
        'historical_average': historical_avg,
        'comparison_percent': round(comparison_pct, 1),
        'comparison_text': 'above' if comparison_pct > 0 else 'below'
    }

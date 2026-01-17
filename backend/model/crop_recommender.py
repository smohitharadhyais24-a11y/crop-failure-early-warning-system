"""
Crop Recommendation Engine
Suggests alternative crops based on current conditions
"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

def train_crop_recommender():
    """Train a crop recommendation model"""
    np.random.seed(42)
    n_samples = 2000
    
    # Features: NDVI, soil_moisture, temperature, rainfall_deviation, season, soil_type
    ndvi = np.random.uniform(0.2, 0.9, n_samples)
    soil_moisture = np.random.uniform(0.2, 0.9, n_samples)
    temperature = np.random.uniform(15, 40, n_samples)
    rainfall_dev = np.random.uniform(-40, 40, n_samples)
    season = np.random.randint(0, 3, n_samples)  # 0=Kharif, 1=Rabi, 2=Zaid
    soil_type = np.random.randint(0, 3, n_samples)  # 0=Sandy, 1=Loamy, 2=Clay
    
    # Crop types (encoded)
    # 0=Rice, 1=Wheat, 2=Cotton, 3=Sugarcane, 4=Corn, 5=Pulses, 6=Vegetables, 7=Fruits
    crops = np.zeros(n_samples, dtype=int)
    
    for i in range(n_samples):
        # Rule-based crop selection based on conditions
        if soil_moisture[i] > 0.7 and rainfall_dev[i] > 10:
            crops[i] = 0 if season[i] == 0 else np.random.choice([0, 3])  # Rice/Sugarcane (water-loving)
        elif temperature[i] < 25 and season[i] == 1:
            crops[i] = 1  # Wheat (cool season)
        elif soil_moisture[i] < 0.4 and rainfall_dev[i] < -20:
            crops[i] = 5  # Pulses (drought-tolerant)
        elif temperature[i] > 30 and soil_type[i] == 2:
            crops[i] = 2  # Cotton (warm, clay soils)
        elif ndvi[i] > 0.7:
            crops[i] = np.random.choice([0, 3, 4, 7])  # High NDVI = productive crops
        else:
            crops[i] = np.random.choice([4, 5, 6])  # Corn, Pulses, Vegetables
    
    # Create features array
    X = np.column_stack([ndvi, soil_moisture, temperature, rainfall_dev, season, soil_type])
    
    # Train Random Forest Classifier
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X, crops)
    
    # Save model
    os.makedirs('backend/model/saved', exist_ok=True)
    with open('backend/model/saved/crop_recommender.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Crop recommender trained with accuracy: {model.score(X, crops):.3f}")
    return model

def load_crop_recommender():
    """Load the trained crop recommender"""
    model_path = 'backend/model/saved/crop_recommender.pkl'
    
    if not os.path.exists(model_path):
        print("Crop recommender not found. Training new model...")
        return train_crop_recommender()
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    return model

def recommend_crops(ndvi, soil_moisture, temperature, rainfall_deviation, season, soil_type):
    """Recommend top 3 crops for given conditions"""
    model = load_crop_recommender()
    
    # Season encoding
    season_map = {'Kharif': 0, 'Rabi': 1, 'Zaid': 2}
    season_encoded = season_map.get(season, 0)
    
    # Soil type encoding
    soil_map = {'Sandy': 0, 'Loamy': 1, 'Clay': 2}
    soil_encoded = soil_map.get(soil_type, 1)
    
    # Create feature vector
    features = np.array([[ndvi, soil_moisture, temperature, rainfall_deviation, season_encoded, soil_encoded]])
    
    # Get probabilities for all crops
    probabilities = model.predict_proba(features)[0]
    
    # Crop names
    crop_names = ['Rice', 'Wheat', 'Cotton', 'Sugarcane', 'Corn', 'Pulses', 'Vegetables', 'Fruits']
    
    # Get top 3 recommendations
    top_indices = np.argsort(probabilities)[-3:][::-1]
    
    recommendations = []
    for idx in top_indices:
        recommendations.append({
            'crop': crop_names[idx],
            'success_probability': round(probabilities[idx] * 100, 1),
            'reason': get_crop_reason(crop_names[idx], ndvi, soil_moisture, temperature, rainfall_deviation)
        })
    
    return recommendations

def get_crop_reason(crop, ndvi, soil_moisture, temperature, rainfall_dev):
    """Generate explanation for crop recommendation"""
    reasons = {
        'Rice': 'High water availability and warm temperature ideal for paddy cultivation',
        'Wheat': 'Cool temperatures and moderate moisture perfect for wheat growth',
        'Cotton': 'Warm climate and well-drained soil suitable for cotton',
        'Sugarcane': 'High soil moisture and warm conditions favor sugarcane',
        'Corn': 'Balanced conditions support good maize production',
        'Pulses': 'Drought-tolerant crop suitable for current water conditions',
        'Vegetables': 'Moderate conditions good for vegetable cultivation',
        'Fruits': 'Healthy vegetation and climate suitable for fruit crops'
    }
    
    return reasons.get(crop, 'Suitable for current environmental conditions')

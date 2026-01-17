import numpy as np
import pickle
import os
from backend.utils.helpers import setup_logger, log_step
from backend.utils.config import MODEL_PATH, FEATURE_IMPORTANCE_PATH
from backend.preprocessing.feature_engineering import prepare_feature_vector

logger = setup_logger(__name__)

class ModelPredictor:
    """Advanced model predictor with confidence scores and detailed explanations."""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_importance = None
        self.model_metrics = None
        self.feature_names = [
            'ndvi_mean', 'ndvi_trend', 'ndvi_variance',
            'rainfall_deviation', 'temperature_anomaly',
            'soil_moisture_index', 'soil_type_encoded',
            'pest_frequency'
        ]
        self.load_model()
    
    def load_model(self):
        """Load trained model, scaler, and metadata from disk."""
        if not os.path.exists(MODEL_PATH):
            logger.error(f"Model not found at {MODEL_PATH}")
            logger.info("Training model now...")
            from backend.model.train import train_crop_failure_model
            train_crop_failure_model()
        
        # Load model
        with open(MODEL_PATH, 'rb') as f:
            self.model = pickle.load(f)
        
        # Load scaler
        scaler_path = MODEL_PATH.replace('.pkl', '_scaler.pkl')
        if os.path.exists(scaler_path):
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
        
        # Load feature importance
        if os.path.exists(FEATURE_IMPORTANCE_PATH):
            with open(FEATURE_IMPORTANCE_PATH, 'rb') as f:
                self.feature_importance = pickle.load(f)
        
        # Load training metrics
        metrics_path = MODEL_PATH.replace('.pkl', '_metrics.pkl')
        if os.path.exists(metrics_path):
            with open(metrics_path, 'rb') as f:
                self.model_metrics = pickle.load(f)
        
        log_step("Model Loading", "success")
    
    def predict(self, state, district, crop, season):
        """
        Predict crop failure risk with confidence scores and detailed explanation.
        Returns: risk_level, probability, confidence, explanation, raw_features
        """
        log_step("Prediction Pipeline", "in_progress")
        
        # Prepare features
        norm_features, raw_features = prepare_feature_vector(state, district, crop, season)
        
        # Create feature vector
        feature_vector = np.array([
            norm_features['ndvi_mean'],
            norm_features['ndvi_trend'],
            norm_features['ndvi_variance'],
            norm_features['rainfall_deviation'],
            norm_features['temperature_anomaly'],
            norm_features['soil_moisture_index'],
            norm_features['soil_type_encoded'],
            norm_features['pest_frequency']
        ]).reshape(1, -1)
        
        # Apply scaling if scaler is available
        if self.scaler is not None:
            feature_vector = self.scaler.transform(feature_vector)
        
        # Get prediction
        prediction = self.model.predict(feature_vector)[0]
        probability = self.model.predict_proba(feature_vector)[0]
        
        # Calculate confidence score (distance from decision boundary)
        risk_probability = probability[1]  # Probability of failure
        confidence = abs(risk_probability - 0.5) * 2  # Scale 0-1
        
        # Determine risk level with refined thresholds
        if risk_probability >= 0.7:
            risk_level = 'High'
        elif risk_probability >= 0.4:
            risk_level = 'Moderate'
        else:
            risk_level = 'Low'
        
        # Get detailed explanation
        explanation = self._get_explanation(norm_features, raw_features, risk_probability, confidence)
        
        log_step("Prediction Pipeline", "success")
        
        return {
            'risk_level': risk_level,
            'probability': float(risk_probability),
            'confidence': float(confidence),
            'explanation': explanation,
            'raw_features': raw_features,
            'model_accuracy': self.model_metrics.get('accuracy', 0.9) if self.model_metrics else 0.9
        }
    
    def _get_explanation(self, norm_features, raw_features, risk_probability, confidence):
        """Generate detailed explanation with top contributing factors."""
        if self.feature_importance is None:
            self.feature_importance = {name: 1.0/8 for name in self.feature_names}
        
        # Calculate contribution = feature_value * feature_importance
        contributions = {}
        for fname in self.feature_names:
            contributions[fname] = norm_features.get(fname, 0) * self.feature_importance.get(fname, 0)
        
        # Get top 5 factors
        top_factors = sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
        
        # Generate human-readable interpretations
        interpretations = {
            'ndvi_mean': self._interpret_ndvi(raw_features.get('ndvi_mean', 0)),
            'rainfall_deviation': self._interpret_rainfall(raw_features.get('rainfall_deviation', 0)),
            'soil_moisture_index': self._interpret_soil_moisture(raw_features.get('soil_moisture_index', 0)),
            'temperature_anomaly': self._interpret_temperature(raw_features.get('temperature_anomaly', 0)),
            'pest_frequency': self._interpret_pest(raw_features.get('pest_frequency', 0))
        }
        
        explanation = {
            'top_factors': [
                {
                    'factor': fname.replace('_', ' ').title(),
                    'contribution': float(contrib),
                    'interpretation': interpretations.get(fname, 'Normal range')
                }
                for fname, contrib in top_factors
            ],
            'risk_probability': float(risk_probability),
            'confidence_score': float(confidence),
            'confidence_level': 'High' if confidence > 0.7 else 'Moderate' if confidence > 0.4 else 'Low'
        }
        
        return explanation
    
    def _interpret_ndvi(self, value):
        """Interpret NDVI values."""
        if value > 0.7:
            return "Excellent vegetation health"
        elif value > 0.5:
            return "Good vegetation health"
        elif value > 0.3:
            return "Moderate vegetation stress"
        else:
            return "Critical vegetation stress"
    
    def _interpret_rainfall(self, deviation):
        """Interpret rainfall deviation."""
        if abs(deviation) < 10:
            return "Normal rainfall pattern"
        elif abs(deviation) < 25:
            return "Moderate rainfall deviation"
        else:
            return "Severe rainfall deficit" if deviation < 0 else "Excessive rainfall"
    
    def _interpret_soil_moisture(self, value):
        """Interpret soil moisture."""
        if value > 60:
            return "Adequate soil moisture"
        elif value > 40:
            return "Moderate soil moisture"
        elif value > 25:
            return "Low soil moisture"
        else:
            return "Critical water deficit"
    
    def _interpret_temperature(self, anomaly):
        """Interpret temperature anomaly."""
        if abs(anomaly) < 1.5:
            return "Normal temperature range"
        elif abs(anomaly) < 3:
            return "Moderate temperature stress"
        else:
            return "Extreme heat stress" if anomaly > 0 else "Extreme cold stress"
    
    def _interpret_pest(self, frequency):
        """Interpret pest frequency."""
        if frequency < 0.3:
            return "Low pest pressure"
        elif frequency < 0.6:
            return "Moderate pest activity"
        else:
            return "High pest infestation risk"

def get_prediction(state, district, crop, season):
    """Public interface for predictions."""
    predictor = ModelPredictor()
    return predictor.predict(state, district, crop, season)

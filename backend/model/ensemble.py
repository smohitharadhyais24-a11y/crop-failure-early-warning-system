"""
Ensemble Predictor: Unified API for ensemble predictions

This module provides the ensemble_predict() function that:
1. Loads RF, XGBoost, and meta-learner from disk
2. Handles missing model failures gracefully with fallbacks
3. Returns ensemble score + base model scores + confidence
"""

import numpy as np
import pickle
import os
from backend.utils.helpers import setup_logger, log_step
from backend.preprocessing.feature_engineering import prepare_feature_vector

logger = setup_logger(__name__)

ENSEMBLE_MODELS_PATH = 'backend/model/saved/ensemble/'


class EnsemblePredictor:
    """Unified ensemble predictor with graceful fallbacks."""
    
    def __init__(self):
        """Initialize ensemble components."""
        self.rf_model = None
        self.xgb_model = None
        self.meta_learner = None
        self.scaler = None
        self.scaler_meta = None
        self.feature_importance = None
        self.test_metrics = None
        
        self.feature_names = [
            'ndvi_mean', 'ndvi_trend', 'ndvi_variance',
            'rainfall_deviation', 'temperature_anomaly',
            'soil_moisture_index', 'soil_type_encoded',
            'pest_frequency'
        ]
        
        self.load_ensemble()
    
    def load_ensemble(self):
        """Load all ensemble components from disk."""
        try:
            log_step("Loading Ensemble Models", "in_progress")
            
            # Check if models exist
            if not os.path.exists(ENSEMBLE_MODELS_PATH):
                logger.warning(f"Ensemble models not found at {ENSEMBLE_MODELS_PATH}")
                logger.info("Training ensemble models now...")
                from backend.model.ensemble_train import train_ensemble_models
                train_ensemble_models()
            
            # Load RF model
            try:
                with open(f'{ENSEMBLE_MODELS_PATH}rf_model.pkl', 'rb') as f:
                    self.rf_model = pickle.load(f)
                logger.info("✓ Loaded RF model")
            except Exception as e:
                logger.warning(f"Failed to load RF model: {e}")
                self.rf_model = None
            
            # Load XGBoost model
            try:
                with open(f'{ENSEMBLE_MODELS_PATH}xgb_model.pkl', 'rb') as f:
                    self.xgb_model = pickle.load(f)
                logger.info("✓ Loaded XGBoost model")
            except Exception as e:
                logger.warning(f"Failed to load XGBoost model: {e}")
                self.xgb_model = None
            
            # Load meta-learner
            try:
                with open(f'{ENSEMBLE_MODELS_PATH}meta_learner.pkl', 'rb') as f:
                    self.meta_learner = pickle.load(f)
                logger.info("✓ Loaded meta-learner")
            except Exception as e:
                logger.warning(f"Failed to load meta-learner: {e}")
                self.meta_learner = None
            
            # Load scalers
            try:
                with open(f'{ENSEMBLE_MODELS_PATH}scaler.pkl', 'rb') as f:
                    self.scaler = pickle.load(f)
                logger.info("✓ Loaded feature scaler")
            except Exception as e:
                logger.warning(f"Failed to load feature scaler: {e}")
                self.scaler = None
            
            try:
                with open(f'{ENSEMBLE_MODELS_PATH}scaler_meta.pkl', 'rb') as f:
                    self.scaler_meta = pickle.load(f)
                logger.info("✓ Loaded meta-feature scaler")
            except Exception as e:
                logger.warning(f"Failed to load meta-feature scaler: {e}")
                self.scaler_meta = None
            
            # Load feature importance
            try:
                with open(f'{ENSEMBLE_MODELS_PATH}feature_importance.pkl', 'rb') as f:
                    self.feature_importance = pickle.load(f)
                logger.info("✓ Loaded feature importance")
            except Exception as e:
                logger.warning(f"Failed to load feature importance: {e}")
                self.feature_importance = None
            
            # Load test metrics
            try:
                with open(f'{ENSEMBLE_MODELS_PATH}test_metrics.pkl', 'rb') as f:
                    self.test_metrics = pickle.load(f)
                logger.info("✓ Loaded test metrics")
            except Exception as e:
                logger.warning(f"Failed to load test metrics: {e}")
                self.test_metrics = None
            
            # Validation
            models_available = sum([
                self.rf_model is not None,
                self.xgb_model is not None,
                self.meta_learner is not None
            ])
            
            if models_available == 0:
                logger.error("No models loaded! Cannot proceed with predictions.")
                raise RuntimeError("Ensemble models not available")
            
            logger.info(f"✓ Ensemble ready ({models_available}/3 models loaded)")
            log_step("Loading Ensemble Models", "success")
            
        except Exception as e:
            logger.error(f"Critical error loading ensemble: {e}")
            raise
    
    def predict(self, state, district, crop, season):
        """
        Make ensemble prediction with fallback logic.
        
        Returns:
            {
                'risk_level': 'Low'/'Medium'/'High',
                'ensemble_probability': 0.45,
                'rf_probability': 0.42,
                'xgb_probability': 0.48,
                'confidence': 0.87,
                'models_used': 3,
                'explanation': 'Ensemble combines RF, XGBoost, and meta-learner'
            }
        """
        try:
            log_step("Ensemble Prediction", "in_progress")
            
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
            
            # Apply feature scaling
            if self.scaler is not None:
                feature_vector_scaled = self.scaler.transform(feature_vector)
            else:
                feature_vector_scaled = feature_vector
                logger.warning("Feature scaler not available; using raw features")
            
            # Get base model predictions
            rf_prob = None
            xgb_prob = None
            models_used = 0
            
            try:
                if self.rf_model is not None:
                    rf_prob = self.rf_model.predict_proba(feature_vector_scaled)[0, 1]
                    models_used += 1
                    logger.debug(f"RF probability: {rf_prob:.4f}")
            except Exception as e:
                logger.warning(f"RF prediction failed: {e}")
            
            try:
                if self.xgb_model is not None:
                    xgb_prob = self.xgb_model.predict_proba(feature_vector_scaled)[0, 1]
                    models_used += 1
                    logger.debug(f"XGBoost probability: {xgb_prob:.4f}")
            except Exception as e:
                logger.warning(f"XGBoost prediction failed: {e}")
            
            # Fallback logic: if base models fail, use simple average
            ensemble_prob = None
            if rf_prob is not None and xgb_prob is not None:
                # Both models available: use meta-learner
                try:
                    if self.meta_learner is not None and self.scaler_meta is not None:
                        meta_features = np.array([[rf_prob, xgb_prob]])
                        meta_features_scaled = self.scaler_meta.transform(meta_features)
                        ensemble_prob = self.meta_learner.predict_proba(meta_features_scaled)[0, 1]
                        logger.debug(f"Ensemble (meta-learner) probability: {ensemble_prob:.4f}")
                    else:
                        # Meta-learner not available, average base models
                        ensemble_prob = (rf_prob + xgb_prob) / 2
                        logger.warning("Meta-learner not available; using average of base models")
                except Exception as e:
                    logger.warning(f"Meta-learner prediction failed: {e}, using average")
                    ensemble_prob = (rf_prob + xgb_prob) / 2
            else:
                # One or both models unavailable: use simple average
                available_probs = [p for p in [rf_prob, xgb_prob] if p is not None]
                if available_probs:
                    ensemble_prob = np.mean(available_probs)
                    logger.warning(f"Using {len(available_probs)} available model(s) for prediction")
                else:
                    logger.error("No models available for prediction!")
                    ensemble_prob = 0.5  # Last resort fallback
            
            # Calculate confidence (agreement between base models)
            confidence = 0.5
            if rf_prob is not None and xgb_prob is not None:
                # Confidence based on model agreement
                agreement = 1 - abs(rf_prob - xgb_prob)
                confidence = min(0.95, 0.5 + 0.45 * agreement)
            elif rf_prob is not None or xgb_prob is not None:
                # Only one model: lower confidence
                confidence = 0.75
            
            # Determine risk level
            if ensemble_prob < 0.33:
                risk_level = 'Low'
            elif ensemble_prob < 0.67:
                risk_level = 'Medium'
            else:
                risk_level = 'High'
            
            result = {
                'risk_level': risk_level,
                'ensemble_probability': float(ensemble_prob),
                'rf_probability': float(rf_prob) if rf_prob is not None else None,
                'xgb_probability': float(xgb_prob) if xgb_prob is not None else None,
                'confidence': float(confidence),
                'models_used': models_used,
                'raw_features': raw_features,
                'normalized_features': norm_features
            }
            
            log_step("Ensemble Prediction", "success")
            
            return result
            
        except Exception as e:
            logger.error(f"Ensemble prediction failed: {e}")
            raise


# Singleton instance for API use
_ensemble_predictor = None


def get_ensemble_predictor():
    """Get or create singleton ensemble predictor."""
    global _ensemble_predictor
    if _ensemble_predictor is None:
        _ensemble_predictor = EnsemblePredictor()
    return _ensemble_predictor


def ensemble_predict(state, district, crop, season):
    """
    Unified ensemble prediction API.
    
    Args:
        state: State name
        district: District name
        crop: Crop name
        season: Season (Kharif/Rabi/Summer)
    
    Returns:
        Ensemble prediction result dict
    """
    predictor = get_ensemble_predictor()
    return predictor.predict(state, district, crop, season)

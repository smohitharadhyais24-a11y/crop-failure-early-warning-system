"""
Counterfactual Reasoning Module - What-If Analysis

Generates actionable "what-if" scenarios for farmers.
Example: "If NDVI improves by 0.1, risk reduces to Medium"
"""

import numpy as np
from backend.model.ensemble import get_ensemble_predictor
from backend.preprocessing.feature_engineering import prepare_feature_vector
from backend.utils.helpers import setup_logger, log_step

logger = setup_logger(__name__)


class CounterfactualGenerator:
    """Generate what-if scenarios for farmer recommendations."""
    
    def __init__(self):
        """Initialize with ensemble predictor."""
        self.predictor = get_ensemble_predictor()
        self.scaler = self.predictor.scaler
        
        self.feature_names = [
            'ndvi_mean', 'ndvi_trend', 'ndvi_variance',
            'rainfall_deviation', 'temperature_anomaly',
            'soil_moisture_index', 'soil_type_encoded',
            'pest_frequency'
        ]
        
        self.display_names = {
            'ndvi_mean': 'Vegetation Health (NDVI)',
            'ndvi_trend': 'Vegetation Trend',
            'rainfall_deviation': 'Rainfall',
            'soil_moisture_index': 'Soil Moisture',
            'temperature_anomaly': 'Temperature',
            'pest_frequency': 'Pest Activity'
        }
    
    def generate_counterfactuals(self, state, district, crop, season, original_prediction):
        """
        Generate what-if scenarios by varying top features.
        
        Returns:
            [
                {
                    'scenario': 'Increase NDVI by 0.1',
                    'changes': {'ndvi_mean': 0.787},
                    'new_probability': 0.08,
                    'new_risk_level': 'Low',
                    'probability_change': -0.035,
                    'actionable': 'Improve irrigation to boost vegetation'
                },
                ...
            ]
        """
        try:
            log_step("Counterfactual Generation", "in_progress")
            
            # Get original features
            norm_features, raw_features = prepare_feature_vector(state, district, crop, season)
            
            original_prob = original_prediction['ensemble_probability']
            
            counterfactuals = []
            
            # 1. Increase NDVI (best agricultural practice)
            if norm_features.get('ndvi_mean', 0.5) < 0.85:
                for delta in [0.05, 0.10, 0.15]:
                    new_norm_features = norm_features.copy()
                    new_ndvi = min(0.85, norm_features['ndvi_mean'] + delta)
                    new_norm_features['ndvi_mean'] = new_ndvi
                    
                    new_pred = self._predict_with_modified_features(new_norm_features)
                    prob_change = new_pred['ensemble_probability'] - original_prob
                    risk_reduction = abs(prob_change) * 100
                    
                    counterfactuals.append({
                        'scenario': f'Improve vegetation health by {delta:.1%}',
                        'feature': 'NDVI Mean',
                        'change_amount': f'+{delta:.1%}',
                        'current_value': f"{norm_features['ndvi_mean']:.3f}",
                        'new_value': f"{new_ndvi:.3f}",
                        'new_probability': new_pred['ensemble_probability'],
                        'new_risk_level': new_pred['risk_level'],
                        'probability_change': prob_change,
                        'impact': f"Risk reduces by {risk_reduction:.1f}%" if prob_change < 0 else f"Risk increases by {risk_reduction:.1f}%",
                        'actionable': 'Improve irrigation, soil health, and pest management to boost vegetation'
                    })
            
            # 2. Reduce rainfall deviation (mitigate drought/excess)
            if abs(norm_features.get('rainfall_deviation', 0)) > 5:
                for improvement in [0.2, 0.35, 0.50]:
                    new_norm_features = norm_features.copy()
                    current_deficit = abs(norm_features['rainfall_deviation'])
                    new_rainfall_dev = norm_features['rainfall_deviation'] * (1 - improvement)
                    new_norm_features['rainfall_deviation'] = new_rainfall_dev
                    
                    new_pred = self._predict_with_modified_features(new_norm_features)
                    prob_change = new_pred['ensemble_probability'] - original_prob
                    
                    counterfactuals.append({
                        'scenario': f'Improve rainfall by {improvement:.0%}',
                        'feature': 'Rainfall Deviation',
                        'change_amount': f'{improvement:.0%} normalization',
                        'current_value': f"{norm_features['rainfall_deviation']:.1f}%",
                        'new_value': f"{new_rainfall_dev:.1f}%",
                        'new_probability': new_pred['ensemble_probability'],
                        'new_risk_level': new_pred['risk_level'],
                        'probability_change': prob_change,
                        'impact': f"Risk reduces by {abs(prob_change)*100:.1f}%" if prob_change < 0 else f"Risk increases",
                        'actionable': 'Use drip irrigation or increase water management during dry season'
                    })
            
            # 3. Increase soil moisture (directly actionable)
            if norm_features.get('soil_moisture_index', 0.5) < 0.85:
                for delta in [0.05, 0.10, 0.15]:
                    new_norm_features = norm_features.copy()
                    new_moisture = min(0.95, norm_features['soil_moisture_index'] + delta)
                    new_norm_features['soil_moisture_index'] = new_moisture
                    
                    new_pred = self._predict_with_modified_features(new_norm_features)
                    prob_change = new_pred['ensemble_probability'] - original_prob
                    
                    counterfactuals.append({
                        'scenario': f'Increase soil moisture by {delta:.0%}',
                        'feature': 'Soil Moisture',
                        'change_amount': f'+{delta:.0%}',
                        'current_value': f"{norm_features['soil_moisture_index']:.1%}",
                        'new_value': f"{new_moisture:.1%}",
                        'new_probability': new_pred['ensemble_probability'],
                        'new_risk_level': new_pred['risk_level'],
                        'probability_change': prob_change,
                        'impact': f"Risk reduces by {abs(prob_change)*100:.1f}%" if prob_change < 0 else "Risk unchanged",
                        'actionable': 'Increase irrigation frequency or add mulch to retain moisture'
                    })
            
            # 4. Reduce pest frequency (integrated pest management)
            if norm_features.get('pest_frequency', 0) > 0.05:
                for reduction in [0.25, 0.50, 0.75]:
                    new_norm_features = norm_features.copy()
                    new_pest_freq = max(0, norm_features['pest_frequency'] * (1 - reduction))
                    new_norm_features['pest_frequency'] = new_pest_freq
                    
                    new_pred = self._predict_with_modified_features(new_norm_features)
                    prob_change = new_pred['ensemble_probability'] - original_prob
                    
                    counterfactuals.append({
                        'scenario': f'Reduce pest activity by {reduction:.0%}',
                        'feature': 'Pest Frequency',
                        'change_amount': f'-{reduction:.0%}',
                        'current_value': f"{norm_features['pest_frequency']:.1%}",
                        'new_value': f"{new_pest_freq:.1%}",
                        'new_probability': new_pred['ensemble_probability'],
                        'new_risk_level': new_pred['risk_level'],
                        'probability_change': prob_change,
                        'impact': f"Risk reduces by {abs(prob_change)*100:.1f}%" if prob_change < 0 else "Risk unchanged",
                        'actionable': 'Use integrated pest management (IPM): crop rotation, biocontrols, targeted spraying'
                    })
            
            # 5. Reduce temperature anomaly (seasonal adaptation)
            if abs(norm_features.get('temperature_anomaly', 0)) > 1:
                new_norm_features = norm_features.copy()
                new_temp_anom = norm_features['temperature_anomaly'] * 0.5  # Reduce by 50%
                new_norm_features['temperature_anomaly'] = new_temp_anom
                
                new_pred = self._predict_with_modified_features(new_norm_features)
                prob_change = new_pred['ensemble_probability'] - original_prob
                
                counterfactuals.append({
                    'scenario': 'Mitigate temperature stress',
                    'feature': 'Temperature Anomaly',
                    'change_amount': '-50%',
                    'current_value': f"{norm_features['temperature_anomaly']:.1f}°C",
                    'new_value': f"{new_temp_anom:.1f}°C",
                    'new_probability': new_pred['ensemble_probability'],
                    'new_risk_level': new_pred['risk_level'],
                    'probability_change': prob_change,
                    'impact': f"Risk reduces by {abs(prob_change)*100:.1f}%" if prob_change < 0 else "Risk unchanged",
                    'actionable': 'Use shade netting, select heat-tolerant varieties, or adjust sowing dates'
                })
            
            # Sort by impact magnitude (descending)
            counterfactuals.sort(key=lambda x: abs(x['probability_change']), reverse=True)
            
            # Keep top 5 most impactful
            counterfactuals = counterfactuals[:5]
            
            log_step("Counterfactual Generation", "success")
            
            return counterfactuals
            
        except Exception as e:
            logger.error(f"Counterfactual generation failed: {e}")
            return []
    
    def _predict_with_modified_features(self, modified_norm_features):
        """Make prediction with modified features."""
        try:
            feature_vector = np.array([
                modified_norm_features.get('ndvi_mean', 0.5),
                modified_norm_features.get('ndvi_trend', 0),
                modified_norm_features.get('ndvi_variance', 0.03),
                modified_norm_features.get('rainfall_deviation', 0),
                modified_norm_features.get('temperature_anomaly', 0),
                modified_norm_features.get('soil_moisture_index', 0.5),
                modified_norm_features.get('soil_type_encoded', 3),
                modified_norm_features.get('pest_frequency', 0.1)
            ]).reshape(1, -1)
            
            if self.scaler is not None:
                feature_vector_scaled = self.scaler.transform(feature_vector)
            else:
                feature_vector_scaled = feature_vector
            
            # Get predictions from base models
            rf_prob = self.predictor.rf_model.predict_proba(feature_vector_scaled)[0, 1]
            xgb_prob = self.predictor.xgb_model.predict_proba(feature_vector_scaled)[0, 1]
            
            # Meta-learner prediction
            meta_features = np.array([[rf_prob, xgb_prob]])
            meta_features_scaled = self.predictor.scaler_meta.transform(meta_features)
            ensemble_prob = self.predictor.meta_learner.predict_proba(meta_features_scaled)[0, 1]
            
            # Determine risk level
            if ensemble_prob < 0.33:
                risk_level = 'Low'
            elif ensemble_prob < 0.67:
                risk_level = 'Medium'
            else:
                risk_level = 'High'
            
            return {
                'ensemble_probability': float(ensemble_prob),
                'rf_probability': float(rf_prob),
                'xgb_probability': float(xgb_prob),
                'risk_level': risk_level
            }
            
        except Exception as e:
            logger.warning(f"Modified prediction failed: {e}")
            return {'ensemble_probability': 0.5, 'risk_level': 'Medium'}


# Singleton instance
_counterfactual_generator = None


def get_counterfactual_generator():
    """Get or create singleton counterfactual generator."""
    global _counterfactual_generator
    if _counterfactual_generator is None:
        _counterfactual_generator = CounterfactualGenerator()
    return _counterfactual_generator


def generate_counterfactuals(state, district, crop, season, original_prediction):
    """
    Unified counterfactual generation API.
    """
    generator = get_counterfactual_generator()
    return generator.generate_counterfactuals(state, district, crop, season, original_prediction)

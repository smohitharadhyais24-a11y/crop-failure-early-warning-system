"""
Ensemble Model Training: RF + XGBoost + Meta-Learner (Stacking)

This module trains three models independently:
1. Random Forest (RF) - captures structured patterns
2. XGBoost - captures nonlinear feature interactions
3. Logistic Regression - meta-learner that stacks the above

The ensemble combines all three predictions into a single robust score.
"""

import numpy as np
import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_predict, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, f1_score
from sklearn.preprocessing import StandardScaler
import xgboost as xgb

from backend.utils.helpers import setup_logger, log_step, ensure_dir_exists
from backend.preprocessing.labeling import LabelGenerator, create_training_dataset
from backend.utils.config import MODEL_PATH, FEATURE_IMPORTANCE_PATH

logger = setup_logger(__name__)

ENSEMBLE_MODELS_PATH = 'backend/model/saved/ensemble/'
ensure_dir_exists(ENSEMBLE_MODELS_PATH)


class EnsembleTrainer:
    """
    Multi-model ensemble trainer with Random Forest, XGBoost, and Logistic Regression meta-learner.
    
    Architecture:
    - Base Model 1: RandomForestClassifier (pattern detection)
    - Base Model 2: XGBoost (nonlinear interactions)
    - Meta-Learner: LogisticRegression (combines base model outputs)
    
    Training approach:
    - Train RF and XGBoost independently on full training set
    - Generate predictions from RF and XGBoost on training set (cross-validation)
    - Train meta-learner on these meta-features
    - Final prediction: meta-learner(rf_pred, xgb_pred)
    """
    
    def __init__(self):
        """Initialize ensemble components."""
        # Base Model 1: Random Forest
        self.rf_model = RandomForestClassifier(
            n_estimators=300,
            max_depth=20,
            min_samples_split=4,
            min_samples_leaf=1,
            max_features='sqrt',
            bootstrap=True,
            oob_score=True,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1,
            verbose=0
        )
        
        # Base Model 2: XGBoost
        self.xgb_model = xgb.XGBClassifier(
            n_estimators=300,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            gamma=1,
            min_child_weight=1,
            random_state=42,
            n_jobs=-1,
            eval_metric='logloss',
            verbosity=0
        )
        
        # Meta-Learner: Logistic Regression
        self.meta_learner = LogisticRegression(
            max_iter=1000,
            random_state=42,
            solver='lbfgs'
        )
        
        self.scaler = StandardScaler()
        self.scaler_meta = StandardScaler()
        
        self.feature_names = [
            'ndvi_mean', 'ndvi_trend', 'ndvi_variance',
            'rainfall_deviation', 'temperature_anomaly',
            'soil_moisture_index', 'soil_type_encoded',
            'pest_frequency'
        ]
        
        self.cv_scores = {}
        self.test_metrics = {}
        self.base_model_importances = {}
    
    def generate_training_data(self, n_samples=2000):
        """Generate realistic training data with correlated features."""
        log_step("Ensemble Training Data Generation", "in_progress")
        
        X = []
        y = []
        
        for _ in range(n_samples):
            # Generate base NDVI with realistic distribution
            ndvi_category = np.random.choice(['healthy', 'stressed', 'critical'], p=[0.65, 0.25, 0.10])
            
            if ndvi_category == 'healthy':
                ndvi_mean = np.random.uniform(0.55, 0.85)
                soil_moisture_base = np.random.uniform(0.5, 0.9)
                pest_freq_base = np.random.uniform(0.0, 0.4)
                risk_prob = 0.05  # 5% failure rate when healthy
            elif ndvi_category == 'stressed':
                ndvi_mean = np.random.uniform(0.3, 0.55)
                soil_moisture_base = np.random.uniform(0.3, 0.6)
                pest_freq_base = np.random.uniform(0.3, 0.7)
                risk_prob = 0.35  # 35% failure rate when stressed
            else:  # critical
                ndvi_mean = np.random.uniform(0.15, 0.35)
                soil_moisture_base = np.random.uniform(0.1, 0.4)
                pest_freq_base = np.random.uniform(0.5, 0.95)
                risk_prob = 0.75  # 75% failure rate when critical
            
            # NDVI trend
            if ndvi_mean > 0.6:
                ndvi_trend = np.random.uniform(-0.02, 0.05)
            elif ndvi_mean > 0.4:
                ndvi_trend = np.random.uniform(-0.05, 0.02)
            else:
                ndvi_trend = np.random.uniform(-0.08, -0.01)
            
            # NDVI variance
            if ndvi_mean > 0.6:
                ndvi_variance = np.random.uniform(0.01, 0.04)
            else:
                ndvi_variance = np.random.uniform(0.04, 0.1)
            
            # Rainfall deviation
            if soil_moisture_base > 0.6:
                rainfall_dev = np.random.uniform(-15, 20)
            elif soil_moisture_base > 0.3:
                rainfall_dev = np.random.uniform(-30, 10)
            else:
                rainfall_dev = np.random.uniform(-50, -15)
            
            # Temperature anomaly
            if ndvi_category == 'healthy':
                temp_anom = np.random.uniform(-2, 2)
            elif ndvi_category == 'stressed':
                temp_anom = np.random.uniform(-4, 5)
            else:
                temp_anom = np.random.uniform(-8, 8)
            
            # Soil moisture
            soil_moisture = soil_moisture_base + np.random.uniform(-0.05, 0.05)
            soil_moisture = np.clip(soil_moisture, 0.1, 0.95)
            
            # Soil type (1-5)
            soil_type = np.random.choice([1, 2, 3, 4, 5])
            
            # Pest frequency
            pest_freq = pest_freq_base + np.random.uniform(-0.05, 0.05)
            pest_freq = np.clip(pest_freq, 0.0, 1.0)
            
            # Label: crop failure (1) or success (0)
            failure = np.random.rand() < risk_prob
            
            X.append([
                ndvi_mean, ndvi_trend, ndvi_variance,
                rainfall_dev, temp_anom,
                soil_moisture, soil_type, pest_freq
            ])
            y.append(1 if failure else 0)
        
        X = np.array(X)
        y = np.array(y)
        
        log_step("Ensemble Training Data Generation", "success")
        logger.info(f"Generated {n_samples} samples: {np.sum(y)} failures ({100*np.sum(y)/n_samples:.1f}%)")
        
        return X, y
    
    def train_ensemble(self, X, y, test_size=0.2, cv_folds=5):
        """
        Train ensemble: RF + XGBoost independently, then meta-learner via stacking.
        
        Args:
            X: Training features
            y: Training labels
            test_size: Fraction for test set
            cv_folds: Number of cross-validation folds
        """
        log_step("Ensemble Training", "in_progress")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # ===== TRAIN BASE MODEL 1: Random Forest =====
        log_step("Training Random Forest", "in_progress")
        self.rf_model.fit(X_train_scaled, y_train)
        rf_pred_train = self.rf_model.predict_proba(X_train_scaled)[:, 1]
        rf_pred_test = self.rf_model.predict_proba(X_test_scaled)[:, 1]
        
        rf_acc = accuracy_score(y_test, self.rf_model.predict(X_test_scaled))
        rf_auc = roc_auc_score(y_test, rf_pred_test)
        self.test_metrics['rf'] = {'accuracy': rf_acc, 'auc': rf_auc}
        logger.info(f"RF - Accuracy: {rf_acc:.4f}, AUC: {rf_auc:.4f}")
        
        # Store feature importance
        self.base_model_importances['rf'] = dict(zip(self.feature_names, self.rf_model.feature_importances_))
        
        # ===== TRAIN BASE MODEL 2: XGBoost =====
        log_step("Training XGBoost", "in_progress")
        self.xgb_model.fit(
            X_train_scaled, y_train,
            eval_set=[(X_test_scaled, y_test)],
            verbose=False
        )
        xgb_pred_train = self.xgb_model.predict_proba(X_train_scaled)[:, 1]
        xgb_pred_test = self.xgb_model.predict_proba(X_test_scaled)[:, 1]
        
        xgb_acc = accuracy_score(y_test, self.xgb_model.predict(X_test_scaled))
        xgb_auc = roc_auc_score(y_test, xgb_pred_test)
        self.test_metrics['xgb'] = {'accuracy': xgb_acc, 'auc': xgb_auc}
        logger.info(f"XGBoost - Accuracy: {xgb_acc:.4f}, AUC: {xgb_auc:.4f}")
        
        # Store feature importance
        self.base_model_importances['xgb'] = dict(zip(self.feature_names, self.xgb_model.feature_importances_))
        
        # ===== CREATE META-FEATURES (Stacking) =====
        log_step("Creating Meta-Features for Stacking", "in_progress")
        
        # Generate meta-features for training set using cross-validation
        skf = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
        rf_meta_train = cross_val_predict(
            self.rf_model, X_train_scaled, y_train, cv=skf, method='predict_proba'
        )[:, 1]
        xgb_meta_train = cross_val_predict(
            self.xgb_model, X_train_scaled, y_train, cv=skf, method='predict_proba'
        )[:, 1]
        
        # Meta-features for test set (from full training)
        rf_meta_test = self.rf_model.predict_proba(X_test_scaled)[:, 1]
        xgb_meta_test = self.xgb_model.predict_proba(X_test_scaled)[:, 1]
        
        # Stack meta-features
        X_meta_train = np.column_stack([rf_meta_train, xgb_meta_train])
        X_meta_test = np.column_stack([rf_meta_test, xgb_meta_test])
        
        # Scale meta-features
        X_meta_train_scaled = self.scaler_meta.fit_transform(X_meta_train)
        X_meta_test_scaled = self.scaler_meta.transform(X_meta_test)
        
        # ===== TRAIN META-LEARNER: Logistic Regression =====
        log_step("Training Meta-Learner (Logistic Regression)", "in_progress")
        self.meta_learner.fit(X_meta_train_scaled, y_train)
        
        # Ensemble predictions
        ensemble_pred_test = self.meta_learner.predict_proba(X_meta_test_scaled)[:, 1]
        ensemble_acc = accuracy_score(y_test, self.meta_learner.predict(X_meta_test_scaled))
        ensemble_auc = roc_auc_score(y_test, ensemble_pred_test)
        self.test_metrics['ensemble'] = {'accuracy': ensemble_acc, 'auc': ensemble_auc}
        logger.info(f"Ensemble - Accuracy: {ensemble_acc:.4f}, AUC: {ensemble_auc:.4f}")
        
        # ===== EVALUATION =====
        log_step("Ensemble Evaluation", "in_progress")
        y_pred_ensemble = self.meta_learner.predict(X_meta_test_scaled)
        
        logger.info("\n=== Ensemble Performance ===")
        logger.info(f"Accuracy:  {ensemble_acc:.4f}")
        logger.info(f"AUC-ROC:   {ensemble_auc:.4f}")
        logger.info(f"\nClassification Report:\n{classification_report(y_test, y_pred_ensemble)}")
        
        comparison = f"""
        ╔══════════════════════════════════════════════════════╗
        ║          MODEL COMPARISON (Test Set)                 ║
        ╠══════════════════════════════════════════════════════╣
        ║ Random Forest    │ Acc: {rf_acc:.4f}  │  AUC: {rf_auc:.4f}          ║
        ║ XGBoost         │ Acc: {xgb_acc:.4f}  │  AUC: {xgb_auc:.4f}          ║
        ║ Ensemble        │ Acc: {ensemble_acc:.4f}  │  AUC: {ensemble_auc:.4f}          ║
        ╚══════════════════════════════════════════════════════╝
        """
        logger.info(comparison)
        
        log_step("Ensemble Training", "success")
        
        return X_test, y_test, rf_pred_test, xgb_pred_test, ensemble_pred_test
    
    def save_ensemble(self):
        """Save all ensemble components to disk."""
        log_step("Saving Ensemble Models", "in_progress")
        
        # Ensure directory exists
        os.makedirs(ENSEMBLE_MODELS_PATH, exist_ok=True)
        
        # Save base models
        with open(f'{ENSEMBLE_MODELS_PATH}rf_model.pkl', 'wb') as f:
            pickle.dump(self.rf_model, f)
        logger.info(f"✓ Saved RF model to {ENSEMBLE_MODELS_PATH}rf_model.pkl")
        
        with open(f'{ENSEMBLE_MODELS_PATH}xgb_model.pkl', 'wb') as f:
            pickle.dump(self.xgb_model, f)
        logger.info(f"✓ Saved XGBoost model to {ENSEMBLE_MODELS_PATH}xgb_model.pkl")
        
        # Save meta-learner
        with open(f'{ENSEMBLE_MODELS_PATH}meta_learner.pkl', 'wb') as f:
            pickle.dump(self.meta_learner, f)
        logger.info(f"✓ Saved meta-learner to {ENSEMBLE_MODELS_PATH}meta_learner.pkl")
        
        # Save scalers
        with open(f'{ENSEMBLE_MODELS_PATH}scaler.pkl', 'wb') as f:
            pickle.dump(self.scaler, f)
        logger.info(f"✓ Saved feature scaler to {ENSEMBLE_MODELS_PATH}scaler.pkl")
        
        with open(f'{ENSEMBLE_MODELS_PATH}scaler_meta.pkl', 'wb') as f:
            pickle.dump(self.scaler_meta, f)
        logger.info(f"✓ Saved meta-feature scaler to {ENSEMBLE_MODELS_PATH}scaler_meta.pkl")
        
        # Save feature importance
        with open(f'{ENSEMBLE_MODELS_PATH}feature_importance.pkl', 'wb') as f:
            pickle.dump(self.base_model_importances, f)
        logger.info(f"✓ Saved feature importance to {ENSEMBLE_MODELS_PATH}feature_importance.pkl")
        
        # Save metrics
        with open(f'{ENSEMBLE_MODELS_PATH}test_metrics.pkl', 'wb') as f:
            pickle.dump(self.test_metrics, f)
        logger.info(f"✓ Saved test metrics to {ENSEMBLE_MODELS_PATH}test_metrics.pkl")
        
        log_step("Saving Ensemble Models", "success")


def train_ensemble_models():
    """Main entry point for ensemble training."""
    logger.info("\n" + "="*60)
    logger.info("ENSEMBLE MODEL TRAINING (RF + XGBoost + Meta-Learner)")
    logger.info("="*60 + "\n")
    
    # Initialize trainer
    trainer = EnsembleTrainer()
    
    # Generate data
    X, y = trainer.generate_training_data(n_samples=2000)
    
    # Train ensemble
    X_test, y_test, rf_pred, xgb_pred, ensemble_pred = trainer.train_ensemble(X, y)
    
    # Save all models
    trainer.save_ensemble()
    
    logger.info("\n" + "="*60)
    logger.info("ENSEMBLE TRAINING COMPLETE")
    logger.info("="*60 + "\n")
    logger.info("Models saved in: backend/model/saved/ensemble/")
    logger.info("Ready for predictions via ensemble_predict()")


if __name__ == '__main__':
    train_ensemble_models()

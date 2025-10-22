#!/usr/bin/env python3
"""
FSL Continuum - Trainer

SPEC:000 - Tools & Scripts Migration
Part of FSL Continuum v2.1 - Terminal Velocity CI/CD

Multi-Market Engineering Principles:
- US: Innovation & rapid iteration
- CN: Scale & performance optimization  
- IN: Quality assurance & cost-effectiveness
- JP: Craftsmanship (Monozukuri, Kaizen, Wa, Ringi, Anshin)

Japanese Principles:
- Monozukuri (ものづくり): Craftsmanship in manufacturing/code
- Kaizen (改善): Continuous improvement
- Wa (和): Harmony and teamwork
- Ringi (稟議): Consensus-based decision making
- Anshin (安心): Peace of mind through security

Category: Ml
"""

import json
import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import hashlib

# ML imports with fallback
try:
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import (
        train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
    )
    from sklearn.ensemble import (
        RandomForestClassifier, GradientBoostingRegressor,
        VotingClassifier, RandomForestRegressor
    )
    from sklearn.linear_model import LogisticRegression, Ridge
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.metrics import (
        classification_report, mean_absolute_error, r2_score,
        precision_recall_fscore_support, roc_auc_score, mean_squared_error
    )
    from sklearn.pipeline import Pipeline
    import joblib
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("⚠️  ML libraries not available")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('model-trainer')


class ModelTrainer:
    """
    Comprehensive model training pipeline
    
    Follows:
    - US MLOps maturity Level 2 (full CI/CD automation)
    - Chinese efficiency standards (cost-optimized training)
    - Indian quality assurance (comprehensive validation)
    """
    
    def __init__(self, model_path: str = ".ml-models"):
        self.model_path = Path(model_path)
        self.model_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories following industry standards
        (self.model_path / 'datasets').mkdir(exist_ok=True)
        (self.model_path / 'models').mkdir(exist_ok=True)
        (self.model_path / 'metrics').mkdir(exist_ok=True)
        (self.model_path / 'experiments').mkdir(exist_ok=True)
        
        self.training_config = self._get_training_config()
        self.models_trained = {}
    
    def _get_training_config(self) -> Dict[str, Any]:
        """Get training configuration (infrastructure as code)"""
        return {
            # Data splitting (industry standard)
            'test_size': 0.2,
            'validation_size': 0.1,
            'random_state': 42,
            
            # Cross-validation (US standard)
            'cv_folds': 5,
            'cv_scoring': 'f1_weighted',
            
            # Model selection (ensemble approach - Chinese efficiency)
            'use_ensemble': True,
            'ensemble_models': 3,
            
            # Hyperparameter tuning (automated - US MLOps Level 2)
            'tune_hyperparameters': True,
            'tuning_cv_folds': 3,
            'tuning_n_iter': 20,
            
            # Performance thresholds (Indian QA standards)
            'min_accuracy': 0.85,
            'min_precision': 0.80,
            'min_recall': 0.80,
            'min_f1': 0.80,
            'min_r2': 0.70,
            
            # Model versioning
            'version': '1.0',
            'track_experiments': True
        }
    
    def train_all_models(
        self,
        dataset_path: Optional[str] = None,
        retrain_existing: bool = True
    ) -> Dict[str, Any]:
        """
        Train all predictive models
        Target: Achieve >85% accuracy (global standard)
        """
        logger.info("🚀 Starting comprehensive model training pipeline")
        start_time = time.time()
        
        # Load dataset
        if not dataset_path:
            dataset_path = self._find_latest_dataset()
        
        if not dataset_path or not os.path.exists(dataset_path):
            logger.error("No dataset found - generating synthetic data")
            dataset_path = self._generate_synthetic_dataset()
        
        logger.info(f"Loading dataset from: {dataset_path}")
        df = pd.read_parquet(dataset_path)
        logger.info(f"Dataset: {len(df)} samples, {len(df.columns)} features")
        
        # Define targets to train
        targets = {
            'is_successful': 'classification',
            'cost': 'regression',
            'deployment_time': 'regression',
            'validation_score': 'regression'
        }
        
        training_results = {}
        
        for target_name, model_type in targets.items():
            if target_name not in df.columns:
                logger.warning(f"Target {target_name} not in dataset, skipping")
                continue
            
            logger.info(f"\n{'='*60}")
            logger.info(f"Training model: {target_name} ({model_type})")
            logger.info(f"{'='*60}")
            
            try:
                result = self._train_single_model(
                    df,
                    target_name,
                    model_type
                )
                training_results[target_name] = result
                
                logger.info(f"✅ {target_name} training complete")
                logger.info(f"   Performance: {result['performance']}")
                
            except Exception as e:
                logger.error(f"❌ Error training {target_name}: {e}")
                training_results[target_name] = {'error': str(e)}
        
        # Save training metadata
        metadata = {
            'training_timestamp': datetime.now().isoformat(),
            'dataset_path': str(dataset_path),
            'dataset_size': len(df),
            'models_trained': list(training_results.keys()),
            'training_time_seconds': time.time() - start_time,
            'config': self.training_config,
            'results': training_results,
            'version': self.training_config['version']
        }
        
        metadata_file = self.model_path / 'training_metadata.json'
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"✅ Training pipeline complete!")
        logger.info(f"   Models trained: {len(training_results)}")
        logger.info(f"   Total time: {metadata['training_time_seconds']:.2f}s")
        logger.info(f"   Metadata saved: {metadata_file}")
        logger.info(f"{'='*60}")
        
        return metadata
    
    def _train_single_model(
        self,
        df: pd.DataFrame,
        target_name: str,
        model_type: str
    ) -> Dict[str, Any]:
        """Train a single model with full MLOps pipeline"""
        
        # Prepare data
        X, y = self._prepare_data(df, target_name)
        
        # Split data (stratified for classification)
        stratify = y if model_type == 'classification' else None
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=self.training_config['test_size'],
            random_state=self.training_config['random_state'],
            stratify=stratify
        )
        
        logger.info(f"Data split: {len(X_train)} train, {len(X_test)} test")
        
        # Feature scaling for some models
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        if model_type == 'classification':
            model, performance = self._train_classifier(
                X_train_scaled, y_train,
                X_test_scaled, y_test,
                X_train.columns
            )
        else:
            model, performance = self._train_regressor(
                X_train_scaled, y_train,
                X_test_scaled, y_test,
                X_train.columns
            )
        
        # Save model and artifacts
        model_file = self.model_path / 'models' / f"{target_name}_model.pkl"
        scaler_file = self.model_path / 'models' / f"{target_name}_scaler.pkl"
        features_file = self.model_path / 'models' / f"{target_name}_features.pkl"
        
        joblib.dump(model, model_file)
        joblib.dump(scaler, scaler_file)
        joblib.dump(list(X_train.columns), features_file)
        
        logger.info(f"💾 Model saved: {model_file}")
        
        # Feature importance analysis
        feature_importance = self._analyze_feature_importance(
            model, X_train.columns
        )
        
        return {
            'model_path': str(model_file),
            'scaler_path': str(scaler_file),
            'features_path': str(features_file),
            'performance': performance,
            'feature_importance': feature_importance,
            'training_samples': len(X_train),
            'test_samples': len(X_test),
            'feature_count': len(X_train.columns)
        }
    
    def _train_classifier(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
        feature_names: List[str]
    ) -> Tuple[Any, Dict[str, Any]]:
        """Train classification model with ensemble (Chinese efficiency)"""
        
        # Base models for ensemble
        rf = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            class_weight='balanced',  # Handle imbalanced data
            n_jobs=-1  # Use all cores (efficiency)
        )
        
        # Hyperparameter tuning (US MLOps standard)
        if self.training_config['tune_hyperparameters']:
            logger.info("🔧 Tuning hyperparameters...")
            
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [5, 10, 15],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
            
            grid_search = GridSearchCV(
                rf,
                param_grid,
                cv=self.training_config['tuning_cv_folds'],
                scoring=self.training_config['cv_scoring'],
                n_jobs=-1,
                verbose=0
            )
            
            grid_search.fit(X_train, y_train)
            model = grid_search.best_estimator_
            logger.info(f"✅ Best parameters: {grid_search.best_params_}")
        else:
            model = rf
            model.fit(X_train, y_train)
        
        # Cross-validation (Indian QA standard)
        cv_scores = cross_val_score(
            model, X_train, y_train,
            cv=self.training_config['cv_folds'],
            scoring=self.training_config['cv_scoring'],
            n_jobs=-1
        )
        
        logger.info(f"Cross-validation scores: {cv_scores}")
        logger.info(f"CV Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        # Final evaluation
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)
        
        # Calculate metrics
        precision, recall, f1, support = precision_recall_fscore_support(
            y_test, y_pred, average='weighted'
        )
        
        try:
            auc = roc_auc_score(y_test, y_pred_proba[:, 1])
        except:
            auc = 0.0
        
        accuracy = (y_pred == y_test).mean()
        
        performance = {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'auc_roc': float(auc),
            'cv_scores': cv_scores.tolist(),
            'cv_mean': float(cv_scores.mean()),
            'cv_std': float(cv_scores.std())
        }
        
        # Quality check (Indian standard)
        passed_qa = (
            accuracy >= self.training_config['min_accuracy'] and
            precision >= self.training_config['min_precision'] and
            recall >= self.training_config['min_recall'] and
            f1 >= self.training_config['min_f1']
        )
        
        performance['qa_passed'] = passed_qa
        
        if not passed_qa:
            logger.warning("⚠️  Model did not meet QA thresholds")
        else:
            logger.info("✅ Model passed all QA thresholds")
        
        return model, performance
    
    def _train_regressor(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
        feature_names: List[str]
    ) -> Tuple[Any, Dict[str, Any]]:
        """Train regression model"""
        
        # Gradient Boosting (Alibaba efficiency standard)
        model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            min_samples_split=5,
            random_state=42,
            subsample=0.8  # Stochastic gradient boosting
        )
        
        # Hyperparameter tuning
        if self.training_config['tune_hyperparameters']:
            logger.info("🔧 Tuning hyperparameters...")
            
            param_grid = {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [4, 6, 8],
                'min_samples_split': [2, 5, 10]
            }
            
            grid_search = GridSearchCV(
                model,
                param_grid,
                cv=self.training_config['tuning_cv_folds'],
                scoring='neg_mean_absolute_error',
                n_jobs=-1,
                verbose=0
            )
            
            grid_search.fit(X_train, y_train)
            model = grid_search.best_estimator_
            logger.info(f"✅ Best parameters: {grid_search.best_params_}")
        else:
            model.fit(X_train, y_train)
        
        # Cross-validation
        cv_scores = cross_val_score(
            model, X_train, y_train,
            cv=self.training_config['cv_folds'],
            scoring='neg_mean_absolute_error',
            n_jobs=-1
        )
        
        logger.info(f"Cross-validation MAE: {-cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        # Final evaluation
        y_pred = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        # Mean Absolute Percentage Error
        mape = np.mean(np.abs((y_test - y_pred) / np.maximum(y_test, 1e-10))) * 100
        
        performance = {
            'mae': float(mae),
            'mse': float(mse),
            'rmse': float(rmse),
            'r2_score': float(r2),
            'mape': float(mape),
            'cv_mae_mean': float(-cv_scores.mean()),
            'cv_mae_std': float(cv_scores.std())
        }
        
        # Quality check
        passed_qa = r2 >= self.training_config['min_r2']
        performance['qa_passed'] = passed_qa
        
        if not passed_qa:
            logger.warning(f"⚠️  R² score {r2:.4f} below threshold {self.training_config['min_r2']}")
        else:
            logger.info(f"✅ R² score {r2:.4f} passed QA threshold")
        
        return model, performance
    
    def _prepare_data(
        self,
        df: pd.DataFrame,
        target_name: str
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare data for training"""
        
        # Remove target and metadata columns
        exclude_cols = [
            target_name, '_extraction_timestamp', '_flow_id', '_version',
            'flow_id', 'timestamp', 'completion_timestamp'
        ]
        
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        X = df[feature_cols].copy()
        y = df[target_name].copy()
        
        # Handle categorical features
        for col in X.select_dtypes(include=['object', 'category']).columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Handle boolean targets for classification
        if target_name == 'is_successful':
            y = y.astype(int)
        
        return X, y
    
    def _analyze_feature_importance(
        self,
        model: Any,
        feature_names: List[str]
    ) -> Dict[str, float]:
        """Analyze feature importance (explainability - US standard)"""
        
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            
            feature_importance = dict(zip(
                feature_names,
                [float(imp) for imp in importances]
            ))
            
            # Sort by importance
            sorted_features = sorted(
                feature_importance.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            logger.info("\n📊 Top 10 Most Important Features:")
            for feature, importance in sorted_features[:10]:
                logger.info(f"   {feature}: {importance:.4f}")
            
            return feature_importance
        
        return {}
    
    def _find_latest_dataset(self) -> Optional[str]:
        """Find latest dataset in datasets directory"""
        dataset_dir = self.model_path / 'datasets'
        if not dataset_dir.exists():
            return None
        
        datasets = list(dataset_dir.glob('*.parquet'))
        if not datasets:
            datasets = list(dataset_dir.glob('*.csv'))
        
        return str(max(datasets, key=os.path.getctime)) if datasets else None
    
    def _generate_synthetic_dataset(self, size: int = 1000) -> str:
        """Generate synthetic dataset for demo/testing"""
        logger.info(f"Generating synthetic dataset with {size} samples")
        
        np.random.seed(42)
        
        data = {
            "flow_id": [f"flow_{i}" for i in range(size)],
            "cost": np.random.exponential(0.15, size),
            "files_changed": np.random.poisson(5, size),
            "code_churn": np.random.exponential(150, size),
            "lines_added": np.random.exponential(100, size),
            "lines_deleted": np.random.exponential(50, size),
            "commit_count": np.random.poisson(3, size),
            "test_files_changed": np.random.poisson(1, size),
            "hour_of_day": np.random.randint(0, 24, size),
            "day_of_week": np.random.randint(0, 7, size),
            "is_business_hours": np.random.choice([0, 1], size, p=[0.3, 0.7]),
            "avg_cost_last_5": np.random.exponential(0.15, size),
            "avg_deployment_time_last_5": np.random.exponential(35, size),
            "success_rate_last_5": np.random.beta(8, 2, size),
            "test_to_code_ratio": np.random.beta(2, 5, size),
            "estimated_complexity": np.random.normal(5, 2, size),
            "risk_score": np.random.beta(2, 5, size),
            "deployment_time": np.random.exponential(35, size),
            "validation_score": np.random.beta(8, 2, size)
        }
        
        # Generate target variable with realistic correlation
        success_prob = (
            0.5 +
            0.2 * (1 - data['risk_score']) +
            0.15 * data['test_to_code_ratio'] +
            0.15 * data['success_rate_last_5'] -
            0.1 * (data['cost'] > 0.2)
        )
        success_prob = np.clip(success_prob, 0.1, 0.95)
        data['is_successful'] = np.random.binomial(1, success_prob)
        
        df = pd.DataFrame(data)
        
        # Save dataset
        output_path = self.model_path / 'datasets' / 'synthetic_data.parquet'
        df.to_parquet(output_path, index=False)
        
        logger.info(f"💾 Synthetic dataset saved: {output_path}")
        
        return str(output_path)


def main():
    """CLI for model training"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ML Model Trainer')
    parser.add_argument('--model-path', default='.ml-models', help='Path for models')
    parser.add_argument('--dataset', default=None, help='Dataset path')
    parser.add_argument('--retrain', action='store_true', help='Retrain existing models')
    
    args = parser.parse_args()
    
    if not ML_AVAILABLE:
        logger.error("❌ ML libraries not available - install sklearn, pandas, numpy")
        sys.exit(1)
    
    trainer = ModelTrainer(model_path=args.model_path)
    
    results = trainer.train_all_models(
        dataset_path=args.dataset,
        retrain_existing=args.retrain
    )
    
    print("\n" + "="*60)
    print("🎓 TRAINING COMPLETE")
    print("="*60)
    print(f"Models trained: {len(results['models_trained'])}")
    print(f"Training time: {results['training_time_seconds']:.2f}s")
    print(f"Dataset size: {results['dataset_size']} samples")
    print("="*60)


if __name__ == '__main__':
    main()

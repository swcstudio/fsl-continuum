#!/usr/bin/env python3
"""
FSL Continuum - Predictor

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
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib

# Try importing ML libraries with fallbacks
try:
    import pandas as pd
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import (
        classification_report, mean_absolute_error, r2_score,
        precision_recall_fscore_support, roc_auc_score
    )
    import joblib
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("⚠️  ML libraries not available - running in limited mode")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ml-predictor')


class RiskLevel(Enum):
    """Risk categorization following global standards"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class PredictionConfidence(Enum):
    """Confidence levels (US MLOps standard)"""
    VERY_HIGH = 0.95
    HIGH = 0.85
    MEDIUM = 0.75
    LOW = 0.60
    VERY_LOW = 0.50


@dataclass
class FeatureStore:
    """
    Feast-inspired feature store (US standard)
    Lightweight implementation following Tecton architecture
    """
    name: str
    features: Dict[str, Any]
    timestamp: str
    version: str = "1.0"
    
    def get_features(self, feature_names: List[str]) -> Dict[str, Any]:
        """Retrieve features with <100ms latency (US standard)"""
        start_time = time.time()
        result = {name: self.features.get(name, 0) for name in feature_names}
        latency_ms = (time.time() - start_time) * 1000
        
        logger.info(f"Feature retrieval latency: {latency_ms:.2f}ms")
        
        if latency_ms > 100:
            logger.warning(f"⚠️  Feature retrieval exceeded 100ms target: {latency_ms:.2f}ms")
        
        return result
    
    def add_features(self, new_features: Dict[str, Any]):
        """Add features to store"""
        self.features.update(new_features)
        self.timestamp = datetime.now().isoformat()


@dataclass
class PredictionRequest:
    """Prediction request structure"""
    flow_id: str
    features: Dict[str, Any]
    request_id: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if not self.request_id:
            self.request_id = f"pred_{hashlib.sha256(self.flow_id.encode()).hexdigest()[:12]}"
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


@dataclass
class PredictionResponse:
    """Prediction response with full observability"""
    request_id: str
    flow_id: str
    predictions: Dict[str, Any]
    confidence: float
    risk_assessment: Dict[str, Any]
    latency_ms: float
    model_version: str
    timestamp: str
    recommendations: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MLPredictor:
    """
    Main ML Prediction Service
    
    Incorporates global best practices:
    - US: MLOps Level 2 automation, real-time serving
    - China: Cost-efficient inference (ByteDance Doubao style)
    - India: DevOps maturity, comprehensive monitoring (TCS standard)
    """
    
    def __init__(self, model_path: str = ".ml-models"):
        self.model_path = Path(model_path)
        self.models = {}
        self.feature_schemas = {}
        self.feature_store = None
        self.prediction_cache = {}
        self.metrics = {
            "predictions_made": 0,
            "cache_hits": 0,
            "average_latency_ms": 0,
            "accuracy_score": 0.0
        }
        
        # Initialize
        self._load_models()
        self._init_feature_store()
        
    def _load_models(self):
        """Load trained models from disk"""
        logger.info(f"Loading models from {self.model_path}")
        
        if not self.model_path.exists():
            logger.warning(f"Model path {self.model_path} does not exist")
            return
        
        # Load model metadata
        metadata_file = self.model_path / "model_metadata.json"
        if metadata_file.exists():
            with open(metadata_file) as f:
                metadata = json.load(f)
            
            # Load each model
            for target in metadata.get("targets_trained", []):
                model_file = self.model_path / f"{target}_model.pkl"
                feature_file = self.model_path / f"{target}_features.pkl"
                
                if model_file.exists() and feature_file.exists() and ML_AVAILABLE:
                    try:
                        self.models[target] = {
                            'model': joblib.load(model_file),
                            'features': joblib.load(feature_file),
                            'metadata': metadata['models'].get(target, {})
                        }
                        logger.info(f"✅ Loaded model: {target}")
                    except Exception as e:
                        logger.error(f"❌ Error loading model {target}: {e}")
        
        logger.info(f"Loaded {len(self.models)} models")
    
    def _init_feature_store(self):
        """Initialize feature store (Feast-inspired)"""
        self.feature_store = FeatureStore(
            name="flow_state_features",
            features={},
            timestamp=datetime.now().isoformat()
        )
        logger.info("✅ Feature store initialized")
    
    def predict(self, request: PredictionRequest) -> PredictionResponse:
        """
        Make predictions with <100ms latency target (US standard)
        Cost-efficient inference (China standard)
        Full observability (India standard)
        """
        start_time = time.time()
        
        # Check cache (Chinese efficiency optimization)
        cache_key = f"{request.flow_id}_{hashlib.sha256(str(request.features).encode()).hexdigest()[:8]}"
        if cache_key in self.prediction_cache:
            cached = self.prediction_cache[cache_key]
            # Return cached if < 5 minutes old
            if (time.time() - cached['timestamp']) < 300:
                self.metrics['cache_hits'] += 1
                logger.info("📦 Returning cached prediction")
                return cached['response']
        
        # Store features in feature store
        self.feature_store.add_features(request.features)
        
        # Make predictions
        predictions = {}
        confidences = {}
        
        for target, model_data in self.models.items():
            try:
                pred_result = self._predict_target(
                    target,
                    model_data,
                    request.features
                )
                predictions[target] = pred_result['prediction']
                confidences[target] = pred_result['confidence']
            except Exception as e:
                logger.error(f"Error predicting {target}: {e}")
                predictions[target] = {"error": str(e)}
                confidences[target] = 0.0
        
        # Calculate overall confidence
        overall_confidence = min(confidences.values()) if confidences else 0.5
        
        # Risk assessment (multi-factor analysis)
        risk_assessment = self._assess_risk(predictions, confidences)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            predictions,
            risk_assessment,
            overall_confidence
        )
        
        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000
        
        # Update metrics
        self.metrics['predictions_made'] += 1
        self.metrics['average_latency_ms'] = (
            (self.metrics['average_latency_ms'] * (self.metrics['predictions_made'] - 1) + latency_ms)
            / self.metrics['predictions_made']
        )
        
        # Create response
        response = PredictionResponse(
            request_id=request.request_id,
            flow_id=request.flow_id,
            predictions=predictions,
            confidence=overall_confidence,
            risk_assessment=risk_assessment,
            latency_ms=latency_ms,
            model_version="1.0",
            timestamp=datetime.now().isoformat(),
            recommendations=recommendations
        )
        
        # Cache response (Chinese efficiency)
        self.prediction_cache[cache_key] = {
            'response': response,
            'timestamp': time.time()
        }
        
        # Log performance (Indian observability standard)
        self._log_prediction_metrics(response)
        
        return response
    
    def _predict_target(
        self,
        target: str,
        model_data: Dict[str, Any],
        features: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Make prediction for specific target"""
        model = model_data['model']
        required_features = model_data['features']
        
        # Prepare input (feature engineering)
        X_input = pd.DataFrame([{
            feat: features.get(feat, 0) for feat in required_features
        }])
        
        # Make prediction
        if target == 'is_successful':
            # Classification
            pred_proba = model.predict_proba(X_input)[0]
            prediction = bool(model.predict(X_input)[0])
            confidence = float(max(pred_proba))
            
            return {
                'prediction': {
                    'value': prediction,
                    'probability': {
                        'success': float(pred_proba[1]),
                        'failure': float(pred_proba[0])
                    }
                },
                'confidence': confidence
            }
        else:
            # Regression
            prediction = float(model.predict(X_input)[0])
            confidence = self._estimate_regression_confidence(model, X_input)
            
            return {
                'prediction': {
                    'value': prediction,
                    'unit': self._get_unit(target)
                },
                'confidence': confidence
            }
    
    def _estimate_regression_confidence(self, model, X_input) -> float:
        """Estimate confidence for regression predictions"""
        if hasattr(model, 'estimators_'):
            # Ensemble model - use variance
            predictions = [
                float(estimator.predict(X_input)[0])
                for estimator in model.estimators_
            ]
            variance = np.var(predictions)
            # Convert variance to confidence (inverse relationship)
            confidence = 1.0 / (1.0 + variance)
            return max(0.1, min(0.95, confidence))
        return 0.75  # Default confidence
    
    def _assess_risk(
        self,
        predictions: Dict[str, Any],
        confidences: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Multi-factor risk assessment
        Follows NIST AI Risk Management Framework
        """
        risk_score = 0.0
        risk_factors = []
        
        # Factor 1: Low confidence predictions
        avg_confidence = sum(confidences.values()) / len(confidences) if confidences else 0.5
        if avg_confidence < 0.75:
            confidence_risk = (0.75 - avg_confidence) * 0.5
            risk_score += confidence_risk
            risk_factors.append({
                'factor': 'low_confidence',
                'score': confidence_risk,
                'description': f'Average confidence {avg_confidence:.2%} below threshold'
            })
        
        # Factor 2: Deployment success probability
        if 'is_successful' in predictions:
            success_pred = predictions['is_successful']
            if 'prediction' in success_pred and isinstance(success_pred['prediction'], dict):
                prob_failure = success_pred['prediction'].get('probability', {}).get('failure', 0.5)
                if prob_failure > 0.3:
                    failure_risk = prob_failure * 0.4
                    risk_score += failure_risk
                    risk_factors.append({
                        'factor': 'high_failure_probability',
                        'score': failure_risk,
                        'description': f'Failure probability: {prob_failure:.2%}'
                    })
        
        # Factor 3: Cost predictions
        if 'cost' in predictions:
            cost_pred = predictions['cost']
            if 'prediction' in cost_pred and isinstance(cost_pred['prediction'], dict):
                predicted_cost = cost_pred['prediction'].get('value', 0.1)
                if predicted_cost > 0.25:
                    cost_risk = min(0.3, (predicted_cost - 0.25) * 2)
                    risk_score += cost_risk
                    risk_factors.append({
                        'factor': 'high_cost',
                        'score': cost_risk,
                        'description': f'Predicted cost ${predicted_cost:.3f} above threshold'
                    })
        
        # Factor 4: Deployment time
        if 'deployment_time' in predictions:
            deploy_pred = predictions['deployment_time']
            if 'prediction' in deploy_pred and isinstance(deploy_pred['prediction'], dict):
                predicted_time = deploy_pred['prediction'].get('value', 30)
                if predicted_time > 60:
                    time_risk = min(0.2, (predicted_time - 60) / 300)
                    risk_score += time_risk
                    risk_factors.append({
                        'factor': 'long_deployment_time',
                        'score': time_risk,
                        'description': f'Predicted deployment time: {predicted_time:.1f}s'
                    })
        
        # Normalize risk score
        risk_score = min(1.0, risk_score)
        
        # Categorize risk
        if risk_score >= 0.75:
            risk_level = RiskLevel.CRITICAL
        elif risk_score >= 0.5:
            risk_level = RiskLevel.HIGH
        elif risk_score >= 0.3:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        return {
            'overall_score': risk_score,
            'level': risk_level.value,
            'factors': risk_factors,
            'threshold_exceeded': risk_score >= 0.5
        }
    
    def _generate_recommendations(
        self,
        predictions: Dict[str, Any],
        risk_assessment: Dict[str, Any],
        confidence: float
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # High risk recommendations
        if risk_assessment['level'] in ['HIGH', 'CRITICAL']:
            recommendations.append("🔴 Manual review required before proceeding")
            recommendations.append("Consider additional testing and validation")
        
        # Low confidence recommendations
        if confidence < 0.75:
            recommendations.append(f"⚠️  Low prediction confidence ({confidence:.2%})")
            recommendations.append("Collect more historical data to improve model accuracy")
        
        # Success probability recommendations
        if 'is_successful' in predictions:
            success_pred = predictions['is_successful']
            if 'prediction' in success_pred and isinstance(success_pred['prediction'], dict):
                prob_success = success_pred['prediction'].get('probability', {}).get('success', 0.5)
                if prob_success < 0.7:
                    recommendations.append("Review code quality metrics and test coverage")
                    recommendations.append("Consider running additional validation tests")
        
        # Cost optimization recommendations
        if 'cost' in predictions:
            cost_pred = predictions['cost']
            if 'prediction' in cost_pred and isinstance(cost_pred['prediction'], dict):
                predicted_cost = cost_pred['prediction'].get('value', 0.1)
                if predicted_cost > 0.20:
                    savings = predicted_cost * 0.3
                    recommendations.append(
                        f"💰 Optimize resources to save ~${savings:.3f} per execution"
                    )
                    recommendations.append("Consider using more efficient runners or caching")
        
        # Default positive recommendation
        if not recommendations:
            recommendations.append("✅ All predictions within acceptable ranges")
            recommendations.append("Proceed with deployment - conditions favorable")
        
        return recommendations
    
    def _get_unit(self, target: str) -> str:
        """Get unit for target metric"""
        units = {
            'cost': 'USD',
            'deployment_time': 'seconds',
            'validation_score': 'score',
            'resource_utilization': 'percent'
        }
        return units.get(target, 'value')
    
    def _log_prediction_metrics(self, response: PredictionResponse):
        """Log comprehensive metrics (Indian DevOps observability standard)"""
        logger.info(f"Prediction ID: {response.request_id}")
        logger.info(f"Latency: {response.latency_ms:.2f}ms")
        logger.info(f"Confidence: {response.confidence:.2%}")
        logger.info(f"Risk Level: {response.risk_assessment['level']}")
        
        # Performance check (US standard: <100ms)
        if response.latency_ms > 100:
            logger.warning(f"⚠️  Latency exceeded target: {response.latency_ms:.2f}ms > 100ms")
        else:
            logger.info(f"✅ Latency within target: {response.latency_ms:.2f}ms < 100ms")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get service metrics for monitoring"""
        return {
            **self.metrics,
            'models_loaded': len(self.models),
            'cache_size': len(self.prediction_cache),
            'cache_hit_rate': (
                self.metrics['cache_hits'] / self.metrics['predictions_made']
                if self.metrics['predictions_made'] > 0 else 0
            )
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Service health check"""
        return {
            'status': 'healthy' if len(self.models) > 0 else 'unhealthy',
            'models_loaded': len(self.models),
            'feature_store_active': self.feature_store is not None,
            'average_latency_ms': self.metrics['average_latency_ms'],
            'timestamp': datetime.now().isoformat()
        }


def main():
    """CLI interface for ML predictor service"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Flow State Loop ML Predictor')
    parser.add_argument('--model-path', default='.ml-models', help='Path to models')
    parser.add_argument('--flow-id', required=True, help='Flow State Loop ID')
    parser.add_argument('--features', required=True, help='Features JSON file or string')
    parser.add_argument('--output', default=None, help='Output file for predictions')
    
    args = parser.parse_args()
    
    # Initialize predictor
    predictor = MLPredictor(model_path=args.model_path)
    
    # Load features
    if os.path.exists(args.features):
        with open(args.features) as f:
            features = json.load(f)
    else:
        features = json.loads(args.features)
    
    # Create request
    request = PredictionRequest(
        flow_id=args.flow_id,
        features=features
    )
    
    # Make prediction
    logger.info(f"Making prediction for flow: {args.flow_id}")
    response = predictor.predict(request)
    
    # Output results
    result = response.to_dict()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        logger.info(f"Results saved to {args.output}")
    else:
        print(json.dumps(result, indent=2))
    
    # Print summary
    print("\n" + "="*60)
    print("🔮 PREDICTION SUMMARY")
    print("="*60)
    print(f"Flow ID: {response.flow_id}")
    print(f"Risk Level: {response.risk_assessment['level']}")
    print(f"Confidence: {response.confidence:.2%}")
    print(f"Latency: {response.latency_ms:.2f}ms")
    print("\n📋 Recommendations:")
    for rec in response.recommendations:
        print(f"  • {rec}")
    print("="*60)


if __name__ == '__main__':
    main()

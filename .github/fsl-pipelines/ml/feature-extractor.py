#!/usr/bin/env python3
"""
FSL Continuum - Feature Extractor

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
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('feature-extractor')


class FeatureType(Enum):
    """Feature type classification"""
    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    TEMPORAL = "temporal"
    DERIVED = "derived"
    AGGREGATED = "aggregated"


@dataclass
class FeatureDefinition:
    """Feature definition following Feast schema"""
    name: str
    feature_type: FeatureType
    description: str
    source: str
    computation: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'type': self.feature_type.value,
            'description': self.description,
            'source': self.source,
            'computation': self.computation,
            'dependencies': self.dependencies,
            'version': self.version
        }


class FeatureExtractor:
    """
    Feature extraction engine following global best practices
    
    Inspiration:
    - US: Feast feature store architecture
    - China: Alibaba feature platform efficiency
    - India: TCS comprehensive data engineering
    """
    
    def __init__(self, flow_state_dir: str = ".flow-state"):
        self.flow_state_dir = Path(flow_state_dir)
        self.feature_definitions = self._init_feature_definitions()
        self.feature_cache = {}
        self.extraction_metrics = {
            'features_extracted': 0,
            'cache_hits': 0,
            'average_extraction_time_ms': 0
        }
    
    def _init_feature_definitions(self) -> Dict[str, FeatureDefinition]:
        """Initialize feature definitions (Feast-style registry)"""
        definitions = {
            # Code complexity features
            'code_churn': FeatureDefinition(
                name='code_churn',
                feature_type=FeatureType.NUMERIC,
                description='Total lines of code changed',
                source='git_metadata',
                computation='lines_added + lines_deleted'
            ),
            'files_changed': FeatureDefinition(
                name='files_changed',
                feature_type=FeatureType.NUMERIC,
                description='Number of files modified',
                source='git_metadata'
            ),
            'avg_file_size_change': FeatureDefinition(
                name='avg_file_size_change',
                feature_type=FeatureType.NUMERIC,
                description='Average size change per file',
                source='git_metadata',
                computation='code_churn / files_changed',
                dependencies=['code_churn', 'files_changed']
            ),
            
            # Commit features
            'commit_count': FeatureDefinition(
                name='commit_count',
                feature_type=FeatureType.NUMERIC,
                description='Number of commits in PR',
                source='git_log'
            ),
            'commit_message_length_avg': FeatureDefinition(
                name='commit_message_length_avg',
                feature_type=FeatureType.NUMERIC,
                description='Average commit message length',
                source='git_log'
            ),
            
            # Author features
            'author_experience_score': FeatureDefinition(
                name='author_experience_score',
                feature_type=FeatureType.NUMERIC,
                description='Author experience based on historical commits',
                source='git_log_historical'
            ),
            'author_success_rate': FeatureDefinition(
                name='author_success_rate',
                feature_type=FeatureType.NUMERIC,
                description='Historical success rate of author commits',
                source='flow_state_history'
            ),
            
            # Temporal features
            'hour_of_day': FeatureDefinition(
                name='hour_of_day',
                feature_type=FeatureType.TEMPORAL,
                description='Hour when commit was made (0-23)',
                source='timestamp'
            ),
            'day_of_week': FeatureDefinition(
                name='day_of_week',
                feature_type=FeatureType.TEMPORAL,
                description='Day of week (0=Monday, 6=Sunday)',
                source='timestamp'
            ),
            'is_business_hours': FeatureDefinition(
                name='is_business_hours',
                feature_type=FeatureType.CATEGORICAL,
                description='Whether commit was during business hours',
                source='timestamp',
                computation='9 <= hour_of_day <= 17 and day_of_week < 5'
            ),
            
            # Branch features
            'branch_age_days': FeatureDefinition(
                name='branch_age_days',
                feature_type=FeatureType.NUMERIC,
                description='Age of branch in days',
                source='git_branch_info'
            ),
            'commits_behind_main': FeatureDefinition(
                name='commits_behind_main',
                feature_type=FeatureType.NUMERIC,
                description='Number of commits branch is behind main',
                source='git_branch_info'
            ),
            
            # Test features
            'test_files_changed': FeatureDefinition(
                name='test_files_changed',
                feature_type=FeatureType.NUMERIC,
                description='Number of test files modified',
                source='git_metadata'
            ),
            'test_to_code_ratio': FeatureDefinition(
                name='test_to_code_ratio',
                feature_type=FeatureType.NUMERIC,
                description='Ratio of test files to code files changed',
                source='git_metadata',
                computation='test_files_changed / files_changed',
                dependencies=['test_files_changed', 'files_changed']
            ),
            
            # Historical features (from EXPChain)
            'previous_deployment_success': FeatureDefinition(
                name='previous_deployment_success',
                feature_type=FeatureType.CATEGORICAL,
                description='Success of previous deployment by same author',
                source='flow_state_history'
            ),
            'avg_cost_last_5': FeatureDefinition(
                name='avg_cost_last_5',
                feature_type=FeatureType.AGGREGATED,
                description='Average cost of last 5 deployments',
                source='flow_state_history'
            ),
            'avg_deployment_time_last_5': FeatureDefinition(
                name='avg_deployment_time_last_5',
                feature_type=FeatureType.AGGREGATED,
                description='Average deployment time of last 5 deployments',
                source='flow_state_history'
            ),
            
            # Quality features
            'estimated_complexity': FeatureDefinition(
                name='estimated_complexity',
                feature_type=FeatureType.NUMERIC,
                description='Estimated code complexity score',
                source='static_analysis'
            ),
            'security_risk_score': FeatureDefinition(
                name='security_risk_score',
                feature_type=FeatureType.NUMERIC,
                description='Security risk score from static analysis',
                source='security_scan'
            ),
        }
        
        return definitions
    
    def extract_features(
        self,
        flow_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Extract all features for a flow
        Target: <50ms extraction time (Tecton standard)
        """
        start_time = time.time()
        
        # Check cache (ByteDance efficiency)
        cache_key = self._get_cache_key(flow_id, context)
        if cache_key in self.feature_cache:
            cached = self.feature_cache[cache_key]
            if (time.time() - cached['timestamp']) < 300:  # 5 minute TTL
                self.extraction_metrics['cache_hits'] += 1
                logger.info(f"📦 Cache hit for {flow_id}")
                return cached['features']
        
        features = {}
        
        # Extract each feature type
        try:
            # Git metadata features
            git_features = self._extract_git_features(flow_id, context)
            features.update(git_features)
            
            # Temporal features
            temporal_features = self._extract_temporal_features()
            features.update(temporal_features)
            
            # Historical features from Flow State
            historical_features = self._extract_historical_features(flow_id, context)
            features.update(historical_features)
            
            # Derived features (computed from other features)
            derived_features = self._compute_derived_features(features)
            features.update(derived_features)
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            features = self._get_default_features()
        
        # Add metadata
        features['_extraction_timestamp'] = datetime.now().isoformat()
        features['_flow_id'] = flow_id
        features['_version'] = '1.0'
        
        # Cache features
        self.feature_cache[cache_key] = {
            'features': features,
            'timestamp': time.time()
        }
        
        # Update metrics
        extraction_time_ms = (time.time() - start_time) * 1000
        self.extraction_metrics['features_extracted'] += 1
        self.extraction_metrics['average_extraction_time_ms'] = (
            (self.extraction_metrics['average_extraction_time_ms'] * 
             (self.extraction_metrics['features_extracted'] - 1) + extraction_time_ms)
            / self.extraction_metrics['features_extracted']
        )
        
        logger.info(f"✅ Extracted {len(features)} features in {extraction_time_ms:.2f}ms")
        
        if extraction_time_ms > 50:
            logger.warning(f"⚠️  Feature extraction exceeded 50ms target: {extraction_time_ms:.2f}ms")
        
        return features
    
    def _extract_git_features(
        self,
        flow_id: str,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Extract features from Git metadata"""
        features = {}
        
        try:
            # Get commit information
            result = subprocess.run(
                ['git', 'log', '--oneline', '-1', '--stat'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                
                # Count files changed
                files_changed = len([l for l in lines if '|' in l])
                features['files_changed'] = float(files_changed)
                
                # Parse insertions/deletions
                for line in lines:
                    if 'insertion' in line or 'deletion' in line:
                        parts = line.split(',')
                        insertions = deletions = 0
                        
                        for part in parts:
                            if 'insertion' in part:
                                insertions = int(''.join(filter(str.isdigit, part)))
                            elif 'deletion' in part:
                                deletions = int(''.join(filter(str.isdigit, part)))
                        
                        features['code_churn'] = float(insertions + deletions)
                        features['lines_added'] = float(insertions)
                        features['lines_deleted'] = float(deletions)
                
                # Get commit count
                result = subprocess.run(
                    ['git', 'rev-list', '--count', 'HEAD'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    features['commit_count'] = float(result.stdout.strip())
            
            # Get test file count
            test_patterns = ['*test*.py', '*_test.py', 'test_*.py', '*.test.js', '*.spec.js']
            test_files = 0
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD~1'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                changed_files = result.stdout.split('\n')
                for file in changed_files:
                    if any(p.replace('*', '') in file.lower() for p in test_patterns):
                        test_files += 1
            
            features['test_files_changed'] = float(test_files)
            
        except Exception as e:
            logger.warning(f"Could not extract git features: {e}")
            features = {
                'files_changed': 5.0,
                'code_churn': 150.0,
                'lines_added': 100.0,
                'lines_deleted': 50.0,
                'commit_count': 3.0,
                'test_files_changed': 1.0
            }
        
        return features
    
    def _extract_temporal_features(self) -> Dict[str, float]:
        """Extract time-based features"""
        now = datetime.now()
        
        return {
            'hour_of_day': float(now.hour),
            'day_of_week': float(now.weekday()),
            'is_business_hours': float(9 <= now.hour <= 17 and now.weekday() < 5),
            'is_weekend': float(now.weekday() >= 5)
        }
    
    def _extract_historical_features(
        self,
        flow_id: str,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Extract features from historical Flow State data"""
        features = {}
        
        try:
            # Look for historical completions
            completion_dir = self.flow_state_dir / 'completion'
            if completion_dir.exists():
                completions = []
                for file in sorted(completion_dir.glob('*.json'))[-5:]:  # Last 5
                    try:
                        with open(file) as f:
                            completions.append(json.load(f))
                    except:
                        continue
                
                if completions:
                    # Calculate aggregated features
                    costs = [c.get('cost', 0.1) for c in completions]
                    times = [c.get('deployment_time', 30) for c in completions if 'deployment_time' in c]
                    successes = [c.get('status') == 'completed' for c in completions]
                    
                    features['avg_cost_last_5'] = sum(costs) / len(costs)
                    features['avg_deployment_time_last_5'] = sum(times) / len(times) if times else 30.0
                    features['success_rate_last_5'] = sum(successes) / len(successes)
                    features['previous_deployment_success'] = float(successes[-1]) if successes else 0.5
        
        except Exception as e:
            logger.warning(f"Could not extract historical features: {e}")
        
        # Default values if not found
        features.setdefault('avg_cost_last_5', 0.15)
        features.setdefault('avg_deployment_time_last_5', 35.0)
        features.setdefault('success_rate_last_5', 0.85)
        features.setdefault('previous_deployment_success', 0.85)
        
        return features
    
    def _compute_derived_features(self, features: Dict[str, float]) -> Dict[str, float]:
        """Compute derived features from base features"""
        derived = {}
        
        # Avoid division by zero
        def safe_divide(a: float, b: float, default: float = 0.0) -> float:
            return a / b if b != 0 else default
        
        # Test to code ratio
        if 'test_files_changed' in features and 'files_changed' in features:
            derived['test_to_code_ratio'] = safe_divide(
                features['test_files_changed'],
                features['files_changed'],
                0.0
            )
        
        # Average file size change
        if 'code_churn' in features and 'files_changed' in features:
            derived['avg_file_size_change'] = safe_divide(
                features['code_churn'],
                features['files_changed'],
                50.0
            )
        
        # Complexity score (heuristic)
        if 'code_churn' in features and 'files_changed' in features:
            code_churn = features['code_churn']
            files_changed = features['files_changed']
            complexity = (code_churn / 100) + (files_changed / 5)
            derived['estimated_complexity'] = min(10.0, max(1.0, complexity))
        
        # Risk score (heuristic)
        risk_score = 0.5  # Base risk
        if features.get('test_to_code_ratio', 0) < 0.3:
            risk_score += 0.2  # Low test coverage
        if features.get('is_business_hours', 1) == 0:
            risk_score += 0.1  # Off-hours deployment
        if features.get('success_rate_last_5', 1.0) < 0.8:
            risk_score += 0.2  # Poor historical success
        
        derived['risk_score'] = min(1.0, risk_score)
        
        return derived
    
    def _get_default_features(self) -> Dict[str, float]:
        """Get default feature values for fallback"""
        return {
            'files_changed': 5.0,
            'code_churn': 150.0,
            'lines_added': 100.0,
            'lines_deleted': 50.0,
            'commit_count': 3.0,
            'test_files_changed': 1.0,
            'hour_of_day': 14.0,
            'day_of_week': 2.0,
            'is_business_hours': 1.0,
            'avg_cost_last_5': 0.15,
            'avg_deployment_time_last_5': 35.0,
            'success_rate_last_5': 0.85,
            'test_to_code_ratio': 0.2,
            'estimated_complexity': 5.0,
            'risk_score': 0.5
        }
    
    def _get_cache_key(self, flow_id: str, context: Optional[Dict[str, Any]]) -> str:
        """Generate cache key"""
        ctx_str = json.dumps(context, sort_keys=True) if context else ""
        return hashlib.sha256(f"{flow_id}:{ctx_str}".encode()).hexdigest()[:16]
    
    def get_feature_schema(self) -> Dict[str, Any]:
        """Get feature schema for documentation"""
        return {
            'features': {
                name: definition.to_dict()
                for name, definition in self.feature_definitions.items()
            },
            'total_features': len(self.feature_definitions),
            'version': '1.0'
        }
    
    def save_features_to_store(
        self,
        flow_id: str,
        features: Dict[str, Any],
        output_path: Optional[str] = None
    ):
        """Save features to persistent store (Feast-style)"""
        if not output_path:
            output_path = self.flow_state_dir / 'features' / f"{flow_id}_features.json"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        feature_record = {
            'flow_id': flow_id,
            'features': features,
            'timestamp': datetime.now().isoformat(),
            'schema_version': '1.0'
        }
        
        with open(output_path, 'w') as f:
            json.dump(feature_record, f, indent=2)
        
        logger.info(f"💾 Features saved to {output_path}")


def main():
    """CLI for feature extraction"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Feature Extractor')
    parser.add_argument('--flow-id', required=True, help='Flow State Loop ID')
    parser.add_argument('--context', default=None, help='Context JSON file')
    parser.add_argument('--output', default=None, help='Output file for features')
    parser.add_argument('--schema', action='store_true', help='Print feature schema')
    
    args = parser.parse_args()
    
    extractor = FeatureExtractor()
    
    if args.schema:
        schema = extractor.get_feature_schema()
        print(json.dumps(schema, indent=2))
        return
    
    # Load context if provided
    context = None
    if args.context and os.path.exists(args.context):
        with open(args.context) as f:
            context = json.load(f)
    
    # Extract features
    features = extractor.extract_features(args.flow_id, context)
    
    # Save or print
    if args.output:
        extractor.save_features_to_store(args.flow_id, features, args.output)
    else:
        print(json.dumps(features, indent=2))
    
    logger.info(f"✅ Extracted {len(features)} features for {args.flow_id}")


if __name__ == '__main__':
    main()

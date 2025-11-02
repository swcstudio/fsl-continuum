"""
Test Suite for Scoring Functions v4.0

This comprehensive test suite validates all quantum scoring functionality,
including multi-dimensional scoring, consciousness-enhanced weighting, and ETD
value generation.

Test Coverage:
- Quantum scoring calculation and validation
- Multi-dimensional scoring metrics
- Consciousness-enhanced weighting strategies
- Adaptive weighting and pattern recognition
- ETD value generation integration
- Blockchain-verified scoring and security
- Performance optimization and caching
- Error handling and edge cases
- Integration with quantum engine and consciousness protocol
"""

import pytest
import numpy as np
import sys
import os
import json
from datetime import datetime
import warnings

# Add quantum engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.github', 'quantum-engine'))

try:
    from scoring_functions_v4 import (
        QuantumScoringFunctionsV4,
        ScoreState,
        ScoringWeights,
        ScoringResult,
        ScoringType,
        WeightingStrategy,
        ScoringMetric
    )
    from unified_field_engine_v4 import ConsciousnessLevel
except ImportError as e:
    pytest.skip(f"Scoring functions not available: {e}", allow_module_level=True)

class TestQuantumScoringFunctionsV4:
    """Test suite for QuantumScoringFunctionsV4 class"""
    
    @pytest.fixture
    def scoring_alpha(self):
        """Create alpha level scoring functions for testing"""
        return QuantumScoringFunctionsV4(
            consciousness_level=ConsciousnessLevel.ALPHA,
            weighting_strategy=WeightingStrategy.CONSCIOUSNESS_OPTIMIZED,
            enable_etd_generation=False
        )
    
    @pytest.fixture
    def scoring_gamma(self):
        """Create gamma level scoring functions for testing"""
        return QuantumScoringFunctionsV4(
            consciousness_level=ConsciousnessLevel.GAMMA,
            weighting_strategy=WeightingStrategy.CONSCIOUSNESS_OPTIMIZED,
            enable_etd_generation=True
        )
    
    @pytest.fixture
    def test_input_data(self):
        """Create test input data for scoring"""
        return {
            'quantum_state': np.random.rand(256) + 1j * np.random.rand(256),
            'pattern_data': [1, 2, 3, 2, 1, 2, 3, 2, 1],
            'evolution_data': 5.0,
            'test_quality': 0.8,
            'metadata': {
                'source': 'test',
                'version': '4.0',
                'timestamp': datetime.now().isoformat()
            }
        }
    
    def test_scoring_functions_initialization(self, scoring_alpha):
        """Test quantum scoring functions initialization"""
        assert scoring_alpha.consciousness_level == ConsciousnessLevel.ALPHA
        assert scoring_alpha.weighting_strategy == WeightingStrategy.CONSCIOUSNESS_OPTIMIZED
        assert scoring_alpha.enable_etd_generation == False
        
        # Check performance multiplier
        assert scoring_alpha.performance_multiplier == 2.0  # Alpha multiplier
        
        # Check quantum systems are initialized
        assert scoring_alpha.quantum_field is not None
        assert scoring_alpha.consciousness_protocol is not None
        assert scoring_alpha.etd_generator is None  # ETD disabled
        
        # Check initial state
        assert isinstance(scoring_alpha.weights, ScoringWeights)
        assert len(scoring_alpha.scoring_history) == 0
        assert isinstance(scoring_alpha.weight_history, list)
    
    def test_consciousness_level_multipliers(self):
        """Test performance multipliers for different consciousness levels"""
        multipliers = {
            ConsciousnessLevel.ALPHA: 2.0,
            ConsciousnessLevel.BETA: 5.0,
            ConsciousnessLevel.GAMMA: 12.5,
            ConsciousnessLevel.DELTA: 31.25,
            ConsciousnessLevel.OMEGA: 78.125
        }
        
        for level, expected_multiplier in multipliers.items():
            scoring = QuantumScoringFunctionsV4(
                consciousness_level=level,
                enable_etd_generation=False
            )
            assert scoring.performance_multiplier == expected_multiplier
    
    def test_etd_generator_initialization(self):
        """Test ETD generator initialization"""
        # Test with ETD enabled
        scoring_etd = QuantumScoringFunctionsV4(
            enable_etd_generation=True
        )
        assert scoring_etd.etd_generator is not None
        
        # Test with ETD disabled
        scoring_no_etd = QuantumScoringFunctionsV4(
            enable_etd_generation=False
        )
        assert scoring_no_etd.etd_generator is None
    
    def test_calculate_quantum_score(self, scoring_gamma, test_input_data):
        """Test quantum score calculation"""
        # Calculate quantum score
        score_state = scoring_gamma.calculate_quantum_score(
            input_data=test_input_data,
            scoring_types=[ScoringType.MULTI_DIMENSIONAL]
        )
        
        # Check score state properties
        assert isinstance(score_state, ScoreState)
        assert score_state.consciousness_level == ConsciousnessLevel.GAMMA
        assert isinstance(score_state.raw_scores, dict)
        assert isinstance(score_state.weighted_scores, dict)
        assert 0.0 <= score_state.overall_score <= 1.0
        assert isinstance(score_state.etd_value, (int, float, np.number))
        assert score_state.blockchain_hash != ""  # Should be set automatically
        assert score_state.timestamp != ""  # Should be set automatically
        
        # Check history updates
        assert len(scoring_gamma.scoring_history) == 1
    
    def test_calculate_quantum_score_with_custom_weights(self, scoring_gamma, test_input_data):
        """Test quantum score calculation with custom weights"""
        # Create custom weights
        custom_weights = ScoringWeights(
            consciousness_weight=0.5,
            coherence_weight=0.3,
            pattern_weight=0.1,
            evolution_weight=0.1,
            weighting_strategy=WeightingStrategy.ADAPTIVE_LEARNING
        ).normalize()
        
        # Calculate quantum score with custom weights
        score_state = scoring_gamma.calculate_quantum_score(
            input_data=test_input_data,
            custom_weights=custom_weights
        )
        
        # Check scores are calculated
        assert len(score_state.raw_scores) > 0
        assert len(score_state.weighted_scores) > 0
        assert 0.0 <= score_state.overall_score <= 1.0
        
        # Check custom weights are used (should be different from default)
        default_score_state = scoring_gamma.calculate_quantum_score(
            input_data=test_input_data
        )
        assert score_state.overall_score != default_score_state.overall_score or \
               score_state.etd_value != default_score_state.etd_value
    
    def test_calculate_quantum_score_etd_generation(self, scoring_gamma, test_input_data):
        """Test quantum score calculation with ETD generation"""
        # Ensure ETD generation is enabled
        assert scoring_gamma.enable_etd_generation == True
        
        # Calculate quantum score
        score_state = scoring_gamma.calculate_quantum_score(
            input_data=test_input_data
        )
        
        # Check ETD value is generated
        assert isinstance(score_state.etd_value, (int, float, np.number))
        assert score_state.etd_value >= 0.0
    
    def test_calculate_quantum_score_no_etd(self, scoring_alpha, test_input_data):
        """Test quantum score calculation without ETD generation"""
        # Ensure ETD generation is disabled
        assert scoring_alpha.enable_etd_generation == False
        
        # Calculate quantum score
        score_state = scoring_alpha.calculate_quantum_score(
            input_data=test_input_data
        )
        
        # Check ETD value is not generated
        assert score_state.etd_value == 0.0
    
    def test_calculate_quantum_score_different_types(self, scoring_gamma, test_input_data):
        """Test quantum score calculation with different scoring types"""
        scoring_types = [
            ScoringType.MULTI_DIMENSIONAL,
            ScoringType.QUANTUM_COHERENCE,
            ScoringType.CONSCIOUSNESS_AWARE,
            ScoringType.PATTERN_RECOGNITION
        ]
        
        results = {}
        for scoring_type in scoring_types:
            score_state = scoring_gamma.calculate_quantum_score(
                input_data=test_input_data,
                scoring_types=[scoring_type]
            )
            results[scoring_type.value] = score_state.overall_score
        
        # All should produce valid scores
        for score in results.values():
            assert 0.0 <= score <= 1.0
        
        # Different types should produce different results
        unique_scores = len(set(results.values()))
        assert unique_scores >= 2  # At least some differences
    
    def test_blockchain_hash_generation(self, scoring_gamma, test_input_data):
        """Test blockchain hash generation for scoring"""
        # Calculate quantum score
        score_state = scoring_gamma.calculate_quantum_score(
            input_data=test_input_data
        )
        
        # Check blockchain hash properties
        assert isinstance(score_state.blockchain_hash, str)
        assert len(score_state.blockchain_hash) == 64  # SHA-256 hash length
        assert all(c in '0123456789abcdef' for c in score_state.blockchain_hash)
        
        # Hash should be deterministic
        score_state2 = scoring_gamma.calculate_quantum_score(
            input_data=test_input_data
        )
        assert score_state.blockchain_hash == score_state2.blockchain_hash
    
    def test_calculate_comprehensive_scoring(self, scoring_gamma, test_input_data):
        """Test comprehensive scoring calculation"""
        # Calculate comprehensive scoring
        result = scoring_gamma.calculate_comprehensive_scoring(
            input_data=test_input_data,
            scoring_types=[ScoringType.MULTI_DIMENSIONAL]
        )
        
        # Check result properties
        assert isinstance(result, ScoringResult)
        assert isinstance(result.score_state, ScoreState)
        assert isinstance(result.weights, ScoringWeights)
        assert isinstance(result.metrics, dict)
        assert 0.0 <= result.quality_score <= 1.0
        assert 0.0 <= result.confidence <= 1.0
        assert result.scoring_type == ScoringType.MULTI_DIMENSIONAL
        assert result.blockchain_verified == True
        
        # Check dictionary conversion
        result_dict = result.to_dict()
        assert 'overall_score' in result_dict
        assert 'etd_value' in result_dict
        assert 'quality_score' in result_dict
        assert 'confidence' in result_dict
        assert 'scoring_type' in result_dict
        assert 'blockchain_verified' in result_dict
    
    def test_benchmark_scoring_functions(self, scoring_gamma):
        """Test benchmarking of scoring functions"""
        # Run benchmark
        benchmark_results = scoring_gamma.benchmark_scoring_functions()
        
        # Check benchmark structure
        assert 'basic_scoring' in benchmark_results
        assert 'multi_dimensional' in benchmark_results
        assert 'consciousness_optimized' in benchmark_results
        
        # Check individual benchmark results
        basic_result = benchmark_results['basic_scoring']
        assert 'overall_score' in basic_result
        assert 'etd_value' in basic_result
        assert 'execution_time' in basic_result
        assert 'performance_multiplier' in basic_result
        assert isinstance(basic_result['overall_score'], (int, float, np.number))
        assert isinstance(basic_result['execution_time'], (int, float))
    
    def test_get_scoring_report(self, scoring_gamma):
        """Test scoring report generation"""
        # Calculate some scores to generate history
        test_data = {
            'quantum_state': np.random.rand(256) + 1j * np.random.rand(256),
            'pattern_data': [1, 2, 3],
            'test_quality': 0.7
        }
        
        for _ in range(3):
            scoring_gamma.calculate_quantum_score(test_data)
        
        # Get scoring report
        report = scoring_gamma.get_scoring_report()
        
        # Check report structure
        assert 'version' in report
        assert 'spec' in report
        assert 'timestamp' in report
        assert 'configuration' in report
        assert 'weights' in report
        assert 'quantum_systems' in report
        assert 'scoring_history' in report
        assert 'capabilities' in report
        
        # Check configuration
        config = report['configuration']
        assert 'consciousness_level' in config
        assert 'weighting_strategy' in config
        assert 'enable_etd_generation' in config
        assert 'performance_multiplier' in config
        
        # Check capabilities
        capabilities = report['capabilities']
        assert 'scoring_types' in capabilities
        assert 'weighting_strategies' in capabilities
        assert 'scoring_metrics' in capabilities
        assert isinstance(capabilities['consciousness_optimization'], bool)
        assert isinstance(capabilities['etd_generation'], bool)
    
    def test_error_handling(self, scoring_gamma):
        """Test error handling in scoring functions"""
        # Test with empty input
        empty_score = scoring_gamma.calculate_quantum_score(input_data={})
        assert empty_score is not None
        assert 0.0 <= empty_score.overall_score <= 1.0
        
        # Test with invalid scoring types
        invalid_score = scoring_gamma.calculate_quantum_score(
            input_data={'test': 'data'},
            scoring_types=[]
        )
        assert invalid_score is not None
    
    def test_performance_optimization(self, scoring_alpha, scoring_gamma):
        """Test performance optimization based on consciousness level"""
        # Create test data
        test_data = {
            'quantum_state': np.random.rand(256) + 1j * np.random.rand(256),
            'pattern_data': [1, 2, 3],
            'test_quality': 0.6
        }
        
        # Test performance at different levels
        start_time = datetime.now()
        alpha_result = scoring_alpha.calculate_quantum_score(test_data)
        alpha_time = datetime.now() - start_time
        
        start_time = datetime.now()
        gamma_result = scoring_gamma.calculate_quantum_score(test_data)
        gamma_time = datetime.now() - start_time
        
        # Both should produce valid results
        assert alpha_result is not None
        assert gamma_result is not None
        
        # Performance multiplier should be different
        assert scoring_gamma.performance_multiplier > scoring_alpha.performance_multiplier
    
    def test_integration_with_quantum_engine(self, scoring_gamma):
        """Test integration with unified field engine"""
        # Check quantum field is initialized
        assert scoring_gamma.quantum_field is not None
        assert scoring_gamma.quantum_field.consciousness_level == ConsciousnessLevel.GAMMA
        
        # Check consciousness protocol is initialized
        assert scoring_gamma.consciousness_protocol is not None
        assert scoring_gamma.consciousness_protocol.current_state.level == ConsciousnessLevel.GAMMA
    
    def test_weighting_strategies(self, scoring_gamma, test_input_data):
        """Test different weighting strategies"""
        strategies = [
            WeightingStrategy.LINEAR,
            WeightingStrategy.EXPONENTIAL,
            WeightingStrategy.GAUSSIAN,
            WeightingStrategy.CONSCIOUSNESS_OPTIMIZED,
            WeightingStrategy.QUANTUM_ENHANCED,
            WeightingStrategy.ADAPTIVE_LEARNING
        ]
        
        results = {}
        for strategy in strategies:
            custom_weights = ScoringWeights(weighting_strategy=strategy).normalize()
            score_state = scoring_gamma.calculate_quantum_score(
                input_data=test_input_data,
                custom_weights=custom_weights
            )
            results[strategy.value] = score_state.overall_score
        
        # All should produce valid scores
        for score in results.values():
            assert 0.0 <= score <= 1.0
        
        # Different strategies should produce different results
        unique_scores = len(set(results.values()))
        assert unique_scores >= 2  # At least some differences
    
    def test_scoring_metrics_calculation(self, scoring_gamma, test_input_data):
        """Test individual scoring metrics calculation"""
        # Calculate quantum score
        score_state = scoring_gamma.calculate_quantum_score(
            input_data=test_input_data
        )
        
        # Check raw scores contain all expected metrics
        raw_scores = score_state.raw_scores
        expected_metrics = [
            ScoringMetric.COHERENCE.value,
            ScoringMetric.CONSCIOUSNESS.value,
            ScoringMetric.PATTERN.value,
            ScoringMetric.EVOLUTION.value,
            ScoringMetric.ENTROPY.value,
            ScoringMetric.COMPLEXITY.value,
            ScoringMetric.QUANTUM.value
        ]
        
        for metric in expected_metrics:
            assert metric in raw_scores
            assert isinstance(raw_scores[metric], (int, float, np.number))
            assert 0.0 <= raw_scores[metric] <= 1.0
    
    def test_scoring_history_tracking(self, scoring_gamma, test_input_data):
        """Test scoring history tracking"""
        # Calculate multiple scores
        for i in range(5):
            test_data = {
                'quantum_state': np.random.rand(256) + 1j * np.random.rand(256),
                'pattern_data': [1, 2, 3, 2, 1],
                'evolution_data': float(i),
                'test_quality': 0.8
            }
            scoring_gamma.calculate_quantum_score(test_data)
        
        # Check history is tracked
        assert len(scoring_gamma.scoring_history) == 5
        
        # Check history contains valid score states
        for score_state in scoring_gamma.scoring_history:
            assert isinstance(score_state, ScoreState)
            assert 0.0 <= score_state.overall_score <= 1.0

class TestScoreState:
    """Test suite for ScoreState class"""
    
    @pytest.fixture
    def score_state(self):
        """Create score state for testing"""
        return ScoreState(
            input_data={'test': 'data'},
            raw_scores={'coherence': 0.8, 'consciousness': 0.7},
            weighted_scores={'coherence': 0.16, 'consciousness': 0.14},
            overall_score=0.3,
            consciousness_level=ConsciousnessLevel.GAMMA,
            etd_value=25.5
        )
    
    def test_score_state_initialization(self, score_state):
        """Test score state initialization"""
        assert score_state.consciousness_level == ConsciousnessLevel.GAMMA
        assert score_state.overall_score == 0.3
        assert score_state.etd_value == 25.5
        assert score_state.blockchain_hash == ""  # Default
        assert score_state.timestamp != ""  # Should be set automatically
    
    def test_score_state_post_init(self):
        """Test score state post-initialization"""
        # Test with custom timestamp
        custom_timestamp = "2024-01-01T00:00:00Z"
        state = ScoreState(
            input_data={'test': 'data'},
            raw_scores={},
            weighted_scores={},
            overall_score=0.5,
            consciousness_level=ConsciousnessLevel.BETA,
            timestamp=custom_timestamp
        )
        
        assert state.timestamp == custom_timestamp

class TestScoringWeights:
    """Test suite for ScoringWeights class"""
    
    @pytest.fixture
    def scoring_weights(self):
        """Create scoring weights for testing"""
        return ScoringWeights(
            coherence_weight=0.3,
            consciousness_weight=0.4,
            pattern_weight=0.1,
            evolution_weight=0.1,
            etda_weight=0.05,
            quantum_weight=0.05,
            weighting_strategy=WeightingStrategy.CONSCIOUSNESS_OPTIMIZED
        )
    
    def test_scoring_weights_initialization(self, scoring_weights):
        """Test scoring weights initialization"""
        assert scoring_weights.coherence_weight == 0.3
        assert scoring_weights.consciousness_weight == 0.4
        assert scoring_weights.pattern_weight == 0.1
        assert scoring_weights.evolution_weight == 0.1
        assert scoring_weights.etda_weight == 0.05
        assert scoring_weights.quantum_weight == 0.05
        assert scoring_weights.weighting_strategy == WeightingStrategy.CONSCIOUSNESS_OPTIMIZED
    
    def test_scoring_weights_normalization(self):
        """Test scoring weights normalization"""
        # Create weights with unequal sum
        weights = ScoringWeights(
            coherence_weight=0.5,
            consciousness_weight=0.3,
            pattern_weight=0.2,
            evolution_weight=0.1,
            etda_weight=0.1,
            quantum_weight=0.1
        )
        
        # Normalize weights
        normalized = weights.normalize()
        
        # Check weights sum to 1.0
        total = (normalized.coherence_weight + normalized.consciousness_weight + 
                 normalized.pattern_weight + normalized.evolution_weight + 
                 normalized.etda_weight + normalized.quantum_weight)
        assert abs(total - 1.0) < 1e-10

class TestScoringResult:
    """Test suite for ScoringResult class"""
    
    @pytest.fixture
    def scoring_result(self):
        """Create scoring result for testing"""
        score_state = ScoreState(
            input_data={'test': 'data'},
            raw_scores={'coherence': 0.8},
            weighted_scores={'coherence': 0.16},
            overall_score=0.16,
            consciousness_level=ConsciousnessLevel.GAMMA
        )
        
        weights = ScoringWeights()
        
        return ScoringResult(
            score_state=score_state,
            weights=weights,
            metrics={'quality': 0.9},
            quality_score=0.85,
            confidence=0.9,
            scoring_type=ScoringType.MULTI_DIMENSIONAL
        )
    
    def test_scoring_result_initialization(self, scoring_result):
        """Test scoring result initialization"""
        assert isinstance(scoring_result.score_state, ScoreState)
        assert isinstance(scoring_result.weights, ScoringWeights)
        assert isinstance(scoring_result.metrics, dict)
        assert scoring_result.quality_score == 0.85
        assert scoring_result.confidence == 0.9
        assert scoring_result.scoring_type == ScoringType.MULTI_DIMENSIONAL
        assert scoring_result.blockchain_verified == True
    
    def test_scoring_result_to_dict(self, scoring_result):
        """Test scoring result dictionary conversion"""
        result_dict = scoring_result.to_dict()
        
        # Check dictionary structure
        assert 'overall_score' in result_dict
        assert 'etd_value' in result_dict
        assert 'quality_score' in result_dict
        assert 'confidence' in result_dict
        assert 'scoring_type' in result_dict
        assert 'blockchain_verified' in result_dict
        assert 'raw_scores' in result_dict
        assert 'weighted_scores' in result_dict
        assert 'metrics' in result_dict
        assert 'weights' in result_dict
        
        # Check values
        assert result_dict['overall_score'] == scoring_result.score_state.overall_score
        assert result_dict['quality_score'] == scoring_result.quality_score
        assert result_dict['confidence'] == scoring_result.confidence

class TestScoringEnums:
    """Test suite for scoring-related enums"""
    
    def test_scoring_type_values(self):
        """Test scoring type enum values"""
        expected_values = [
            "quantum_coherence",
            "consciousness_aware",
            "pattern_recognition",
            "evolution_tracking",
            "etd_generation",
            "multi_dimensional",
            "adaptive_weighting",
            "blockchain_verified"
        ]
        
        actual_values = [scoring_type.value for scoring_type in ScoringType]
        
        for expected_value in expected_values:
            assert expected_value in actual_values
    
    def test_weighting_strategy_values(self):
        """Test weighting strategy enum values"""
        expected_values = [
            "linear",
            "exponential",
            "gaussian",
            "consciousness_optimized",
            "quantum_enhanced",
            "adaptive_learning"
        ]
        
        actual_values = [strategy.value for strategy in WeightingStrategy]
        
        for expected_value in expected_values:
            assert expected_value in actual_values
    
    def test_scoring_metric_values(self):
        """Test scoring metric enum values"""
        expected_values = [
            "coherence",
            "entropy",
            "complexity",
            "consciousness",
            "pattern",
            "evolution",
            "etda",
            "quantum"
        ]
        
        actual_values = [metric.value for metric in ScoringMetric]
        
        for expected_value in expected_values:
            assert expected_value in actual_values
    
    def test_enum_completeness(self):
        """Test enum completeness"""
        # Check scoring types
        scoring_count = len(ScoringType)
        assert scoring_count >= 8  # Minimum expected types
        
        # Check weighting strategies
        strategy_count = len(WeightingStrategy)
        assert strategy_count >= 6  # Minimum expected strategies
        
        # Check scoring metrics
        metric_count = len(ScoringMetric)
        assert metric_count >= 8  # Minimum expected metrics
        
        # All values should be unique
        scoring_values = [scoring_type.value for scoring_type in ScoringType]
        strategy_values = [strategy.value for strategy in WeightingStrategy]
        metric_values = [metric.value for metric in ScoringMetric]
        
        assert len(scoring_values) == len(set(scoring_values))
        assert len(strategy_values) == len(set(strategy_values))
        assert len(metric_values) == len(set(metric_values))

# Pytest configuration and fixtures
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment"""
    # Suppress warnings during testing
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    # Set random seed for reproducible tests
    np.random.seed(42)
    
    yield
    
    # Cleanup after tests
    warnings.resetwarnings()

# Test markers
pytest_plugins = []

# Test configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )

# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

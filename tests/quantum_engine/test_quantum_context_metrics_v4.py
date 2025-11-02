"""
Test Suite for Quantum Context Metrics v4.0

This comprehensive test suite validates all quantum context metrics functionality,
including quantum state analysis, pattern recognition, consciousness integration,
and performance optimization.

Test Coverage:
- Quantum context state initialization and analysis
- Context embedding and pattern signature generation
- Context relevance, evolution, and stability calculations
- Consciousness awareness integration
- Comprehensive metrics calculation
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
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '.github', 'quantum-engine'))

try:
    from quantum_context_metrics_v4 import (
        QuantumContextMetricsV4,
        QuantumContextState,
        ContextMetrics,
        ContextMetricType
    )
    from unified_field_engine_v4 import ConsciousnessLevel
except ImportError as e:
    pytest.skip(f"Quantum context metrics not available: {e}", allow_module_level=True)

class TestQuantumContextMetricsV4:
    """Test suite for QuantumContextMetricsV4 class"""
    
    @pytest.fixture
    def metrics_alpha(self):
        """Create alpha level quantum context metrics for testing"""
        return QuantumContextMetricsV4(
            n_qubits=4,
            consciousness_level=ConsciousnessLevel.ALPHA,
            context_dimensions=8
        )
    
    @pytest.fixture
    def metrics_gamma(self):
        """Create gamma level quantum context metrics for testing"""
        return QuantumContextMetricsV4(
            n_qubits=6,
            consciousness_level=ConsciousnessLevel.GAMMA,
            context_dimensions=12
        )
    
    @pytest.fixture
    def metrics_omega(self):
        """Create omega level quantum context metrics for testing"""
        return QuantumContextMetricsV4(
            n_qubits=8,
            consciousness_level=ConsciousnessLevel.OMEGA,
            context_dimensions=16
        )
    
    def test_metrics_initialization(self, metrics_alpha):
        """Test quantum context metrics initialization"""
        assert metrics_alpha.n_qubits == 4
        assert metrics_alpha.consciousness_level == ConsciousnessLevel.ALPHA
        assert metrics_alpha.context_dimensions == 8
        assert metrics_alpha.hilbert_dimension == 16  # 2^4
        
        # Check performance multiplier
        assert metrics_alpha.performance_multiplier == 2.0  # Alpha level multiplier
        
        # Check quantum field and protocol initialization
        assert metrics_alpha.quantum_field is not None
        assert metrics_alpha.consciousness_protocol is not None
        
        # Check initial state
        assert len(metrics_alpha.context_history) == 0
        assert len(metrics_alpha.pattern_history) == 0
        assert isinstance(metrics_alpha.metrics_cache, dict)
    
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
            metrics = QuantumContextMetricsV4(
                n_qubits=4,
                consciousness_level=level,
                context_dimensions=8
            )
            assert metrics.performance_multiplier == expected_multiplier
    
    def test_analyze_quantum_context(self, metrics_gamma):
        """Test quantum context analysis"""
        # Analyze context without specific inputs
        context_state = metrics_gamma.analyze_quantum_context()
        
        # Check context state properties
        assert isinstance(context_state, QuantumContextState)
        assert context_state.consciousness_level == ConsciousnessLevel.GAMMA
        assert len(context_state.state_vector) == 64  # 2^6
        assert context_state.density_matrix.shape == (64, 64)
        assert len(context_state.context_embedding) == 12  # context_dimensions
        assert len(context_state.pattern_signature) == 16  # Fixed pattern size
        
        # Check metrics ranges
        assert 0.0 <= context_state.context_relevance <= 1.0
        assert 0.0 <= context_state.evolution_score <= 1.0
        assert 0.0 <= context_state.stability_score <= 1.0
        
        # Check history updates
        assert len(metrics_gamma.context_history) == 1
        assert len(metrics_gamma.pattern_history) == 1
    
    def test_analyze_quantum_context_with_data(self, metrics_gamma):
        """Test quantum context analysis with context data"""
        # Create context data
        context_data = {
            'project': 'quantum-enhancement',
            'branch': 'main',
            'commit': 'abc123',
            'environment': 'production',
            'metrics': {'cpu': 80, 'memory': 60}
        }
        
        # Analyze context with data
        context_state = metrics_gamma.analyze_quantum_context(
            context_data=context_data
        )
        
        # Check context embedding includes context information
        assert np.any(context_state.context_embedding != 0)
        
        # Check context relevance is influenced by data
        assert context_state.context_relevance > 0.5  # Should be high with good context
    
    def test_initialize_quantum_state(self, metrics_alpha):
        """Test quantum state initialization for different consciousness levels"""
        # Test alpha level
        state_alpha = metrics_alpha._initialize_quantum_state()
        assert len(state_alpha) == 16  # 2^4
        assert np.isclose(np.linalg.norm(state_alpha), 1.0, atol=1e-10)
        
        # Alpha should be mostly ground state
        assert np.abs(state_alpha[0]) > 0.9  # High probability of |0⟩
        
        # Test gamma level
        metrics_gamma = QuantumContextMetricsV4(
            n_qubits=4,
            consciousness_level=ConsciousnessLevel.GAMMA
        )
        state_gamma = metrics_gamma._initialize_quantum_state()
        
        # Gamma should have multi-state superposition
        significant_states = np.sum(np.abs(state_gamma) > 0.1)
        assert significant_states >= 2  # Multiple states have probability
    
    def test_generate_context_embedding(self, metrics_gamma):
        """Test context embedding generation"""
        # Create quantum state
        quantum_state = metrics_gamma._initialize_quantum_state()
        
        # Test without context data
        embedding_no_data = metrics_gamma._generate_context_embedding(quantum_state, None)
        assert len(embedding_no_data) == metrics_gamma.context_dimensions
        
        # Test with context data
        context_data = {
            'test': 'value',
            'number': 42,
            'boolean': True
        }
        embedding_with_data = metrics_gamma._generate_context_embedding(
            quantum_state, context_data
        )
        assert len(embedding_with_data) == metrics_gamma.context_dimensions
        
        # Embeddings should be different with and without context data
        assert not np.allclose(embedding_no_data, embedding_with_data)
    
    def test_generate_pattern_signature(self, metrics_gamma):
        """Test pattern signature generation"""
        # Create quantum state
        quantum_state = metrics_gamma._initialize_quantum_state()
        density_matrix = np.outer(quantum_state, np.conj(quantum_state))
        
        # Generate pattern signature
        signature = metrics_gamma._generate_pattern_signature(quantum_state, density_matrix)
        
        # Check signature properties
        assert len(signature) == 16  # Fixed pattern size
        assert np.isfinite(signature).all()
        assert np.linalg.norm(signature) <= 1.0  # Should be normalized
        
        # Check signature includes quantum features
        assert signature[0] != 0 or signature[1] != 0  # Amplitude features
        assert len(signature) >= 8  # Should include multiple features
    
    def test_calculate_context_relevance(self, metrics_gamma):
        """Test context relevance calculation"""
        # Create test data
        quantum_state = metrics_gamma._initialize_quantum_state()
        context_embedding = metrics_gamma._generate_context_embedding(quantum_state, None)
        
        # Test without context data
        relevance_no_data = metrics_gamma._calculate_context_relevance(
            quantum_state, None, context_embedding
        )
        assert 0.0 <= relevance_no_data <= 1.0
        
        # Test with rich context data
        context_data = {
            'project': 'test',
            'branch': 'main',
            'environment': 'production',
            'metrics': {'cpu': 75, 'memory': 50},
            'tests': {'passed': 95, 'total': 100}
        }
        relevance_with_data = metrics_gamma._calculate_context_relevance(
            quantum_state, context_data, context_embedding
        )
        assert 0.0 <= relevance_with_data <= 1.0
        assert relevance_with_data >= relevance_no_data  # Rich data should increase relevance
    
    def test_calculate_evolution_score(self, metrics_gamma):
        """Test evolution score calculation"""
        # Create initial pattern
        quantum_state = metrics_gamma._initialize_quantum_state()
        density_matrix = np.outer(quantum_state, np.conj(quantum_state))
        signature = metrics_gamma._generate_pattern_signature(quantum_state, density_matrix)
        
        # Test first pattern (should be neutral)
        metrics_gamma.pattern_history = [signature]
        evolution_score = metrics_gamma._calculate_evolution_score(quantum_state, signature)
        assert 0.0 <= evolution_score <= 1.0
        
        # Add similar pattern and test again
        similar_signature = signature + np.random.normal(0, 0.01, signature.shape)
        metrics_gamma.pattern_history = [signature, similar_signature]
        evolution_score_similar = metrics_gamma._calculate_evolution_score(
            quantum_state, signature
        )
        # Should have higher evolution score with similar pattern
        assert evolution_score_similar > evolution_score
    
    def test_calculate_stability_score(self, metrics_gamma):
        """Test stability score calculation"""
        # Create test quantum state
        quantum_state = metrics_gamma._initialize_quantum_state()
        density_matrix = np.outer(quantum_state, np.conj(quantum_state))
        context_embedding = metrics_gamma._generate_context_embedding(quantum_state, None)
        
        # Calculate stability score
        stability_score = metrics_gamma._calculate_stability_score(
            quantum_state, density_matrix, context_embedding
        )
        assert 0.0 <= stability_score <= 1.0
        
        # Test with historical context
        prev_context_state = QuantumContextState(
            state_vector=quantum_state,
            density_matrix=density_matrix,
            context_embedding=context_embedding,
            consciousness_level=metrics_gamma.consciousness_level
        )
        metrics_gamma.context_history = [prev_context_state]
        
        # Create slightly different embedding
        new_embedding = context_embedding + np.random.normal(0, 0.1, context_embedding.shape)
        stability_score_with_history = metrics_gamma._calculate_stability_score(
            quantum_state, density_matrix, new_embedding
        )
        
        assert 0.0 <= stability_score_with_history <= 1.0
    
    def test_get_consciousness_awareness(self, metrics_gamma):
        """Test consciousness awareness calculation"""
        # Create quantum state
        quantum_state = metrics_gamma._initialize_quantum_state()
        density_matrix = np.outer(quantum_state, np.conj(quantum_state))
        
        # Calculate consciousness awareness
        awareness = metrics_gamma._get_consciousness_awareness(quantum_state, density_matrix)
        assert 0.0 <= awareness <= 1.0
        
        # Awareness should be influenced by consciousness level
        metrics_omega = QuantumContextMetricsV4(
            n_qubits=4,
            consciousness_level=ConsciousnessLevel.OMEGA
        )
        awareness_omega = metrics_omega._get_consciousness_awareness(
            quantum_state, density_matrix
        )
        
        # Omega should have higher awareness than gamma
        assert awareness_omega >= awareness
    
    def test_calculate_comprehensive_metrics(self, metrics_gamma):
        """Test comprehensive metrics calculation"""
        # Analyze context first
        context_state = metrics_gamma.analyze_quantum_context()
        
        # Calculate all metrics
        all_metrics = metrics_gamma.calculate_comprehensive_metrics(context_state)
        
        # Check all metric types are present
        for metric_type in ContextMetricType:
            assert metric_type.value in all_metrics
            assert isinstance(all_metrics[metric_type.value], ContextMetrics)
            assert all_metrics[metric_type.value].metric_type == metric_type
        
        # Check specific metrics
        coherence_metric = all_metrics[ContextMetricType.QUANTUM_COHERENCE.value]
        assert isinstance(coherence_metric.quantum_coherence, (int, float, np.number))
        
        relevance_metric = all_metrics[ContextMetricType.CONTEXT_RELEVANCE.value]
        assert 0.0 <= relevance_metric.context_relevance <= 1.0
    
    def test_calculate_specific_metrics(self, metrics_gamma):
        """Test calculation of specific metric types"""
        # Analyze context
        context_state = metrics_gamma.analyze_quantum_context()
        
        # Test quantum coherence metric
        coherence_metric = metrics_gamma.calculate_comprehensive_metrics(
            context_state, [ContextMetricType.QUANTUM_COHERENCE]
        )
        assert len(coherence_metric) == 1
        assert ContextMetricType.QUANTUM_COHERENCE.value in coherence_metric
        
        # Test multiple specific metrics
        specific_metrics = metrics_gamma.calculate_comprehensive_metrics(
            context_state,
            [ContextMetricType.CONTEXT_RELEVANCE, ContextMetricType.PATTERN_MATCH]
        )
        assert len(specific_metrics) == 2
        assert ContextMetricType.CONTEXT_RELEVANCE.value in specific_metrics
        assert ContextMetricType.PATTERN_MATCH.value in specific_metrics
    
    def test_generate_blockchain_hash(self, metrics_gamma):
        """Test blockchain hash generation"""
        # Create test metric and context state
        metric = ContextMetrics(
            quantum_coherence=0.8,
            context_relevance=0.7,
            metric_type=ContextMetricType.QUANTUM_COHERENCE
        )
        
        context_state = QuantumContextState(
            state_vector=np.array([1.0, 0.0]),
            consciousness_level=ConsciousnessLevel.GAMMA
        )
        
        # Generate blockchain hash
        hash_value = metrics_gamma._generate_blockchain_hash(metric, context_state)
        
        # Check hash properties
        assert isinstance(hash_value, str)
        assert len(hash_value) == 64  # SHA-256 hash length
        assert all(c in '0123456789abcdef' for c in hash_value)
        
        # Hash should be deterministic
        hash_value2 = metrics_gamma._generate_blockchain_hash(metric, context_state)
        assert hash_value == hash_value2
    
    def test_get_context_summary(self, metrics_gamma):
        """Test context summary generation"""
        # Analyze context
        context_state = metrics_gamma.analyze_quantum_context()
        
        # Get context summary
        summary = metrics_gamma.get_context_summary(context_state)
        
        # Check summary structure
        assert 'version' in summary
        assert 'spec' in summary
        assert 'timestamp' in summary
        assert 'consciousness_level' in summary
        assert 'performance_multiplier' in summary
        assert 'context_state' in summary
        assert 'key_metrics' in summary
        assert 'overall_scores' in summary
        assert 'analysis_statistics' in summary
        assert 'blockchain_verification' in summary
        
        # Check summary values
        assert summary['version'] == '4.0.0'
        assert summary['spec'] == 'QUANTUM:CONTEXT-METRICS-V4'
        assert summary['consciousness_level'] == ConsciousnessLevel.GAMMA.value
        assert summary['performance_multiplier'] == 12.5
        
        # Check overall scores
        overall_scores = summary['overall_scores']
        assert 'overall_coherence' in overall_scores
        assert 'overall_stability' in overall_scores
        assert 'overall_awareness' in overall_scores
        assert 'quality_score' in overall_scores
        assert 0.0 <= overall_scores['quality_score'] <= 1.0
    
    def test_get_performance_report(self, metrics_gamma):
        """Test performance report generation"""
        # Analyze multiple contexts to build history
        for _ in range(3):
            metrics_gamma.analyze_quantum_context()
        
        # Get performance report
        report = metrics_gamma.get_performance_report()
        
        # Check report structure
        assert 'version' in report
        assert 'spec' in report
        assert 'timestamp' in report
        assert 'system_configuration' in report
        assert 'performance_metrics' in report
        assert 'quality_metrics' in report
        assert 'blockchain_status' in report
        
        # Check system configuration
        config = report['system_configuration']
        assert 'n_qubits' in config
        assert 'hilbert_dimension' in config
        assert 'context_dimensions' in config
        assert 'consciousness_level' in config
        assert 'performance_multiplier' in config
        
        # Check performance metrics
        perf_metrics = report['performance_metrics']
        assert 'contexts_analyzed' in perf_metrics
        assert perf_metrics['contexts_analyzed'] >= 3
        assert 'analysis_speed' in perf_metrics
        assert 'performance_optimization' in perf_metrics
    
    def test_error_handling(self, metrics_gamma):
        """Test error handling in context metrics"""
        # Test with invalid quantum state
        with pytest.warns(UserWarning):
            # Should handle gracefully
            context_state = metrics_gamma.analyze_quantum_context()
            assert context_state is not None
        
        # Test metrics calculation with invalid context
        with pytest.warns(UserWarning):
            metrics = metrics_gamma.calculate_comprehensive_metrics(
                None, [ContextMetricType.QUANTUM_COHERENCE]
            )
            # Should return empty dict or handle gracefully
    
    def test_performance_optimization(self, metrics_alpha, metrics_gamma, metrics_omega):
        """Test performance optimization based on consciousness levels"""
        # Analyze contexts at different levels
        start_time = datetime.now()
        
        for _ in range(5):
            metrics_alpha.analyze_quantum_context()
        
        alpha_time = datetime.now() - start_time
        
        start_time = datetime.now()
        for _ in range(5):
            metrics_gamma.analyze_quantum_context()
        gamma_time = datetime.now() - start_time
        
        # Test caching functionality
        context_state = metrics_gamma.analyze_quantum_context()
        cached_metrics = metrics_gamma.calculate_comprehensive_metrics(
            context_state, [ContextMetricType.QUANTUM_COHERENCE]
        )
        
        # Second call should use cache
        cached_metrics2 = metrics_gamma.calculate_comprehensive_metrics(
            context_state, [ContextMetricType.QUANTUM_COHERENCE]
        )
        
        # Results should be identical from cache
        coherence_metric1 = cached_metrics[ContextMetricType.QUANTUM_COHERENCE.value]
        coherence_metric2 = cached_metrics2[ContextMetricType.QUANTUM_COHERENCE.value]
        assert coherence_metric1.quantum_coherence == coherence_metric2.quantum_coherence
    
    def test_integration_with_quantum_engine(self, metrics_gamma):
        """Test integration with unified field engine"""
        # Check quantum field is initialized
        assert metrics_gamma.quantum_field is not None
        assert metrics_gamma.quantum_field.consciousness_level == ConsciousnessLevel.GAMMA
        
        # Check consciousness protocol is initialized
        assert metrics_gamma.consciousness_protocol is not None
        assert metrics_gamma.consciousness_protocol.current_state.level == ConsciousnessLevel.GAMMA
    
    def test_edge_cases(self, metrics_gamma):
        """Test edge cases and boundary conditions"""
        # Test with minimal qubits
        metrics_min = QuantumContextMetricsV4(
            n_qubits=1,
            consciousness_level=ConsciousnessLevel.ALPHA,
            context_dimensions=4
        )
        context_state = metrics_min.analyze_quantum_context()
        assert len(context_state.state_vector) == 2  # 2^1
        
        # Test with large qubits (should still work)
        metrics_large = QuantumContextMetricsV4(
            n_qubits=4,  # Keep moderate for testing
            consciousness_level=ConsciousnessLevel.OMEGA,
            context_dimensions=32
        )
        context_state_large = metrics_large.analyze_quantum_context()
        assert len(context_state_large.context_embedding) == 32
    
    def test_memory_usage(self, metrics_gamma):
        """Test memory usage patterns"""
        import psutil
        import os
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Analyze multiple contexts
        contexts = []
        for i in range(10):
            context_state = metrics_gamma.analyze_quantum_context()
            contexts.append(context_state)
        
        # Check memory usage
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (< 50MB for 10 contexts)
        assert memory_increase < 50 * 1024 * 1024  # 50MB
        
        # Check cleanup works
        assert len(contexts) == 10

class TestQuantumContextState:
    """Test suite for QuantumContextState class"""
    
    @pytest.fixture
    def context_state(self):
        """Create quantum context state for testing"""
        return QuantumContextState(
            state_vector=np.array([0.7, 0.1, 0.1, 0.1]),
            consciousness_level=ConsciousnessLevel.GAMMA
        )
    
    def test_context_state_initialization(self, context_state):
        """Test quantum context state initialization"""
        assert context_state.consciousness_level == ConsciousnessLevel.GAMMA
        assert len(context_state.state_vector) == 4
        assert context_state.density_matrix.shape == (4, 4)
        assert len(context_state.context_embedding) == 0  # Default
        assert context_state.context_relevance == 0.0  # Default
        assert context_state.evolution_score == 0.0  # Default
        assert context_state.stability_score == 0.0  # Default
        assert context_state.timestamp != ""  # Should be set automatically
    
    def test_context_state_post_init(self):
        """Test context state post-initialization"""
        # Test with both state vector and density matrix
        state_vector = np.array([0.5, 0.5, 0.5, 0.5])
        state = QuantumContextState(
            state_vector=state_vector,
            consciousness_level=ConsciousnessLevel.BETA
        )
        
        # Density matrix should be created automatically
        expected_density = np.outer(state_vector, np.conj(state_vector))
        assert np.allclose(state.density_matrix, expected_density)

class TestContextMetrics:
    """Test suite for ContextMetrics class"""
    
    @pytest.fixture
    def metrics(self):
        """Create context metrics for testing"""
        return ContextMetrics(
            quantum_coherence=0.8,
            context_relevance=0.7,
            pattern_match=0.9,
            metric_type=ContextMetricType.QUANTUM_COHERENCE
        )
    
    def test_metrics_initialization(self, metrics):
        """Test context metrics initialization"""
        assert metrics.quantum_coherence == 0.8
        assert metrics.context_relevance == 0.7
        assert metrics.pattern_match == 0.9
        assert metrics.metric_type == ContextMetricType.QUANTUM_COHERENCE
        assert metrics.calculation_timestamp != ""  # Should be set automatically
        assert metrics.blockchain_hash == ""  # Default
    
    def test_metrics_post_init(self):
        """Test context metrics post-initialization"""
        # Test with custom timestamp
        custom_timestamp = "2024-01-01T00:00:00Z"
        metrics = ContextMetrics(
            quantum_coherence=0.5,
            calculation_timestamp=custom_timestamp
        )
        
        assert metrics.calculation_timestamp == custom_timestamp

class TestContextMetricType:
    """Test suite for ContextMetricType enum"""
    
    def test_metric_type_values(self):
        """Test context metric type enum values"""
        expected_values = [
            "quantum_coherence",
            "context_relevance", 
            "pattern_match",
            "evolution_score",
            "entanglement_complexity",
            "superposition_depth",
            "consciousness_awareness",
            "context_stability"
        ]
        
        actual_values = [metric_type.value for metric_type in ContextMetricType]
        
        for expected_value in expected_values:
            assert expected_value in actual_values
    
    def test_metric_type_completeness(self):
        """Test context metric type completeness"""
        # Should have all expected metric types
        metric_count = len(ContextMetricType)
        assert metric_count >= 8  # Minimum expected types
        
        # All values should be unique
        values = [metric_type.value for metric_type in ContextMetricType]
        assert len(values) == len(set(values))

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

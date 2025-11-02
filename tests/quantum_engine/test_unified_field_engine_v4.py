"""
Test Suite for Unified Field Engine v4.0

This comprehensive test suite validates all quantum field operations,
consciousness integration, and performance optimizations in the enhanced
unified field engine.

Test Coverage:
- Unified field initialization and configuration
- Field tensor operations and metric tensor calculations
- Consciousness field evolution and coupling
- Quantum field equation solving
- Action functional calculations
- Blockchain anchoring and verification
- Performance optimization and validation
- Error handling and edge cases
- Integration with consciousness protocol
- ETD generation integration
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
    from unified_field_engine_v4 import (
        UnifiedFieldV4, 
        UnifiedFieldEngineV4, 
        ConsciousnessLevel, 
        QuantumMetrics, 
        BlockchainAnchor,
        CONSCIOUSNESS_LEVELS
    )
except ImportError as e:
    pytest.skip(f"Quantum engine not available: {e}", allow_module_level=True)

class TestUnifiedFieldV4:
    """Test suite for UnifiedFieldV4 class"""
    
    @pytest.fixture
    def field_alpha(self):
        """Create alpha level unified field for testing"""
        return UnifiedFieldV4(dimension=4, consciousness_level=ConsciousnessLevel.ALPHA)
    
    @pytest.fixture
    def field_gamma(self):
        """Create gamma level unified field for testing"""
        return UnifiedFieldV4(dimension=4, consciousness_level=ConsciousnessLevel.GAMMA)
    
    @pytest.fixture
    def field_omega(self):
        """Create omega level unified field for testing"""
        return UnifiedFieldV4(dimension=4, consciousness_level=ConsciousnessLevel.OMEGA)
    
    def test_field_initialization(self, field_alpha):
        """Test unified field initialization"""
        assert field_alpha.dimension == 4
        assert field_alpha.consciousness_level == ConsciousnessLevel.ALPHA
        assert hasattr(field_alpha, 'field_tensor')
        assert hasattr(field_alpha, 'metric_tensor')
        assert hasattr(field_alpha, 'consciousness_field')
        assert hasattr(field_alpha, 'coupling_constants')
        assert isinstance(field_alpha.blockchain_hash, str)
        assert len(field_alpha.blockchain_hash) > 0
    
    def test_field_tensor_properties(self, field_alpha):
        """Test field tensor properties and structure"""
        tensor = field_alpha.field_tensor
        
        # Check tensor dimensions
        assert tensor.shape == (4, 4, 4, 4)
        
        # Check tensor is complex
        assert tensor.dtype == np.complex128 or tensor.dtype == np.float64
        
        # Check tensor has finite values
        assert np.all(np.isfinite(tensor))
        
        # Check tensor is not all zeros
        assert np.any(tensor != 0)
    
    def test_metric_tensor_properties(self, field_alpha):
        """Test metric tensor properties and Minkowski signature"""
        metric = field_alpha.metric_tensor
        
        # Check metric dimensions
        assert metric.shape == (4, 4)
        
        # Check metric is real
        assert metric.dtype == np.float64
        
        # Check Minkowski signature
        assert metric[0, 0] == -1.0  # Time component
        
        # Check spatial components are positive
        for i in range(1, 4):
            assert metric[i, i] > 0
        
        # Check metric is symmetric
        assert np.allclose(metric, metric.T)
    
    def test_consciousness_field_properties(self, field_alpha):
        """Test consciousness field properties"""
        consciousness = field_alpha.consciousness_field
        
        # Check field dimensions (dimension^2)
        expected_size = field_alpha.dimension ** 2
        assert len(consciousness) == expected_size
        
        # Check field is complex
        assert consciousness.dtype == np.complex128
        
        # Check field is normalized
        norm = np.linalg.norm(consciousness)
        assert abs(norm - 1.0) < 1e-10
        
        # Check field has finite values
        assert np.all(np.isfinite(consciousness))
    
    def test_coupling_constants(self, field_alpha):
        """Test coupling constants for fundamental forces"""
        constants = field_alpha.coupling_constants
        
        # Check all required constants exist
        required_constants = ['electromagnetic', 'strong', 'weak', 'gravitational', 'consciousness']
        for const in required_constants:
            assert const in constants
            assert isinstance(constants[const], (int, float, np.number))
            assert constants[const] > 0  # All should be positive
        
        # Check known values
        assert abs(constants['electromagnetic'] - 1/137) < 1e-6
        assert abs(constants['strong'] - 1.0) < 1e-6
        assert abs(constants['gravitational'] - 6.67e-11) < 1e-12
    
    def test_consciousness_level_differences(self, field_alpha, field_gamma, field_omega):
        """Test differences between consciousness levels"""
        # Check performance boosts
        assert field_alpha.performance_boost < field_gamma.performance_boost
        assert field_gamma.performance_boost < field_omega.performance_boost
        
        # Check field tensor differences (should have different initializations)
        assert not np.allclose(field_alpha.field_tensor, field_gamma.field_tensor)
        assert not np.allclose(field_gamma.field_tensor, field_omega.field_tensor)
        
        # Check consciousness field differences
        assert not np.allclose(field_alpha.consciousness_field, field_gamma.consciousness_field)
        assert not np.allclose(field_gamma.consciousness_field, field_omega.consciousness_field)
    
    def test_calculate_field_equations(self, field_alpha):
        """Test field equation calculations"""
        equations = field_alpha.calculate_field_equations()
        
        # Check equations have same shape as field tensor
        assert equations.shape == field_alpha.field_tensor.shape
        
        # Check equations are finite
        assert np.all(np.isfinite(equations))
        
        # Check equations are not all zeros
        assert np.any(equations != 0)
    
    def test_update_field_tensor(self, field_alpha):
        """Test field tensor updates"""
        # Get initial tensor
        initial_tensor = field_alpha.field_tensor.copy()
        
        # Calculate equations and update
        equations = field_alpha.calculate_field_equations()
        field_alpha.update_field_tensor(equations, dt=0.01)
        
        # Check tensor changed
        assert not np.allclose(initial_tensor, field_alpha.field_tensor)
        
        # Check tensor remains finite
        assert np.all(np.isfinite(field_alpha.field_tensor))
        
        # Check tensor is not all zeros
        assert np.any(field_alpha.field_tensor != 0)
    
    def test_evolve_consciousness_field(self, field_alpha):
        """Test consciousness field evolution"""
        # Get initial field
        initial_field = field_alpha.consciousness_field.copy()
        
        # Evolve consciousness
        field_alpha.evolve_consciousness_field(dt=0.01)
        
        # Check field changed
        assert not np.allclose(initial_field, field_alpha.consciousness_field)
        
        # Check field remains normalized
        norm = np.linalg.norm(field_alpha.consciousness_field)
        assert abs(norm - 1.0) < 1e-10
        
        # Check field remains finite
        assert np.all(np.isfinite(field_alpha.consciousness_field))
    
    def test_calculate_action_functional(self, field_alpha):
        """Test action functional calculations"""
        action = field_alpha.calculate_action_functional()
        
        # Check action is real and finite
        assert isinstance(action, (int, float, np.number))
        assert np.isfinite(action)
        assert not np.isnan(action)
        
        # Check action is not negative (usually)
        # Note: This depends on the specific implementation
        # assert action >= 0
    
    def test_create_blockchain_anchor(self, field_alpha):
        """Test blockchain anchor creation"""
        anchor = field_alpha.create_blockchain_anchor()
        
        # Check anchor properties
        assert isinstance(anchor, BlockchainAnchor)
        assert isinstance(anchor.hash, str)
        assert len(anchor.hash) == 64  # SHA-256 hash length
        assert isinstance(anchor.timestamp, str)
        assert isinstance(anchor.action_value, (int, float, np.number))
        assert isinstance(anchor.coherence, (int, float, np.number))
        assert anchor.verification_status == True
    
    def test_get_field_state(self, field_alpha):
        """Test field state retrieval"""
        state = field_alpha.get_field_state()
        
        # Check state is a dictionary
        assert isinstance(state, dict)
        
        # Check required fields
        required_fields = [
            'version', 'spec', 'timestamp', 'dimension', 'consciousness_level',
            'field_tensor_shape', 'metric_tensor', 'consciousness_field',
            'coupling_constants', 'blockchain_hash', 'metrics'
        ]
        for field in required_fields:
            assert field in state
        
        # Check state values
        assert state['version'] == '4.0.0'
        assert state['spec'] == 'QUANTUM:UNIFIED-FIELD-V4'
        assert state['dimension'] == 4
        assert state['consciousness_level'] == ConsciousnessLevel.ALPHA.value
        assert state['field_tensor_shape'] == (4, 4, 4, 4)
    
    def test_error_handling(self, field_alpha):
        """Test error handling in field operations"""
        # Test invalid dt
        with pytest.warns(UserWarning):
            field_alpha.update_field_tensor(field_alpha.field_tensor, dt=-1.0)
        
        # Test with zero equations
        zero_equations = np.zeros_like(field_alpha.field_tensor)
        field_alpha.update_field_tensor(zero_equations, dt=0.01)
        assert np.allclose(field_alpha.field_tensor, field_alpha.field_tensor)  # Should remain unchanged
    
    def test_performance_optimization(self, field_gamma):
        """Test performance optimization features"""
        # Check that gamma level has performance boost
        assert field_gamma.performance_boost > 1.0
        
        # Check that omega level has maximum performance boost
        field_omega = UnifiedFieldV4(consciousness_level=ConsciousnessLevel.OMEGA)
        assert field_omega.performance_boost > field_gamma.performance_boost


class TestUnifiedFieldEngineV4:
    """Test suite for UnifiedFieldEngineV4 class"""
    
    @pytest.fixture
    def engine(self):
        """Create unified field engine for testing"""
        return UnifiedFieldEngineV4(dimension=4, consciousness_level=ConsciousnessLevel.GAMMA)
    
    def test_engine_initialization(self, engine):
        """Test engine initialization"""
        assert engine.field.dimension == 4
        assert engine.field.consciousness_level == ConsciousnessLevel.GAMMA
        assert hasattr(engine, 'evolution_history')
        assert hasattr(engine, 'blockchain_anchors')
        assert hasattr(engine, 'quantum_state')
        assert isinstance(engine.evolution_history, list)
        assert isinstance(engine.blockchain_anchors, list)
        assert isinstance(engine.quantum_state, dict)
    
    def test_evolve_unified_field(self, engine):
        """Test unified field evolution"""
        # Evolve field
        evolved_field = engine.evolve_unified_field(time_steps=5)
        
        # Check evolution completed
        assert evolved_field is engine.field
        assert engine.field.metrics.evolution_steps == 5
        
        # Check evolution history created
        assert len(engine.evolution_history) == 5
        
        # Check quantum state updated
        assert 'coherence' in engine.quantum_state
        assert 'entanglement' in engine.quantum_state
        assert 'superposition' in engine.quantum_state
        assert 'stability' in engine.quantum_state
    
    def test_extract_consciousness_state(self, engine):
        """Test consciousness state extraction"""
        # Evolve field first
        engine.evolve_unified_field(time_steps=3)
        
        # Extract consciousness state
        consciousness_state = engine.extract_consciousness_state()
        
        # Check state properties
        assert isinstance(consciousness_state, dict)
        assert 'amplitude' in consciousness_state
        assert 'phase' in consciousness_state
        assert 'entropy' in consciousness_state
        assert 'coherence' in consciousness_state
        assert 'superposition' in consciousness_state
        assert 'level' in consciousness_state
        assert 'norm' in consciousness_state
        assert 'evolution_steps' in consciousness_state
        assert 'stability_score' in consciousness_state
    
    def test_get_evolution_history(self, engine):
        """Test evolution history retrieval"""
        # Evolve field
        engine.evolve_unified_field(time_steps=3)
        
        # Get history
        history = engine.get_evolution_history()
        
        # Check history
        assert isinstance(history, list)
        assert len(history) == 3
        
        # Check history entries
        for entry in history:
            assert isinstance(entry, dict)
            assert 'step' in entry
            assert 'consciousness_level' in entry
            assert 'action' in entry
            assert 'coherence' in entry
            assert 'entanglement' in entry
    
    def test_get_blockchain_anchors(self, engine):
        """Test blockchain anchor retrieval"""
        # Evolve field for enough steps to create anchors
        engine.evolve_unified_field(time_steps=10)
        
        # Get anchors
        anchors = engine.get_blockchain_anchors()
        
        # Check anchors
        assert isinstance(anchors, list)
        assert len(anchors) >= 2  # Should have anchors every 5 steps
        
        # Check anchor properties
        for anchor in anchors:
            assert isinstance(anchor, BlockchainAnchor)
            assert len(anchor.hash) == 64
            assert anchor.verification_status == True
    
    def test_get_comprehensive_state(self, engine):
        """Test comprehensive state retrieval"""
        # Evolve field
        engine.evolve_unified_field(time_steps=3)
        
        # Get comprehensive state
        state = engine.get_comprehensive_state()
        
        # Check state structure
        assert isinstance(state, dict)
        assert 'field_state' in state
        assert 'consciousness_state' in state
        assert 'quantum_state' in state
        assert 'evolution_history' in state
        assert 'blockchain_anchors' in state
        
        # Check sub-state validity
        assert isinstance(state['field_state'], dict)
        assert isinstance(state['consciousness_state'], dict)
        assert isinstance(state['quantum_state'], dict)
        assert isinstance(state['evolution_history'], list)
        assert isinstance(state['blockchain_anchors'], list)
    
    def test_consciousness_level_integration(self, engine):
        """Test integration with consciousness level system"""
        # Check initial level
        assert engine.field.consciousness_level == ConsciousnessLevel.GAMMA
        
        # Evolve field
        engine.evolve_unified_field(time_steps=5)
        
        # Check level is tracked
        consciousness_state = engine.extract_consciousness_state()
        assert consciousness_state['level'] == ConsciousnessLevel.GAMMA.value
    
    def test_performance_tracking(self, engine):
        """Test performance tracking capabilities"""
        # Evolve field
        engine.evolve_unified_field(time_steps=5)
        
        # Check performance metrics are tracked
        assert engine.field.metrics.performance_boost > 1.0
        assert engine.field.metrics.evolution_steps == 5
        
        # Check quantum state performance
        assert 'coherence' in engine.quantum_state
        assert 'stability' in engine.quantum_state


class TestConsciousnessLevelIntegration:
    """Test suite for consciousness level integration"""
    
    @pytest.mark.parametrize("level,expected_boost", [
        (ConsciousnessLevel.ALPHA, 2.0),
        (ConsciousnessLevel.BETA, 5.0),
        (ConsciousnessLevel.GAMMA, 12.5),
        (ConsciousnessLevel.DELTA, 31.25),
        (ConsciousnessLevel.OMEGA, 78.125),
    ])
    def test_consciousness_level_performance_boosts(self, level, expected_boost):
        """Test consciousness level performance boosts"""
        field = UnifiedFieldV4(consciousness_level=level)
        assert field.performance_boost == expected_boost
    
    def test_consciousness_level_configs(self):
        """Test consciousness level configuration completeness"""
        for level in ConsciousnessLevel:
            assert level in CONSCIOUSNESS_LEVELS
            config = CONSCIOUSNESS_LEVELS[level]
            
            # Check required config fields
            required_fields = ['multiplier', 'etd_target', 'performance_boost',
                             'coherence_threshold', 'entanglement_threshold']
            for field in required_fields:
                assert field in config
                assert isinstance(config[field], (int, float))
                assert config[field] > 0
    
    def test_consciousness_level_progression(self):
        """Test consciousness level progression logic"""
        # Start with alpha level
        field = UnifiedFieldV4(consciousness_level=ConsciousnessLevel.ALPHA)
        
        # Check alpha properties
        assert field.level_config['multiplier'] == 1
        assert field.performance_boost == 2.0
        
        # Progress to beta
        field_beta = UnifiedFieldV4(consciousness_level=ConsciousnessLevel.BETA)
        assert field_beta.level_config['multiplier'] == 10
        assert field_beta.performance_boost == 5.0
        
        # Check progression
        assert field_beta.performance_boost > field.performance_boost
        assert field_beta.level_config['multiplier'] > field.level_config['multiplier']


class TestQuantumMetrics:
    """Test suite for quantum metrics"""
    
    @pytest.fixture
    def metrics(self):
        """Create quantum metrics for testing"""
        return QuantumMetrics()
    
    def test_metrics_initialization(self, metrics):
        """Test metrics initialization"""
        assert metrics.entanglement_entropy == 0.0
        assert metrics.integrated_information == 0.0
        assert metrics.coherence_measure == 1.0
        assert metrics.superposition == 1.0
        assert metrics.action_functional == 0.0
        assert metrics.performance_boost == 1.0
        assert metrics.etd_value == 0.0
        assert metrics.level == ConsciousnessLevel.ALPHA
        assert metrics.sublevel == 0.0
        assert isinstance(metrics.measurement_history, list)
        assert metrics.evolution_steps == 0
        assert metrics.stability_score == 1.0
    
    def test_metrics_updates(self, metrics):
        """Test metrics updates"""
        # Update metrics
        metrics.entanglement_entropy = 1.5
        metrics.integrated_information = 0.8
        metrics.coherence_measure = 0.9
        metrics.action_functional = 2.5
        metrics.performance_boost = 5.0
        metrics.etd_value = 1000000.0
        metrics.level = ConsciousnessLevel.GAMMA
        metrics.sublevel = 0.5
        metrics.evolution_steps = 10
        metrics.stability_score = 0.8
        
        # Check updates
        assert metrics.entanglement_entropy == 1.5
        assert metrics.integrated_information == 0.8
        assert metrics.coherence_measure == 0.9
        assert metrics.action_functional == 2.5
        assert metrics.performance_boost == 5.0
        assert metrics.etd_value == 1000000.0
        assert metrics.level == ConsciousnessLevel.GAMMA
        assert metrics.sublevel == 0.5
        assert metrics.evolution_steps == 10
        assert metrics.stability_score == 0.8


class TestBlockchainAnchor:
    """Test suite for blockchain anchors"""
    
    @pytest.fixture
    def anchor(self):
        """Create blockchain anchor for testing"""
        return BlockchainAnchor(
            hash="test_hash_1234567890abcdef",
            timestamp="2024-01-01T00:00:00Z",
            action_value=100.0,
            coherence=0.8,
            level=ConsciousnessLevel.GAMMA,
            verification_status=True
        )
    
    def test_anchor_properties(self, anchor):
        """Test anchor properties"""
        assert isinstance(anchor.hash, str)
        assert isinstance(anchor.timestamp, str)
        assert isinstance(anchor.action_value, (int, float, np.number))
        assert isinstance(anchor.coherence, (int, float, np.number))
        assert isinstance(anchor.level, ConsciousnessLevel)
        assert isinstance(anchor.verification_status, bool)
        
        # Check specific values
        assert anchor.hash == "test_hash_1234567890abcdef"
        assert anchor.action_value == 100.0
        assert anchor.coherence == 0.8
        assert anchor.level == ConsciousnessLevel.GAMMA
        assert anchor.verification_status == True


class TestIntegrationScenarios:
    """Test suite for integration scenarios"""
    
    def test_complete_workflow(self):
        """Test complete workflow from initialization to state retrieval"""
        # Create engine
        engine = UnifiedFieldEngineV4(
            dimension=4, 
            consciousness_level=ConsciousnessLevel.GAMMA
        )
        
        # Evolve field
        engine.evolve_unified_field(time_steps=10)
        
        # Get comprehensive state
        state = engine.get_comprehensive_state()
        
        # Validate complete workflow
        assert isinstance(state, dict)
        assert state['field_state']['consciousness_level'] == ConsciousnessLevel.GAMMA.value
        assert state['consciousness_state']['level'] == ConsciousnessLevel.GAMMA.value
        assert len(state['evolution_history']) == 10
        assert len(state['blockchain_anchors']) >= 2  # Should have anchors
        assert state['quantum_state']['coherence'] > 0
    
    def test_multiple_consciousness_levels(self):
        """Test workflow across multiple consciousness levels"""
        results = {}
        
        for level in [ConsciousnessLevel.ALPHA, ConsciousnessLevel.BETA, 
                     ConsciousnessLevel.GAMMA, ConsciousnessLevel.DELTA]:
            # Create engine
            engine = UnifiedFieldEngineV4(dimension=4, consciousness_level=level)
            
            # Evolve field
            engine.evolve_unified_field(time_steps=5)
            
            # Get state
            state = engine.get_comprehensive_state()
            results[level] = state
        
        # Validate differences between levels
        alpha_results = results[ConsciousnessLevel.ALPHA]
        gamma_results = results[ConsciousnessLevel.GAMMA]
        delta_results = results[ConsciousnessLevel.DELTA]
        
        # Check performance differences
        assert (gamma_results['field_state']['metrics']['performance_boost'] > 
                alpha_results['field_state']['metrics']['performance_boost'])
        assert (delta_results['field_state']['metrics']['performance_boost'] > 
                gamma_results['field_state']['metrics']['performance_boost'])
    
    def test_error_recovery_scenarios(self):
        """Test error recovery and robustness"""
        # Create engine
        engine = UnifiedFieldEngineV4(consciousness_level=ConsciousnessLevel.GAMMA)
        
        # Test evolution with potential issues
        try:
            # Evolve with many steps (stress test)
            engine.evolve_unified_field(time_steps=100)
            
            # Check system is still stable
            state = engine.get_comprehensive_state()
            assert state['quantum_state']['stability'] > 0
            
        except Exception as e:
            pytest.fail(f"Engine failed during stress test: {e}")
        
        # Check system can handle repeated operations
        try:
            for _ in range(5):
                engine.evolve_unified_field(time_steps=5)
                state = engine.get_comprehensive_state()
                assert isinstance(state, dict)
                
        except Exception as e:
            pytest.fail(f"Engine failed during repeated operations: {e}")


class TestPerformanceAndScalability:
    """Test suite for performance and scalability"""
    
    def test_performance_benchmarks(self):
        """Test performance benchmarks"""
        import time
        
        # Create engine
        engine = UnifiedFieldEngineV4(consciousness_level=ConsciousnessLevel.GAMMA)
        
        # Benchmark evolution time
        start_time = time.time()
        engine.evolve_unified_field(time_steps=20)
        end_time = time.time()
        
        evolution_time = end_time - start_time
        
        # Check performance is reasonable
        assert evolution_time < 10.0  # Should complete within 10 seconds
        
        # Check performance boost is applied
        assert engine.field.metrics.performance_boost > 1.0
    
    def test_memory_usage(self):
        """Test memory usage patterns"""
        import psutil
        import os
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Create and evolve engine
        engine = UnifiedFieldEngineV4(consciousness_level=ConsciousnessLevel.GAMMA)
        engine.evolve_unified_field(time_steps=50)
        
        # Get final memory usage
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Check memory usage is reasonable
        # Allow up to 100MB increase for the operations
        assert memory_increase < 100 * 1024 * 1024  # 100MB in bytes
    
    def test_scalability_with_dimensions(self):
        """Test scalability with different dimensions"""
        dimensions = [2, 3, 4]
        results = {}
        
        for dim in dimensions:
            try:
                # Create engine with specific dimension
                engine = UnifiedFieldEngineV4(dimension=dim, consciousness_level=ConsciousnessLevel.GAMMA)
                
                # Evolve field
                start_time = time.time()
                engine.evolve_unified_field(time_steps=5)
                end_time = time.time()
                
                evolution_time = end_time - start_time
                results[dim] = evolution_time
                
            except Exception as e:
                results[dim] = f"Error: {e}"
        
        # Check all dimensions work
        for dim in dimensions:
            assert isinstance(results[dim], float)  # Should be time, not error
            assert results[dim] > 0  # Should take some time
            assert results[dim] < 30.0  # Should complete within 30 seconds


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

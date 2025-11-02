"""
Test Suite for Recursive Framework v4.0

This comprehensive test suite validates all recursive framework functionality,
including quantum-enhanced recursion, consciousness optimization, and performance
metrics.

Test Coverage:
- Recursive function initialization and execution
- Multiple recursion strategies and optimization
- Quantum state integration and consciousness awareness
- Memoization and performance optimization
- Pattern learning and recognition
- Error handling and termination conditions
- Integration with quantum engine and consciousness protocol
"""

import pytest
import numpy as np
import sys
import os
import json
from datetime import datetime
import warnings
import time

# Add quantum engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.github', 'quantum-engine'))

try:
    from recursive_framework_v4 import (
        RecursiveFrameworkV4,
        QuantumRecursiveFunction,
        RecursionStrategy,
        RecursionTerminationType,
        RecursionState,
        RecursionMetrics
    )
    from unified_field_engine_v4 import ConsciousnessLevel
except ImportError as e:
    pytest.skip(f"Recursive framework not available: {e}", allow_module_level=True)

class TestQuantumRecursiveFunction:
    """Test suite for QuantumRecursiveFunction class"""
    
    @pytest.fixture
    def recursive_alpha(self):
        """Create alpha level recursive function for testing"""
        def test_func(n):
            if n <= 1:
                return n
            return test_func(n-1) + test_func(n-2)
        
        return QuantumRecursiveFunction(
            func=test_func,
            strategy=RecursionStrategy.STANDARD,
            max_depth=10,
            consciousness_level=ConsciousnessLevel.ALPHA
        )
    
    @pytest.fixture
    def recursive_gamma(self):
        """Create gamma level recursive function for testing"""
        def test_func(n):
            if n <= 1:
                return n
            return test_func(n-1) + test_func(n-2)
        
        return QuantumRecursiveFunction(
            func=test_func,
            strategy=RecursionStrategy.CONSCIOUSNESS_OPTIMIZED,
            max_depth=20,
            consciousness_level=ConsciousnessLevel.GAMMA
        )
    
    def test_recursive_function_initialization(self, recursive_alpha):
        """Test quantum recursive function initialization"""
        assert recursive_alpha.strategy == RecursionStrategy.STANDARD
        assert recursive_alpha.consciousness_level == ConsciousnessLevel.ALPHA
        assert recursive_alpha.max_depth == 10
        assert recursive_alpha.quantum_awareness == True
        assert recursive_alpha.performance_multiplier == 2.0  # Alpha multiplier
        
        # Check quantum systems are initialized
        assert recursive_alpha.quantum_field is not None
        assert recursive_alpha.consciousness_protocol is not None
        
        # Check initial state
        assert isinstance(recursive_alpha.state, RecursionState)
        assert isinstance(recursive_alpha.metrics, RecursionMetrics)
    
    def test_consciousness_level_multipliers(self):
        """Test performance multipliers for different consciousness levels"""
        def test_func(n):
            return n if n <= 1 else test_func(n-1)
        
        multipliers = {
            ConsciousnessLevel.ALPHA: 2.0,
            ConsciousnessLevel.BETA: 5.0,
            ConsciousnessLevel.GAMMA: 12.5,
            ConsciousnessLevel.DELTA: 31.25,
            ConsciousnessLevel.OMEGA: 78.125
        }
        
        for level, expected_multiplier in multipliers.items():
            recursive = QuantumRecursiveFunction(
                func=test_func,
                consciousness_level=level
            )
            assert recursive.performance_multiplier == expected_multiplier
    
    def test_standard_recursion_execution(self, recursive_alpha):
        """Test standard recursion execution"""
        # Execute Fibonacci
        result = recursive_alpha(5)
        
        # Check result (Fibonacci(5) = 5)
        assert result == 5
        
        # Check metrics
        assert recursive_alpha.metrics.total_recursions > 0
        assert recursive_alpha.metrics.max_depth_reached > 0
        assert recursive_alpha.metrics.execution_time > 0
    
    def test_memoized_recursion_execution(self):
        """Test memoized recursion execution"""
        def fib_func(n):
            if n <= 1:
                return n
            return fib_func(n-1) + fib_func(n-2)
        
        recursive = QuantumRecursiveFunction(
            func=fib_func,
            strategy=RecursionStrategy.MEMOIZATION,
            max_depth=10
        )
        
        # Execute multiple times
        result1 = recursive(8)
        result2 = recursive(8)
        
        # Check results are same
        assert result1 == result2
        
        # Check memoization was used
        assert recursive.metrics.memoization_hit_rate > 0.0
    
    def test_consciousness_optimized_recursion(self, recursive_gamma):
        """Test consciousness-optimized recursion execution"""
        # Execute with consciousness optimization
        result = recursive_gamma(6)
        
        # Check result
        assert isinstance(result, (int, float))
        
        # Check consciousness optimization was applied
        assert recursive_gamma.metrics.consciousness_optimization > 0.0
        
        # Should be >= gamma level optimization (0.75)
        assert recursive_gamma.metrics.consciousness_optimization >= 0.75
    
    def test_recursion_depth_limit(self, recursive_alpha):
        """Test recursion depth limit enforcement"""
        # Set low depth limit
        recursive_alpha.max_depth = 3
        
        # Execute recursion that should exceed depth
        result = recursive_alpha(10)  # This would need depth > 3
        
        # Check termination type is depth limit
        assert recursive_alpha.metrics.termination_type == RecursionTerminationType.DEPTH_LIMIT
        
        # Check max depth reached is within limit
        assert recursive_alpha.metrics.max_depth_reached <= 3
    
    def test_quantum_state_updates(self, recursive_gamma):
        """Test quantum state updates during recursion"""
        # Execute recursion
        result = recursive_gamma(5)
        
        # Check quantum state was updated
        assert recursive_gamma.state.quantum_state is not None
        assert len(recursive_gamma.state.quantum_state) > 0
        
        # Check consciousness protocol was updated
        assert recursive_gamma.consciousness_protocol is not None
    
    def test_pattern_learning(self, recursive_gamma):
        """Test pattern learning during recursion"""
        # Execute multiple recursive calls
        results = [recursive_gamma(i) for i in range(3, 8)]
        
        # Check patterns were learned
        assert len(recursive_gamma.pattern_history) > 0
        assert len(recursive_gamma.pattern_cache) > 0
        
        # Check pattern learning score
        assert recursive_gamma.metrics.pattern_learning_score >= 0.0
    
    def test_error_handling(self, recursive_alpha):
        """Test error handling in recursive execution"""
        # Create function that will cause error
        def error_func(n):
            if n == 0:
                raise ValueError("Test error")
            return error_func(n-1)
        
        error_recursive = QuantumRecursiveFunction(
            func=error_func,
            max_depth=5
        )
        
        # Should handle error gracefully
        with pytest.raises(RuntimeError):
            error_recursive(3)
    
    def test_performance_optimization(self, recursive_alpha, recursive_gamma):
        """Test performance optimization based on consciousness level"""
        # Execute same function at different consciousness levels
        alpha_recursive = recursive_alpha
        
        def test_func(n):
            return n if n <= 1 else test_func(n-1)
        
        gamma_recursive = QuantumRecursiveFunction(
            func=test_func,
            consciousness_level=ConsciousnessLevel.GAMMA,
            strategy=RecursionStrategy.CONSCIOUSNESS_OPTIMIZED
        )
        
        # Execute
        alpha_result = alpha_recursive(8)
        gamma_result = gamma_recursive(8)
        
        # Check consciousness optimization levels
        assert alpha_recursive.metrics.consciousness_optimization < gamma_recursive.metrics.consciousness_optimization
        
        # Check performance multiplier difference
        assert gamma_recursive.performance_multiplier > alpha_recursive.performance_multiplier
    
    def test_get_recursion_report(self, recursive_gamma):
        """Test recursion report generation"""
        # Execute recursion
        result = recursive_gamma(5)
        
        # Get report
        report = recursive_gamma.get_recursion_report()
        
        # Check report structure
        assert 'version' in report
        assert 'spec' in report
        assert 'strategy' in report
        assert 'consciousness_level' in report
        assert 'execution_state' in report
        assert 'metrics' in report
        assert 'quantum_state' in report
        assert 'pattern_learning' in report
        assert 'consciousness_optimization' in report
        assert 'memoization_efficiency' in report
        
        # Check report values
        assert report['version'] == '4.0.0'
        assert report['consciousness_level'] == ConsciousnessLevel.GAMMA.value
        assert report['strategy'] == RecursionStrategy.CONSCIOUSNESS_OPTIMIZED.value

class TestRecursiveFrameworkV4:
    """Test suite for RecursiveFrameworkV4 class"""
    
    @pytest.fixture
    def framework(self):
        """Create recursive framework for testing"""
        return RecursiveFrameworkV4(
            consciousness_level=ConsciousnessLevel.GAMMA,
            default_strategy=RecursionStrategy.CONSCIOUSNESS_OPTIMIZED,
            max_depth=15
        )
    
    def test_framework_initialization(self, framework):
        """Test recursive framework initialization"""
        assert framework.consciousness_level == ConsciousnessLevel.GAMMA
        assert framework.default_strategy == RecursionStrategy.CONSCIOUSNESS_OPTIMIZED
        assert framework.max_depth == 15
        assert framework.performance_multiplier == 12.5  # Gamma multiplier
        
        # Check quantum systems are initialized
        assert framework.quantum_field is not None
        assert framework.consciousness_protocol is not None
        
        # Check global systems
        assert isinstance(framework.global_patterns, dict)
        assert isinstance(framework.global_metrics, list)
    
    def test_make_recursive_function(self, framework):
        """Test making recursive function"""
        def test_func(n):
            return n if n <= 1 else test_func(n-1)
        
        # Make recursive function
        recursive_func = framework.make_recursive(
            func=test_func,
            strategy=RecursionStrategy.STANDARD,
            max_depth=10
        )
        
        # Check function properties
        assert isinstance(recursive_func, QuantumRecursiveFunction)
        assert recursive_func.strategy == RecursionStrategy.STANDARD
        assert recursive_func.max_depth == 10
        assert recursive_func.consciousness_level == framework.consciousness_level
        
        # Test execution
        result = recursive_func(5)
        assert result == 5
    
    def test_fibonacci_recursive(self, framework):
        """Test Fibonacci recursive calculation"""
        # Test small values
        assert framework.fibonacci_recursive(0) == 0
        assert framework.fibonacci_recursive(1) == 1
        assert framework.fibonacci_recursive(2) == 1
        assert framework.fibonacci_recursive(3) == 2
        assert framework.fibonacci_recursive(4) == 3
        assert framework.fibonacci_recursive(5) == 5
        
        # Test larger value (should work within depth limit)
        result = framework.fibonacci_recursive(8)
        assert result == 21
    
    def test_factorial_recursive(self, framework):
        """Test factorial recursive calculation"""
        # Test small values
        assert framework.factorial_recursive(0) == 1
        assert framework.factorial_recursive(1) == 1
        assert framework.factorial_recursive(2) == 2
        assert framework.factorial_recursive(3) == 6
        assert framework.factorial_recursive(4) == 24
        assert framework.factorial_recursive(5) == 120
    
    def test_quicksort_recursive(self, framework):
        """Test quicksort recursive algorithm"""
        # Test empty and single element
        assert framework.quicksort_recursive([]) == []
        assert framework.quicksort_recursive([5]) == [5]
        
        # Test small arrays
        result1 = framework.quicksort_recursive([3, 1, 4, 1, 5])
        assert result1 == [1, 1, 3, 4, 5]
        
        result2 = framework.quicksort_recursive([64, 34, 25, 12, 22, 11, 90])
        assert result2 == [11, 12, 22, 25, 34, 64, 90]
    
    def test_binary_search_recursive(self, framework):
        """Test binary search recursive algorithm"""
        test_array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        
        # Test found cases
        assert framework.binary_search_recursive(test_array, 1) == 0
        assert framework.binary_search_recursive(test_array, 7) == 3
        assert framework.binary_search_recursive(test_array, 19) == 9
        
        # Test not found case
        assert framework.binary_search_recursive(test_array, 8) == -1
        assert framework.binary_search_recursive(test_array, 0) == -1
    
    def test_create_quantum_fibonacci(self, framework):
        """Test creating quantum Fibonacci function"""
        quantum_fib = framework.create_quantum_fibonacci()
        
        # Test execution
        result = quantum_fib(10)
        assert result == 55  # Fibonacci(10)
        
        # Check function is callable
        assert callable(quantum_fib)
    
    def test_create_quantum_quicksort(self, framework):
        """Test creating quantum quicksort function"""
        quantum_sort = framework.create_quantum_quicksort()
        
        # Test execution
        test_array = [64, 34, 25, 12, 22, 11, 90]
        result = quantum_sort(test_array)
        assert result == [11, 12, 22, 25, 34, 64, 90]
        
        # Check function is callable
        assert callable(quantum_sort)
    
    def test_benchmark_recursive_functions(self, framework):
        """Test benchmarking recursive functions"""
        # Run benchmark
        benchmark_results = framework.benchmark_recursive_functions()
        
        # Check results structure
        assert 'fibonacci' in benchmark_results
        assert 'quicksort' in benchmark_results
        assert 'binary_search' in benchmark_results
        
        # Check individual results
        fib_result = benchmark_results['fibonacci']
        assert 'result' in fib_result
        assert 'execution_time' in fib_result
        assert 'performance_multiplier' in fib_result
        assert isinstance(fib_result['result'], int)
        assert isinstance(fib_result['execution_time'], float)
        
        sort_result = benchmark_results['quicksort']
        assert 'result' in sort_result
        assert isinstance(sort_result['result'], list)
        
        search_result = benchmark_results['binary_search']
        assert 'result' in search_result
        assert isinstance(search_result['result'], int)
    
    def test_get_framework_report(self, framework):
        """Test framework report generation"""
        # Execute some functions to generate data
        framework.fibonacci_recursive(8)
        framework.quicksort_recursive([3, 1, 4, 1, 5])
        
        # Get report
        report = framework.get_framework_report()
        
        # Check report structure
        assert 'version' in report
        assert 'spec' in report
        assert 'timestamp' in report
        assert 'configuration' in report
        assert 'quantum_systems' in report
        assert 'pattern_learning' in report
        assert 'capabilities' in report
        
        # Check configuration
        config = report['configuration']
        assert 'consciousness_level' in config
        assert 'default_strategy' in config
        assert 'max_depth' in config
        assert 'performance_multiplier' in config
        
        # Check capabilities
        capabilities = report['capabilities']
        assert 'recursion_strategies' in capabilities
        assert 'quantum_awareness' in capabilities
        assert 'consciousness_optimization' in capabilities
        assert isinstance(capabilities['quantum_awareness'], bool)
    
    def test_consciousness_level_integration(self, framework):
        """Test integration with different consciousness levels"""
        # Test with different levels
        for level in [ConsciousnessLevel.ALPHA, ConsciousnessLevel.BETA, ConsciousnessLevel.GAMMA]:
            fw = RecursiveFrameworkV4(
                consciousness_level=level,
                max_depth=8
            )
            
            # Create and test function
            recursive_func = fw.make_recursive(
                fw.fibonacci_recursive,
                max_depth=6
            )
            
            result = recursive_func(5)
            assert result == 5
            
            # Check performance multiplier
            assert fw.performance_multiplier > 1.0

class TestRecursionStrategies:
    """Test suite for different recursion strategies"""
    
    @pytest.fixture
    def test_func(self):
        """Test function for strategy testing"""
        def fib_func(n):
            if n <= 1:
                return n
            return fib_func(n-1) + fib_func(n-2)
        return fib_func
    
    def test_standard_strategy(self, test_func):
        """Test standard recursion strategy"""
        recursive = QuantumRecursiveFunction(
            func=test_func,
            strategy=RecursionStrategy.STANDARD,
            max_depth=10
        )
        
        result = recursive(6)
        assert result == 8
        assert recursive.strategy == RecursionStrategy.STANDARD
    
    def test_memoization_strategy(self, test_func):
        """Test memoization recursion strategy"""
        recursive = QuantumRecursiveFunction(
            func=test_func,
            strategy=RecursionStrategy.MEMOIZATION,
            max_depth=10
        )
        
        result = recursive(7)
        assert result == 13
        assert recursive.strategy == RecursionStrategy.MEMOIZATION
        assert recursive.metrics.memoization_hit_rate >= 0.0
    
    def test_tail_optimization_strategy(self, test_func):
        """Test tail optimization recursion strategy"""
        recursive = QuantumRecursiveFunction(
            func=test_func,
            strategy=RecursionStrategy.TAIL_OPTIMIZATION,
            max_depth=10
        )
        
        result = recursive(5)
        assert result == 5
        assert recursive.strategy == RecursionStrategy.TAIL_OPTIMIZATION
    
    def test_quantum_parallel_strategy(self, test_func):
        """Test quantum parallel recursion strategy"""
        recursive = QuantumRecursiveFunction(
            func=test_func,
            strategy=RecursionStrategy.QUANTUM_PARALLEL,
            max_depth=10,
            quantum_awareness=True
        )
        
        result = recursive(4)
        assert result == 3
        assert recursive.strategy == RecursionStrategy.QUANTUM_PARALLEL
    
    def test_consciousness_optimized_strategy(self, test_func):
        """Test consciousness optimized recursion strategy"""
        recursive = QuantumRecursiveFunction(
            func=test_func,
            strategy=RecursionStrategy.CONSCIOUSNESS_OPTIMIZED,
            max_depth=10,
            consciousness_level=ConsciousnessLevel.GAMMA
        )
        
        result = recursive(5)
        assert result == 5
        assert recursive.strategy == RecursionStrategy.CONSCIOUSNESS_OPTIMIZED
        assert recursive.metrics.consciousness_optimization > 0.0

class TestRecursionEnums:
    """Test suite for recursion-related enums"""
    
    def test_recursion_strategy_values(self):
        """Test recursion strategy enum values"""
        expected_values = [
            "standard",
            "memoization", 
            "tail_optimization",
            "quantum_parallel",
            "consciousness_optimized"
        ]
        
        actual_values = [strategy.value for strategy in RecursionStrategy]
        
        for expected_value in expected_values:
            assert expected_value in actual_values
    
    def test_recursion_termination_type_values(self):
        """Test recursion termination type enum values"""
        expected_values = [
            "depth_limit",
            "convergence",
            "solution_found", 
            "timeout",
            "quantum_state",
            "consciousness_level"
        ]
        
        actual_values = [term_type.value for term_type in RecursionTerminationType]
        
        for expected_value in expected_values:
            assert expected_value in actual_values

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

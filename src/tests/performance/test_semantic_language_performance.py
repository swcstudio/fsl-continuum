"""
FSL Continuum - Semantic Language Performance Tests

Complete performance tests and benchmarking for BAML and Pareto-Lang
semantic languages with XML transformation support and AI integration.
"""

import unittest
import time
import psutil
import os
import concurrent.futures
import json
from pathlib import Path

# Test fixtures
from src.tests.test_framework.test_data_manager import TestDataManager
from src.tests.test_framework.mock_components import MockComponents

# Import semantic language components
try:
    from src.semantic_languages.baml import BAMLParser
    from src.semantic_languages.pareto_lang import ParetoLangParser
    from src.semantic_languages.xml_processor import UnifiedXMLProcessor
    from src.semantic_languages.ai_integration import SemanticAIProcessor
except ImportError:
    # Fallback for direct testing
    import sys
    sys.path.insert(0, 'src')
    from semantic_languages.baml import BAMLParser
    from semantic_languages.pareto_lang import ParetoLangParser
    from semantic_languages.xml_processor import UnifiedXMLProcessor
    from semantic_languages.ai_integration import SemanticAIProcessor


class TestSemanticLanguagePerformance(unittest.TestCase):
    """Complete performance tests for semantic language processing."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.baml_parser = BAMLParser()
        self.pareto_parser = ParetoLangParser()
        self.xml_processor = UnifiedXMLProcessor()
        self.ai_processor = SemanticAIProcessor()
        
        self.test_data_manager = TestDataManager()
        self.mock_components = MockComponents()
        
        # Performance thresholds
        self.baml_parsing_threshold = 0.1  # 100ms per document
        self.pareto_lang_parsing_threshold = 0.1  # 100ms per document
        self.xml_transformation_threshold = 0.5  # 500ms per transformation
        self.ai_processing_threshold = 2.0  # 2 seconds per AI operation
        
        self.baml_parsing_memory_threshold = 50  # 50MB
        self.pareto_lang_parsing_memory_threshold = 50  # 50MB
        self.xml_transformation_memory_threshold = 100  # 100MB
        self.ai_processing_memory_threshold = 200  # 200MB
        
        # Generate test data
        self.small_baml_data = self.generate_baml_data(10)
        self.medium_baml_data = self.generate_baml_data(100)
        self.large_baml_data = self.generate_baml_data(1000)
        
        self.small_pareto_data = self.generate_pareto_data(10)
        self.medium_pareto_data = self.generate_pareto_data(100)
        self.large_pareto_data = self.generate_pareto_data(1000)
        
        # Performance tracking
        self.performance_metrics = {
            'baml_parsing': [],
            'pareto_lang_parsing': [],
            'xml_transformation': [],
            'ai_processing': [],
            'concurrent_processing': []
        }
    
    def generate_baml_data(self, boundary_count):
        """Generate BAML test data with specified boundary count."""
        data = {
            "version": "1.0.0-fsl-integration",
            "spec": "BAML-SEMANTIC-001",
            "description": f"BAML performance test data with {boundary_count} boundaries",
            "boundaries": [],
            "connections": [],
            "constraints": []
        }
        
        for i in range(boundary_count):
            boundary = {
                "name": f"perf_boundary_{i}",
                "type": "data" if i % 3 == 0 else "process" if i % 3 == 1 else "system",
                "ai_enhanced": i % 4 == 0,
                "constraints": [
                    {
                        "type": "validation",
                        "operator": "contains",
                        "value": f"performance_constraint_{i}",
                        "ai_enforced": i % 5 == 0
                    }
                ],
                "metadata": {
                    "created_at": "2025-01-22T12:00:00Z",
                    "priority": (i % 10) + 1,
                    "owner": "performance_test"
                }
            }
            data["boundaries"].append(boundary)
            
            # Add connections (sparse)
            if i > 0 and i % 3 == 0:
                connection = {
                    "source": f"perf_boundary_{i-1}",
                    "target": f"perf_boundary_{i}",
                    "type": "data_flow" if i % 2 == 0 else "control_flow",
                    "direction": "unidirectional",
                    "priority": (i % 10) + 1,
                    "weight": 0.5 + (i % 5) * 0.1
                }
                data["connections"].append(connection)
        
        return data
    
    def generate_pareto_data(self, optimization_count):
        """Generate Pareto-Lang test data with specified optimization count."""
        data = {
            "version": "1.0.0-fsl-integration",
            "spec": "PARETO-SEMANTIC-001",
            "description": f"Pareto-Lang performance test data with {optimization_count} optimizations",
            "optimizations": [],
            "constraints": []
        }
        
        for i in range(optimization_count):
            optimization = {
                "name": f"perf_optimization_{i}",
                "type": "pareto",
                "target": "efficiency_maximization" if i % 2 == 0 else "resource_minimization",
                "efficiency": 0.5 + (i * 0.001) % 0.5,
                "constraints": [
                    {
                        "type": "performance",
                        "operator": ">=",
                        "value": f"min_efficiency_{i}",
                        "ai_enforced": i % 3 == 0
                    }
                ],
                "metadata": {
                    "created_at": "2025-01-22T12:00:00Z",
                    "priority": (i % 10) + 1,
                    "owner": "performance_test"
                }
            }
            data["optimizations"].append(optimization)
        
        return data
    
    def track_performance(self, operation, start_time, end_time, memory_before, memory_after, **kwargs):
        """Track performance metrics."""
        execution_time = end_time - start_time
        memory_used = memory_after - memory_before
        
        metric = {
            'operation': operation,
            'execution_time': execution_time,
            'memory_used': memory_used,
            'timestamp': time.time()
        }
        metric.update(kwargs)
        
        self.performance_metrics[operation].append(metric)
        
        return metric
    
    def test_baml_parsing_performance_small(self):
        """Test BAML parsing performance with small dataset."""
        process = psutil.Process(os.getpid())
        
        # Memory before
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        
        # Parse small BAML data 100 times
        for _ in range(100):
            result = self.baml_parser.parse(self.small_baml_data)
            self.assertTrue(result.success)
        
        end_time = time.time()
        
        # Memory after
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        
        metric = self.track_performance(
            'baml_parsing', start_time, end_time, memory_before, memory_after,
            dataset_size='small', iterations=100, boundaries_per_doc=10
        )
        
        # Performance assertions
        self.assertLess(metric['execution_time'], 2.0)  # Should complete in under 2 seconds
        self.assertLess(metric['memory_used'], self.baml_parsing_memory_threshold)
        
        # Rate assertions
        parsing_rate = (100 * 10) / metric['execution_time']  # boundaries/second
        self.assertGreater(parsing_rate, 100)  # Should parse at least 100 boundaries/second
        
        print(f"Small BAML Parsing Performance:")
        print(f"  Execution Time: {metric['execution_time']:.3f} seconds")
        print(f"  Memory Used: {metric['memory_used']:.2f} MB")
        print(f"  Boundaries/sec: {parsing_rate:.2f}")
    
    def test_baml_parsing_performance_medium(self):
        """Test BAML parsing performance with medium dataset."""
        process = psutil.Process(os.getpid())
        
        # Memory before
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        
        # Parse medium BAML data 10 times
        for _ in range(10):
            result = self.baml_parser.parse(self.medium_baml_data)
            self.assertTrue(result.success)
        
        end_time = time.time()
        
        # Memory after
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        
        metric = self.track_performance(
            'baml_parsing', start_time, end_time, memory_before, memory_after,
            dataset_size='medium', iterations=10, boundaries_per_doc=100
        )
        
        # Performance assertions
        self.assertLess(metric['execution_time'], 1.0)  # Should complete in under 1 second
        self.assertLess(metric['memory_used'], self.baml_parsing_memory_threshold)
        
        # Rate assertions
        parsing_rate = (10 * 100) / metric['execution_time']  # boundaries/second
        self.assertGreater(parsing_rate, 500)  # Should parse at least 500 boundaries/second
        
        print(f"Medium BAML Parsing Performance:")
        print(f"  Execution Time: {metric['execution_time']:.3f} seconds")
        print(f"  Memory Used: {metric['memory_used']:.2f} MB")
        print(f"  Boundaries/sec: {parsing_rate:.2f}")
    
    def test_baml_parsing_performance_large(self):
        """Test BAML parsing performance with large dataset."""
        process = psutil.Process(os.getpid())
        
        # Memory before
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        
        # Parse large BAML data 1 time
        result = self.baml_parser.parse(self.large_baml_data)
        self.assertTrue(result.success)
        
        end_time = time.time()
        
        # Memory after
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        
        metric = self.track_performance(
            'baml_parsing', start_time, end_time, memory_before, memory_after,
            dataset_size='large', iterations=1, boundaries_per_doc=1000
        )
        
        # Performance assertions
        self.assertLess(metric['execution_time'], 2.0)  # Should complete in under 2 seconds
        self.assertLess(metric['memory_used'], self.baml_parsing_memory_threshold)
        
        # Rate assertions
        parsing_rate = 1000 / metric['execution_time']  # boundaries/second
        self.assertGreater(parsing_rate, 200)  # Should parse at least 200 boundaries/second
        
        print(f"Large BAML Parsing Performance:")
        print(f"  Execution Time: {metric['execution_time']:.3f} seconds")
        print(f"  Memory Used: {metric['memory_used']:.2f} MB")
        print(f"  Boundaries/sec: {parsing_rate:.2f}")
    
    def test_pareto_lang_parsing_performance_small(self):
        """Test Pareto-Lang parsing performance with small dataset."""
        process = psutil.Process(os.getpid())
        
        # Memory before
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        
        # Parse small Pareto-Lang data 100 times
        for _ in range(100):
            result = self.pareto_parser.parse(self.small_pareto_data)
            self.assertTrue(result.success)
        
        end_time = time.time()
        
        # Memory after
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        
        metric = self.track_performance(
            'pareto_lang_parsing', start_time, end_time, memory_before, memory_after,
            dataset_size='small', iterations=100, optimizations_per_doc=10
        )
        
        # Performance assertions
        self.assertLess(metric['execution_time'], 2.0)  # Should complete in under 2 seconds
        self.assertLess(metric['memory_used'], self.pareto_lang_parsing_memory_threshold)
        
        # Rate assertions
        parsing_rate = (100 * 10) / metric['execution_time']  # optimizations/second
        self.assertGreater(parsing_rate, 100)  # Should parse at least 100 optimizations/second
        
        print(f"Small Pareto-Lang Parsing Performance:")
        print(f"  Execution Time: {metric['execution_time']:.3f} seconds")
        print(f"  Memory Used: {metric['memory_used']:.2f} MB")
        print(f"  Optimizations/sec: {parsing_rate:.2f}")
    
    def test_pareto_lang_parsing_performance_medium(self):
        """Test Pareto-Lang parsing performance with medium dataset."""
        process = psutil.Process(os.getpid())
        
        # Memory before
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        
        # Parse medium Pareto-Lang data 10 times
        for _ in range(10):
            result = self.pareto_parser.parse(self.medium_pareto_data)
            self.assertTrue(result.success)
        
        end_time = time.time()
        
        # Memory after
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        
        metric = self.track_performance(
            'pareto_lang_parsing', start_time, end_time, memory_before, memory_after,
            dataset_size='medium', iterations=10, optimizations_per_doc=100
        )
        
        # Performance assertions
        self.assertLess(metric['execution_time'], 1.0)  # Should complete in under 1 second
        self.assertLess(metric['memory_used'], self.pareto_lang_parsing_memory_threshold)
        
        # Rate assertions
        parsing_rate = (10 * 100) / metric['execution_time']  # optimizations/second
        self.assertGreater(parsing_rate, 500)  # Should parse at least 500 optimizations/second
        
        print(f"Medium Pareto-Lang Parsing Performance:")
        print(f"  Execution Time: {metric['execution_time']:.3f} seconds")
        print(f"  Memory Used: {metric['memory_used']:.2f} MB")
        print(f"  Optimizations/sec: {parsing_rate:.2f}")
    
    def test_pareto_lang_parsing_performance_large(self):
        """Test Pareto-Lang parsing performance with large dataset."""
        process = psutil.Process(os.getpid())
        
        # Memory before
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        
        # Parse large Pareto-Lang data 1 time
        result = self.pareto_parser.parse(self.large_pareto_data)
        self.assertTrue(result.success)
        
        end_time = time.time()
        
        # Memory after
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        
        metric = self.track_performance(
            'pareto_lang_parsing', start_time, end_time, memory_before, memory_after,
            dataset_size='large', iterations=1, optimizations_per_doc=1000
        )
        
        # Performance assertions
        self.assertLess(metric['execution_time'], 2.0)  # Should complete in under 2 seconds
        self.assertLess(metric['memory_used'], self.pareto_lang_parsing_memory_threshold)
        
        # Rate assertions
        parsing_rate = 1000 / metric['execution_time']  # optimizations/second
        self.assertGreater(parsing_rate, 200)  # Should parse at least 200 optimizations/second
        
        print(f"Large Pareto-Lang Parsing Performance:")
        print(f"  Execution Time: {metric['execution_time']:.3f} seconds")
        print(f"  Memory Used: {metric['memory_used']:.2f} MB")
        print(f"  Optimizations/sec: {parsing_rate:.2f}")
    
    def test_xml_transformation_performance(self):
        """Test XML transformation performance."""
        process = psutil.Process(os.getpid())
        
        # Memory before
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        
        # Transform medium data to XML 10 times
        for _ in range(10):
            result = self.xml_processor.process_multiple_semantic_data_with_xml({
                "baml": self.medium_baml_data,
                "pareto_lang": self.medium_pareto_data
            })
            self.assertTrue(result.success)
        
        end_time = time.time()
        
        # Memory after
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        
        metric = self.track_performance(
            'xml_transformation', start_time, end_time, memory_before, memory_after,
            dataset_size='medium', iterations=10, boundaries_per_doc=100, optimizations_per_doc=100
        )
        
        # Performance assertions
        self.assertLess(metric['execution_time'], 5.0)  # Should complete in under 5 seconds
        self.assertLess(metric['memory_used'], self.xml_transformation_memory_threshold)
        
        # Rate assertions
        transformation_rate = 10 / metric['execution_time']  # documents/second
        self.assertGreater(transformation_rate, 2.0)  # Should transform at least 2 docs/second
        
        print(f"XML Transformation Performance:")
        print(f"  Execution Time: {metric['execution_time']:.3f} seconds")
        print(f"  Memory Used: {metric['memory_used']:.2f} MB")
        print(f"  Documents/sec: {transformation_rate:.2f}")
    
    def test_ai_processing_performance(self):
        """Test AI processing performance."""
        process = psutil.Process(os.getpid())
        
        # Memory before
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        
        # Process medium data with AI 5 times
        for _ in range(5):
            result = self.ai_processor.process_semantic_languages({
                "baml": self.medium_baml_data,
                "pareto_lang": self.medium_pareto_data
            })
            self.assertTrue(result.success)
        
        end_time = time.time()
        
        # Memory after
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        
        metric = self.track_performance(
            'ai_processing', start_time, end_time, memory_before, memory_after,
            dataset_size='medium', iterations=5, boundaries_per_doc=100, optimizations_per_doc=100
        )
        
        # Performance assertions
        self.assertLess(metric['execution_time'], 10.0)  # Should complete in under 10 seconds
        self.assertLess(metric['memory_used'], self.ai_processing_memory_threshold)
        
        # Rate assertions
        processing_rate = 5 / metric['execution_time']  # documents/second
        self.assertGreater(processing_rate, 0.5)  # Should process at least 0.5 docs/second
        
        print(f"AI Processing Performance:")
        print(f"  Execution Time: {metric['execution_time']:.3f} seconds")
        print(f"  Memory Used: {metric['memory_used']:.2f} MB")
        print(f"  Documents/sec: {processing_rate:.2f}")
    
    def test_concurrent_processing_performance(self):
        """Test concurrent processing performance."""
        process = psutil.Process(os.getpid())
        
        def process_baml():
            return self.baml_parser.parse(self.small_baml_data)
        
        def process_pareto_lang():
            return self.pareto_parser.parse(self.small_pareto_data)
        
        def process_multi_language():
            return self.xml_processor.process_multiple_semantic_data_with_xml({
                "baml": self.small_baml_data,
                "pareto_lang": self.small_pareto_data
            })
        
        def process_ai():
            return self.ai_processor.process_semantic_languages({
                "baml": self.small_baml_data,
                "pareto_lang": self.small_pareto_data
            })
        
        # Memory before
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        
        # Run concurrent processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            
            # Submit concurrent tasks
            for _ in range(5):  # 5 rounds of concurrent processing
                futures.append(executor.submit(process_baml))
                futures.append(executor.submit(process_pareto_lang))
                futures.append(executor.submit(process_multi_language))
                futures.append(executor.submit(process_ai))
            
            # Collect results
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        end_time = time.time()
        
        # Memory after
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        
        metric = self.track_performance(
            'concurrent_processing', start_time, end_time, memory_before, memory_after,
            dataset_size='small', rounds=5, tasks_per_round=4, total_tasks=20
        )
        
        # All results should be successful
        for i, result in enumerate(results):
            self.assertTrue(result.success, f"Result {i} should be successful")
        
        # Performance assertions
        self.assertLess(metric['execution_time'], 8.0)  # Should complete in under 8 seconds
        self.assertLess(metric['memory_used'], 200)  # Should use less than 200MB
        
        # Rate assertions
        processing_rate = 20 / metric['execution_time']  # tasks/second
        concurrency_efficiency = processing_rate / 4  # efficiency relative to 4 workers
        
        self.assertGreater(processing_rate, 2.5)  # Should process at least 2.5 tasks/second
        self.assertGreater(concurrency_efficiency, 0.6)  # Should have at least 60% efficiency
        
        print(f"Concurrent Processing Performance:")
        print(f"  Execution Time: {metric['execution_time']:.3f} seconds")
        print(f"  Memory Used: {metric['memory_used']:.2f} MB")
        print(f"  Tasks/sec: {processing_rate:.2f}")
        print(f"  Concurrency Efficiency: {concurrency_efficiency:.2f}")
    
    def test_memory_efficiency_large_data(self):
        """Test memory efficiency with large data processing."""
        process = psutil.Process(os.getpid())
        
        # Generate very large data
        very_large_baml = self.generate_baml_data(5000)
        very_large_pareto = self.generate_pareto_data(5000)
        
        # Memory before
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        
        # Process large data
        result = self.xml_processor.process_multiple_semantic_data_with_xml({
            "baml": very_large_baml,
            "pareto_lang": very_large_pareto
        })
        
        end_time = time.time()
        
        # Memory after
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        
        metric = self.track_performance(
            'xml_transformation', start_time, end_time, memory_before, memory_after,
            dataset_size='very_large', iterations=1, boundaries_per_doc=5000, optimizations_per_doc=5000
        )
        
        self.assertTrue(result.success)
        
        # Memory efficiency assertions
        self.assertLess(metric['memory_used'], 500)  # Should use less than 500MB
        self.assertLess(metric['execution_time'], 15.0)  # Should complete in under 15 seconds
        
        # Calculate efficiency
        total_elements = 10000  # 5000 boundaries + 5000 optimizations
        memory_per_element = metric['memory_used'] / total_elements  # MB per element
        
        self.assertLess(memory_per_element, 0.05)  # Should use less than 0.05MB per element
        
        print(f"Large Data Memory Efficiency:")
        print(f"  Execution Time: {metric['execution_time']:.3f} seconds")
        print(f"  Memory Used: {metric['memory_used']:.2f} MB")
        print(f"  Total Elements: {total_elements}")
        print(f"  Memory per Element: {memory_per_element:.6f} MB")
        print(f"  Elements/sec: {total_elements / metric['execution_time']:.2f}")
    
    def test_performance_regression_detection(self):
        """Test performance regression detection."""
        # Define baseline performance metrics
        baseline_metrics = {
            'small_baml_parsing': {'execution_time': 0.5, 'memory_used': 20},
            'medium_baml_parsing': {'execution_time': 0.8, 'memory_used': 40},
            'small_pareto_parsing': {'execution_time': 0.5, 'memory_used': 20},
            'medium_pareto_parsing': {'execution_time': 0.8, 'memory_used': 40},
            'xml_transformation': {'execution_time': 2.0, 'memory_used': 80},
            'concurrent_processing': {'execution_time': 4.0, 'memory_used': 150}
        }
        
        # Collect current performance metrics
        current_metrics = {}
        
        # Test small BAML parsing
        start_time = time.time()
        for _ in range(50):
            self.baml_parser.parse(self.small_baml_data)
        execution_time = time.time() - start_time
        
        process = psutil.Process(os.getpid())
        memory_used = process.memory_info().rss / 1024 / 1024  # MB
        
        current_metrics['small_baml_parsing'] = {
            'execution_time': execution_time,
            'memory_used': memory_used
        }
        
        # Test medium BAML parsing
        start_time = time.time()
        for _ in range(5):
            self.baml_parser.parse(self.medium_baml_data)
        execution_time = time.time() - start_time
        
        current_metrics['medium_baml_parsing'] = {
            'execution_time': execution_time,
            'memory_used': memory_used
        }
        
        # Test small Pareto-Lang parsing
        start_time = time.time()
        for _ in range(50):
            self.pareto_parser.parse(self.small_pareto_data)
        execution_time = time.time() - start_time
        
        current_metrics['small_pareto_parsing'] = {
            'execution_time': execution_time,
            'memory_used': memory_used
        }
        
        # Test medium Pareto-Lang parsing
        start_time = time.time()
        for _ in range(5):
            self.pareto_parser.parse(self.medium_pareto_data)
        execution_time = time.time() - start_time
        
        current_metrics['medium_pareto_parsing'] = {
            'execution_time': execution_time,
            'memory_used': memory_used
        }
        
        # Test XML transformation
        start_time = time.time()
        for _ in range(3):
            self.xml_processor.process_multiple_semantic_data_with_xml({
                "baml": self.medium_baml_data,
                "pareto_lang": self.medium_pareto_data
            })
        execution_time = time.time() - start_time
        
        current_metrics['xml_transformation'] = {
            'execution_time': execution_time,
            'memory_used': memory_used
        }
        
        # Test concurrent processing
        def process_concurrent():
            self.xml_processor.process_multiple_semantic_data_with_xml({
                "baml": self.small_baml_data,
                "pareto_lang": self.small_pareto_data
            })
        
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(process_concurrent) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        execution_time = time.time() - start_time
        
        current_metrics['concurrent_processing'] = {
            'execution_time': execution_time,
            'memory_used': memory_used
        }
        
        # Check for performance regressions (10% tolerance)
        regression_detected = False
        
        for metric_name, baseline in baseline_metrics.items():
            if metric_name in current_metrics:
                current = current_metrics[metric_name]
                
                # Check execution time regression
                execution_time_regression = current['execution_time'] > baseline['execution_time'] * 1.1
                
                # Check memory usage regression
                memory_regression = current['memory_used'] > baseline['memory_used'] * 1.1
                
                if execution_time_regression or memory_regression:
                    regression_detected = True
                    
                    print(f"PERFORMANCE REGRESSION DETECTED in {metric_name}:")
                    if execution_time_regression:
                        print(f"  Execution Time: {current['execution_time']:.3f}s (baseline: {baseline['execution_time']:.3f}s)")
                    if memory_regression:
                        print(f"  Memory Usage: {current['memory_used']:.2f}MB (baseline: {baseline['memory_used']:.2f}MB)")
        
        # Regression assertions
        self.assertFalse(regression_detected, "Performance regression detected!")
        
        print("Performance Regression Detection:")
        print(f"  Regression Detected: {regression_detected}")
        if not regression_detected:
            print("  ✅ No performance regressions detected")
    
    def test_performance_benchmarking(self):
        """Test comprehensive performance benchmarking."""
        # Collect performance metrics for all operations
        benchmark_results = {}
        
        # BAML parsing benchmark
        baml_times = []
        for _ in range(10):
            start_time = time.time()
            self.baml_parser.parse(self.large_baml_data)
            baml_times.append(time.time() - start_time)
        
        benchmark_results['baml_parsing'] = {
            'mean': sum(baml_times) / len(baml_times),
            'min': min(baml_times),
            'max': max(baml_times),
            'std': (sum((x - sum(baml_times)/len(baml_times))**2 for x in baml_times) / len(baml_times))**0.5
        }
        
        # Pareto-Lang parsing benchmark
        pareto_times = []
        for _ in range(10):
            start_time = time.time()
            self.pareto_parser.parse(self.large_pareto_data)
            pareto_times.append(time.time() - start_time)
        
        benchmark_results['pareto_lang_parsing'] = {
            'mean': sum(pareto_times) / len(pareto_times),
            'min': min(pareto_times),
            'max': max(pareto_times),
            'std': (sum((x - sum(pareto_times)/len(pareto_times))**2 for x in pareto_times) / len(pareto_times))**0.5
        }
        
        # XML transformation benchmark
        xml_times = []
        for _ in range(5):
            start_time = time.time()
            self.xml_processor.process_multiple_semantic_data_with_xml({
                "baml": self.large_baml_data,
                "pareto_lang": self.large_pareto_data
            })
            xml_times.append(time.time() - start_time)
        
        benchmark_results['xml_transformation'] = {
            'mean': sum(xml_times) / len(xml_times),
            'min': min(xml_times),
            'max': max(xml_times),
            'std': (sum((x - sum(xml_times)/len(xml_times))**2 for x in xml_times) / len(xml_times))**0.5
        }
        
        # Print benchmark results
        print("Performance Benchmarking Results:")
        print("=" * 60)
        
        for operation, metrics in benchmark_results.items():
            print(f"\n{operation.replace('_', ' ').title()}:")
            print(f"  Mean: {metrics['mean']:.3f}s")
            print(f"  Min:  {metrics['min']:.3f}s")
            print(f"  Max:  {metrics['max']:.3f}s")
            print(f"  Std:  {metrics['std']:.3f}s")
        
        # Performance assertions
        self.assertLess(benchmark_results['baml_parsing']['mean'], 1.0)
        self.assertLess(benchmark_results['pareto_lang_parsing']['mean'], 1.0)
        self.assertLess(benchmark_results['xml_transformation']['mean'], 3.0)
        
        # Stability assertions (standard deviation should be small)
        self.assertLess(benchmark_results['baml_parsing']['std'], 0.1)
        self.assertLess(benchmark_results['pareto_lang_parsing']['std'], 0.1)
        self.assertLess(benchmark_results['xml_transformation']['std'], 0.2)
    
    def tearDown(self):
        """Clean up after tests."""
        # Save performance metrics to file
        performance_file = Path('performance_metrics.json')
        with open(performance_file, 'w') as f:
            json.dump(self.performance_metrics, f, indent=2)
        
        print(f"Performance metrics saved to: {performance_file}")


if __name__ == '__main__':
    unittest.main()

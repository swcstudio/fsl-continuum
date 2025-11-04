"""
Unit tests for Performance Benchmark module.
"""

import unittest
import tempfile
import json
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from fsl_continuum.performance_benchmark import (
    PerformanceBenchmark, BenchmarkResult, MetricsCollector,
    VelocityMetrics, BenchmarkMetric
)


class TestMetricsCollector(unittest.TestCase):
    """Test cases for MetricsCollector."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.collector = MetricsCollector()
    
    def test_initialization(self):
        """Test collector initialization."""
        self.assertIsInstance(self.collector, MetricsCollector)
        self.assertFalse(self.collector.monitoring)
        self.assertEqual(len(self.collector.system_samples), 0)
        self.assertIsNone(self.collector.start_time)
        self.assertIsNone(self.collector.end_time)
    
    def test_start_monitoring(self):
        """Test starting performance monitoring."""
        self.collector.start_monitoring()
        
        self.assertTrue(self.collector.monitoring)
        self.assertIsNotNone(self.collector.start_time)
        self.assertEqual(len(self.collector.system_samples), 0)  # Starts empty
        
        # Stop monitoring to clean up
        self.collector.stop_monitoring()
    
    def test_stop_monitoring(self):
        """Test stopping performance monitoring."""
        self.collector.start_monitoring()
        time.sleep(0.1)  # Let it collect some data
        
        self.collector.stop_monitoring()
        
        self.assertFalse(self.collector.monitoring)
        self.assertIsNotNone(self.collector.end_time)
        self.assertGreater(len(self.collector.system_samples), 0)
    
    def test_get_average_metrics(self):
        """Test calculating average metrics."""
        # Start and let collect some data
        self.collector.start_monitoring()
        time.sleep(0.1)
        self.collector.stop_monitoring()
        
        avg_metrics = self.collector.get_average_metrics()
        
        self.assertIsInstance(avg_metrics, dict)
        if avg_metrics:  # Only test if data was collected
            self.assertIn('cpu_percent', avg_metrics)
            self.assertIn('memory_mb', avg_metrics)
            self.assertIsInstance(avg_metrics['cpu_percent'], (int, float))
    
    def test_get_peak_metrics(self):
        """Test getting peak metrics."""
        self.collector.start_monitoring()
        time.sleep(0.1)
        self.collector.stop_monitoring()
        
        peak_metrics = self.collector.get_peak_metrics()
        
        self.assertIsInstance(peak_metrics, dict)
        if peak_metrics:
            self.assertIn('peak_cpu_percent', peak_metrics)
            self.assertIn('peak_memory_mb', peak_metrics)


class TestPerformanceBenchmark(unittest.TestCase):
    """Test cases for PerformanceBenchmark."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.benchmark = PerformanceBenchmark()
    
    def test_initialization(self):
        """Test benchmark initialization."""
        self.assertIsInstance(self.benchmark, PerformanceBenchmark)
        self.assertIsInstance(self.benchmark.metrics_collector, MetricsCollector)
        self.assertIsInstance(self.benchmark.benchmark_results, list)
        self.assertEqual(len(self.benchmark.benchmark_results), 0)
    
    def test_benchmark_test_execution(self):
        """Test benchmark test execution."""
        def dummy_test_function():
            """Dummy test function to benchmark."""
            time.sleep(0.01)  # Simulate some work
            return "test_result"
        
        result = self.benchmark.benchmark_test_execution(
            dummy_test_function,
            'test_function',
            iterations=2
        )
        
        self.assertIsInstance(result, BenchmarkResult)
        self.assertEqual(result.test_name, 'test_function')
        self.assertTrue(result.passed)
        self.assertEqual(len(result.errors), 0)
        self.assertGreater(result.duration, 0)
        self.assertGreater(len(result.metrics), 0)
        
        # Check system info
        self.assertIsInstance(result.system_info, dict)
        self.assertIn('cpu_count', result.system_info)
    
    def test_benchmark_test_execution_with_failure(self):
        """Test benchmark execution with failing test."""
        def failing_test_function():
            """Failing test function."""
            raise ValueError("Test failure")
        
        result = self.benchmark.benchmark_test_execution(
            failing_test_function,
            'failing_function',
            iterations=1
        )
        
        self.assertIsInstance(result, BenchmarkResult)
        self.assertEqual(result.test_name, 'failing_function')
        self.assertFalse(result.passed)
        self.assertGreater(len(result.errors), 0)
        self.assertIn("Test failure", str(result.errors[0]))
    
    def test_benchmark_terminal_velocity(self):
        """Test terminal velocity benchmarking."""
        # Mock subprocess to avoid actual test execution
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.stdout = "5 passed in 0.50s"
            mock_result.returncode = 0
            mock_run.return_value = mock_result
            
            velocity = self.benchmark.benchmark_terminal_velocity(
                'src/tests/unit/',
                'python -m pytest src/tests/unit/ --tb=short -q'
            )
            
            self.assertIsInstance(velocity, VelocityMetrics)
            self.assertGreater(velocity.throughput, 0)
            self.assertGreater(velocity.latency, 0)
            self.assertGreaterEqual(velocity.efficiency, 0)
            self.assertLessEqual(velocity.flow_state_score, 100)
    
    def test_benchmark_terminal_velocity_timeout(self):
        """Test terminal velocity with timeout."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired('cmd', 300)
            
            velocity = self.benchmark.benchmark_terminal_velocity(
                'src/tests/unit/',
                'python -m pytest src/tests/unit/ --tb=short -q'
            )
            
            # Should return empty metrics on timeout
            self.assertEqual(velocity.throughput, 0)
            self.assertEqual(velocity.latency, 0)
            self.assertEqual(velocity.efficiency, 0)
            self.assertEqual(velocity.flow_state_score, 0)
    
    def test_calculate_execution_metrics(self):
        """Test execution metrics calculation."""
        execution_times = [0.1, 0.2, 0.15, 0.18, 0.12]
        metrics = self.benchmark._calculate_execution_metrics(execution_times, 'test_name')
        
        self.assertIsInstance(metrics, list)
        self.assertGreater(len(metrics), 0)
        
        # Check for expected metric types
        metric_names = [m.name for m in metrics]
        self.assertIn('test_name_avg_time', metric_names)
        self.assertIn('test_name_min_time', metric_names)
        self.assertIn('test_name_max_time', metric_names)
        self.assertIn('test_name_std_dev', metric_names)
        self.assertIn('test_name_operations_per_sec', metric_names)
        
        # Check metric units
        for metric in metrics:
            self.assertIsInstance(metric, BenchmarkMetric)
            self.assertIsInstance(metric.name, str)
            self.assertIsInstance(metric.value, (int, float))
            self.assertIsInstance(metric.unit, str)
    
    def test_benchmark_import_time(self):
        """Test import time benchmark."""
        time_taken = self.benchmark._benchmark_import_time()
        
        self.assertIsInstance(time_taken, float)
        self.assertGreater(time_taken, 0)
        self.assertLess(time_taken, 10)  # Should be under 10 seconds
    
    def test_benchmark_module_loading(self):
        """Test module loading benchmark."""
        time_taken = self.benchmark._benchmark_module_loading()
        
        self.assertIsInstance(time_taken, float)
        self.assertGreaterEqual(time_taken, 0)
    
    def test_benchmark_data_generation(self):
        """Test data generation benchmark."""
        # Mock the data generator to avoid actual generation
        with patch('fsl_continuum.test_data_generator.TestDataGenerator') as mock_generator:
            mock_instance = MagicMock()
            mock_instance.generate_data.return_value = MagicMock()
            mock_generator.return_value = mock_instance
            
            time_taken = self.benchmark._benchmark_data_generation()
            
            self.assertIsInstance(time_taken, float)
            self.assertGreater(time_taken, 0)
    
    def test_benchmark_xml_processing(self):
        """Test XML processing benchmark."""
        time_taken = self.benchmark._benchmark_xml_processing()
        
        self.assertIsInstance(time_taken, float)
        self.assertGreater(time_taken, 0)
    
    def test_get_system_info(self):
        """Test system information collection."""
        system_info = self.benchmark._get_system_info()
        
        self.assertIsInstance(system_info, dict)
        self.assertIn('platform', system_info)
        self.assertIn('system', system_info)
        self.assertIn('cpu_count', system_info)
        self.assertIn('memory_total', system_info)
        self.assertIn('python_version', system_info)
    
    def test_save_baseline_data(self):
        """Test saving baseline data."""
        # Add some dummy results first
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.stdout = "5 passed in 0.50s"
            mock_result.returncode = 0
            mock_run.return_value = mock_result
            
            dummy_test = lambda: None
            result = self.benchmark.benchmark_test_execution(
                dummy_test, 'dummy_test', iterations=1
            )
            self.benchmark.benchmark_results.append(result)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Mock the baseline file path
            original_baseline = Path('test_baselines.json')
            with patch.object(self.benchmark, 'baseline_data'):
                with patch('builtins.open') as mock_open:
                    mock_file = MagicMock()
                    mock_open.return_value.__enter__.return_value = mock_file
                    
                    self.benchmark.save_baseline_data()
                    
                    # Verify write was called
                    mock_file.write.assert_called()
        finally:
            if Path(temp_file).exists():
                Path(temp_file).unlink()
    
    def test_get_performance_report(self):
        """Test getting performance report."""
        # Add some dummy results
        dummy_test = lambda: None
        result = self.benchmark.benchmark_test_execution(
            dummy_test, 'dummy_test', iterations=1
        )
        
        report = self.benchmark.get_performance_report()
        
        self.assertIsInstance(report, dict)
        self.assertIn('last_benchmark', report)
        self.assertIn('total_benchmarks', report)
        self.assertIn('system_info', report)
    
    def test_get_performance_report_empty(self):
        """Test performance report with no results."""
        self.benchmark.benchmark_results = []
        report = self.benchmark.get_performance_report()
        
        self.assertIsInstance(report, dict)
        self.assertIn('error', report)
        self.assertEqual(report['error'], 'No benchmark results available')


class TestBenchmarkUtilityFunctions(unittest.TestCase):
    """Test utility functions for benchmarking."""
    
    def test_run_performance_benchmark_function(self):
        """Test standalone run_performance_benchmark function."""
        # Mock the PerformanceBenchmark to avoid actual benchmarking
        with patch('fsl_continuum.performance_benchmark.PerformanceBenchmark') as mock_benchmark:
            mock_instance = MagicMock()
            mock_instance.run_comprehensive_benchmark.return_value = {
                'benchmark_results': {}
            }
            mock_instance.save_baseline_data.return_value = None
            mock_instance.get_performance_report.return_value = {}
            mock_benchmark.return_value = mock_instance
            
            from fsl_continuum.performance_benchmark import run_performance_benchmark
            
            result = run_performance_benchmark('src/tests/', save_baseline=False)
            
            self.assertIsInstance(result, dict)
            mock_instance.run_comprehensive_benchmark.assert_called_once_with('src/tests/')
    
    def test_parse_test_count(self):
        """Test parsing test count from pytest output."""
        test_cases = [
            ("5 passed in 0.50s", 5),
            ("10 passed, 2 failed in 1.20s", 10),
            ("1 passed in 0.05s", 1),
            ("No tests run", 0),
            ("", 0)
        ]
        
        for output, expected_count in test_cases:
            with self.subTest(output=output):
                count = self.benchmark._parse_test_count(output)
                self.assertEqual(count, expected_count)


if __name__ == '__main__':
    unittest.main()

"""
FSL Continuum - Performance Benchmarking Module

Comprehensive performance benchmarking for CI/CD terminal velocity,
test execution, and system resource monitoring.
"""

import time
import psutil
import threading
import json
import statistics
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from rich.console import Console
from rich.progress import Progress, TaskID
from rich.table import Table

console = Console()


@dataclass
class BenchmarkMetric:
    """Individual benchmark metric."""
    name: str
    value: float
    unit: str
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkResult:
    """Complete benchmark execution result."""
    test_name: str
    start_time: datetime
    end_time: datetime
    duration: float
    metrics: List[BenchmarkMetric]
    system_info: Dict[str, Any]
    baseline_comparison: Optional[Dict[str, float]] = None
    passed: bool = True
    errors: List[str] = field(default_factory=list)


@dataclass
class VelocityMetrics:
    """Terminal velocity performance metrics."""
    throughput: float  # Tests per second
    latency: float     # Average test execution time
    efficiency: float  # Resource utilization efficiency
    flow_state_score: float  # Flow state optimization score
    metrics_collected_at: datetime


class MetricsCollector:
    """Collects system and performance metrics during benchmarking."""
    
    def __init__(self):
        self.metrics = []
        self.start_time = None
        self.end_time = None
        self.monitoring = False
        self.monitor_thread = None
        self.system_samples = []
        
    def start_monitoring(self):
        """Start performance monitoring."""
        self.start_time = time.time()
        self.monitoring = True
        self.system_samples = []
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_system)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        console.print("[green]📊 Started performance monitoring[/green]")
    
    def stop_monitoring(self):
        """Stop performance monitoring."""
        self.end_time = time.time()
        self.monitoring = False
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        
        console.print("[yellow]⏹️ Stopped performance monitoring[/yellow]")
    
    def _monitor_system(self):
        """Monitor system resources in background."""
        while self.monitoring:
            try:
                sample = {
                    'timestamp': time.time(),
                    'cpu_percent': psutil.cpu_percent(interval=0.1),
                    'memory_mb': psutil.virtual_memory().used / 1024 / 1024,
                    'disk_io_read': psutil.disk_io_counters().read_bytes if psutil.disk_io_counters() else 0,
                    'disk_io_write': psutil.disk_io_counters().write_bytes if psutil.disk_io_counters() else 0,
                    'network_io_recv': psutil.net_io_counters().bytes_recv if psutil.net_io_counters() else 0,
                    'network_io_sent': psutil.net_io_counters().bytes_sent if psutil.net_io_counters() else 0
                }
                self.system_samples.append(sample)
                time.sleep(0.5)  # Sample every 500ms
            except Exception as e:
                console.print(f"[red]⚠️ Monitoring error: {e}[/red]")
    
    def get_average_metrics(self) -> Dict[str, float]:
        """Calculate average system metrics."""
        if not self.system_samples:
            return {}
        
        return {
            'cpu_percent': statistics.mean([s['cpu_percent'] for s in self.system_samples]),
            'memory_mb': statistics.mean([s['memory_mb'] for s in self.system_samples]),
            'disk_io_read_mb': statistics.mean([s['disk_io_read'] / 1024 / 1024 for s in self.system_samples]),
            'disk_io_write_mb': statistics.mean([s['disk_io_write'] / 1024 / 1024 for s in self.system_samples]),
            'network_io_recv_mb': statistics.mean([s['network_io_recv'] / 1024 / 1024 for s in self.system_samples]),
            'network_io_sent_mb': statistics.mean([s['network_io_sent'] / 1024 / 1024 for s in self.system_samples])
        }
    
    def get_peak_metrics(self) -> Dict[str, float]:
        """Get peak system metrics."""
        if not self.system_samples:
            return {}
        
        return {
            'peak_cpu_percent': max([s['cpu_percent'] for s in self.system_samples]),
            'peak_memory_mb': max([s['memory_mb'] for s in self.system_samples]),
            'peak_disk_io_read_mb': max([s['disk_io_read'] / 1024 / 1024 for s in self.system_samples]),
            'peak_disk_io_write_mb': max([s['disk_io_write'] / 1024 / 1024 for s in self.system_samples])
        }


class PerformanceBenchmark:
    """Comprehensive performance benchmarking for CI/CD terminal velocity."""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.baseline_data = {}
        self.benchmark_results = []
        self.current_benchmark = None
        self.load_baseline_data()
    
    def load_baseline_data(self):
        """Load baseline performance data."""
        baseline_file = Path('test_baselines.json')
        if baseline_file.exists():
            try:
                with open(baseline_file, 'r') as f:
                    self.baseline_data = json.load(f)
                console.print(f"[green]📈 Loaded baseline data from {baseline_file}[/green]")
            except Exception as e:
                console.print(f"[yellow]⚠️ Could not load baseline: {e}[/yellow]")
        else:
            console.print("[yellow]⚠️ No baseline data found. Use --save-baseline to create one.[/yellow]")
    
    def save_baseline_data(self):
        """Save current performance as baseline."""
        if not self.benchmark_results:
            console.print("[red]❌ No benchmark results to save as baseline[/red]")
            return
        
        # Calculate averages from latest results
        latest_results = self.benchmark_results[-5:]  # Last 5 results
        baseline_data = {}
        
        for result in latest_results:
            for metric in result.metrics:
                if metric.name not in baseline_data:
                    baseline_data[metric.name] = []
                baseline_data[metric.name].append(metric.value)
        
        # Calculate averages
        baseline_averages = {}
        for metric_name, values in baseline_data.items():
            baseline_averages[metric_name] = statistics.mean(values)
        
        baseline_averages['created_at'] = datetime.now().isoformat()
        baseline_averages['sample_size'] = len(latest_results)
        
        baseline_file = Path('test_baselines.json')
        with open(baseline_file, 'w') as f:
            json.dump(baseline_averages, f, indent=2, default=str)
        
        console.print(f"[green]💾 Saved baseline data to {baseline_file}[/green]")
    
    def benchmark_test_execution(self, test_function: Callable, test_name: str, 
                           iterations: int = 5) -> BenchmarkResult:
        """Benchmark test execution performance."""
        console.print(f"[blue]🏁 Benchmarking {test_name}...[/blue]")
        
        start_time = datetime.now()
        self.metrics_collector.start_monitoring()
        
        try:
            # Run benchmark iterations
            execution_times = []
            for i in range(iterations):
                with Progress() as progress:
                    task = progress.add_task(f"Run {i+1}/{iterations}", total=100)
                    
                    iteration_start = time.time()
                    test_function()
                    iteration_end = time.time()
                    
                    execution_time = iteration_end - iteration_start
                    execution_times.append(execution_time)
                    
                    progress.update(task, completed=100)
            
            # Calculate metrics
            with Progress() as progress:
                task = progress.add_task("Calculating metrics...", total=100)
                
                metrics = self._calculate_execution_metrics(execution_times, test_name)
                progress.update(task, completed=50)
                
                system_metrics = self.metrics_collector.get_average_metrics()
                system_metrics = {f"system_{k}": v for k, v in system_metrics.items()}
                metrics.extend(self._create_system_metrics(system_metrics))
                progress.update(task, completed=100)
            
            end_time = datetime.now()
            self.metrics_collector.stop_monitoring()
            
            # Create result
            result = BenchmarkResult(
                test_name=test_name,
                start_time=start_time,
                end_time=end_time,
                duration=(end_time - start_time).total_seconds(),
                metrics=metrics,
                system_info={
                    'cpu_count': psutil.cpu_count(),
                    'memory_total_gb': psutil.virtual_memory().total / 1024 / 1024 / 1024,
                    'disk_total_gb': psutil.disk_usage('/').total / 1024 / 1024 / 1024,
                    'python_version': f"{__import__('sys').version}",
                    'platform': f"{__import__('platform').system()} {__import__('platform').release()}"
                },
                baseline_comparison=self._compare_with_baseline(test_name, metrics)
            )
            
            self.benchmark_results.append(result)
            console.print(f"[green]✅ Benchmark completed for {test_name}[/green]")
            self._display_benchmark_summary(result)
            
            return result
            
        except Exception as e:
            self.metrics_collector.stop_monitoring()
            end_time = datetime.now()
            
            error_result = BenchmarkResult(
                test_name=test_name,
                start_time=start_time,
                end_time=end_time,
                duration=(end_time - start_time).total_seconds(),
                metrics=[],
                system_info={},
                passed=False,
                errors=[str(e)]
            )
            
            console.print(f"[red]❌ Benchmark failed for {test_name}: {e}[/red]")
            return error_result
    
    def benchmark_terminal_velocity(self, test_suite_path: str, 
                              test_command: str) -> VelocityMetrics:
        """Measure terminal velocity metrics for test execution."""
        console.print(f"[blue]🌊 Measuring terminal velocity for {test_suite_path}...[/blue]")
        
        start_time = time.time()
        self.metrics_collector.start_monitoring()
        
        try:
            # Execute test suite
            import subprocess
            result = subprocess.run(
                test_command.split(),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            end_time = time.time()
            self.metrics_collector.stop_monitoring()
            
            # Parse test results
            total_tests = self._parse_test_count(result.stdout)
            execution_time = end_time - start_time
            
            # Calculate velocity metrics
            with Progress() as progress:
                task = progress.add_task("Calculating velocity metrics...", total=100)
                
                throughput = total_tests / execution_time if execution_time > 0 else 0
                latency = execution_time / total_tests if total_tests > 0 else 0
                
                # Calculate efficiency (inverse of resource usage)
                system_metrics = self.metrics_collector.get_average_metrics()
                resource_score = system_metrics.get('cpu_percent', 0) + system_metrics.get('memory_mb', 0) / 1000
                efficiency = 100 / (resource_score + 1) if resource_score > 0 else 100
                
                # Calculate flow state score (simplified)
                flow_state_score = self._calculate_flow_state_score(
                    throughput, latency, efficiency
                )
                
                progress.update(task, advance=50)
                
                velocity_metrics = VelocityMetrics(
                    throughput=throughput,
                    latency=latency,
                    efficiency=efficiency,
                    flow_state_score=flow_state_score,
                    metrics_collected_at=datetime.now()
                )
                
                progress.update(task, completed=100)
            
            console.print(f"[green]✅ Terminal velocity measured: {throughput:.2f} tests/sec[/green]")
            self._display_velocity_summary(velocity_metrics)
            
            return velocity_metrics
            
        except subprocess.TimeoutExpired:
            self.metrics_collector.stop_monitoring()
            console.print("[red]❌ Test execution timed out[/red]")
            return self._create_empty_velocity_metrics()
        except Exception as e:
            self.metrics_collector.stop_monitoring()
            console.print(f"[red]❌ Velocity measurement failed: {e}[/red]")
            return self._create_empty_velocity_metrics()
    
    def run_comprehensive_benchmark(self, test_suite_path: str) -> Dict[str, Any]:
        """Run comprehensive benchmarking suite."""
        console.print("[bold blue]🎯 Running Comprehensive Performance Benchmark[/bold blue]")
        
        benchmark_results = {}
        
        # Define benchmark tests
        benchmark_tests = [
            ('test_import_time', self._benchmark_import_time),
            ('test_module_loading', self._benchmark_module_loading),
            ('test_data_generation', self._benchmark_data_generation),
            ('test_xml_processing', self._benchmark_xml_processing),
            ('test_semantic_parsing', self._benchmark_semantic_parsing)
        ]
        
        with Progress() as progress:
            task = progress.add_task("Running benchmarks...", total=len(benchmark_tests))
            
            for test_name, test_func in benchmark_tests:
                result = self.benchmark_test_execution(test_func, test_name)
                benchmark_results[test_name] = asdict(result)
                progress.update(task, advance=1)
        
        # Add terminal velocity measurement
        velocity_metrics = self.benchmark_terminal_velocity(
            test_suite_path, 
            f"python -m pytest {test_suite_path} --tb=short -q"
        )
        benchmark_results['terminal_velocity'] = asdict(velocity_metrics)
        
        # Save results
        self._save_benchmark_results(benchmark_results)
        
        return benchmark_results
    
    def _calculate_execution_metrics(self, execution_times: List[float], test_name: str) -> List[BenchmarkMetric]:
        """Calculate execution time metrics."""
        if not execution_times:
            return []
        
        metrics = [
            BenchmarkMetric(
                name=f"{test_name}_avg_time",
                value=statistics.mean(execution_times),
                unit='seconds',
                timestamp=datetime.now()
            ),
            BenchmarkMetric(
                name=f"{test_name}_min_time",
                value=min(execution_times),
                unit='seconds',
                timestamp=datetime.now()
            ),
            BenchmarkMetric(
                name=f"{test_name}_max_time",
                value=max(execution_times),
                unit='seconds',
                timestamp=datetime.now()
            ),
            BenchmarkMetric(
                name=f"{test_name}_std_dev",
                value=statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
                unit='seconds',
                timestamp=datetime.now()
            ),
            BenchmarkMetric(
                name=f"{test_name}_operations_per_sec",
                value=1 / statistics.mean(execution_times) if statistics.mean(execution_times) > 0 else 0,
                unit='ops/sec',
                timestamp=datetime.now()
            )
        ]
        
        return metrics
    
    def _create_system_metrics(self, system_metrics: Dict[str, float]) -> List[BenchmarkMetric]:
        """Create benchmark metrics from system measurements."""
        metrics = []
        for metric_name, value in system_metrics.items():
            if 'cpu' in metric_name:
                unit = 'percent'
            elif 'memory' in metric_name:
                unit = 'MB'
            elif 'disk_io' in metric_name:
                unit = 'MB/s'
            elif 'network_io' in metric_name:
                unit = 'MB/s'
            else:
                unit = 'unknown'
            
            metrics.append(BenchmarkMetric(
                name=metric_name,
                value=value,
                unit=unit,
                timestamp=datetime.now()
            ))
        
        return metrics
    
    def _compare_with_baseline(self, test_name: str, current_metrics: List[BenchmarkMetric]) -> Optional[Dict[str, float]]:
        """Compare current metrics with baseline data."""
        if not self.baseline_data:
            return None
        
        comparison = {}
        for metric in current_metrics:
            if metric.name in self.baseline_data:
                baseline_value = self.baseline_data[metric.name]
                improvement = ((baseline_value - metric.value) / baseline_value) * 100
                comparison[metric.name] = improvement
        
        return comparison
    
    def _calculate_flow_state_score(self, throughput: float, latency: float, efficiency: float) -> float:
        """Calculate flow state optimization score."""
        # Simplified flow state calculation
        # Higher throughput, lower latency, and higher efficiency = better flow state
        
        # Normalize values (0-100 scale)
        throughput_score = min(throughput * 10, 100)  # Assume 10 tests/sec is ideal
        latency_score = max(0, 100 - (latency * 1000))  # Lower latency is better
        efficiency_score = min(efficiency, 100)
        
        # Weighted average (adjust weights as needed)
        flow_state_score = (
            throughput_score * 0.4 +
            latency_score * 0.3 +
            efficiency_score * 0.3
        )
        
        return flow_state_score
    
    def _parse_test_count(self, test_output: str) -> int:
        """Parse number of tests from pytest output."""
        lines = test_output.split('\n')
        for line in lines:
            if 'passed in ' in line or 'failed in ' in line:
                try:
                    count_part = line.split()[0]
                    return int(count_part)
                except:
                    continue
        return 0
    
    def _create_empty_velocity_metrics(self) -> VelocityMetrics:
        """Create empty velocity metrics for failed measurements."""
        return VelocityMetrics(
            throughput=0,
            latency=0,
            efficiency=0,
            flow_state_score=0,
            metrics_collected_at=datetime.now()
        )
    
    def _benchmark_import_time(self):
        """Benchmark module import time."""
        import importlib
        import time
        
        start = time.time()
        importlib.import_module('fsl_continuum')
        return time.time() - start
    
    def _benchmark_module_loading(self):
        """Benchmark loading multiple modules."""
        import importlib
        import time
        
        modules = ['test_runner', 'test_env', 'cli']
        total_time = 0
        
        for module_name in modules:
            start = time.time()
            try:
                importlib.import_module(f'fsl_continuum.{module_name}')
                total_time += time.time() - start
            except ImportError:
                pass
        
        return total_time
    
    def _benchmark_data_generation(self):
        """Benchmark test data generation."""
        from .test_data_generator import TestDataGenerator, DataGenerationConfig
        
        config = DataGenerationConfig(num_records=50)
        generator = TestDataGenerator(config)
        
        start = time.time()
        generator.generate_data('baml')
        return time.time() - start
    
    def _benchmark_xml_processing(self):
        """Benchmark XML processing performance."""
        import xml.etree.ElementTree as ET
        import time
        
        # Create test XML
        root = ET.Element("root")
        for i in range(100):
            child = ET.SubElement(root, "item", id=str(i))
            child.text = f"Test data {i}"
        
        xml_str = ET.tostring(root)
        
        # Benchmark parsing
        start = time.time()
        ET.fromstring(xml_str)
        return time.time() - start
    
    def _benchmark_semantic_parsing(self):
        """Benchmark semantic language parsing."""
        # Simulate semantic language parsing
        import time
        
        test_data = [
            "entity User { name: string, age: number, active: boolean }",
            "constraint UniqueUser(email: string)",
            "relation User -> Profile[1]"
        ]
        
        start = time.time()
        for data in test_data:
            # Simulate parsing operations
            tokens = data.split()
            for token in tokens:
                pass  # Simulate token processing
        
        return time.time() - start
    
    def _save_benchmark_results(self, results: Dict[str, Any]):
        """Save benchmark results to file."""
        results_file = Path('benchmark_results.json')
        
        benchmark_data = {
            'timestamp': datetime.now().isoformat(),
            'system_info': self._get_system_info(),
            'results': results,
            'baseline_used': self.baseline_data is not None
        }
        
        with open(results_file, 'w') as f:
            json.dump(benchmark_data, f, indent=2, default=str)
        
        console.print(f"[green]💾 Benchmark results saved to {results_file}[/green]")
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information."""
        import platform
        import sys
        
        return {
            'platform': platform.platform(),
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': sys.version,
            'python_implementation': platform.python_implementation(),
            'cpu_count': psutil.cpu_count(),
            'cpu_freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {},
            'memory_total': psutil.virtual_memory().total,
            'disk_total': psutil.disk_usage('/').total,
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat()
        }
    
    def _display_benchmark_summary(self, result: BenchmarkResult):
        """Display benchmark result summary."""
        table = Table(title=f"Benchmark Results: {result.test_name}")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Unit", style="white")
        
        for metric in result.metrics[:10]:  # Show top 10 metrics
            table.add_row(
                metric.name.replace('_', ' ').title(),
                f"{metric.value:.4f}",
                metric.unit
            )
        
        console.print(table)
        
        if result.baseline_comparison:
            console.print("\n[bold]Baseline Comparison:[/bold]")
            for metric_name, improvement in result.baseline_comparison.items():
                if improvement > 0:
                    console.print(f"  [green]✅ {metric_name}: +{improvement:.1f}% improvement[/green]")
                else:
                    console.print(f"  [red]❌ {metric_name}: {improvement:.1f}% regression[/red]")
    
    def _display_velocity_summary(self, metrics: VelocityMetrics):
        """Display terminal velocity metrics."""
        table = Table(title="Terminal Velocity Metrics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Description", style="white")
        
        table.add_row(
            "Throughput",
            f"{metrics.throughput:.2f}",
            "Tests per second"
        )
        table.add_row(
            "Latency",
            f"{metrics.latency:.4f}",
            "Average test execution time (seconds)"
        )
        table.add_row(
            "Efficiency",
            f"{metrics.efficiency:.1f}%",
            "Resource utilization efficiency"
        )
        table.add_row(
            "Flow State Score",
            f"{metrics.flow_state_score:.1f}%",
            "Flow state optimization score"
        )
        
        console.print(table)
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report."""
        if not self.benchmark_results:
            return {'error': 'No benchmark results available'}
        
        return {
            'last_benchmark': asdict(self.benchmark_results[-1]),
            'total_benchmarks': len(self.benchmark_results),
            'baseline_available': self.baseline_data is not None,
            'system_info': self._get_system_info(),
            'trends': self._calculate_performance_trends()
        }
    
    def _calculate_performance_trends(self) -> Dict[str, Any]:
        """Calculate performance trends from benchmark history."""
        if len(self.benchmark_results) < 2:
            return {'message': 'Insufficient data for trend analysis'}
        
        # Compare latest with previous results
        latest = self.benchmark_results[-1]
        previous = self.benchmark_results[-2]
        
        trends = {}
        for latest_metric in latest.metrics:
            # Find corresponding metric in previous result
            previous_metric = next((m for m in previous.metrics if m.name == latest_metric.name), None)
            if previous_metric:
                change = latest_metric.value - previous_metric.value
                percent_change = (change / previous_metric.value) * 100 if previous_metric.value != 0 else 0
                trends[latest_metric.name] = {
                    'change': change,
                    'percent_change': percent_change,
                    'trend': 'improving' if change < 0 and 'time' in latest_metric.name else 'improving' if change > 0 and 'ops' in latest_metric.name else 'stable'
                }
        
        return trends


# Utility functions for standalone usage
def run_performance_benchmark(test_suite_path: str = "src/tests/", save_baseline: bool = False) -> Dict[str, Any]:
    """Utility function to run performance benchmarking."""
    benchmark = PerformanceBenchmark()
    
    # Run comprehensive benchmarking
    results = benchmark.run_comprehensive_benchmark(test_suite_path)
    
    # Save baseline if requested
    if save_baseline:
        benchmark.save_baseline_data()
    
    return results.get_performance_report()


if __name__ == "__main__":
    console.print("[bold blue]🎯 FSL Continuum Performance Benchmark[/bold blue]")
    
    import argparse
    parser = argparse.ArgumentParser(description="Run performance benchmarks for FSL Continuum")
    parser.add_argument('--test-suite', default='src/tests/', help='Path to test suite')
    parser.add_argument('--save-baseline', action='store_true', help='Save results as baseline')
    parser.add_argument('--compare-baseline', action='store_true', help='Compare with baseline')
    
    args = parser.parse_args()
    
    benchmark = PerformanceBenchmark()
    
    if args.compare_baseline:
        # Just run terminal velocity and compare
        velocity = benchmark.benchmark_terminal_velocity(
            args.test_suite,
            f"python -m pytest {args.test_suite} --tb=short -q"
        )
    else:
        # Run comprehensive benchmarking
        report = run_performance_benchmark(args.test_suite, args.save_baseline)
        console.print("\n[bold green]✅ Performance benchmarking complete![/bold green]")

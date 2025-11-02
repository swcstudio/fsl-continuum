"""
FSL Continuum - Test Automation Framework

Automated testing framework for semantic languages with CI/CD integration.
Provides test scheduling, execution, reporting, and continuous integration.
"""

import os
import json
import time
import logging
import threading
from typing import Dict, List, Optional, Any, Union, Tuple, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import psutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestStatus(Enum):
    """Test execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"

class TestPriority(Enum):
    """Test execution priority."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class TestExecutionConfig:
    """Test execution configuration."""
    test_suite: str
    test_categories: List[str]
    execution_mode: str  # "sequential", "parallel", "distributed"
    parallel_workers: int
    timeout_seconds: int
    retry_attempts: int
    enable_profiling: bool
    enable_coverage: bool
    enable_performance_monitoring: bool
    output_directory: str
    log_directory: str
    ci_cd_integration: Dict[str, Any]

@dataclass
class TestResult:
    """Test execution result."""
    test_name: str
    test_suite: str
    status: TestStatus
    execution_time: float
    memory_usage: float
    cpu_usage: float
    success: bool
    error_message: Optional[str]
    stack_trace: Optional[str]
    performance_metrics: Optional[Dict[str, Any]]
    coverage_metrics: Optional[Dict[str, Any]]
    timestamp: datetime
    retry_count: int

@dataclass
class TestSuiteResult:
    """Test suite execution result."""
    suite_name: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    cancelled_tests: int
    success_rate: float
    total_execution_time: float
    average_execution_time: float
    peak_memory_usage: float
    total_cpu_usage: float
    test_results: List[TestResult]
    performance_summary: Optional[Dict[str, Any]]
    coverage_summary: Optional[Dict[str, Any]]
    execution_timestamp: datetime

class TestRunner:
    """Test execution runner with monitoring and profiling."""
    
    def __init__(self):
        self.test_queue = Queue()
        self.result_queue = Queue()
        self.executor = None
        self.monitoring_active = False
        self.monitoring_thread = None
        self.performance_data = {}
        self.coverage_data = {}
    
    def run_test_function(self, test_function: Callable, test_name: str, timeout: int = 300) -> TestResult:
        """Run individual test function with monitoring."""
        start_time = time.time()
        start_memory = self._get_memory_usage()
        start_cpu = self._get_cpu_usage()
        
        try:
            # Execute test with timeout
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError(f"Test {test_name} timed out after {timeout} seconds")
            
            if hasattr(signal, 'SIGALRM'):
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(timeout)
            
            # Run test function
            test_result = test_function()
            success = True
            error_message = None
            stack_trace = None
            
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            
        except TimeoutError as e:
            success = False
            error_message = str(e)
            stack_trace = None
            test_result = None
            
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            
        except Exception as e:
            success = False
            error_message = str(e)
            stack_trace = traceback.format_exc()
            test_result = None
            
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
        
        end_time = time.time()
        end_memory = self._get_memory_usage()
        end_cpu = self._get_cpu_usage()
        
        execution_time = end_time - start_time
        memory_usage = end_memory - start_memory
        cpu_usage = end_cpu - start_cpu
        
        # Create test result
        result = TestResult(
            test_name=test_name,
            test_suite="unknown",
            status=TestStatus.COMPLETED if success else TestStatus.FAILED,
            execution_time=execution_time,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            success=success,
            error_message=error_message,
            stack_trace=stack_trace,
            performance_metrics=self._get_performance_metrics(test_name),
            coverage_metrics=self._get_coverage_metrics(test_name),
            timestamp=datetime.now(),
            retry_count=0
        )
        
        return result
    
    def run_test_suite(self, test_config: TestExecutionConfig) -> TestSuiteResult:
        """Run entire test suite with configuration."""
        logger.info(f"Running test suite: {test_config.test_suite}")
        
        start_time = time.time()
        test_results = []
        
        try:
            # Load test functions
            test_functions = self._load_test_functions(test_config)
            
            # Execute tests based on execution mode
            if test_config.execution_mode == "sequential":
                test_results = self._run_tests_sequential(test_functions, test_config)
            elif test_config.execution_mode == "parallel":
                test_results = self._run_tests_parallel(test_functions, test_config)
            else:
                raise ValueError(f"Unknown execution mode: {test_config.execution_mode}")
            
        except Exception as e:
            logger.error(f"Error running test suite: {e}")
            raise
        
        end_time = time.time()
        total_execution_time = end_time - start_time
        
        # Create test suite result
        suite_result = TestSuiteResult(
            suite_name=test_config.test_suite,
            total_tests=len(test_results),
            passed_tests=sum(1 for r in test_results if r.status == TestStatus.COMPLETED and r.success),
            failed_tests=sum(1 for r in test_results if r.status == TestStatus.FAILED or (r.status == TestStatus.COMPLETED and not r.success)),
            skipped_tests=sum(1 for r in test_results if r.status == TestStatus.SKIPPED),
            cancelled_tests=sum(1 for r in test_results if r.status == TestStatus.CANCELLED),
            success_rate=sum(1 for r in test_results if r.status == TestStatus.COMPLETED and r.success) / len(test_results) if test_results else 0,
            total_execution_time=total_execution_time,
            average_execution_time=sum(r.execution_time for r in test_results) / len(test_results) if test_results else 0,
            peak_memory_usage=max(r.memory_usage for r in test_results) if test_results else 0,
            total_cpu_usage=sum(r.cpu_usage for r in test_results),
            test_results=test_results,
            performance_summary=self._create_performance_summary(test_results),
            coverage_summary=self._create_coverage_summary(test_results),
            execution_timestamp=datetime.now()
        )
        
        return suite_result
    
    def _run_tests_sequential(self, test_functions: List[Tuple[str, Callable]], test_config: TestExecutionConfig) -> List[TestResult]:
        """Run tests sequentially."""
        results = []
        
        for test_name, test_function in test_functions:
            logger.info(f"Running test: {test_name}")
            
            result = self.run_test_function(test_function, test_name, test_config.timeout_seconds)
            results.append(result)
            
            # Log test result
            if result.success:
                logger.info(f"Test {test_name} passed in {result.execution_time:.3f}s")
            else:
                logger.error(f"Test {test_name} failed: {result.error_message}")
        
        return results
    
    def _run_tests_parallel(self, test_functions: List[Tuple[str, Callable]], test_config: TestExecutionConfig) -> List[TestResult]:
        """Run tests in parallel."""
        results = []
        
        with ThreadPoolExecutor(max_workers=test_config.parallel_workers) as executor:
            # Submit all tests
            future_to_test = {
                executor.submit(self.run_test_function, test_function, test_name, test_config.timeout_seconds): test_name
                for test_name, test_function in test_functions
            }
            
            # Collect results
            for future in as_completed(future_to_test):
                test_name = future_to_test[future]
                
                try:
                    result = future.result()
                    results.append(result)
                    
                    # Log test result
                    if result.success:
                        logger.info(f"Test {test_name} passed in {result.execution_time:.3f}s")
                    else:
                        logger.error(f"Test {test_name} failed: {result.error_message}")
                        
                except Exception as e:
                    logger.error(f"Error in test {test_name}: {e}")
                    
                    # Create failure result
                    failure_result = TestResult(
                        test_name=test_name,
                        test_suite=test_config.test_suite,
                        status=TestStatus.FAILED,
                        execution_time=0,
                        memory_usage=0,
                        cpu_usage=0,
                        success=False,
                        error_message=str(e),
                        stack_trace=traceback.format_exc(),
                        performance_metrics=None,
                        coverage_metrics=None,
                        timestamp=datetime.now(),
                        retry_count=0
                    )
                    results.append(failure_result)
        
        return results
    
    def _load_test_functions(self, test_config: TestExecutionConfig) -> List[Tuple[str, Callable]]:
        """Load test functions based on configuration."""
        test_functions = []
        
        # Import test modules based on test suite
        if test_config.test_suite == "baml":
            test_functions = self._load_baml_test_functions(test_config.test_categories)
        elif test_config.test_suite == "pareto_lang":
            test_functions = self._load_pareto_lang_test_functions(test_config.test_categories)
        elif test_config.test_suite == "xml_processing":
            test_functions = self._load_xml_processing_test_functions(test_config.test_categories)
        elif test_config.test_suite == "integration":
            test_functions = self._load_integration_test_functions(test_config.test_categories)
        elif test_config.test_suite == "performance":
            test_functions = self._load_performance_test_functions(test_config.test_categories)
        else:
            raise ValueError(f"Unknown test suite: {test_config.test_suite}")
        
        return test_functions
    
    def _load_baml_test_functions(self, categories: List[str]) -> List[Tuple[str, Callable]]:
        """Load BAML test functions."""
        test_functions = []
        
        try:
            from ..semantic_languages.baml import TestBAMLParser, TestBAMLValidator, TestBAMLXMLTransformer
            
            # Create test instances
            test_instances = []
            
            if "parser" in categories:
                test_instances.append(TestBAMLParser())
            if "validator" in categories:
                test_instances.append(TestBAMLValidator())
            if "xml_transformer" in categories:
                test_instances.append(TestBAMLXMLTransformer())
            
            # Collect test methods
            for test_instance in test_instances:
                for method_name in dir(test_instance):
                    if method_name.startswith("test_") and callable(getattr(test_instance, method_name)):
                        test_function = getattr(test_instance, method_name)
                        test_functions.append((f"{test_instance.__class__.__name__}.{method_name}", test_function))
        
        except ImportError as e:
            logger.error(f"Failed to load BAML test functions: {e}")
        
        return test_functions
    
    def _load_pareto_lang_test_functions(self, categories: List[str]) -> List[Tuple[str, Callable]]:
        """Load Pareto-Lang test functions."""
        test_functions = []
        
        try:
            from ..semantic_languages.pareto_lang import TestParetoLangParser, TestParetoLangValidator, TestParetoLangXMLTransformer
            
            # Create test instances
            test_instances = []
            
            if "parser" in categories:
                test_instances.append(TestParetoLangParser())
            if "validator" in categories:
                test_instances.append(TestParetoLangValidator())
            if "xml_transformer" in categories:
                test_instances.append(TestParetoLangXMLTransformer())
            
            # Collect test methods
            for test_instance in test_instances:
                for method_name in dir(test_instance):
                    if method_name.startswith("test_") and callable(getattr(test_instance, method_name)):
                        test_function = getattr(test_instance, method_name)
                        test_functions.append((f"{test_instance.__class__.__name__}.{method_name}", test_function))
        
        except ImportError as e:
            logger.error(f"Failed to load Pareto-Lang test functions: {e}")
        
        return test_functions
    
    def _load_xml_processing_test_functions(self, categories: List[str]) -> List[Tuple[str, Callable]]:
        """Load XML processing test functions."""
        test_functions = []
        
        try:
            from ..semantic_languages.xml_processing import TestUnifiedXMLProcessor
            
            # Create test instances
            test_instances = []
            
            if "unified_processor" in categories:
                test_instances.append(TestUnifiedXMLProcessor())
            
            # Collect test methods
            for test_instance in test_instances:
                for method_name in dir(test_instance):
                    if method_name.startswith("test_") and callable(getattr(test_instance, method_name)):
                        test_function = getattr(test_instance, method_name)
                        test_functions.append((f"{test_instance.__class__.__name__}.{method_name}", test_function))
        
        except ImportError as e:
            logger.error(f"Failed to load XML processing test functions: {e}")
        
        return test_functions
    
    def _load_integration_test_functions(self, categories: List[str]) -> List[Tuple[str, Callable]]:
        """Load integration test functions."""
        test_functions = []
        
        try:
            from ..semantic_languages.integration import TestEndToEnd, TestMultiLanguage
            
            # Create test instances
            test_instances = []
            
            if "end_to_end" in categories:
                test_instances.append(TestEndToEnd())
            if "multi_language" in categories:
                test_instances.append(TestMultiLanguage())
            
            # Collect test methods
            for test_instance in test_instances:
                for method_name in dir(test_instance):
                    if method_name.startswith("test_") and callable(getattr(test_instance, method_name)):
                        test_function = getattr(test_instance, method_name)
                        test_functions.append((f"{test_instance.__class__.__name__}.{method_name}", test_function))
        
        except ImportError as e:
            logger.error(f"Failed to load integration test functions: {e}")
        
        return test_functions
    
    def _load_performance_test_functions(self, categories: List[str]) -> List[Tuple[str, Callable]]:
        """Load performance test functions."""
        test_functions = []
        
        try:
            from ..performance import TestPerformanceBenchmarks, TestScalability
            
            # Create test instances
            test_instances = []
            
            if "benchmarks" in categories:
                test_instances.append(TestPerformanceBenchmarks())
            if "scalability" in categories:
                test_instances.append(TestScalability())
            
            # Collect test methods
            for test_instance in test_instances:
                for method_name in dir(test_instance):
                    if method_name.startswith("test_") and callable(getattr(test_instance, method_name)):
                        test_function = getattr(test_instance, method_name)
                        test_functions.append((f"{test_instance.__class__.__name__}.{method_name}", test_function))
        
        except ImportError as e:
            logger.error(f"Failed to load performance test functions: {e}")
        
        return test_functions
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except:
            return 0.0
    
    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage."""
        try:
            process = psutil.Process()
            return process.cpu_percent()
        except:
            return 0.0
    
    def _get_performance_metrics(self, test_name: str) -> Optional[Dict[str, Any]]:
        """Get performance metrics for test."""
        return self.performance_data.get(test_name)
    
    def _get_coverage_metrics(self, test_name: str) -> Optional[Dict[str, Any]]:
        """Get coverage metrics for test."""
        return self.coverage_data.get(test_name)
    
    def _create_performance_summary(self, test_results: List[TestResult]) -> Optional[Dict[str, Any]]:
        """Create performance summary from test results."""
        if not test_results:
            return None
        
        return {
            "total_tests": len(test_results),
            "passed_tests": sum(1 for r in test_results if r.success),
            "failed_tests": sum(1 for r in test_results if not r.success),
            "success_rate": sum(1 for r in test_results if r.success) / len(test_results),
            "total_execution_time": sum(r.execution_time for r in test_results),
            "average_execution_time": sum(r.execution_time for r in test_results) / len(test_results),
            "peak_memory_usage": max(r.memory_usage for r in test_results),
            "total_cpu_usage": sum(r.cpu_usage for r in test_results),
            "slowest_test": max(test_results, key=lambda r: r.execution_time).test_name,
            "fastest_test": min(test_results, key=lambda r: r.execution_time).test_name
        }
    
    def _create_coverage_summary(self, test_results: List[TestResult]) -> Optional[Dict[str, Any]]:
        """Create coverage summary from test results."""
        if not test_results:
            return None
        
        # Aggregate coverage metrics
        coverage_data = [r.coverage_metrics for r in test_results if r.coverage_metrics]
        
        if not coverage_data:
            return None
        
        return {
            "total_coverage_tests": len(coverage_data),
            "average_line_coverage": sum(c.get("line_coverage", 0) for c in coverage_data) / len(coverage_data),
            "average_branch_coverage": sum(c.get("branch_coverage", 0) for c in coverage_data) / len(coverage_data),
            "average_function_coverage": sum(c.get("function_coverage", 0) for c in coverage_data) / len(coverage_data),
            "total_lines_covered": sum(c.get("lines_covered", 0) for c in coverage_data),
            "total_branches_covered": sum(c.get("branches_covered", 0) for c in coverage_data),
            "total_functions_covered": sum(c.get("functions_covered", 0) for c in coverage_data)
        }

class TestScheduler:
    """Test scheduling and execution management."""
    
    def __init__(self):
        self.scheduled_tests = {}
        self.test_queue = Queue()
        self.scheduler_active = False
        self.scheduler_thread = None
    
    def schedule_test(self, test_config: TestExecutionConfig, scheduled_time: datetime):
        """Schedule test execution at specific time."""
        test_id = f"{test_config.test_suite}_{scheduled_time.isoformat()}"
        self.scheduled_tests[test_id] = {
            "config": test_config,
            "scheduled_time": scheduled_time,
            "status": "scheduled"
        }
        
        logger.info(f"Scheduled test {test_id} for {scheduled_time}")
        return test_id
    
    def schedule_continuous_testing(self, schedule_config: Dict[str, Any]):
        """Setup continuous testing schedule."""
        interval_minutes = schedule_config.get("interval_minutes", 60)
        test_suites = schedule_config.get("test_suites", ["baml", "pareto_lang"])
        
        def continuous_test_runner():
            while self.scheduler_active:
                try:
                    current_time = datetime.now()
                    
                    for test_suite in test_suites:
                        test_config = TestExecutionConfig(
                            test_suite=test_suite,
                            test_categories=["parser", "validator", "xml_transformer"],
                            execution_mode="parallel",
                            parallel_workers=4,
                            timeout_seconds=300,
                            retry_attempts=2,
                            enable_profiling=True,
                            enable_coverage=True,
                            enable_performance_monitoring=True,
                            output_directory="output/continuous",
                            log_directory="logs/continuous",
                            ci_cd_integration={}
                        )
                        
                        # Schedule next execution
                        next_execution = current_time + timedelta(minutes=interval_minutes)
                        test_id = f"{test_suite}_continuous_{next_execution.isoformat()}"
                        
                        self.scheduled_tests[test_id] = {
                            "config": test_config,
                            "scheduled_time": next_execution,
                            "status": "continuous"
                        }
                        
                        logger.info(f"Scheduled continuous test {test_id} for {next_execution}")
                    
                    # Wait for next scheduling cycle
                    time.sleep(interval_minutes * 60)
                    
                except Exception as e:
                    logger.error(f"Error in continuous test scheduler: {e}")
                    time.sleep(60)  # Wait before retrying
        
        # Start continuous test scheduler thread
        self.scheduler_active = True
        self.scheduler_thread = threading.Thread(target=continuous_test_runner)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        logger.info("Continuous test scheduler started")
    
    def stop_scheduler(self):
        """Stop test scheduler."""
        self.scheduler_active = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        
        logger.info("Test scheduler stopped")

class TestReporter:
    """Test reporting and result analysis."""
    
    def __init__(self):
        self.report_directory = "output/reports"
        self.template_directory = "templates"
    
    def generate_test_report(self, suite_result: TestSuiteResult, report_format: str = "json") -> str:
        """Generate test report in specified format."""
        timestamp = datetime.now().isoformat()
        
        if report_format == "json":
            return self._generate_json_report(suite_result, timestamp)
        elif report_format == "html":
            return self._generate_html_report(suite_result, timestamp)
        elif report_format == "junit":
            return self._generate_junit_report(suite_result, timestamp)
        else:
            raise ValueError(f"Unknown report format: {report_format}")
    
    def _generate_json_report(self, suite_result: TestSuiteResult, timestamp: str) -> str:
        """Generate JSON test report."""
        report_data = {
            "report_metadata": {
                "report_type": "test_suite_report",
                "format": "json",
                "timestamp": timestamp,
                "suite_name": suite_result.suite_name
            },
            "test_summary": {
                "total_tests": suite_result.total_tests,
                "passed_tests": suite_result.passed_tests,
                "failed_tests": suite_result.failed_tests,
                "skipped_tests": suite_result.skipped_tests,
                "cancelled_tests": suite_result.cancelled_tests,
                "success_rate": suite_result.success_rate,
                "total_execution_time": suite_result.total_execution_time,
                "average_execution_time": suite_result.average_execution_time,
                "peak_memory_usage": suite_result.peak_memory_usage,
                "total_cpu_usage": suite_result.total_cpu_usage
            },
            "performance_summary": suite_result.performance_summary,
            "coverage_summary": suite_result.coverage_summary,
            "test_results": [asdict(result) for result in suite_result.test_results]
        }
        
        # Create report file
        os.makedirs(self.report_directory, exist_ok=True)
        report_file = os.path.join(self.report_directory, f"{suite_result.suite_name}_report_{timestamp}.json")
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        logger.info(f"Generated JSON test report: {report_file}")
        return report_file
    
    def _generate_html_report(self, suite_result: TestSuiteResult, timestamp: str) -> str:
        """Generate HTML test report."""
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Suite Report: {suite_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .summary {{ margin: 20px 0; }}
        .passed {{ color: green; }}
        .failed {{ color: red; }}
        .skipped {{ color: orange; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .test-result {{ margin: 10px 0; padding: 10px; border-radius: 5px; }}
        .test-result.passed {{ background-color: #e8f5e8; }}
        .test-result.failed {{ background-color: #ffe8e8; }}
        .test-result.skipped {{ background-color: #fff0e8; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Test Suite Report: {suite_name}</h1>
        <p>Generated: {timestamp}</p>
    </div>
    
    <div class="summary">
        <h2>Test Summary</h2>
        <table>
            <tr><th>Total Tests</th><td>{total_tests}</td></tr>
            <tr><th>Passed</th><td class="passed">{passed_tests}</td></tr>
            <tr><th>Failed</th><td class="failed">{failed_tests}</td></tr>
            <tr><th>Skipped</th><td class="skipped">{skipped_tests}</td></tr>
            <tr><th>Success Rate</th><td>{success_rate:.2%}</td></tr>
            <tr><th>Total Execution Time</th><td>{total_execution_time:.3f}s</td></tr>
            <tr><th>Average Execution Time</th><td>{average_execution_time:.3f}s</td></tr>
            <tr><th>Peak Memory Usage</th><td>{peak_memory_usage:.2f}MB</td></tr>
        </table>
    </div>
    
    <div class="test-results">
        <h2>Test Results</h2>
        {test_results_html}
    </div>
</body>
</html>
        """
        
        # Generate test results HTML
        test_results_html = ""
        for result in suite_result.test_results:
            status_class = result.status.value
            error_info = ""
            if result.error_message:
                error_info = f"<p><strong>Error:</strong> {result.error_message}</p>"
            if result.stack_trace:
                error_info += f"<details><summary>Stack Trace</summary><pre>{result.stack_trace}</pre></details>"
            
            test_results_html += f"""
            <div class="test-result {status_class}">
                <h3>{result.test_name}</h3>
                <p><strong>Status:</strong> {result.status.value}</p>
                <p><strong>Execution Time:</strong> {result.execution_time:.3f}s</p>
                <p><strong>Memory Usage:</strong> {result.memory_usage:.2f}MB</p>
                <p><strong>CPU Usage:</strong> {result.cpu_usage:.2f}%</p>
                {error_info}
            </div>
            """
        
        # Fill template
        html_content = html_template.format(
            suite_name=suite_result.suite_name,
            timestamp=timestamp,
            total_tests=suite_result.total_tests,
            passed_tests=suite_result.passed_tests,
            failed_tests=suite_result.failed_tests,
            skipped_tests=suite_result.skipped_tests,
            cancelled_tests=suite_result.cancelled_tests,
            success_rate=suite_result.success_rate,
            total_execution_time=suite_result.total_execution_time,
            average_execution_time=suite_result.average_execution_time,
            peak_memory_usage=suite_result.peak_memory_usage,
            test_results_html=test_results_html
        )
        
        # Create report file
        os.makedirs(self.report_directory, exist_ok=True)
        report_file = os.path.join(self.report_directory, f"{suite_result.suite_name}_report_{timestamp}.html")
        
        with open(report_file, 'w') as f:
            f.write(html_content)
        
        logger.info(f"Generated HTML test report: {report_file}")
        return report_file
    
    def _generate_junit_report(self, suite_result: TestSuiteResult, timestamp: str) -> str:
        """Generate JUnit XML test report."""
        xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="{suite_name}" tests="{total_tests}" failures="{failed_tests}" skipped="{skipped_tests}" time="{total_execution_time}" timestamp="{timestamp}">
{test_cases_xml}
</testsuite>"""
        
        # Generate test case XML
        test_cases_xml = ""
        for result in suite_result.test_results:
            failure_xml = ""
            if not result.success and result.error_message:
                failure_xml = f'<failure message="{self._escape_xml(result.error_message)}">{self._escape_xml(result.stack_trace or "")}</failure>'
            
            skipped_xml = ""
            if result.status == TestStatus.SKIPPED:
                skipped_xml = '<skipped/>'
            
            test_cases_xml += f"""
    <testcase name="{result.test_name}" time="{result.execution_time}" classname="{suite_result.suite_name}">
        {failure_xml}
        {skipped_xml}
    </testcase>"""
        
        # Fill template
        xml_content = xml_template.format(
            suite_name=suite_result.suite_name,
            total_tests=suite_result.total_tests,
            failed_tests=suite_result.failed_tests,
            skipped_tests=suite_result.skipped_tests,
            total_execution_time=suite_result.total_execution_time,
            timestamp=timestamp,
            test_cases_xml=test_cases_xml
        )
        
        # Create report file
        os.makedirs(self.report_directory, exist_ok=True)
        report_file = os.path.join(self.report_directory, f"{suite_result.suite_name}_junit_{timestamp}.xml")
        
        with open(report_file, 'w') as f:
            f.write(xml_content)
        
        logger.info(f"Generated JUnit test report: {report_file}")
        return report_file
    
    def _escape_xml(self, text: str) -> str:
        """Escape text for XML."""
        if not text:
            return ""
        
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        text = text.replace('"', "&quot;")
        text = text.replace("'", "&apos;")
        
        return text

class CICDIntegration:
    """CI/CD integration for automated testing."""
    
    def __init__(self):
        self.github_actions_enabled = True
        self.gitlab_ci_enabled = True
        self.jenkins_enabled = True
        self.azure_devops_enabled = True
    
    def setup_github_actions(self, config: Dict[str, Any]) -> bool:
        """Setup GitHub Actions integration."""
        try:
            github_actions_config = {
                "name": "Semantic Language Tests",
                "on": {
                    "push": {
                        "branches": ["main", "develop"]
                    },
                    "pull_request": {
                        "branches": ["main"]
                    },
                    "schedule": [{
                        "cron": "0 2 * * *"
                    }]
                },
                "jobs": {
                    "semantic-language-tests": {
                        "runs-on": "ubuntu-latest",
                        "strategy": {
                            "matrix": {
                                "python-version": ["3.9", "3.10", "3.11"]
                            }
                        },
                        "steps": [
                            {
                                "uses": "actions/checkout@v3"
                            },
                            {
                                "name": "Set up Python ${{ matrix.python-version }}",
                                "uses": "actions/setup-python@v4",
                                "with": {
                                    "python-version": "${{ matrix.python-version }}"
                                }
                            },
                            {
                                "name": "Install dependencies",
                                "run": "pip install -r requirements.txt"
                            },
                            {
                                "name": "Run tests",
                                "run": f"python -m pytest src/tests/ -v --cov=src --cov-report=xml --cov-report=html"
                            },
                            {
                                "name": "Upload coverage to Codecov",
                                "uses": "codecov/codecov-action@v3",
                                "with": {
                                    "file": "./coverage.xml",
                                    "flags": "semantic-languages",
                                    "name": "semantic-language-coverage"
                                }
                            }
                        ]
                    }
                }
            }
            
            # Create GitHub Actions workflow file
            os.makedirs(".github/workflows", exist_ok=True)
            workflow_file = ".github/workflows/semantic_language_tests.yml"
            
            import yaml
            with open(workflow_file, 'w') as f:
                yaml.dump(github_actions_config, f, default_flow_style=False)
            
            logger.info(f"GitHub Actions workflow created: {workflow_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup GitHub Actions: {e}")
            return False
    
    def publish_results(self, test_results: List[TestResult], test_report: str) -> bool:
        """Publish test results to CI/CD systems."""
        success = True
        
        try:
            # GitHub Actions integration
            if self.github_actions_enabled and os.getenv("GITHUB_ACTIONS") == "true":
                self._publish_to_github_actions(test_results, test_report)
            
            # GitLab CI integration
            if self.gitlab_ci_enabled and os.getenv("GITLAB_CI") == "true":
                self._publish_to_gitlab_ci(test_results, test_report)
            
            # Jenkins integration
            if self.jenkins_enabled and os.getenv("JENKINS_URL"):
                self._publish_to_jenkins(test_results, test_report)
            
            # Azure DevOps integration
            if self.azure_devops_enabled and os.getenv("SYSTEM_TEAMFOUNDATIONCOLLECTIONURI"):
                self._publish_to_azure_devops(test_results, test_report)
            
        except Exception as e:
            logger.error(f"Failed to publish test results: {e}")
            success = False
        
        return success
    
    def _publish_to_github_actions(self, test_results: List[TestResult], test_report: str):
        """Publish results to GitHub Actions."""
        # Create GitHub Actions annotations for failed tests
        for result in test_results:
            if not result.success:
                error_message = f"##[error] {result.test_name}: {result.error_message}"
                print(error_message, flush=True)
        
        # Create summary
        total_tests = len(test_results)
        passed_tests = sum(1 for r in test_results if r.success)
        failed_tests = total_tests - passed_tests
        
        summary = f"""
## Test Summary
- **Total Tests**: {total_tests}
- **Passed**: {passed_tests}
- **Failed**: {failed_tests}
- **Success Rate**: {passed_tests/total_tests:.2%}

[Test Report]({test_report})
        """
        
        print(f"##[group]Test Results")
        print(summary, flush=True)
        print("##[endgroup]", flush=True)
    
    def _publish_to_gitlab_ci(self, test_results: List[TestResult], test_report: str):
        """Publish results to GitLab CI."""
        # Create GitLab CI artifacts
        for result in test_results:
            if not result.success:
                print(f"ERROR: {result.test_name}: {result.error_message}", flush=True)
        
        # Create summary
        total_tests = len(test_results)
        passed_tests = sum(1 for r in test_results if r.success)
        failed_tests = total_tests - passed_tests
        
        print(f"Test Summary: {passed_tests}/{total_tests} passed", flush=True)
        print(f"Test Report: {test_report}", flush=True)
    
    def _publish_to_jenkins(self, test_results: List[TestResult], test_report: str):
        """Publish results to Jenkins."""
        # Jenkins integration would be implemented here
        pass
    
    def _publish_to_azure_devops(self, test_results: List[TestResult], test_report: str):
        """Publish results to Azure DevOps."""
        # Azure DevOps integration would be implemented here
        pass

class TestAutomationFramework:
    """Main test automation framework manager."""
    
    def __init__(self):
        self.test_runner = TestRunner()
        self.test_scheduler = TestScheduler()
        self.test_reporter = TestReporter()
        self.ci_cd_integration = CICDIntegration()
        self.framework_status = "initialized"
        
        logger.info("Test automation framework initialized")
    
    def run_automated_test_suite(self, test_config: Optional[Dict[str, Any]] = None) -> Tuple[List[TestSuiteResult], str]:
        """Run automated test suite with configuration."""
        try:
            self.framework_status = "running"
            
            # Load default configuration if none provided
            if test_config is None:
                test_config = self._load_default_test_config()
            
            # Create test execution config
            execution_config = TestExecutionConfig(
                test_suite=test_config.get("test_suite", "baml"),
                test_categories=test_config.get("test_categories", ["parser", "validator", "xml_transformer"]),
                execution_mode=test_config.get("execution_mode", "parallel"),
                parallel_workers=test_config.get("parallel_workers", 4),
                timeout_seconds=test_config.get("timeout_seconds", 300),
                retry_attempts=test_config.get("retry_attempts", 2),
                enable_profiling=test_config.get("enable_profiling", True),
                enable_coverage=test_config.get("enable_coverage", True),
                enable_performance_monitoring=test_config.get("enable_performance_monitoring", True),
                output_directory=test_config.get("output_directory", "output"),
                log_directory=test_config.get("log_directory", "logs"),
                ci_cd_integration=test_config.get("ci_cd_integration", {})
            )
            
            # Run test suite
            suite_result = self.test_runner.run_test_suite(execution_config)
            
            # Generate reports
            json_report = self.test_reporter.generate_test_report(suite_result, "json")
            html_report = self.test_reporter.generate_test_report(suite_result, "html")
            junit_report = self.test_reporter.generate_test_report(suite_result, "junit")
            
            # Publish results to CI/CD
            self.ci_cd_integration.publish_results(suite_result.test_results, html_report)
            
            self.framework_status = "completed"
            
            return [suite_result], html_report
            
        except Exception as e:
            logger.error(f"Error running automated test suite: {e}")
            self.framework_status = "error"
            raise
    
    def schedule_continuous_testing(self, schedule_config: Dict[str, Any]) -> bool:
        """Schedule continuous automated testing."""
        try:
            self.test_scheduler.schedule_continuous_testing(schedule_config)
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling continuous testing: {e}")
            return False
    
    def setup_ci_cd_integration(self, ci_cd_config: Dict[str, Any]) -> bool:
        """Setup CI/CD integration."""
        try:
            success = True
            
            if ci_cd_config.get("github_actions", False):
                success &= self.ci_cd_integration.setup_github_actions(ci_cd_config.get("github_actions_config", {}))
            
            return success
            
        except Exception as e:
            logger.error(f"Error setting up CI/CD integration: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get test automation framework status."""
        return {
            "framework_status": self.framework_status,
            "test_runner_status": "active",
            "test_scheduler_status": "active" if self.test_scheduler.scheduler_active else "inactive",
            "test_reporter_status": "active",
            "ci_cd_integration_status": {
                "github_actions_enabled": self.ci_cd_integration.github_actions_enabled,
                "gitlab_ci_enabled": self.ci_cd_integration.gitlab_ci_enabled,
                "jenkins_enabled": self.ci_cd_integration.jenkins_enabled,
                "azure_devops_enabled": self.ci_cd_integration.azure_devops_enabled
            }
        }
    
    def _load_default_test_config(self) -> Dict[str, Any]:
        """Load default test configuration."""
        return {
            "test_suite": "baml",
            "test_categories": ["parser", "validator", "xml_transformer"],
            "execution_mode": "parallel",
            "parallel_workers": 4,
            "timeout_seconds": 300,
            "retry_attempts": 2,
            "enable_profiling": True,
            "enable_coverage": True,
            "enable_performance_monitoring": True,
            "output_directory": "output",
            "log_directory": "logs",
            "ci_cd_integration": {
                "github_actions": True,
                "gitlab_ci": True,
                "jenkins": False,
                "azure_devops": False
            }
        }

# Export main classes
__all__ = [
    'TestAutomationFramework',
    'TestRunner',
    'TestScheduler',
    'TestReporter',
    'CICDIntegration',
    'TestExecutionConfig',
    'TestResult',
    'TestSuiteResult',
    'TestStatus',
    'TestPriority'
]

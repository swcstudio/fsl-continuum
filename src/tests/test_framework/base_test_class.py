"""
FSL Continuum - Semantic Language Base Test Class

Base test class for all semantic language testing components.
Provides common testing utilities, setup/teardown, and test framework integration.
"""

import time
import logging
import unittest
from typing import Dict, List, Optional, Any, Union, Tuple, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from unittest.mock import Mock, MagicMock

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TestEnvironment:
    """Test environment configuration."""
    environment_name: str
    python_version: str
    semantic_languages_version: str
    xml_transformation_version: str
    ai_integration_version: str
    test_data_path: str
    fixtures_path: str
    output_path: str
    temp_path: str
    debug_mode: bool = False
    performance_monitoring: bool = True
    error_simulation: bool = False

@dataclass
class TestResult:
    """Result of a test execution."""
    test_name: str
    success: bool
    execution_time: float
    memory_usage: float
    error_message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    performance_metrics: Optional[Dict[str, Any]] = None

class SemanticLanguageBaseTest:
    """Base test class for all semantic language testing components."""
    
    def __init__(self):
        # Import semantic language components
        try:
            from ..semantic_languages import SemanticLanguageManager
            self.semantic_manager = SemanticLanguageManager()
        except ImportError as e:
            logger.error(f"Failed to import semantic language manager: {e}")
            self.semantic_manager = None
        
        # Test environment
        self.test_environment = None
        self.test_data = None
        self.test_fixtures = None
        self.mock_components = None
        self.test_utils = None
        self.test_config = None
        
        # Test execution tracking
        self.test_results = []
        self.performance_metrics = {}
        self.error_scenarios = []
        self.memory_snapshots = []
        
        # Test configuration
        self.test_timeout = 300  # 5 minutes default
        self.memory_limit = 1024  # 1GB default
        self.performance_thresholds = {
            "max_execution_time": 2.0,  # 2 seconds
            "max_memory_usage": 256,  # 256MB
            "min_success_rate": 0.95  # 95%
        }
    
    def setup_method(self, method_name: str):
        """Setup test method environment."""
        try:
            logger.info(f"Setting up test method: {method_name}")
            
            # Initialize test environment
            self.test_environment = self._create_test_environment()
            
            # Initialize test data
            self.test_data = self._load_test_data()
            
            # Initialize test fixtures
            self.test_fixtures = self._load_test_fixtures()
            
            # Initialize mock components
            self.mock_components = self._initialize_mock_components()
            
            # Initialize test utilities
            self.test_utils = self._initialize_test_utils()
            
            # Initialize test configuration
            self.test_config = self._initialize_test_configuration()
            
            # Setup monitoring
            self._setup_monitoring()
            
            logger.info(f"Test method setup complete: {method_name}")
            
        except Exception as e:
            logger.error(f"Failed to setup test method {method_name}: {e}")
            raise
    
    def teardown_method(self, method_name: str):
        """Teardown test method environment."""
        try:
            logger.info(f"Tearing down test method: {method_name}")
            
            # Cleanup test environment
            self._cleanup_test_environment()
            
            # Generate test report
            self._generate_test_report(method_name)
            
            # Reset test state
            self._reset_test_state()
            
            logger.info(f"Test method teardown complete: {method_name}")
            
        except Exception as e:
            logger.error(f"Failed to teardown test method {method_name}: {e}")
            raise
    
    def _create_test_environment(self) -> TestEnvironment:
        """Create test environment configuration."""
        import sys
        import platform
        
        return TestEnvironment(
            environment_name="semantic-language-test",
            python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            semantic_languages_version="1.0.0-fsl-integration",
            xml_transformation_version="1.0.0-xml-integration",
            ai_integration_version="1.0.0-ai-integration",
            test_data_path=str(Path(__file__).parent.parent / "fixtures" / "test_data"),
            fixtures_path=str(Path(__file__).parent.parent / "fixtures"),
            output_path=str(Path(__file__).parent.parent / "output"),
            temp_path=str(Path(__file__).parent.parent / "temp"),
            debug_mode=self.test_config.debug_mode if self.test_config else False,
            performance_monitoring=True,
            error_simulation=False
        )
    
    def _load_test_data(self) -> Dict[str, Any]:
        """Load test data for semantic language testing."""
        test_data = {}
        
        try:
            # Load BAML test data
            baml_test_data_path = Path(self.test_environment.test_data_path) / "baml_test_data"
            if baml_test_data_path.exists():
                test_data["baml"] = self._load_yaml_files(baml_test_data_path)
            
            # Load Pareto-Lang test data
            pareto_test_data_path = Path(self.test_environment.test_data_path) / "pareto_lang_test_data"
            if pareto_test_data_path.exists():
                test_data["pareto_lang"] = self._load_yaml_files(pareto_test_data_path)
            
            # Load XML test data
            xml_test_data_path = Path(self.test_environment.test_data_path) / "xml_test_data"
            if xml_test_data_path.exists():
                test_data["xml"] = self._load_xml_files(xml_test_data_path)
            
            # Load integration test data
            integration_test_data_path = Path(self.test_environment.test_data_path) / "integration_test_data"
            if integration_test_data_path.exists():
                test_data["integration"] = self._load_yaml_files(integration_test_data_path)
            
            return test_data
            
        except Exception as e:
            logger.error(f"Failed to load test data: {e}")
            return {}
    
    def _load_test_fixtures(self) -> Dict[str, Any]:
        """Load test fixtures for semantic language testing."""
        fixtures = {}
        
        try:
            fixtures_path = Path(self.test_environment.fixtures_path)
            
            # Load BAML fixtures
            baml_fixtures_path = fixtures_path / "baml_test_data"
            if baml_fixtures_path.exists():
                fixtures["baml"] = self._load_yaml_files(baml_fixtures_path)
            
            # Load Pareto-Lang fixtures
            pareto_fixtures_path = fixtures_path / "pareto_lang_test_data"
            if pareto_fixtures_path.exists():
                fixtures["pareto_lang"] = self._load_yaml_files(pareto_fixtures_path)
            
            # Load XML fixtures
            xml_fixtures_path = fixtures_path / "xml_test_data"
            if xml_fixtures_path.exists():
                fixtures["xml"] = self._load_xml_files(xml_fixtures_path)
            
            return fixtures
            
        except Exception as e:
            logger.error(f"Failed to load test fixtures: {e}")
            return {}
    
    def _initialize_mock_components(self):
        """Initialize mock components for testing."""
        return MockComponents()
    
    def _initialize_test_utils(self):
        """Initialize test utilities."""
        try:
            from .test_utils import TestUtils
            return TestUtils()
        except ImportError:
            logger.warning("TestUtils not available, using basic utilities")
            return BasicTestUtils()
    
    def _initialize_test_configuration(self):
        """Initialize test configuration."""
        return TestConfig()
    
    def _setup_monitoring(self):
        """Setup test monitoring."""
        if self.test_environment.performance_monitoring:
            self._setup_performance_monitoring()
        
        if self.test_environment.debug_mode:
            self._setup_debug_monitoring()
    
    def _cleanup_test_environment(self):
        """Cleanup test environment."""
        try:
            # Clean up temporary files
            temp_path = Path(self.test_environment.temp_path)
            if temp_path.exists():
                for temp_file in temp_path.glob("*"):
                    try:
                        temp_file.unlink()
                    except Exception as e:
                        logger.warning(f"Failed to delete temp file {temp_file}: {e}")
            
            # Clean up output files
            output_path = Path(self.test_environment.output_path)
            if output_path.exists():
                for output_file in output_path.glob("*"):
                    if output_file.is_file():
                        try:
                            output_file.unlink()
                        except Exception as e:
                            logger.warning(f"Failed to delete output file {output_file}: {e}")
        
        except Exception as e:
            logger.error(f"Failed to cleanup test environment: {e}")
    
    def _generate_test_report(self, method_name: str):
        """Generate test report for method."""
        try:
            report = {
                "method_name": method_name,
                "test_environment": asdict(self.test_environment),
                "test_results": self.test_results,
                "performance_metrics": self.performance_metrics,
                "memory_snapshots": self.memory_snapshots,
                "error_scenarios": self.error_scenarios,
                "timestamp": time.time()
            }
            
            # Save report to file
            report_path = Path(self.test_environment.output_path) / f"{method_name}_report.json"
            with open(report_path, 'w') as f:
                import json
                json.dump(report, f, indent=2)
            
        except Exception as e:
            logger.error(f"Failed to generate test report: {e}")
    
    def _reset_test_state(self):
        """Reset test state for next test."""
        self.test_results = []
        self.performance_metrics = {}
        self.error_scenarios = []
        self.memory_snapshots = []
    
    def _load_yaml_files(self, directory_path: Path) -> Dict[str, Any]:
        """Load YAML files from directory."""
        import yaml
        
        data = {}
        try:
            for yaml_file in directory_path.glob("*.yaml"):
                with open(yaml_file, 'r') as f:
                    file_data = yaml.safe_load(f)
                    data[yaml_file.stem] = file_data
        except Exception as e:
            logger.error(f"Failed to load YAML files from {directory_path}: {e}")
        
        return data
    
    def _load_xml_files(self, directory_path: Path) -> Dict[str, Any]:
        """Load XML files from directory."""
        import xml.etree.ElementTree as ET
        
        data = {}
        try:
            for xml_file in directory_path.glob("*.xml"):
                xml_tree = ET.parse(xml_file)
                xml_root = xml_tree.getroot()
                data[xml_file.stem] = xml_root
        except Exception as e:
            logger.error(f"Failed to load XML files from {directory_path}: {e}")
        
        return data
    
    def _setup_performance_monitoring(self):
        """Setup performance monitoring."""
        try:
            import psutil
            self.process = psutil.Process()
            self.initial_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        except ImportError:
            logger.warning("psutil not available, performance monitoring limited")
    
    def _setup_debug_monitoring(self):
        """Setup debug monitoring."""
        self.debug_log = []
    
    def run_test_with_monitoring(self, test_function: Callable, *args, **kwargs) -> TestResult:
        """Run test function with monitoring."""
        start_time = time.time()
        start_memory = self._get_memory_usage() if hasattr(self, '_get_memory_usage') else 0
        
        try:
            # Execute test function
            result = test_function(*args, **kwargs)
            success = True
            error_message = None
            
        except Exception as e:
            success = False
            error_message = str(e)
            result = None
            logger.error(f"Test execution failed: {error_message}")
        
        end_time = time.time()
        end_memory = self._get_memory_usage() if hasattr(self, '_get_memory_usage') else 0
        
        # Calculate metrics
        execution_time = end_time - start_time
        memory_usage = max(end_memory - start_memory, 0)
        
        # Create test result
        test_result = TestResult(
            test_name=test_function.__name__,
            success=success,
            execution_time=execution_time,
            memory_usage=memory_usage,
            error_message=error_message,
            details={"result": result},
            performance_metrics={
                "start_memory": start_memory,
                "end_memory": end_memory,
                "memory_delta": memory_usage,
                "execution_time": execution_time
            }
        )
        
        # Store test result
        self.test_results.append(asdict(test_result))
        
        # Check performance thresholds
        self._check_performance_thresholds(test_result)
        
        return test_result
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            if hasattr(self, 'process'):
                return self.process.memory_info().rss / 1024 / 1024
            return 0
        except Exception:
            return 0
    
    def _check_performance_thresholds(self, test_result: TestResult):
        """Check if test results meet performance thresholds."""
        warnings = []
        
        # Check execution time
        if test_result.execution_time > self.performance_thresholds["max_execution_time"]:
            warnings.append(f"Execution time exceeded threshold: {test_result.execution_time:.3f}s > {self.performance_thresholds['max_execution_time']}s")
        
        # Check memory usage
        if test_result.memory_usage > self.performance_thresholds["max_memory_usage"]:
            warnings.append(f"Memory usage exceeded threshold: {test_result.memory_usage:.2f}MB > {self.performance_thresholds['max_memory_usage']}MB")
        
        # Log warnings if any
        for warning in warnings:
            logger.warning(f"Performance warning: {warning}")
    
    def assert_test_result(self, test_result: TestResult, expected_success: bool = True):
        """Assert test result meets expectations."""
        assert test_result.success == expected_success, f"Test {'should' if expected_success else 'should not'} have succeeded"
        
        if not test_result.success:
            assert test_result.error_message is not None, "Test failed but no error message provided"
            logger.info(f"Test failed as expected: {test_result.error_message}")
    
    def assert_performance_thresholds(self, test_result: TestResult):
        """Assert test result meets performance thresholds."""
        if test_result.execution_time > self.performance_thresholds["max_execution_time"]:
            raise AssertionError(f"Execution time exceeded threshold: {test_result.execution_time:.3f}s > {self.performance_thresholds['max_execution_time']}s")
        
        if test_result.memory_usage > self.performance_thresholds["max_memory_usage"]:
            raise AssertionError(f"Memory usage exceeded threshold: {test_result.memory_usage:.2f}MB > {self.performance_thresholds['max_memory_usage']}MB")
    
    def get_test_summary(self) -> Dict[str, Any]:
        """Get summary of test results."""
        if not self.test_results:
            return {"status": "no_tests_run"}
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result["success"])
        
        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": successful_tests / total_tests,
            "average_execution_time": sum(result["execution_time"] for result in self.test_results) / total_tests,
            "average_memory_usage": sum(result["memory_usage"] for result in self.test_results) / total_tests,
            "test_environment": asdict(self.test_environment) if self.test_environment else None,
            "performance_thresholds_met": all(
                result["execution_time"] <= self.performance_thresholds["max_execution_time"] and
                result["memory_usage"] <= self.performance_thresholds["max_memory_usage"]
                for result in self.test_results
            )
        }

class BasicTestUtils:
    """Basic test utilities for when TestUtils is not available."""
    
    def __init__(self):
        pass
    
    def validate_xml_structure(self, xml_string: str, expected_structure: Dict[str, Any]) -> bool:
        """Basic XML structure validation."""
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(xml_string)
            return True
        except ET.ParseError:
            return False
    
    def validate_semantic_preservation(self, original_data: Dict[str, Any], transformed_data: Dict[str, Any]) -> bool:
        """Basic semantic preservation validation."""
        return original_data == transformed_data

class MockComponents:
    """Mock components for testing."""
    
    def __init__(self):
        self.mock_baml_parser = Mock()
        self.mock_pareto_lang_parser = Mock()
        self.mock_xml_processor = Mock()
        self.mock_ai_processor = Mock()
    
    def create_mock_baml_parser(self):
        """Create mock BAML parser."""
        return self.mock_baml_parser
    
    def create_mock_pareto_lang_parser(self):
        """Create mock Pareto-Lang parser."""
        return self.mock_pareto_lang_parser
    
    def create_mock_xml_processor(self):
        """Create mock XML processor."""
        return self.mock_xml_processor
    
    def create_mock_ai_processor(self):
        """Create mock AI processor."""
        return self.mock_ai_processor

class TestConfig:
    """Test configuration."""
    
    def __init__(self):
        self.debug_mode = False
        self.performance_monitoring = True
        self.error_simulation = False
        self.test_timeout = 300
        self.memory_limit = 1024
        self.log_level = "INFO"
    
    def get_test_environment(self):
        """Get test environment configuration."""
        return {
            "debug_mode": self.debug_mode,
            "performance_monitoring": self.performance_monitoring,
            "error_simulation": self.error_simulation,
            "test_timeout": self.test_timeout,
            "memory_limit": self.memory_limit,
            "log_level": self.log_level
        }

# Export main classes
__all__ = [
    'SemanticLanguageBaseTest',
    'TestEnvironment',
    'TestResult',
    'MockComponents',
    'TestConfig',
    'BasicTestUtils'
]

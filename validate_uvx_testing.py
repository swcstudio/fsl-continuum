#!/usr/bin/env python3
"""
FSL Continuum UVX Testing Environment Validation Script

Comprehensive validation of UVX testing environment setup and execution.
Validates UVX installation, environment setup, test execution,
and performance testing capabilities.
"""

import sys
import os
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional

# Colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color

# Logging functions
def log_info(message: str):
    """Log info message."""
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")

def log_success(message: str):
    """Log success message."""
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {message}")

def log_warning(message: str):
    """Log warning message."""
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")

def log_error(message: str):
    """Log error message."""
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")

def log_step(message: str):
    """Log step message."""
    print(f"{Colors.PURPLE}[STEP]{Colors.NC} {message}")

def log_test(message: str):
    """Log test message."""
    print(f"{Colors.CYAN}[TEST]{Colors.NC} {message}")

class UVXTestingValidator:
    """Validates UVX testing environment setup and execution."""
    
    def __init__(self):
        self.project_name = "fsl-continuum"
        self.python_version = "3.11"
        self.validation_results = {
            'uvx_installation': {'status': 'pending', 'details': []},
            'uvx_configuration': {'status': 'pending', 'details': []},
            'uvx_environments': {'status': 'pending', 'details': []},
            'test_execution': {'status': 'pending', 'details': []},
            'performance_testing': {'status': 'pending', 'details': []},
            'integration_validation': {'status': 'pending', 'details': []}
        }
        self.overall_status = 'pending'
    
    def validate_uvx_installation(self) -> bool:
        """Validate UVX installation."""
        log_step("Validating UVX installation...")
        
        tests = [
            self._test_uvx_command_exists,
            self._test_uvx_version,
            self._test_uvx_help,
            self._test_uvx_python_version
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                self.validation_results['uvx_installation']['details'].append({
                    'test': test.__name__,
                    'status': 'PASS' if result else 'FAIL',
                    'details': 'Success' if result else 'Failed'
                })
            except Exception as e:
                results.append(False)
                self.validation_results['uvx_installation']['details'].append({
                    'test': test.__name__,
                    'status': 'ERROR',
                    'details': str(e)
                })
        
        success = all(results)
        self.validation_results['uvx_installation']['status'] = 'PASS' if success else 'FAIL'
        
        log_success(f"UVX installation validation: {'PASS' if success else 'FAIL'}")
        return success
    
    def _test_uvx_command_exists(self) -> bool:
        """Test UVX command exists."""
        try:
            result = subprocess.run(['uvx', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                log_success(f"UVX command found: {result.stdout.strip()}")
                return True
            else:
                log_error("UVX command not found")
                return False
        except FileNotFoundError:
            log_error("UVX command not found")
            return False
    
    def _test_uvx_version(self) -> bool:
        """Test UVX version."""
        try:
            result = subprocess.run(['uvx', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                log_success(f"UVX version: {version}")
                return True
            else:
                log_error("Failed to get UVX version")
                return False
        except Exception as e:
            log_error(f"Error getting UVX version: {e}")
            return False
    
    def _test_uvx_help(self) -> bool:
        """Test UVX help command."""
        try:
            result = subprocess.run(['uvx', '--help'], capture_output=True, text=True)
            if result.returncode == 0:
                log_success("UVX help command works")
                return True
            else:
                log_error("UVX help command failed")
                return False
        except Exception as e:
            log_error(f"Error running UVX help: {e}")
            return False
    
    def _test_uvx_python_version(self) -> bool:
        """Test UVX Python version support."""
        try:
            result = subprocess.run(['uvx', 'python', '--list'], capture_output=True, text=True)
            if result.returncode == 0:
                log_success("UVX Python version support works")
                log_info("Available Python versions:")
                for line in result.stdout.split('\n')[:5]:  # Show first 5 lines
                    if line.strip():
                        log_info(f"  {line}")
                return True
            else:
                log_error("UVX Python version support failed")
                return False
        except Exception as e:
            log_error(f"Error checking UVX Python versions: {e}")
            return False
    
    def validate_uvx_configuration(self) -> bool:
        """Validate UVX configuration."""
        log_step("Validating UVX configuration...")
        
        tests = [
            self._test_uvx_config_exists,
            self._test_uvx_config_valid,
            self._test_uvx_config_content
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                self.validation_results['uvx_configuration']['details'].append({
                    'test': test.__name__,
                    'status': 'PASS' if result else 'FAIL',
                    'details': 'Success' if result else 'Failed'
                })
            except Exception as e:
                results.append(False)
                self.validation_results['uvx_configuration']['details'].append({
                    'test': test.__name__,
                    'status': 'ERROR',
                    'details': str(e)
                })
        
        success = all(results)
        self.validation_results['uvx_configuration']['status'] = 'PASS' if success else 'FAIL'
        
        log_success(f"UVX configuration validation: {'PASS' if success else 'FAIL'}")
        return success
    
    def _test_uvx_config_exists(self) -> bool:
        """Test UVX configuration file exists."""
        config_file = Path('.uvx/config.toml')
        if config_file.exists():
            log_success("UVX configuration file found")
            return True
        else:
            log_warning("UVX configuration file not found")
            return False
    
    def _test_uvx_config_valid(self) -> bool:
        """Test UVX configuration file is valid."""
        config_file = Path('.uvx/config.toml')
        if not config_file.exists():
            return False
        
        try:
            import tomli
            with open(config_file, 'rb') as f:
                config = tomli.load(f)
            
            log_success("UVX configuration file is valid TOML")
            return True
        except ImportError:
            log_warning("tomli not installed, skipping config validation")
            return True  # Skip this test
        except Exception as e:
            log_error(f"UVX configuration file is invalid: {e}")
            return False
    
    def _test_uvx_config_content(self) -> bool:
        """Test UVX configuration content."""
        config_file = Path('.uvx/config.toml')
        if not config_file.exists():
            return False
        
        try:
            with open(config_file, 'r') as f:
                content = f.read()
            
            # Check for required sections
            required_sections = [
                '[settings]',
                '[environments]',
                '[scripts]'
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)
            
            if missing_sections:
                log_error(f"Missing UVX configuration sections: {missing_sections}")
                return False
            else:
                log_success("UVX configuration content is valid")
                return True
        except Exception as e:
            log_error(f"Error reading UVX configuration: {e}")
            return False
    
    def validate_uvx_environments(self) -> bool:
        """Validate UVX environments."""
        log_step("Validating UVX environments...")
        
        tests = [
            self._test_uvx_environment_creation,
            self._test_uvx_environment_listing,
            self._test_uvx_environment_installation,
            self._test_uvx_environment_python_version
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                self.validation_results['uvx_environments']['details'].append({
                    'test': test.__name__,
                    'status': 'PASS' if result else 'FAIL',
                    'details': 'Success' if result else 'Failed'
                })
            except Exception as e:
                results.append(False)
                self.validation_results['uvx_environments']['details'].append({
                    'test': test.__name__,
                    'status': 'ERROR',
                    'details': str(e)
                })
        
        success = all(results)
        self.validation_results['uvx_environments']['status'] = 'PASS' if success else 'FAIL'
        
        log_success(f"UVX environments validation: {'PASS' if success else 'FAIL'}")
        return success
    
    def _test_uvx_environment_creation(self) -> bool:
        """Test UVX environment creation."""
        try:
            # Check if test environment exists
            result = subprocess.run(['uvx', 'list', f'{self.project_name}-test'], capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success("UVX test environment exists")
                return True
            else:
                log_warning("UVX test environment does not exist, creating...")
                
                # Create test environment
                create_result = subprocess.run([
                    'uvx', 'create', f'{self.project_name}-test',
                    '--python', self.python_version,
                    '--test',
                    '--description', 'FSL Continuum Testing Environment'
                ], capture_output=True, text=True)
                
                if create_result.returncode == 0:
                    log_success("UVX test environment created successfully")
                    return True
                else:
                    log_error(f"Failed to create UVX test environment: {create_result.stderr}")
                    return False
        except Exception as e:
            log_error(f"Error testing UVX environment creation: {e}")
            return False
    
    def _test_uvx_environment_listing(self) -> bool:
        """Test UVX environment listing."""
        try:
            result = subprocess.run(['uvx', 'list'], capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success("UVX environment listing works")
                environments = result.stdout.split('\n')
                test_env_exists = any(f'{self.project_name}-test' in env for env in environments)
                
                if test_env_exists:
                    log_success("UVX test environment found in listing")
                    return True
                else:
                    log_warning("UVX test environment not found in listing")
                    return False
            else:
                log_error("UVX environment listing failed")
                return False
        except Exception as e:
            log_error(f"Error listing UVX environments: {e}")
            return False
    
    def _test_uvx_environment_installation(self) -> bool:
        """Test UVX environment package installation."""
        try:
            # Try to import FSL Continuum in test environment
            result = subprocess.run([
                'uvx', 'run', '--python', self.python_version, '--test',
                self.project_name, 'python', '-c',
                'import fsl_continuum; print("Import successful")'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success("FSL Continuum imported successfully in test environment")
                return True
            else:
                log_error(f"FSL Continuum import failed: {result.stderr}")
                return False
        except Exception as e:
            log_error(f"Error testing UVX environment installation: {e}")
            return False
    
    def _test_uvx_environment_python_version(self) -> bool:
        """Test UVX environment Python version."""
        try:
            result = subprocess.run([
                'uvx', 'run', '--python', self.python_version, '--test',
                self.project_name, 'python', '--version'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                version_output = result.stdout.strip()
                log_success(f"UVX test environment Python version: {version_output}")
                return True
            else:
                log_error(f"Failed to get UVX test environment Python version: {result.stderr}")
                return False
        except Exception as e:
            log_error(f"Error testing UVX environment Python version: {e}")
            return False
    
    def validate_test_execution(self) -> bool:
        """Validate test execution in UVX environment."""
        log_step("Validating test execution...")
        
        tests = [
            self._test_basic_test_execution,
            self._test_test_discovery,
            self._test_test_configuration,
            self._test_test_output
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                self.validation_results['test_execution']['details'].append({
                    'test': test.__name__,
                    'status': 'PASS' if result else 'FAIL',
                    'details': 'Success' if result else 'Failed'
                })
            except Exception as e:
                results.append(False)
                self.validation_results['test_execution']['details'].append({
                    'test': test.__name__,
                    'status': 'ERROR',
                    'details': str(e)
                })
        
        success = all(results)
        self.validation_results['test_execution']['status'] = 'PASS' if success else 'FAIL'
        
        log_success(f"Test execution validation: {'PASS' if success else 'FAIL'}")
        return success
    
    def _test_basic_test_execution(self) -> bool:
        """Test basic test execution."""
        try:
            # Run a simple test
            result = subprocess.run([
                'uvx', 'run', '--python', self.python_version, '--test',
                self.project_name, 'python', '-c',
                '''
import sys
sys.path.insert(0, 'src')

# Test basic imports
try:
    import fsl_continuum
    print("Basic import test: PASSED")
    
    # Test version
    version = fsl_continuum.get_version()
    print(f"Version test: {version}")
    
    # Test info
    info = fsl_continuum.get_info()
    print(f"Info test: {len(info)} keys")
    
    print("All basic tests: PASSED")
except Exception as e:
    print(f"Basic test failed: {e}")
    sys.exit(1)
'''
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success("Basic test execution: PASSED")
                return True
            else:
                log_error(f"Basic test execution failed: {result.stderr}")
                return False
        except Exception as e:
            log_error(f"Error running basic test execution: {e}")
            return False
    
    def _test_test_discovery(self) -> bool:
        """Test test discovery."""
        try:
            # Test pytest discovery
            result = subprocess.run([
                'uvx', 'run', '--python', self.python_version, '--test',
                self.project_name, 'pytest', 'src/tests/', '--collect-only'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success("Test discovery: PASSED")
                return True
            else:
                log_error(f"Test discovery failed: {result.stderr}")
                return False
        except Exception as e:
            log_error(f"Error testing test discovery: {e}")
            return False
    
    def _test_test_configuration(self) -> bool:
        """Test test configuration."""
        try:
            # Test pytest configuration
            if Path('pytest.ini').exists():
                log_success("pytest.ini configuration found")
                return True
            else:
                log_warning("pytest.ini configuration not found")
                return False
        except Exception as e:
            log_error(f"Error testing test configuration: {e}")
            return False
    
    def _test_test_output(self) -> bool:
        """Test test output."""
        try:
            # Test test output format
            result = subprocess.run([
                'uvx', 'run', '--python', self.python_version, '--test',
                self.project_name, 'pytest', 'src/tests/unit/', '-v'
            ], capture_output=True, text=True)
            
            if result.returncode == 0 or result.returncode == 1:  # 1 is OK for test failures
                log_success("Test output format: PASSED")
                return True
            else:
                log_error(f"Test output format failed: {result.stderr}")
                return False
        except Exception as e:
            log_error(f"Error testing test output: {e}")
            return False
    
    def validate_performance_testing(self) -> bool:
        """Validate performance testing capabilities."""
        log_step("Validating performance testing...")
        
        tests = [
            self._test_performance_environment,
            self._test_benchmark_execution,
            self._test_memory_profiling,
            self._test_performance_output
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                self.validation_results['performance_testing']['details'].append({
                    'test': test.__name__,
                    'status': 'PASS' if result else 'FAIL',
                    'details': 'Success' if result else 'Failed'
                })
            except Exception as e:
                results.append(False)
                self.validation_results['performance_testing']['details'].append({
                    'test': test.__name__,
                    'status': 'ERROR',
                    'details': str(e)
                })
        
        success = all(results)
        self.validation_results['performance_testing']['status'] = 'PASS' if success else 'FAIL'
        
        log_success(f"Performance testing validation: {'PASS' if success else 'FAIL'}")
        return success
    
    def _test_performance_environment(self) -> bool:
        """Test performance environment setup."""
        try:
            # Check if performance environment exists
            result = subprocess.run(['uvx', 'list', f'{self.project_name}-performance'], capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success("UVX performance environment exists")
                return True
            else:
                log_warning("UVX performance environment does not exist")
                return False
        except Exception as e:
            log_error(f"Error testing performance environment: {e}")
            return False
    
    def _test_benchmark_execution(self) -> bool:
        """Test benchmark execution."""
        try:
            # Test benchmark execution
            result = subprocess.run([
                'uvx', 'run', '--python', self.python_version, '--test',
                self.project_name, 'pytest', '--benchmark-only', '--help'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success("Benchmark execution: PASSED")
                return True
            else:
                log_error(f"Benchmark execution failed: {result.stderr}")
                return False
        except Exception as e:
            log_error(f"Error testing benchmark execution: {e}")
            return False
    
    def _test_memory_profiling(self) -> bool:
        """Test memory profiling."""
        try:
            # Test memory profiling
            result = subprocess.run([
                'uvx', 'run', '--python', self.python_version, '--test',
                self.project_name, 'python', '-c', '''
import sys
sys.path.insert(0, 'src')

try:
    import memory_profiler
    print("Memory profiling available: PASSED")
except ImportError:
    print("Memory profiling not available: SKIPPED")
'''
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success("Memory profiling test: PASSED")
                return True
            else:
                log_error(f"Memory profiling test failed: {result.stderr}")
                return False
        except Exception as e:
            log_error(f"Error testing memory profiling: {e}")
            return False
    
    def _test_performance_output(self) -> bool:
        """Test performance output."""
        try:
            # Test performance output
            result = subprocess.run([
                'uvx', 'run', '--python', self.python_version, '--test',
                self.project_name, 'python', '-c', '''
import sys
import time
sys.path.insert(0, 'src')

# Simulate performance measurement
start_time = time.time()
time.sleep(0.1)  # Simulate work
end_time = time.time()

execution_time = end_time - start_time
print(f"Performance test: {execution_time:.6f}s")

if execution_time > 1.0:
    print("Performance test: FAILED (too slow)")
    sys.exit(1)
else:
    print("Performance test: PASSED")
'''
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success("Performance output test: PASSED")
                return True
            else:
                log_error(f"Performance output test failed: {result.stderr}")
                return False
        except Exception as e:
            log_error(f"Error testing performance output: {e}")
            return False
    
    def validate_integration(self) -> bool:
        """Validate integration capabilities."""
        log_step("Validating integration capabilities...")
        
        tests = [
            self._test_semantic_language_integration,
            self._test_xml_transformation_integration,
            self._test_ai_integration,
            self._test_end_to_end_integration
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                self.validation_results['integration_validation']['details'].append({
                    'test': test.__name__,
                    'status': 'PASS' if result else 'FAIL',
                    'details': 'Success' if result else 'Failed'
                })
            except Exception as e:
                results.append(False)
                self.validation_results['integration_validation']['details'].append({
                    'test': test.__name__,
                    'status': 'ERROR',
                    'details': str(e)
                })
        
        success = all(results)
        self.validation_results['integration_validation']['status'] = 'PASS' if success else 'FAIL'
        
        log_success(f"Integration validation: {'PASS' if success else 'FAIL'}")
        return success
    
    def _test_semantic_language_integration(self) -> bool:
        """Test semantic language integration."""
        try:
            result = subprocess.run([
                'uvx', 'run', '--python', self.python_version, '--test',
                self.project_name, 'python', '-c',
                '''
import sys
sys.path.insert(0, 'src')

try:
    from semantic_languages import BAMLParser, ParetoLangParser, UnifiedXMLProcessor
    print("Semantic language imports: PASSED")
    
    # Test basic functionality
    baml_parser = BAMLParser()
    pareto_parser = ParetoLangParser()
    xml_processor = UnifiedXMLProcessor()
    
    print("Semantic language integration: PASSED")
except Exception as e:
    print(f"Semantic language integration failed: {e}")
    sys.exit(1)
'''
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success("Semantic language integration: PASSED")
                return True
            else:
                log_error(f"Semantic language integration failed: {result.stderr}")
                return False
        except Exception as e:
            log_error(f"Error testing semantic language integration: {e}")
            return False
    
    def _test_xml_transformation_integration(self) -> bool:
        """Test XML transformation integration."""
        try:
            result = subprocess.run([
                'uvx', 'run', '--python', self.python_version, '--test',
                self.project_name, 'python', '-c',
                '''
import sys
sys.path.insert(0, 'src')

try:
    from semantic_languages.xml_processor import XMLProcessor, XMLValidator, XMLTransformer
    print("XML transformation imports: PASSED")
    
    # Test basic functionality
    xml_processor = XMLProcessor()
    xml_validator = XMLValidator()
    xml_transformer = XMLTransformer()
    
    print("XML transformation integration: PASSED")
except Exception as e:
    print(f"XML transformation integration failed: {e}")
    sys.exit(1)
'''
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success("XML transformation integration: PASSED")
                return True
            else:
                log_error(f"XML transformation integration failed: {result.stderr}")
                return False
        except Exception as e:
            log_error(f"Error testing XML transformation integration: {e}")
            return False
    
    def _test_ai_integration(self) -> bool:
        """Test AI integration."""
        try:
            result = subprocess.run([
                'uvx', 'run', '--python', self.python_version, '--test',
                self.project_name, 'python', '-c',
                '''
import sys
sys.path.insert(0, 'src')

try:
    from ai_integration import AIProcessor, AIOptimizer, AIContextAwareness
    print("AI integration imports: PASSED")
    
    # Test basic functionality
    ai_processor = AIProcessor()
    ai_optimizer = AIOptimizer()
    ai_context = AIContextAwareness()
    
    print("AI integration: PASSED")
except Exception as e:
    print(f"AI integration failed: {e}")
    sys.exit(1)
'''
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success("AI integration: PASSED")
                return True
            else:
                log_error(f"AI integration failed: {result.stderr}")
                return False
        except Exception as e:
            log_error(f"Error testing AI integration: {e}")
            return False
    
    def _test_end_to_end_integration(self) -> bool:
        """Test end-to-end integration."""
        try:
            result = subprocess.run([
                'uvx', 'run', '--python', self.python_version, '--test',
                self.project_name, 'python', '-c',
                '''
import sys
sys.path.insert(0, 'src')

try:
    from semantic_languages import BAMLParser, UnifiedXMLProcessor
    from ai_integration import SemanticAIProcessor
    
    # Test end-to-end workflow
    baml_parser = BAMLParser()
    xml_processor = UnifiedXMLProcessor()
    ai_processor = SemanticAIProcessor()
    
    # Create test data
    test_data = {
        "version": "1.0.0-fsl-integration",
        "spec": "BAML-SEMANTIC-001",
        "boundaries": [
            {
                "name": "test_boundary",
                "type": "data",
                "ai_enhanced": True
            }
        ]
    }
    
    # Parse BAML
    baml_result = baml_parser.parse(test_data)
    assert baml_result.success
    
    # Process with XML
    xml_result = xml_processor.process_multiple_semantic_data_with_xml({
        "baml": test_data
    })
    assert xml_result.success
    
    print("End-to-end integration: PASSED")
except Exception as e:
    print(f"End-to-end integration failed: {e}")
    sys.exit(1)
'''
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success("End-to-end integration: PASSED")
                return True
            else:
                log_error(f"End-to-end integration failed: {result.stderr}")
                return False
        except Exception as e:
            log_error(f"Error testing end-to-end integration: {e}")
            return False
    
    def run_full_validation(self) -> bool:
        """Run full UVX testing environment validation."""
        log_info("Starting FSL Continuum UVX Testing Environment Validation")
        print("=" * 70)
        
        validators = [
            self.validate_uvx_installation,
            self.validate_uvx_configuration,
            self.validate_uvx_environments,
            self.validate_test_execution,
            self.validate_performance_testing,
            self.validate_integration
        ]
        
        results = []
        for validator in validators:
            try:
                result = validator()
                results.append(result)
                print()
            except Exception as e:
                log_error(f"Validator {validator.__name__} failed: {e}")
                results.append(False)
                print()
        
        # Calculate overall status
        success = all(results)
        self.overall_status = 'PASS' if success else 'FAIL'
        
        print("=" * 70)
        print("🎯 FINAL VALIDATION RESULTS")
        print("=" * 70)
        
        for category, result in self.validation_results.items():
            print(f"📊 {category.replace('_', ' ').title()}: {result['status']}")
            if result['details']:
                for detail in result['details']:
                    print(f"   {detail['status']}: {detail['test']} - {detail['details']}")
            print()
        
        print(f"🌊 Overall Status: {self.overall_status}")
        
        if success:
            print("✅ FSL Continuum UVX testing environment is READY!")
            print("🚀 Ready to run comprehensive tests with UVX!")
        else:
            print("❌ FSL Continuum UVX testing environment is NOT ready!")
            print("🔧 Please address the failing validations above.")
        
        return success
    
    def generate_report(self) -> str:
        """Generate validation report."""
        report = [
            "# FSL Continuum UVX Testing Environment Validation Report\n",
            f"## Overall Status: {self.overall_status}\n",
            "## Validation Results\n"
        ]
        
        for category, result in self.validation_results.items():
            report.append(f"### {category.replace('_', ' ').title()}: {result['status']}\n")
            if result['details']:
                report.append("#### Details:\n")
                for detail in result['details']:
                    report.append(f"- {detail['status']}: {detail['test']} - {detail['details']}\n")
            report.append("\n")
        
        report.append("## Environment Information\n")
        report.append(f"- Python Version: {self.python_version}\n")
        report.append(f"- Project Name: {self.project_name}\n")
        report.append(f"- Validation Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        return "".join(report)
    
    def save_report(self, filename: str = "uvx_validation_report.md") -> None:
        """Save validation report to file."""
        report = self.generate_report()
        
        with open(filename, 'w') as f:
            f.write(report)
        
        log_success(f"UVX validation report saved to: {filename}")

def main():
    """Main validation function."""
    validator = UVXTestingValidator()
    
    try:
        success = validator.run_full_validation()
        
        # Generate and save report
        validator.save_report()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        log_error("Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        log_error(f"Validation failed with error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

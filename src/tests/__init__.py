"""
FSL Continuum - Semantic Languages Testing Framework

Comprehensive testing framework for BAML and Pareto-Lang semantic languages
with XML transformation support and AI integration.

Provides:
- Unit testing for all semantic language components
- Integration testing for multi-language scenarios
- Performance testing and benchmarking
- AI processing validation testing
- XML transformation testing
- End-to-end testing frameworks
"""

# Core testing framework modules
from .test_framework import (
    SemanticLanguageBaseTest,
    TestDataManager,
    TestUtils,
    MockComponents,
    TestConfig
)

# Test automation modules
from .test_automation import (
    TestAutomationFramework,
    CICDIntegration,
    TestRunner,
    TestScheduler,
    TestReporter
)

# Test utilities
from .test_utils import (
    XMLTestValidator,
    JSONTestValidator,
    PerformanceTestMonitor,
    SemanticLanguageAssertions,
    TestReporting
)

# Test configurations
from .test_config import (
    TestConfiguration,
    TestEnvironmentConfig,
    TestDatabaseConfig,
    TestReportingConfig
)

# Version and compatibility
__version__ = "1.0.0-testing-framework"
__semantic_languages_version__ = "compatible-with-latest"
__xml_transformation_version__ = "compatible-with-latest"
__ai_integration_version__ = "compatible-with-latest"

# Test framework capabilities
TEST_FRAMEWORK_CAPABILITIES = {
    "unit_testing": True,
    "integration_testing": True,
    "performance_testing": True,
    "ai_testing": True,
    "xml_testing": True,
    "end_to_end_testing": True,
    "test_automation": True,
    "ci_cd_integration": True,
    "benchmarking": True,
    "reporting": True,
    "monitoring": True,
    "debugging": True,
    "profiling": True,
    "coverage_reporting": True
}

# Testing standards compliance
TESTING_STANDARDS = {
    "pytest_compliant": True,
    "unittest_compliant": True,
    "coverage_minimum": 90.0,
    "performance_benchmarks": True,
    "security_testing": True,
    "accessibility_testing": True,
    "compatibility_testing": True,
    "scalability_testing": True,
    "reliability_testing": True,
    "maintainability_testing": True
}

class SemanticLanguageTestFramework:
    """Main test framework manager for semantic languages."""
    
    def __init__(self):
        self.test_data_manager = TestDataManager()
        self.test_utils = TestUtils()
        self.mock_components = MockComponents()
        self.test_config = TestConfig()
        self.test_automation = TestAutomationFramework()
        
    def get_framework_capabilities(self):
        """Get test framework capabilities."""
        return {
            "capabilities": TEST_FRAMEWORK_CAPABILITIES,
            "standards": TESTING_STANDARDS,
            "version": __version__,
            "compatibility": {
                "semantic_languages": __semantic_languages_version__,
                "xml_transformation": __xml_transformation_version__,
                "ai_integration": __ai_integration_version__
            }
        }
    
    def run_full_test_suite(self, test_config=None):
        """Run full test suite for semantic languages."""
        return self.test_automation.run_automated_test_suite(test_config)
    
    def get_test_status(self):
        """Get current test framework status."""
        return {
            "framework_status": "active",
            "test_environment": self.test_config.get_test_environment(),
            "test_data_status": self.test_data_manager.get_status(),
            "automation_status": self.test_automation.get_status(),
            "capabilities": TEST_FRAMEWORK_CAPABILITIES
        }

# Export main classes and configuration
__all__ = [
    # Core framework classes
    'SemanticLanguageTestFramework',
    'SemanticLanguageBaseTest',
    'TestDataManager',
    'TestUtils',
    'MockComponents',
    'TestConfig',
    
    # Automation classes
    'TestAutomationFramework',
    'CICDIntegration',
    'TestRunner',
    'TestScheduler',
    'TestReporter',
    
    # Utility classes
    'XMLTestValidator',
    'JSONTestValidator',
    'PerformanceTestMonitor',
    'SemanticLanguageAssertions',
    'TestReporting',
    
    # Configuration classes
    'TestConfiguration',
    'TestEnvironmentConfig',
    'TestDatabaseConfig',
    'TestReportingConfig',
    
    # Constants
    'TEST_FRAMEWORK_CAPABILITIES',
    'TESTING_STANDARDS',
    '__version__',
    '__semantic_languages_version__',
    '__xml_transformation_version__',
    '__ai_integration_version__'
]

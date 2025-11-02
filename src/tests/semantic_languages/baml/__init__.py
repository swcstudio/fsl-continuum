"""
FSL Continuum - BAML Language Testing

Comprehensive testing for BAML (BoundaryML) semantic language
with XML transformation support and AI integration.
"""

from .test_baml_parser import TestBAMLParser
from .test_baml_validator import TestBAMLValidator
from .test_baml_schema import TestBAMLSchema
from .test_baml_generator import TestBAMLGenerator
from .test_baml_interpreter import TestBAMLInterpreter
from .test_baml_bridge import TestBAMLBridge
from .test_baml_xml_transformer import TestBAMLXMLTransformer
from .test_baml_integration import TestBAMLIntegration

# Test version and compatibility
__version__ = "1.0.0-baml-testing"
__baml_version__ = "compatible-with-latest"
__xml_transformation_version__ = "compatible-with-latest"
__ai_integration_version__ = "compatible-with-latest"

# BAML testing capabilities
BAML_TESTING_CAPABILITIES = {
    "parser_testing": True,
    "validator_testing": True,
    "schema_testing": True,
    "generator_testing": True,
    "interpreter_testing": True,
    "bridge_testing": True,
    "xml_transformer_testing": True,
    "integration_testing": True,
    "ai_integration_testing": True,
    "performance_testing": True,
    "error_handling_testing": True
}

class BAMLTestSuite:
    """Main test suite manager for BAML language testing."""
    
    def __init__(self):
        self.test_data_manager = None
        self.test_utils = None
        self.mock_components = None
        self.test_config = None
        
        # Test result tracking
        self.test_results = {}
        self.performance_metrics = {}
        self.error_scenarios = {}
    
    def run_baml_test_suite(self, test_config=None):
        """Run BAML test suite."""
        from ...test_framework import TestAutomationFramework
        test_automation = TestAutomationFramework()
        return test_automation.run_test_suite("baml", test_config)
    
    def get_baml_test_status(self):
        """Get status of BAML test suite."""
        return {
            "status": "active",
            "capabilities": BAML_TESTING_CAPABILITIES,
            "test_results": self.test_results,
            "performance_metrics": self.performance_metrics,
            "error_scenarios": self.error_scenarios
        }

# Export main classes
__all__ = [
    # Test classes
    'TestBAMLParser', 'TestBAMLValidator', 'TestBAMLSchema', 
    'TestBAMLGenerator', 'TestBAMLInterpreter', 'TestBAMLBridge', 
    'TestBAMLXMLTransformer', 'TestBAMLIntegration',
    
    # Test suite manager
    'BAMLTestSuite',
    
    # Configuration
    'BAML_TESTING_CAPABILITIES',
    '__version__', '__baml_version__', '__xml_transformation_version__', '__ai_integration_version__'
]

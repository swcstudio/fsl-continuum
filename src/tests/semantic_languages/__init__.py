"""
FSL Continuum - Semantic Languages Testing

Comprehensive testing for BAML and Pareto-Lang semantic languages
with XML transformation support and AI integration.
"""

# BAML language tests
from .baml import (
    TestBAMLParser,
    TestBAMLValidator,
    TestBAMLSchema,
    TestBAMLGenerator,
    TestBAMLInterpreter,
    TestBAMLBridge,
    TestBAMLXMLTransformer,
    TestBAMLIntegration
)

# Pareto-Lang language tests
from .pareto_lang import (
    TestParetoLangParser,
    TestParetoLangValidator,
    TestParetoLangSchema,
    TestParetoLangGenerator,
    TestParetoLangInterpreter,
    TestParetoLangBridge,
    TestParetoLangXMLTransformer,
    TestParetoLangIntegration
)

# XML processing tests
from .xml_processing import (
    TestUnifiedXMLProcessor,
    TestXMLTransformation,
    TestXMLValidation,
    TestXMLRoundTrip
)

# Semantic bridge tests
from .semantic_bridge import (
    TestBridgeIntegration,
    TestBridgeAIIntegration,
    TestBridgeXMLIntegration
)

# AI integration tests
from .ai_integration import (
    TestAIProcessor,
    TestAIOptimizer,
    TestAIXMLProcessor,
    TestAILearning
)

# Integration tests
from .integration import (
    TestEndToEnd,
    TestMultiLanguage,
    TestPerformance,
    TestErrorHandling
)

# Test framework version and compatibility
__version__ = "1.0.0-testing-framework"
__semantic_languages_version__ = "compatible-with-latest"
__xml_transformation_version__ = "compatible-with-latest"
__ai_integration_version__ = "compatible-with-latest"

# Test framework capabilities
SEMANTIC_LANGUAGE_TESTS_AVAILABLE = {
    "baml_testing": True,
    "pareto_lang_testing": True,
    "xml_processing_testing": True,
    "semantic_bridge_testing": True,
    "ai_integration_testing": True,
    "integration_testing": True,
    "performance_testing": True,
    "error_handling_testing": True
}

class SemanticLanguageTestSuite:
    """Main test suite manager for semantic language testing."""
    
    def __init__(self):
        self.test_data_manager = None
        self.test_utils = None
        self.mock_components = None
        self.test_config = None
        
        # Test result tracking
        self.test_results = {}
        self.performance_metrics = {}
        self.error_scenarios = {}
    
    def run_full_test_suite(self, test_config=None):
        """Run full semantic language test suite."""
        from ..test_framework import TestAutomationFramework
        test_automation = TestAutomationFramework()
        return test_automation.run_automated_test_suite(test_config)
    
    def get_test_suite_status(self):
        """Get status of semantic language test suite."""
        return {
            "status": "active",
            "available_tests": SEMANTIC_LANGUAGE_TESTS_AVAILABLE,
            "test_results": self.test_results,
            "performance_metrics": self.performance_metrics,
            "error_scenarios": self.error_scenarios
        }

# Export main classes and test modules
__all__ = [
    # BAML test classes
    'TestBAMLParser', 'TestBAMLValidator', 'TestBAMLSchema', 
    'TestBAMLGenerator', 'TestBAMLInterpreter', 'TestBAMLBridge', 
    'TestBAMLXMLTransformer', 'TestBAMLIntegration',
    
    # Pareto-Lang test classes
    'TestParetoLangParser', 'TestParetoLangValidator', 'TestParetoLangSchema', 
    'TestParetoLangGenerator', 'TestParetoLangInterpreter', 'TestParetoLangBridge', 
    'TestParetoLangXMLTransformer', 'TestParetoLangIntegration',
    
    # XML processing test classes
    'TestUnifiedXMLProcessor', 'TestXMLTransformation', 'TestXMLValidation', 'TestXMLRoundTrip',
    
    # Semantic bridge test classes
    'TestBridgeIntegration', 'TestBridgeAIIntegration', 'TestBridgeXMLIntegration',
    
    # AI integration test classes
    'TestAIProcessor', 'TestAIOptimizer', 'TestAIXMLProcessor', 'TestAILearning',
    
    # Integration test classes
    'TestEndToEnd', 'TestMultiLanguage', 'TestPerformance', 'TestErrorHandling',
    
    # Test suite manager
    'SemanticLanguageTestSuite',
    
    # Configuration
    'SEMANTIC_LANGUAGE_TESTS_AVAILABLE',
    '__version__', '__semantic_languages_version__', '__xml_transformation_version__', '__ai_integration_version__'
]

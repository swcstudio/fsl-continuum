"""
FSL Continuum - Terminal Velocity CI/CD System

A flow-state-optimized CI/CD platform with persistent state,
blockchain auditing, and 4-market integration (US, China, India, Japan).
"""

__version__ = "3.0.0"
__author__ = "FSL Continuum Team"
__description__ = "Terminal Velocity CI/CD with persistent state and AI-native features"
__license__ = "MIT"

# Core imports
from .continuum import FSLContinuum, TerminalVelocityMetrics, create_fsl_continuum
from .continuum.terminal_velocity import TerminalVelocity
from .continuum.state_management import StateManager
from .continuum.ai_orchestrator import AIOrchestrator

# Semantic language imports
from .semantic_languages import (
    BAMLParser, BAMLValidator, BAMLSchema, BAMLGenerator, BAMLInterpreter, BAMLBridge, BAMLXMLTransformer,
    ParetoLangParser, ParetoLangValidator, ParetoLangSchema, ParetoLangGenerator, ParetoLangInterpreter, ParetoLangBridge, ParetoLangXMLTransformer,
    SemanticLanguageBridge, SemanticDataConnections, SemanticLanguageSchemas, SemanticAIProcessor, SemanticAIOptimizer, UnifiedXMLProcessor
)

# AI integration imports
from .ai_integration import (
    AIProcessor, AIOptimizer, AILearningSystem, AIPredictionEngine, 
    AIModelManager, AIContextAwareness, AISemanticAnalyzer
)

# XML processing imports
from .xml_processing import (
    XMLProcessor, XMLValidator, XMLTransformer, XMLSchemaManager,
    XMLRoundTripProcessor, XMLSemanticPreservation
)

# Testing imports
from .testing import (
    SemanticLanguageBaseTest, TestDataManager, TestUtils, MockComponents,
    TestAutomationFramework, CICDIntegration
)

__all__ = [
    # Core
    'FSLContinuum',
    'TerminalVelocityMetrics',
    'create_fsl_continuum',
    'TerminalVelocity',
    'StateManager',
    'AIOrchestrator',
    
    # Semantic Languages
    'BAMLParser', 'BAMLValidator', 'BAMLSchema', 'BAMLGenerator', 'BAMLInterpreter', 'BAMLBridge', 'BAMLXMLTransformer',
    'ParetoLangParser', 'ParetoLangValidator', 'ParetoLangSchema', 'ParetoLangGenerator', 'ParetoLangInterpreter', 'ParetoLangBridge', 'ParetoLangXMLTransformer',
    'SemanticLanguageBridge', 'SemanticDataConnections', 'SemanticLanguageSchemas', 'SemanticAIProcessor', 'SemanticAIOptimizer', 'UnifiedXMLProcessor',
    
    # AI Integration
    'AIProcessor', 'AIOptimizer', 'AILearningSystem', 'AIPredictionEngine',
    'AIModelManager', 'AIContextAwareness', 'AISemanticAnalyzer',
    
    # XML Processing
    'XMLProcessor', 'XMLValidator', 'XMLTransformer', 'XMLSchemaManager',
    'XMLRoundTripProcessor', 'XMLSemanticPreservation',
    
    # Testing
    'SemanticLanguageBaseTest', 'TestDataManager', 'TestUtils', 'MockComponents',
    'TestAutomationFramework', 'CICDIntegration'
]

# Version and compatibility
FSL_CONTINUUM_VERSION = __version__
SEMANTIC_LANGUAGES_VERSION = "1.0.0-fsl-integration"
AI_INTEGRATION_VERSION = "1.0.0-ai-integration"
XML_PROCESSING_VERSION = "1.0.0-xml-integration"

# Compatibility information
PYTHON_MIN_VERSION = "3.9"
PYTHON_MAX_VERSION = "3.12"

# Feature flags
ENABLE_SEMANTIC_LANGUAGES = True
ENABLE_AI_INTEGRATION = True
ENABLE_XML_PROCESSING = True
ENABLE_TESTING_FRAMEWORK = True

# Integration status
SEMANTIC_LANGUAGES_INTEGRATED = True
AI_INTEGRATION_COMPLETE = True
XML_PROCESSING_COMPLETE = True
TESTING_FRAMEWORK_COMPLETE = True

def get_version():
    """Get FSL Continuum version."""
    return __version__

def get_info():
    """Get FSL Continuum package information."""
    return {
        'version': __version__,
        'author': __author__,
        'description': __description__,
        'license': __license__,
        'semantic_languages_version': SEMANTIC_LANGUAGES_VERSION,
        'ai_integration_version': AI_INTEGRATION_VERSION,
        'xml_processing_version': XML_PROCESSING_VERSION,
        'python_min_version': PYTHON_MIN_VERSION,
        'python_max_version': PYTHON_MAX_VERSION,
        'features': {
            'semantic_languages': ENABLE_SEMANTIC_LANGUAGES,
            'ai_integration': ENABLE_AI_INTEGRATION,
            'xml_processing': ENABLE_XML_PROCESSING,
            'testing_framework': ENABLE_TESTING_FRAMEWORK
        },
        'integration_status': {
            'semantic_languages_integrated': SEMANTIC_LANGUAGES_INTEGRATED,
            'ai_integration_complete': AI_INTEGRATION_COMPLETE,
            'xml_processing_complete': XML_PROCESSING_COMPLETE,
            'testing_framework_complete': TESTING_FRAMEWORK_COMPLETE
        }
    }

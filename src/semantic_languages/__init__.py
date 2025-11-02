"""
FSL Continuum - Semantic Languages Module

Unified semantic language integration for BAML and Pareto-Lang.
Provides semantic parsing, validation, generation, and AI integration
with proper data connections and schema definitions.

This module integrates:
- BAML (BoundaryML): https://github.com/caspiankeyes/pareto-lang
- Pareto-Lang: https://docs.boundaryml.com/home
- AI-enhanced semantic processing
- Semantic data connections and flow
"""

from .baml import BAMLParser, BAMLValidator, BAMLSchema, BAMLGenerator, BAMLInterpreter, BAMLBridge, BAMLXMLTransformer
from .pareto_lang import ParetoLangParser, ParetoLangValidator, ParetoLangSchema, ParetoLangGenerator, ParetoLangInterpreter, ParetoLangBridge, ParetoLangXMLTransformer
from .bridge import SemanticLanguageBridge
from .connections import SemanticDataConnections
from .schemas import SemanticLanguageSchemas
from .ai_integration import SemanticAIProcessor, SemanticAIOptimizer
from .xml_processor import UnifiedXMLProcessor

# Semantic languages version and compatibility
__version__ = "1.0.0-fsl-integration"
__baml_version__ = "compatible-with-boundaryml-latest"
__pareto_lang_version__ = "compatible-with-pareto-lang-latest"
__xml_transformation_version__ = "1.0.0-xml-integration"

# Semantic language configurations
BAML_CONFIG_PATH = "src/semantic_languages/baml_config/baml_schemas.json"
PARETO_LANG_CONFIG_PATH = "src/semantic_languages/pareto_config/pareto_schemas.json"
CONNECTIONS_CONFIG_PATH = "src/semantic_languages/config/connections.json"
SCHEMAS_CONFIG_PATH = "src/semantic_languages/config/schemas.json"
XML_CONFIG_PATH = "src/semantic_languages/config/xml_transformation.json"

# Semantic language status
SEMANTIC_LANGUAGES_AVAILABLE = {
    "baml": True,
    "pareto_lang": True,
    "xml_transformation": True,
    "ai_integration": True,
    "bridge_functionality": True,
    "data_connections": True,
    "schema_validation": True,
    "unified_xml_processing": True
}

class SemanticLanguageManager:
    """Unified manager for semantic language operations with XML transformation support."""
    
    def __init__(self):
        self.baml_parser = BAMLParser()
        self.pareto_lang_parser = ParetoLangParser()
        self.semantic_bridge = SemanticLanguageBridge()
        self.ai_processor = SemanticAIProcessor()
        self.data_connections = SemanticDataConnections()
        self.schemas = SemanticLanguageSchemas()
        self.unified_xml_processor = UnifiedXMLProcessor()
    
    def get_semantic_language_status(self):
        """Get status of all semantic language components."""
        return {
            "status": "active",
            "available_languages": SEMANTIC_LANGUAGES_AVAILABLE,
            "baml_parser": self.baml_parser.get_status(),
            "pareto_lang_parser": self.pareto_lang_parser.get_status(),
            "semantic_bridge": self.semantic_bridge.get_status(),
            "ai_processor": self.ai_processor.get_status(),
            "data_connections": self.data_connections.get_status(),
            "schemas": self.schemas.get_status(),
            "unified_xml_processor": self.unified_xml_processor.get_unified_processor_status()
        }
    
    def process_semantic_data(self, data, language_type, context=None):
        """Process semantic data with appropriate language and XML transformation support."""
        if language_type == "baml":
            return self.baml_parser.parse(data, context)
        elif language_type == "pareto_lang":
            return self.pareto_lang_parser.parse(data, context)
        else:
            raise ValueError(f"Unsupported semantic language: {language_type}")
    
    def integrate_semantic_languages_with_xml(self, baml_data, pareto_data, context=None):
        """Integrate BAML and Pareto-Lang semantic data with XML transformation support."""
        return self.semantic_bridge.integrate(baml_data, pareto_data, context)
    
    def process_with_xml_transformation(self, semantic_data_dict, context=None):
        """Process multiple semantic data types with unified XML transformation."""
        return self.unified_xml_processor.process_multiple_semantic_data_with_xml(
            semantic_data_dict, context
        )
    
    def create_unified_xml_wrapper(self, semantic_data_dict, context=None):
        """Create unified XML wrapper for multiple semantic languages."""
        return self.unified_xml_processor.create_unified_xml_wrapper(
            semantic_data_dict, context
        )
    
    def parse_unified_xml_wrapper(self, unified_xml_wrapper, context=None):
        """Parse unified XML wrapper back to semantic data."""
        return self.unified_xml_processor.parse_unified_xml_wrapper(
            unified_xml_wrapper, context
        )
    
    def optimize_with_ai(self, semantic_data, optimization_target, context=None):
        """Optimize semantic data using AI with XML transformation support."""
        return self.ai_processor.optimize(semantic_data, optimization_target, context)

# Export main classes and manager
__all__ = [
    # Core semantic language classes
    'BAMLParser', 'BAMLValidator', 'BAMLSchema', 'BAMLGenerator', 'BAMLInterpreter', 'BAMLBridge', 'BAMLXMLTransformer',
    'ParetoLangParser', 'ParetoLangValidator', 'ParetoLangSchema', 'ParetoLangGenerator', 'ParetoLangInterpreter', 'ParetoLangBridge', 'ParetoLangXMLTransformer',
    
    # Integration classes
    'SemanticLanguageBridge', 'SemanticDataConnections', 'SemanticLanguageSchemas',
    'SemanticAIProcessor', 'SemanticAIOptimizer', 'UnifiedXMLProcessor',
    
    # Manager
    'SemanticLanguageManager',
    
    # Configuration
    'BAML_CONFIG_PATH', 'PARETO_LANG_CONFIG_PATH', 'CONNECTIONS_CONFIG_PATH', 'SCHEMAS_CONFIG_PATH', 'XML_CONFIG_PATH',
    'SEMANTIC_LANGUAGES_AVAILABLE'
]

"""
FSL Continuum - Pareto-Lang Semantic Language Integration

Integration for Pareto-Lang semantic language with FSL Continuum.
Provides semantic parsing, validation, optimization, and AI integration with XML transformation support.

Pareto-Lang: https://docs.boundaryml.com/home
"""

from .parser import ParetoLangParser
from .validator import ParetoLangValidator
from .schema import ParetoLangSchema
from .generator import ParetoLangGenerator
from .interpreter import ParetoLangInterpreter
from .bridge import ParetoLangBridge
from .xml_transformer import ParetoLangXMLTransformer

# Pareto-Lang version and compatibility
__version__ = "1.0.0-fsl-integration"
__pareto_lang_version__ = "compatible-with-latest"
__xml_transformation_version__ = "1.0.0-xml-integration"

# Pareto-Lang configuration paths
PARETO_LANG_CONFIG_PATH = "src/semantic_languages/pareto_config/pareto_schemas.json"
PARETO_LANG_RULES_PATH = "src/semantic_languages/pareto_config/pareto_rules.json"
PARETO_LANG_CONNECTIONS_PATH = "src/semantic_languages/pareto_config/pareto_connections.json"
PARETO_LANG_XML_CONFIG_PATH = "src/semantic_languages/pareto_config/pareto_xml_transformation.json"

class ParetoLangManager:
    """Manager for Pareto-Lang semantic language operations with XML support."""
    
    def __init__(self):
        self.parser = ParetoLangParser()
        self.validator = ParetoLangValidator()
        self.schema = ParetoLangSchema()
        self.generator = ParetoLangGenerator()
        self.interpreter = ParetoLangInterpreter()
        self.bridge = ParetoLangBridge()
        self.xml_transformer = ParetoLangXMLTransformer()
    
    def parse_pareto_lang_data(self, data, context=None):
        """Parse Pareto-Lang semantic data with optional XML transformation."""
        return self.parser.parse(data, context)
    
    def validate_pareto_lang_data(self, data, schema, context=None):
        """Validate Pareto-Lang semantic data with XML support."""
        return self.validator.validate(data, schema, context)
    
    def generate_from_pareto_lang(self, pareto_data, target_language, context=None):
        """Generate code from Pareto-Lang semantic data with XML support."""
        return self.generator.generate(pareto_data, target_language, context)
    
    def interpret_pareto_lang_semantics(self, pareto_data, context=None):
        """Interpret Pareto-Lang semantic data with XML support."""
        return self.interpreter.interpret(pareto_data, context)
    
    def optimize_pareto_lang(self, pareto_data, constraints, context=None):
        """Optimize Pareto-Lang semantic data with XML support."""
        return self.bridge.optimize(pareto_data, constraints, context)
    
    def bridge_to_python(self, pareto_data, context=None):
        """Bridge Pareto-Lang data to Python with XML support."""
        return self.bridge.bridge(pareto_data, context)
    
    def transform_pareto_lang_to_xml(self, pareto_data, context=None):
        """Transform Pareto-Lang data to XML-wrapped format."""
        return self.xml_transformer.wrap_pareto_lang_with_xml(pareto_data, context)
    
    def transform_xml_to_pareto_lang(self, xml_wrapper, context=None):
        """Transform XML-wrapped data back to Pareto-Lang format."""
        return self.xml_transformer.unwrap_xml_to_pareto_lang(xml_wrapper, context)
    
    def process_pareto_lang_with_xml(self, pareto_data, context=None):
        """Process Pareto-Lang data with XML transformation support."""
        # Parse Pareto-Lang data with XML support
        parsed_data = self.parse_pareto_lang_data(pareto_data, context)
        
        # Apply XML transformation if enabled
        if context and context.get("xml_transformation_enabled", False):
            xml_result = self.transform_pareto_lang_to_xml(pareto_data, context)
            parsed_data["xml_wrapped"] = xml_result
        
        return parsed_data

# Export Pareto-Lang classes and manager
__all__ = [
    'ParetoLangParser', 'ParetoLangValidator', 'ParetoLangSchema', 
    'ParetoLangGenerator', 'ParetoLangInterpreter', 'ParetoLangBridge',
    'ParetoLangXMLTransformer', 'ParetoLangManager',
    'PARETO_LANG_CONFIG_PATH', 'PARETO_LANG_RULES_PATH', 'PARETO_LANG_CONNECTIONS_PATH', 'PARETO_LANG_XML_CONFIG_PATH',
    '__version__', '__pareto_lang_version__', '__xml_transformation_version__'
]

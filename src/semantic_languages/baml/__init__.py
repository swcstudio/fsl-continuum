"""
FSL Continuum - BAML (BoundaryML) Semantic Language Integration

Integration for BAML (BoundaryML) semantic language with FSL Continuum.
Provides semantic parsing, validation, generation, and AI integration with XML transformation support.

BAML (BoundaryML): https://github.com/caspiankeyes/pareto-lang
"""

from .parser import BAMLParser
from .validator import BAMLValidator
from .schema import BAMLSchema
from .generator import BAMLGenerator
from .interpreter import BAMLInterpreter
from .bridge import BAMLBridge
from .xml_transformer import BAMLXMLTransformer

# BAML version and compatibility
__version__ = "1.0.0-fsl-integration"
__boundaryml_version__ = "compatible-with-latest"
__xml_transformation_version__ = "1.0.0-xml-integration"

# BAML configuration paths
BAML_CONFIG_PATH = "src/semantic_languages/baml_config/baml_schemas.json"
BAML_RULES_PATH = "src/semantic_languages/baml_config/baml_rules.json"
BAML_CONNECTIONS_PATH = "src/semantic_languages/baml_config/baml_connections.json"
BAML_XML_CONFIG_PATH = "src/semantic_languages/baml_config/baml_xml_transformation.json"

class BAMLManager:
    """Manager for BAML semantic language operations with XML support."""
    
    def __init__(self):
        self.parser = BAMLParser()
        self.validator = BAMLValidator()
        self.schema = BAMLSchema()
        self.generator = BAMLGenerator()
        self.interpreter = BAMLInterpreter()
        self.bridge = BAMLBridge()
        self.xml_transformer = BAMLXMLTransformer()
    
    def parse_baml_data(self, data, context=None):
        """Parse BAML semantic data with optional XML transformation."""
        return self.parser.parse(data, context)
    
    def validate_baml_data(self, data, schema, context=None):
        """Validate BAML semantic data with XML support."""
        return self.validator.validate(data, schema, context)
    
    def generate_from_baml(self, baml_data, target_language, context=None):
        """Generate code from BAML semantic data with XML support."""
        return self.generator.generate(baml_data, target_language, context)
    
    def interpret_baml_semantics(self, baml_data, context=None):
        """Interpret BAML semantic data with XML support."""
        return self.interpreter.interpret(baml_data, context)
    
    def bridge_to_python(self, baml_data, context=None):
        """Bridge BAML data to Python with XML support."""
        return self.bridge.bridge(baml_data, context)
    
    def transform_baml_to_xml(self, baml_data, context=None):
        """Transform BAML data to XML-wrapped format."""
        return self.xml_transformer.wrap_baml_with_xml(baml_data, context)
    
    def transform_xml_to_baml(self, xml_wrapper, context=None):
        """Transform XML-wrapped data back to BAML format."""
        return self.xml_transformer.unwrap_xml_to_baml(xml_wrapper, context)
    
    def process_baml_with_xml(self, baml_data, context=None):
        """Process BAML data with XML transformation support."""
        # Parse BAML data with XML support
        parsed_data = self.parse_baml_data(baml_data, context)
        
        # Apply XML transformation if enabled
        if context and context.get("xml_transformation_enabled", False):
            xml_result = self.transform_baml_to_xml(baml_data, context)
            parsed_data["xml_wrapped"] = xml_result
        
        return parsed_data

# Export BAML classes and manager
__all__ = [
    'BAMLParser', 'BAMLValidator', 'BAMLSchema', 'BAMLGenerator', 
    'BAMLInterpreter', 'BAMLBridge', 'BAMLXMLTransformer', 'BAMLManager',
    'BAML_CONFIG_PATH', 'BAML_RULES_PATH', 'BAML_CONNECTIONS_PATH', 'BAML_XML_CONFIG_PATH',
    '__version__', '__boundaryml_version__', '__xml_transformation_version__'
]

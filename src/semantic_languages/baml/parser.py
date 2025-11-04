"""
FSL Continuum - BAML Parser

Core parser for BAML semantic language with XML transformation support.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ParseResult:
    """Result of parsing operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None
    warnings: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class BAMLParser:
    """Parser for BAML semantic language with XML transformation support."""
    
    def __init__(self):
        self.version = "1.0.0-fsl-integration"
        logger.info(f"BAMLParser initialized (version {self.version})")
    
    def get_status(self) -> Dict[str, Any]:
        """Get parser status."""
        return {
            "status": "active",
            "version": self.version,
            "language": "baml"
        }
    
    def parse(self, data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> ParseResult:
        """
        Parse BAML semantic data.
        
        Args:
            data: BAML semantic data to parse
            context: Optional context for parsing (e.g., xml_transformation_enabled)
            
        Returns:
            ParseResult with parsed data and metadata
        """
        try:
            if context is None:
                context = {}
            
            # Validate basic structure
            if not isinstance(data, dict):
                return ParseResult(
                    success=False,
                    errors=["Data must be a dictionary"]
                )
            
            # Parse BAML data
            parsed_data = {
                "version": data.get("version", "unknown"),
                "spec": data.get("spec", "unknown"),
                "description": data.get("description", ""),
                "boundaries": data.get("boundaries", []),
                "connections": data.get("connections", []),
                "constraints": data.get("constraints", []),
                "metadata": {
                    "parsed_at": datetime.now().isoformat(),
                    "parser_version": self.version
                }
            }
            
            # Apply XML transformation if enabled
            if context.get("xml_transformation_enabled", False):
                from .xml_transformer import BAMLXMLTransformer
                xml_transformer = BAMLXMLTransformer()
                xml_result = xml_transformer.wrap_baml_with_xml(data, context)
                parsed_data["xml_wrapped"] = xml_result
            
            return ParseResult(
                success=True,
                data=parsed_data,
                metadata={
                    "parse_time": datetime.now().isoformat(),
                    "context": context
                }
            )
            
        except Exception as e:
            logger.error(f"Error parsing BAML data: {e}")
            return ParseResult(
                success=False,
                errors=[str(e)]
            )

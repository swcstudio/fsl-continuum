"""
FSL Continuum - Pareto-Lang Parser

Core parser for Pareto-Lang semantic language with XML transformation support.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
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

class ParetoLangParser:
    """Parser for Pareto-Lang semantic language with XML transformation support."""
    
    def __init__(self):
        self.version = "1.0.0-fsl-integration"
        logger.info(f"ParetoLangParser initialized (version {self.version})")
    
    def parse(self, data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> ParseResult:
        """
        Parse Pareto-Lang semantic data.
        
        Args:
            data: Pareto-Lang semantic data to parse
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
            
            # Parse Pareto-Lang data
            parsed_data = {
                "version": data.get("version", "unknown"),
                "spec": data.get("spec", "unknown"),
                "description": data.get("description", ""),
                "optimizations": data.get("optimizations", []),
                "constraints": data.get("constraints", []),
                "metadata": {
                    "parsed_at": datetime.now().isoformat(),
                    "parser_version": self.version
                }
            }
            
            # Apply XML transformation if enabled
            if context.get("xml_transformation_enabled", False):
                from .xml_transformer import ParetoLangXMLTransformer
                xml_transformer = ParetoLangXMLTransformer()
                xml_result = xml_transformer.wrap_pareto_lang_with_xml(data, context)
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
            logger.error(f"Error parsing Pareto-Lang data: {e}")
            return ParseResult(
                success=False,
                errors=[str(e)]
            )

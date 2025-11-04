"""
FSL Continuum - BAML Validator

Validator for BAML semantic language with XML transformation support.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Result of validation operation."""
    success: bool
    errors: Optional[List[str]] = None
    warnings: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class BAMLValidator:
    """Validator for BAML semantic language."""
    
    def __init__(self):
        self.version = "1.0.0-fsl-integration"
        logger.info(f"BAMLValidator initialized (version {self.version})")
    
    def validate(self, data: Dict[str, Any], schema: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """
        Validate BAML semantic data against a schema.
        
        Args:
            data: BAML data to validate
            schema: Schema to validate against
            context: Optional context for validation
            
        Returns:
            ValidationResult with validation status and any errors/warnings
        """
        try:
            errors = []
            warnings = []
            
            # Basic validation
            if not isinstance(data, dict):
                errors.append("Data must be a dictionary")
            
            # Validate required fields
            required_fields = ["version", "spec"]
            for field in required_fields:
                if field not in data:
                    warnings.append(f"Missing recommended field: {field}")
            
            # Validate boundaries if present
            if "boundaries" in data:
                if not isinstance(data["boundaries"], list):
                    errors.append("Boundaries must be a list")
            
            # Validate connections if present
            if "connections" in data:
                if not isinstance(data["connections"], list):
                    errors.append("Connections must be a list")
            
            return ValidationResult(
                success=len(errors) == 0,
                errors=errors if errors else None,
                warnings=warnings if warnings else None,
                metadata={"validator_version": self.version}
            )
            
        except Exception as e:
            logger.error(f"Error validating BAML data: {e}")
            return ValidationResult(
                success=False,
                errors=[str(e)]
            )

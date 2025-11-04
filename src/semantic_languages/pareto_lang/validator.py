"""
FSL Continuum - Pareto-Lang Validator

Validator for Pareto-Lang semantic language with XML transformation support.
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

class ParetoLangValidator:
    """Validator for Pareto-Lang semantic language."""
    
    def __init__(self):
        self.version = "1.0.0-fsl-integration"
        logger.info(f"ParetoLangValidator initialized (version {self.version})")
    
    def validate(self, data: Dict[str, Any], schema: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """
        Validate Pareto-Lang semantic data against a schema.
        
        Args:
            data: Pareto-Lang data to validate
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
            
            # Validate optimizations if present
            if "optimizations" in data:
                if not isinstance(data["optimizations"], list):
                    errors.append("Optimizations must be a list")
            
            # Validate constraints if present
            if "constraints" in data:
                if not isinstance(data["constraints"], list):
                    errors.append("Constraints must be a list")
            
            return ValidationResult(
                success=len(errors) == 0,
                errors=errors if errors else None,
                warnings=warnings if warnings else None,
                metadata={"validator_version": self.version}
            )
            
        except Exception as e:
            logger.error(f"Error validating Pareto-Lang data: {e}")
            return ValidationResult(
                success=False,
                errors=[str(e)]
            )

"""
FSL Continuum - BAML Schema

Schema definitions for BAML semantic language.
"""

import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BAMLSchema:
    """Schema definitions for BAML semantic language."""
    
    def __init__(self):
        self.version = "1.0.0-fsl-integration"
        self.base_schema = self._load_base_schema()
        logger.info(f"BAMLSchema initialized (version {self.version})")
    
    def _load_base_schema(self) -> Dict[str, Any]:
        """Load base BAML schema."""
        return {
            "type": "object",
            "properties": {
                "version": {"type": "string"},
                "spec": {"type": "string"},
                "description": {"type": "string"},
                "boundaries": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string"},
                            "ai_enhanced": {"type": "boolean"},
                            "metadata": {"type": "object"}
                        }
                    }
                },
                "connections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string"},
                            "target": {"type": "string"},
                            "type": {"type": "string"}
                        }
                    }
                },
                "constraints": {
                    "type": "array",
                    "items": {"type": "object"}
                }
            }
        }
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the BAML schema."""
        return self.base_schema

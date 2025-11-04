"""
FSL Continuum - Test Utilities

Utilities for semantic language testing.
"""

import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestUtils:
    """Utilities for semantic language testing."""
    
    def __init__(self):
        self.version = "1.0.0-test"
        logger.info(f"TestUtils initialized (version {self.version})")
    
    def compare_data(self, data1: Dict[str, Any], data2: Dict[str, Any]) -> bool:
        """Compare two data dictionaries."""
        return data1 == data2
    
    def validate_structure(self, data: Dict[str, Any], expected_keys: list) -> bool:
        """Validate data structure has expected keys."""
        return all(key in data for key in expected_keys)
    
    def format_test_output(self, result: Any) -> str:
        """Format test output for display."""
        return str(result)

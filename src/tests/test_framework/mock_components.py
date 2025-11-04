"""
FSL Continuum - Mock Components

Mock components for testing semantic language integration.
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MockResult:
    """Mock result for testing."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    errors: Optional[list] = None
    metadata: Optional[Dict[str, Any]] = None

class MockComponents:
    """Mock components for semantic language testing."""
    
    def __init__(self):
        self.version = "1.0.0-test"
        logger.info(f"MockComponents initialized (version {self.version})")
    
    def mock_parser(self, data: Dict[str, Any]) -> MockResult:
        """Mock parser for testing."""
        return MockResult(
            success=True,
            data=data,
            metadata={"mock": True}
        )
    
    def mock_validator(self, data: Dict[str, Any]) -> MockResult:
        """Mock validator for testing."""
        return MockResult(
            success=True,
            data={"valid": True},
            metadata={"mock": True}
        )
    
    def mock_transformer(self, data: Dict[str, Any]) -> MockResult:
        """Mock transformer for testing."""
        return MockResult(
            success=True,
            data={"transformed": True},
            metadata={"mock": True}
        )
    
    def mock_bridge(self, data: Dict[str, Any]) -> MockResult:
        """Mock bridge for testing."""
        return MockResult(
            success=True,
            data={"bridged": True},
            metadata={"mock": True}
        )
    
    def mock_ai_processor(self, data: Dict[str, Any]) -> MockResult:
        """Mock AI processor for testing."""
        return MockResult(
            success=True,
            data={"ai_processed": True},
            metadata={"mock": True}
        )

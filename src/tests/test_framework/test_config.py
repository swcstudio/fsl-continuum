"""
FSL Continuum - Test Configuration

Configuration for semantic language testing.
"""

import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestConfig:
    """Configuration for semantic language testing."""
    
    def __init__(self):
        self.version = "1.0.0-test"
        self.config = self._load_default_config()
        logger.info(f"TestConfig initialized (version {self.version})")
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default test configuration."""
        return {
            "timeout": 30,
            "max_retries": 3,
            "verbose": True,
            "parallel_tests": False,
            "test_data_path": "src/tests/fixtures/test_data"
        }
    
    def get_config(self, key: str) -> Any:
        """Get configuration value."""
        return self.config.get(key)
    
    def set_config(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config[key] = value

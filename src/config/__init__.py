"""
FSL Continuum - Configuration Module

This module provides centralized configuration management for FSL Continuum.
Includes enhanced state management, schematics bridge, dynamic loading,
and AI-enhanced optimization with hot-reload capabilities.
"""

from .enhanced_continuum_state import EnhancedStateManager
from .schematics_continuum_bridge import SchematicsBridgeManager
from .config_manager import ConfigManager
from .dynamic_loader import DynamicConfigLoader

__version__ = "3.0.0"
__all__ = [
    "EnhancedStateManager", 
    "SchematicsBridgeManager", 
    "ConfigManager", 
    "DynamicConfigLoader"
]

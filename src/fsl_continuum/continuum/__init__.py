"""
FSL Continuum Core Module

Core functionality for Terminal Velocity CI/CD with persistent state.
"""

from .core import FSLContinuum
from .metrics import TerminalVelocityMetrics
from .terminal_velocity import TerminalVelocity
from .state_management import StateManager
from .ai_orchestrator import AIOrchestrator

def create_fsl_continuum(config):
    """Create FSL Continuum instance with configuration."""
    return FSLContinuum(config)

__all__ = [
    'FSLContinuum',
    'TerminalVelocityMetrics', 
    'create_fsl_continuum',
    'TerminalVelocity',
    'StateManager',
    'AIOrchestrator'
]

"""
FSL Continuum - Terminal Velocity CI/CD System

A flow-state-optimized CI/CD platform with persistent state,
blockchain auditing, and 4-market integration (US, China, India, Japan).
"""

__version__ = "3.0.0"
__author__ = "FSL Continuum Team"
__description__ = "Terminal Velocity CI/CD with persistent state"

from .fsl_core import FSLContinuum, TerminalVelocityMetrics, create_fsl_continuum
from .terminal_velocity import TerminalVelocity
from .state_management import StateManager
from .ai_orchestrator import AIOrchestrator

__all__ = [
    'FSLContinuum',
    'TerminalVelocityMetrics',
    'create_fsl_continuum',
    'TerminalVelocity', 
    'StateManager',
    'AIOrchestrator'
]

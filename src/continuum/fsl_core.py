"""
FSL Continuum Core Engine

Main orchestration engine for terminal velocity CI/CD with persistent state.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

from ..quantum_engine.consciousness_detector import ConsciousnessDetector
from ..quantum_engine.field_manipulator import QuantumFieldManipulator
from .state_management import StateManager
from .ai_orchestrator import AIOrchestrator


@dataclass
class TerminalVelocityMetrics:
    """Metrics for terminal velocity calculation."""
    developer_productivity: float
    context_switches: int
    flow_state_duration: float
    velocity_score: float
    efficiency_improvement: float


class FSLContinuum:
    """
    Main FSL Continuum engine for terminal velocity CI/CD.
    
    Orchestrates flow-state-optimized development with persistent state,
    AI-native features, and 4-market integration.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.state_manager = StateManager()
        self.ai_orchestrator = AIOrchestrator()
        self.consciousness_detector = ConsciousnessDetector()
        self.quantum_field = QuantumFieldManipulator()
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize metrics
        self.metrics = TerminalVelocityMetrics(
            developer_productivity=0.0,
            context_switches=0,
            flow_state_duration=0.0,
            velocity_score=0.0,
            efficiency_improvement=0.0
        )
        
        self.logger.info("FSL Continuum initialized with terminal velocity engine")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load FSL configuration from file or defaults."""
        default_config = {
            "markets": ["US", "China", "India", "Japan"],
            "features": {
                "auto_pr": True,
                "genetic_testing": True,
                "dao_governance": True,
                "progressive_deployment": True
            },
            "quantum": {
                "consciousness_threshold": 0.7,
                "field_coherence": 0.8,
                "attractor_formation": True
            },
            "terminal_velocity": {
                "max_context_switches": 2,
                "flow_state_target": 0.9,
                "productivity_multiplier": 5.0
            }
        }
        
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                # Merge with defaults
                return {**default_config, **user_config}
            except Exception as e:
                self.logger.warning(f"Could not load config {config_path}: {e}")
                return default_config
        
        return default_config
    
    async def initialize(self) -> bool:
        """Initialize FSL Continuum systems."""
        try:
            # Initialize state management
            await self.state_manager.initialize()
            
            # Initialize quantum field
            await self.quantum_field.initialize(
                coherence=self.config["quantum"]["field_coherence"]
            )
            
            # Initialize AI orchestrator with market integration
            await self.ai_orchestrator.initialize(
                markets=self.config["markets"],
                features=self.config["features"]
            )
            
            # Load persistent state if available
            await self._load_persistent_state()
            
            self.logger.info("FSL Continuum systems initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize FSL Continuum: {e}")
            return False
    
    async def trigger_fsl_pipeline(
        self, 
        trigger_type: str,
        parameters: Dict[str, Any],
        maintain_flow_state: bool = True
    ) -> Dict[str, Any]:
        """
        Trigger FSL pipeline with flow state preservation.
        
        Args:
            trigger_type: Type of pipeline to trigger
            parameters: Pipeline parameters
            maintain_flow_state: Whether to maintain developer flow state
            
        Returns:
            Pipeline execution results
        """
        start_time = datetime.now()
        
        try:
            # Record metrics before pipeline
            self.metrics.context_switches = 0 if maintain_flow_state else 1
            self.metrics.flow_state_duration = 0.0 if maintain_flow_state else 300.0
            
            # Execute pipeline in background
            result = await self._execute_pipeline_background(
                trigger_type, parameters, maintain_flow_state
            )
            
            # Calculate terminal velocity metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            self._update_velocity_metrics(execution_time, maintain_flow_state)
            
            # Save persistent state
            await self._save_persistent_state()
            
            self.logger.info(f"FSL pipeline {trigger_type} completed in {execution_time:.2f}s")
            
            return {
                "success": True,
                "result": result,
                "metrics": asdict(self.metrics),
                "execution_time": execution_time,
                "flow_state_preserved": maintain_flow_state
            }
            
        except Exception as e:
            self.logger.error(f"FSL pipeline {trigger_type} failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "metrics": asdict(self.metrics),
                "flow_state_preserved": False
            }
    
    async def _execute_pipeline_background(
        self,
        trigger_type: str,
        parameters: Dict[str, Any],
        maintain_flow_state: bool
    ) -> Dict[str, Any]:
        """Execute pipeline in background without disrupting flow state."""
        
        # Route to appropriate FSL feature
        if trigger_type == "genetic_tests":
            return await self.ai_orchestrator.run_genetic_tests(
                generations=parameters.get("generations", 20)
            )
        elif trigger_type == "auto_pr":
            return await self.ai_orchestrator.create_auto_pr(
                message=parameters.get("message", "")
            )
        elif trigger_type == "deploy":
            return await self.ai_orchestrator.progressive_deployment(
                version=parameters.get("version", "latest"),
                environment=parameters.get("environment", "staging")
            )
        elif trigger_type == "dao_vote":
            return await self.ai_orchestrator.create_dao_proposal(
                proposal=parameters.get("proposal", "")
            )
        else:
            # Default to general AI orchestration
            return await self.ai_orchestrator.execute_with_optimal_ai(
                task=trigger_type,
                parameters=parameters
            )
    
    def _update_velocity_metrics(
        self, 
        execution_time: float, 
        maintain_flow_state: bool
    ) -> None:
        """Update terminal velocity metrics based on execution."""
        # Calculate productivity improvement
        if maintain_flow_state:
            productivity_gain = 5.0 * (1.0 / (1.0 + execution_time))
        else:
            productivity_gain = 2.0 * (1.0 / (1.0 + execution_time))
        
        # Update metrics
        self.metrics.developer_productivity += productivity_gain
        self.metrics.velocity_score = (
            self.metrics.developer_productivity / 
            (1 + self.metrics.context_switches)
        )
        self.metrics.efficiency_improvement = (
            (self.metrics.velocity_score - 1.0) * 100.0
        )
    
    async def _load_persistent_state(self) -> None:
        """Load persistent continuum state from storage."""
        try:
            state = await self.state_manager.load_state()
            if state:
                self.metrics.developer_productivity = state.get("productivity", 0.0)
                self.logger.info("Persistent state loaded successfully")
        except Exception as e:
            self.logger.warning(f"Could not load persistent state: {e}")
    
    async def _save_persistent_state(self) -> None:
        """Save continuum state to persistent storage."""
        try:
            state = {
                "productivity": self.metrics.developer_productivity,
                "velocity_score": self.metrics.velocity_score,
                "timestamp": datetime.now().isoformat()
            }
            await self.state_manager.save_state(state)
            self.logger.debug("Persistent state saved")
        except Exception as e:
            self.logger.error(f"Could not save persistent state: {e}")
    
    async def get_consciousness_level(self) -> Dict[str, float]:
        """Get current consciousness level of the continuum."""
        return await self.consciousness_detector.analyze_consciousness()
    
    async def manipulate_quantum_field(
        self,
        operation: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform quantum field manipulation operations."""
        return await self.quantum_field.manipulate(operation, parameters)
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current terminal velocity metrics."""
        return asdict(self.metrics)
    
    async def shutdown(self) -> None:
        """Shutdown FSL Continuum gracefully."""
        await self.state_manager.shutdown()
        await self.quantum_field.shutdown()
        await self.ai_orchestrator.shutdown()
        self.logger.info("FSL Continuum shutdown complete")


# Factory function for easy initialization
def create_fsl_continuum(config_path: Optional[str] = None) -> FSLContinuum:
    """Factory function to create and initialize FSL Continuum."""
    continuum = FSLContinuum(config_path)
    return continuum

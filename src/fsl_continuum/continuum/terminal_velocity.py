"""
Terminal Velocity

Flow state optimization and terminal velocity calculations.

Velocity Model:
- Velocity increases with uptime (building momentum)
- Flow state provides a velocity multiplier
- Configurable acceleration and max velocity
- Intuitive: higher values = better performance
"""

import time
from typing import Dict, Any, Optional


class TerminalVelocity:
    """Terminal Velocity optimization class.
    
    The velocity calculation uses a growth model where:
    - Base velocity grows with uptime (momentum building)
    - Flow state applies a multiplier to velocity
    - Configurable acceleration factor and velocity cap
    - Higher values indicate better/faster performance
    """
    
    # Default configuration
    DEFAULT_ACCELERATION = 1.0  # Base acceleration factor
    DEFAULT_MAX_VELOCITY = 100.0  # Maximum velocity cap
    FLOW_STATE_MULTIPLIER = 1.5  # Velocity boost when in flow state
    BASE_VELOCITY = 1.0  # Starting velocity
    
    def __init__(self, acceleration: float = None, max_velocity: float = None):
        """Initialize Terminal Velocity with optional configuration.
        
        Args:
            acceleration: Acceleration factor (higher = faster velocity growth)
            max_velocity: Maximum velocity cap (prevents unbounded growth)
        """
        self.flow_state = False
        self.metrics = {}
        self.start_time = time.time()
        self.acceleration = acceleration if acceleration is not None else self.DEFAULT_ACCELERATION
        self.max_velocity = max_velocity if max_velocity is not None else self.DEFAULT_MAX_VELOCITY
        
    def enter_flow_state(self):
        """Enter flow state."""
        self.flow_state = True
        self.metrics['flow_state_start'] = time.time()
        
    def exit_flow_state(self):
        """Exit flow state."""
        if self.flow_state:
            self.flow_state = False
            if 'flow_state_start' in self.metrics:
                duration = time.time() - self.metrics['flow_state_start']
                self.metrics['last_flow_duration'] = duration
                
    def get_velocity(self) -> float:
        """Calculate terminal velocity.
        
        Uses a growth-based model where velocity increases with uptime.
        Formula: velocity = BASE + (uptime * acceleration) * flow_multiplier
        
        Returns:
            Current velocity (higher = better performance)
        """
        uptime = time.time() - self.start_time
        
        # Calculate base velocity with acceleration
        # Velocity grows linearly with uptime and acceleration factor
        velocity = self.BASE_VELOCITY + (uptime * self.acceleration)
        
        # Apply flow state multiplier if in flow state
        if self.flow_state:
            velocity *= self.FLOW_STATE_MULTIPLIER
        
        # Cap at maximum velocity
        velocity = min(velocity, self.max_velocity)
        
        return velocity
        
    def get_status(self) -> Dict[str, Any]:
        """Get current status."""
        return {
            'flow_state': self.flow_state,
            'velocity': self.get_velocity(),
            'metrics': self.metrics,
            'uptime': time.time() - self.start_time,
            'config': {
                'acceleration': self.acceleration,
                'max_velocity': self.max_velocity,
                'flow_multiplier': self.FLOW_STATE_MULTIPLIER
            }
        }
    
    def set_acceleration(self, acceleration: float) -> None:
        """Update acceleration factor for velocity growth.
        
        Args:
            acceleration: New acceleration factor (higher = faster growth)
        """
        if acceleration < 0:
            raise ValueError("Acceleration must be non-negative")
        self.acceleration = acceleration
        
    def set_max_velocity(self, max_velocity: float) -> None:
        """Update maximum velocity cap.
        
        Args:
            max_velocity: New maximum velocity cap
        """
        if max_velocity <= 0:
            raise ValueError("Max velocity must be positive")
        self.max_velocity = max_velocity
    
    def get_config(self) -> Dict[str, float]:
        """Get current velocity configuration.
        
        Returns:
            Dictionary with acceleration, max_velocity, and flow_multiplier
        """
        return {
            'acceleration': self.acceleration,
            'max_velocity': self.max_velocity,
            'flow_multiplier': self.FLOW_STATE_MULTIPLIER,
            'base_velocity': self.BASE_VELOCITY
        }

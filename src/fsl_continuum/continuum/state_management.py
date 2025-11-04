"""
State Management

Persistent state management for FSL Continuum.
"""

import json
import asyncio
from typing import Dict, Any, Optional
from pathlib import Path


class StateManager:
    """State manager for FSL Continuum."""
    
    def __init__(self, state_file: Optional[str] = None):
        self.state_file = Path(state_file or "fsl_state.json")
        self.state = {}
        self.lock = asyncio.Lock()
        
    async def load_state(self) -> Dict[str, Any]:
        """Load state from file."""
        async with self.lock:
            try:
                if self.state_file.exists():
                    with open(self.state_file, 'r') as f:
                        self.state = json.load(f)
                return self.state
            except Exception as e:
                print(f"Error loading state: {e}")
                return {}
                
    async def save_state(self):
        """Save state to file."""
        async with self.lock:
            try:
                with open(self.state_file, 'w') as f:
                    json.dump(self.state, f, indent=2)
            except Exception as e:
                print(f"Error saving state: {e}")
                
    async def get(self, key: str, default: Any = None) -> Any:
        """Get state value."""
        await self.load_state()
        return self.state.get(key, default)
        
    async def set(self, key: str, value: Any):
        """Set state value."""
        await self.load_state()
        self.state[key] = value
        await self.save_state()
        
    async def update(self, updates: Dict[str, Any]):
        """Update multiple state values."""
        await self.load_state()
        self.state.update(updates)
        await self.save_state()

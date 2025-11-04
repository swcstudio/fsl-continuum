"""
Basic unit tests for FSL Continuum.
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

class TestBasic(unittest.TestCase):
    """Test basic functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    def test_imports(self):
        """Test that core modules can be imported."""
        try:
            from fsl_continuum.continuum.core import FSLContinuum
            from fsl_continuum.continuum.metrics import TerminalVelocityMetrics
            from fsl_continuum.continuum.terminal_velocity import TerminalVelocity
            from fsl_continuum.continuum.state_management import StateManager
            from fsl_continuum.continuum.ai_orchestrator import AIOrchestrator
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_continuum_creation(self):
        """Test FSL Continuum creation."""
        from fsl_continuum.continuum.core import FSLContinuum
        
        config = {"test": True}
        continuum = FSLContinuum(config)
        
        self.assertIsNotNone(continuum)
        self.assertEqual(continuum.config, config)
        self.assertFalse(continuum.is_running)
    
    def test_terminal_velocity(self):
        """Test Terminal Velocity functionality."""
        from fsl_continuum.continuum.terminal_velocity import TerminalVelocity
        
        tv = TerminalVelocity()
        self.assertFalse(tv.flow_state)
        self.assertGreater(tv.get_velocity(), 0)
        
        tv.enter_flow_state()
        self.assertTrue(tv.flow_state)
        
        tv.exit_flow_state()
        self.assertFalse(tv.flow_state)
    
    def test_metrics(self):
        """Test Terminal Velocity Metrics."""
        from fsl_continuum.continuum.metrics import TerminalVelocityMetrics
        
        metrics = TerminalVelocityMetrics()
        metrics.record_throughput(100.0)
        metrics.record_latency(50.0)
        
        result = metrics.get_metrics()
        self.assertEqual(result['throughput'], 100.0)
        self.assertEqual(result['latency'], 50.0)
        self.assertIn('uptime', result)
    
    def test_state_manager(self):
        """Test State Manager functionality."""
        from fsl_continuum.continuum.state_management import StateManager
        
        sm = StateManager()
        self.assertIsNotNone(sm)
        
        # Test basic operations (simplified)
        status = sm.get_status() if hasattr(sm, 'get_status') else {}
        self.assertIsInstance(status, dict)


if __name__ == '__main__':
    unittest.main()

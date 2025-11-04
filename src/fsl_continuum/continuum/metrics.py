"""
Terminal Velocity Metrics

Metrics collection and analysis for FSL Continuum.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import time


class TerminalVelocityMetrics:
    """Metrics for Terminal Velocity performance."""
    
    def __init__(self):
        self.metrics = {}
        self.start_time = time.time()
        
    def record_execution_time(self, operation: str, duration: float):
        """Record operation execution time."""
        if 'execution_times' not in self.metrics:
            self.metrics['execution_times'] = {}
        self.metrics['execution_times'][operation] = duration
        
    def record_throughput(self, value: float):
        """Record throughput metric."""
        self.metrics['throughput'] = value
        
    def record_latency(self, value: float):
        """Record latency metric."""
        self.metrics['latency'] = value
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics."""
        self.metrics['uptime'] = time.time() - self.start_time
        self.metrics['last_updated'] = datetime.now().isoformat()
        return self.metrics

#!/usr/bin/env python3
"""
FSL Continuum - Health Monitor

SPEC:000 - Tools & Scripts Migration
Part of FSL Continuum v2.1 - Terminal Velocity CI/CD

Multi-Market Engineering Principles:
- US: Innovation & rapid iteration
- CN: Scale & performance optimization  
- IN: Quality assurance & cost-effectiveness
- JP: Craftsmanship (Monozukuri, Kaizen, Wa, Ringi, Anshin)

Japanese Principles:
- Monozukuri (ものづくり): Craftsmanship in manufacturing/code
- Kaizen (改善): Continuous improvement
- Wa (和): Harmony and teamwork
- Ringi (稟議): Consensus-based decision making
- Anshin (安心): Peace of mind through security

Category: Monitoring
"""

import json
import os
import sys
import time
import logging
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import statistics

try:
    import numpy as np
    from sklearn.ensemble import IsolationForest
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('health-monitor')


class HealthStatus(Enum):
    """Health status levels"""
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    CRITICAL = "CRITICAL"


class AnomalyType(Enum):
    """Types of anomalies detected"""
    LATENCY_SPIKE = "latency_spike"
    ERROR_RATE_HIGH = "error_rate_high"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    COST_ANOMALY = "cost_anomaly"
    PATTERN_DEVIATION = "pattern_deviation"


@dataclass
class HealthMetric:
    """Individual health metric"""
    name: str
    value: float
    threshold: float
    status: str
    timestamp: str
    anomaly_score: float = 0.0


@dataclass
class HealthReport:
    """Comprehensive health report"""
    overall_status: HealthStatus
    health_score: float
    metrics: List[HealthMetric]
    anomalies: List[Dict[str, Any]]
    recommendations: List[str]
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'overall_status': self.overall_status.value,
            'health_score': self.health_score,
            'metrics': [asdict(m) for m in self.metrics],
            'anomalies': self.anomalies,
            'recommendations': self.recommendations,
            'timestamp': self.timestamp
        }


class HealthMonitor:
    """
    Comprehensive health monitoring system
    
    Incorporates:
    - US: Netflix Chaos Engineering principles
    - China: Alibaba self-healing patterns
    - India: TCS SRE observability standards
    """
    
    def __init__(self, flow_state_dir: str = ".flow-state"):
        self.flow_state_dir = Path(flow_state_dir)
        self.metrics_dir = self.flow_state_dir / "health-metrics"
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        
        self.baseline_metrics = self._load_baseline_metrics()
        self.anomaly_detector = self._init_anomaly_detector()
        
        # Health thresholds (industry standards)
        self.thresholds = {
            'latency_p95_ms': 150.0,  # US standard
            'error_rate': 0.01,  # 1% (Netflix standard)
            'cost_per_execution': 0.50,  # Cost control
            'success_rate': 0.95,  # 95% success (SRE standard)
            'resource_utilization': 0.85,  # 85% max utilization
            'transaction_integrity': 0.99,  # 99% integrity (TCS standard)
        }
    
    def _init_anomaly_detector(self):
        """Initialize ML-based anomaly detector"""
        if ML_AVAILABLE:
            return IsolationForest(
                contamination=0.1,  # 10% expected anomalies
                random_state=42,
                n_estimators=100
            )
        return None
    
    def _load_baseline_metrics(self) -> Dict[str, Any]:
        """Load baseline metrics for comparison"""
        baseline_file = self.metrics_dir / "baseline.json"
        
        if baseline_file.exists():
            with open(baseline_file) as f:
                return json.load(f)
        
        # Default baseline (healthy system)
        return {
            'latency_p95_ms': 80.0,
            'error_rate': 0.005,
            'cost_per_execution': 0.15,
            'success_rate': 0.92,
            'resource_utilization': 0.65,
            'transaction_integrity': 0.995
        }
    
    def check_health(self) -> HealthReport:
        """
        Comprehensive health check
        Target: <100ms check time (US standard)
        """
        start_time = time.time()
        
        logger.info("🏥 Starting comprehensive health check...")
        
        # Collect all metrics
        metrics = []
        
        # Flow State specific health checks
        flow_metrics = self._check_flow_state_health()
        metrics.extend(flow_metrics)
        
        # Transaction integrity (China: Alibaba pattern)
        transaction_metric = self._check_transaction_integrity()
        metrics.append(transaction_metric)
        
        # Context lineage health (India: TCS data integrity)
        lineage_metric = self._check_context_lineage()
        metrics.append(lineage_metric)
        
        # Resource utilization (US: AWS best practices)
        resource_metric = self._check_resource_utilization()
        metrics.append(resource_metric)
        
        # Cost anomalies (China: ByteDance cost monitoring)
        cost_metric = self._check_cost_anomalies()
        metrics.append(cost_metric)
        
        # Performance metrics (US: Netflix observability)
        perf_metrics = self._check_performance_metrics()
        metrics.extend(perf_metrics)
        
        # Detect anomalies using ML
        anomalies = self._detect_anomalies(metrics)
        
        # Calculate overall health score
        health_score = self._calculate_health_score(metrics)
        
        # Determine overall status
        overall_status = self._determine_status(health_score, anomalies)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(metrics, anomalies)
        
        check_duration = (time.time() - start_time) * 1000
        
        report = HealthReport(
            overall_status=overall_status,
            health_score=health_score,
            metrics=metrics,
            anomalies=anomalies,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )
        
        # Save report
        self._save_health_report(report)
        
        logger.info(f"✅ Health check complete in {check_duration:.2f}ms")
        logger.info(f"   Status: {overall_status.value}")
        logger.info(f"   Health Score: {health_score:.2f}")
        logger.info(f"   Anomalies: {len(anomalies)}")
        
        return report
    
    def _check_flow_state_health(self) -> List[HealthMetric]:
        """Check Flow State Loop specific health"""
        metrics = []
        
        try:
            # Check recent executions
            completion_dir = self.flow_state_dir / "completion"
            if completion_dir.exists():
                recent_completions = sorted(
                    completion_dir.glob("*.json"),
                    key=os.path.getmtime
                )[-20:]  # Last 20
                
                if recent_completions:
                    success_count = 0
                    total_cost = 0.0
                    execution_times = []
                    
                    for file in recent_completions:
                        try:
                            with open(file) as f:
                                data = json.load(f)
                            
                            if data.get('status') == 'completed':
                                success_count += 1
                            
                            total_cost += data.get('cost', 0.0)
                            
                            if 'execution_time' in data:
                                execution_times.append(data['execution_time'])
                        except:
                            continue
                    
                    # Success rate metric
                    success_rate = success_count / len(recent_completions)
                    metrics.append(HealthMetric(
                        name='success_rate',
                        value=success_rate,
                        threshold=self.thresholds['success_rate'],
                        status='healthy' if success_rate >= self.thresholds['success_rate'] else 'degraded',
                        timestamp=datetime.now().isoformat(),
                        anomaly_score=abs(success_rate - self.baseline_metrics['success_rate'])
                    ))
                    
                    # Average cost metric
                    avg_cost = total_cost / len(recent_completions)
                    metrics.append(HealthMetric(
                        name='cost_per_execution',
                        value=avg_cost,
                        threshold=self.thresholds['cost_per_execution'],
                        status='healthy' if avg_cost <= self.thresholds['cost_per_execution'] else 'warning',
                        timestamp=datetime.now().isoformat(),
                        anomaly_score=abs(avg_cost - self.baseline_metrics['cost_per_execution'])
                    ))
                    
                    # Latency metric
                    if execution_times:
                        p95_latency = np.percentile(execution_times, 95) if ML_AVAILABLE else max(execution_times)
                        metrics.append(HealthMetric(
                            name='latency_p95_ms',
                            value=p95_latency,
                            threshold=self.thresholds['latency_p95_ms'],
                            status='healthy' if p95_latency <= self.thresholds['latency_p95_ms'] else 'degraded',
                            timestamp=datetime.now().isoformat(),
                            anomaly_score=abs(p95_latency - self.baseline_metrics['latency_p95_ms']) / 100
                        ))
        
        except Exception as e:
            logger.warning(f"Error checking flow state health: {e}")
        
        return metrics
    
    def _check_transaction_integrity(self) -> HealthMetric:
        """Check EXPChain transaction integrity"""
        try:
            # Check for orphaned transactions
            transaction_dir = self.flow_state_dir / "transactions"
            if transaction_dir.exists():
                transactions = list(transaction_dir.glob("*.json"))
                
                if transactions:
                    valid_count = 0
                    for file in transactions[-50:]:  # Check last 50
                        try:
                            with open(file) as f:
                                data = json.load(f)
                            
                            # Check for required fields
                            if all(k in data for k in ['transaction_id', 'flow_id', 'timestamp']):
                                valid_count += 1
                        except:
                            continue
                    
                    integrity = valid_count / min(len(transactions), 50)
                    
                    return HealthMetric(
                        name='transaction_integrity',
                        value=integrity,
                        threshold=self.thresholds['transaction_integrity'],
                        status='healthy' if integrity >= self.thresholds['transaction_integrity'] else 'critical',
                        timestamp=datetime.now().isoformat(),
                        anomaly_score=1.0 - integrity
                    )
        
        except Exception as e:
            logger.warning(f"Error checking transaction integrity: {e}")
        
        # Default healthy metric
        return HealthMetric(
            name='transaction_integrity',
            value=1.0,
            threshold=self.thresholds['transaction_integrity'],
            status='healthy',
            timestamp=datetime.now().isoformat(),
            anomaly_score=0.0
        )
    
    def _check_context_lineage(self) -> HealthMetric:
        """Check context lineage health (India: TCS data integrity)"""
        try:
            context_dir = self.flow_state_dir / "contexts"
            if context_dir.exists():
                contexts = list(context_dir.glob("*.json"))
                
                if contexts:
                    valid_lineage = 0
                    for file in contexts[-30:]:  # Check last 30
                        try:
                            with open(file) as f:
                                data = json.load(f)
                            
                            # Check lineage completeness
                            if 'parent_context' in data or 'context_lineage' in data:
                                valid_lineage += 1
                        except:
                            continue
                    
                    lineage_health = valid_lineage / min(len(contexts), 30)
                    
                    return HealthMetric(
                        name='context_lineage_health',
                        value=lineage_health,
                        threshold=0.95,
                        status='healthy' if lineage_health >= 0.95 else 'degraded',
                        timestamp=datetime.now().isoformat(),
                        anomaly_score=1.0 - lineage_health
                    )
        
        except Exception as e:
            logger.warning(f"Error checking context lineage: {e}")
        
        return HealthMetric(
            name='context_lineage_health',
            value=1.0,
            threshold=0.95,
            status='healthy',
            timestamp=datetime.now().isoformat(),
            anomaly_score=0.0
        )
    
    def _check_resource_utilization(self) -> HealthMetric:
        """Check resource utilization (US: AWS patterns)"""
        try:
            # Check disk usage
            result = subprocess.run(
                ['df', '-h', str(self.flow_state_dir)],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                if len(lines) > 1:
                    parts = lines[1].split()
                    if len(parts) >= 5:
                        usage_str = parts[4].rstrip('%')
                        usage = float(usage_str) / 100.0
                        
                        return HealthMetric(
                            name='resource_utilization',
                            value=usage,
                            threshold=self.thresholds['resource_utilization'],
                            status='healthy' if usage <= self.thresholds['resource_utilization'] else 'warning',
                            timestamp=datetime.now().isoformat(),
                            anomaly_score=max(0, usage - self.baseline_metrics['resource_utilization'])
                        )
        
        except Exception as e:
            logger.warning(f"Error checking resource utilization: {e}")
        
        return HealthMetric(
            name='resource_utilization',
            value=0.5,
            threshold=self.thresholds['resource_utilization'],
            status='healthy',
            timestamp=datetime.now().isoformat(),
            anomaly_score=0.0
        )
    
    def _check_cost_anomalies(self) -> HealthMetric:
        """Check for cost anomalies (China: ByteDance cost monitoring)"""
        try:
            cost_dir = self.flow_state_dir / "cost-tracking"
            if cost_dir.exists():
                cost_files = sorted(cost_dir.glob("*.json"), key=os.path.getmtime)[-10:]
                
                if len(cost_files) >= 3:
                    costs = []
                    for file in cost_files:
                        try:
                            with open(file) as f:
                                data = json.load(f)
                            costs.append(data.get('total_cost', 0.0))
                        except:
                            continue
                    
                    if costs:
                        avg_cost = statistics.mean(costs)
                        std_cost = statistics.stdev(costs) if len(costs) > 1 else 0.0
                        
                        # Detect anomaly if latest cost is >2 std deviations
                        latest_cost = costs[-1]
                        z_score = abs(latest_cost - avg_cost) / (std_cost + 0.001)
                        
                        is_anomaly = z_score > 2.0
                        
                        return HealthMetric(
                            name='cost_stability',
                            value=1.0 - min(z_score / 5.0, 1.0),  # Convert z-score to 0-1 scale
                            threshold=0.7,
                            status='healthy' if not is_anomaly else 'warning',
                            timestamp=datetime.now().isoformat(),
                            anomaly_score=z_score / 3.0
                        )
        
        except Exception as e:
            logger.warning(f"Error checking cost anomalies: {e}")
        
        return HealthMetric(
            name='cost_stability',
            value=0.95,
            threshold=0.7,
            status='healthy',
            timestamp=datetime.now().isoformat(),
            anomaly_score=0.05
        )
    
    def _check_performance_metrics(self) -> List[HealthMetric]:
        """Check performance metrics (US: Netflix observability)"""
        metrics = []
        
        try:
            # Check ML prediction service metrics
            ml_metrics_file = Path(".ml-models/metrics/latest.json")
            if ml_metrics_file.exists():
                with open(ml_metrics_file) as f:
                    ml_metrics = json.load(f)
                
                # Prediction latency
                if 'average_latency_ms' in ml_metrics:
                    latency = ml_metrics['average_latency_ms']
                    metrics.append(HealthMetric(
                        name='ml_prediction_latency',
                        value=latency,
                        threshold=100.0,
                        status='healthy' if latency <= 100.0 else 'degraded',
                        timestamp=datetime.now().isoformat(),
                        anomaly_score=max(0, (latency - 80) / 100)
                    ))
                
                # Cache hit rate
                if 'cache_hit_rate' in ml_metrics:
                    cache_rate = ml_metrics['cache_hit_rate']
                    metrics.append(HealthMetric(
                        name='cache_hit_rate',
                        value=cache_rate,
                        threshold=0.5,
                        status='healthy' if cache_rate >= 0.5 else 'degraded',
                        timestamp=datetime.now().isoformat(),
                        anomaly_score=max(0, 0.6 - cache_rate)
                    ))
        
        except Exception as e:
            logger.warning(f"Error checking performance metrics: {e}")
        
        return metrics
    
    def _detect_anomalies(self, metrics: List[HealthMetric]) -> List[Dict[str, Any]]:
        """Detect anomalies using ML (US: Netflix anomaly detection)"""
        anomalies = []
        
        # Rule-based anomaly detection
        for metric in metrics:
            if metric.anomaly_score > 0.3:  # Threshold for anomaly
                anomaly_type = self._classify_anomaly(metric)
                
                anomalies.append({
                    'type': anomaly_type.value if isinstance(anomaly_type, AnomalyType) else 'unknown',
                    'metric': metric.name,
                    'severity': self._get_anomaly_severity(metric.anomaly_score),
                    'current_value': metric.value,
                    'threshold': metric.threshold,
                    'anomaly_score': metric.anomaly_score,
                    'timestamp': metric.timestamp
                })
        
        # ML-based anomaly detection (if available)
        if self.anomaly_detector and ML_AVAILABLE and len(metrics) > 5:
            try:
                values = np.array([[m.value, m.anomaly_score] for m in metrics])
                predictions = self.anomaly_detector.fit_predict(values)
                
                for i, pred in enumerate(predictions):
                    if pred == -1:  # Anomaly detected
                        if metrics[i].name not in [a['metric'] for a in anomalies]:
                            anomalies.append({
                                'type': 'ml_detected_anomaly',
                                'metric': metrics[i].name,
                                'severity': 'medium',
                                'detection_method': 'isolation_forest',
                                'timestamp': metrics[i].timestamp
                            })
            except Exception as e:
                logger.warning(f"ML anomaly detection failed: {e}")
        
        return anomalies
    
    def _classify_anomaly(self, metric: HealthMetric) -> AnomalyType:
        """Classify type of anomaly"""
        if 'latency' in metric.name:
            return AnomalyType.LATENCY_SPIKE
        elif 'error' in metric.name:
            return AnomalyType.ERROR_RATE_HIGH
        elif 'resource' in metric.name or 'utilization' in metric.name:
            return AnomalyType.RESOURCE_EXHAUSTION
        elif 'cost' in metric.name:
            return AnomalyType.COST_ANOMALY
        else:
            return AnomalyType.PATTERN_DEVIATION
    
    def _get_anomaly_severity(self, score: float) -> str:
        """Get anomaly severity level"""
        if score >= 0.7:
            return 'critical'
        elif score >= 0.5:
            return 'high'
        elif score >= 0.3:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_health_score(self, metrics: List[HealthMetric]) -> float:
        """Calculate overall health score (0-1 scale)"""
        if not metrics:
            return 0.5
        
        # Weighted average of metrics
        total_score = 0.0
        total_weight = 0.0
        
        # Define weights for different metrics
        weights = {
            'success_rate': 0.25,
            'transaction_integrity': 0.20,
            'latency_p95_ms': 0.15,
            'cost_per_execution': 0.10,
            'resource_utilization': 0.10,
            'context_lineage_health': 0.10,
            'ml_prediction_latency': 0.05,
            'cache_hit_rate': 0.05
        }
        
        for metric in metrics:
            weight = weights.get(metric.name, 0.05)
            
            # Normalize metric value to 0-1 scale
            if metric.name in ['latency_p95_ms', 'ml_prediction_latency']:
                # Lower is better
                normalized = max(0, 1 - (metric.value / (metric.threshold * 2)))
            elif metric.name == 'resource_utilization':
                # Should be moderate (not too high or low)
                normalized = 1 - abs(metric.value - 0.6) / 0.4
            else:
                # Higher is better (normalize to threshold)
                normalized = min(1.0, metric.value / max(metric.threshold, 0.01))
            
            total_score += normalized * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.5
    
    def _determine_status(
        self,
        health_score: float,
        anomalies: List[Dict[str, Any]]
    ) -> HealthStatus:
        """Determine overall health status"""
        critical_anomalies = [a for a in anomalies if a.get('severity') == 'critical']
        high_anomalies = [a for a in anomalies if a.get('severity') == 'high']
        
        if critical_anomalies or health_score < 0.5:
            return HealthStatus.CRITICAL
        elif high_anomalies or health_score < 0.7:
            return HealthStatus.UNHEALTHY
        elif health_score < 0.85:
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.HEALTHY
    
    def _generate_recommendations(
        self,
        metrics: List[HealthMetric],
        anomalies: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Analyze metrics for recommendations
        for metric in metrics:
            if metric.status in ['degraded', 'warning', 'critical']:
                if metric.name == 'success_rate' and metric.value < self.thresholds['success_rate']:
                    recommendations.append(
                        f"🔴 Success rate at {metric.value:.1%} - Review recent failures and implement fixes"
                    )
                
                elif metric.name == 'latency_p95_ms' and metric.value > self.thresholds['latency_p95_ms']:
                    recommendations.append(
                        f"⚡ High latency detected ({metric.value:.1f}ms) - Consider optimizing slow operations"
                    )
                
                elif metric.name == 'cost_per_execution' and metric.value > self.thresholds['cost_per_execution']:
                    recommendations.append(
                        f"💰 Cost per execution at ${metric.value:.3f} - Implement cost optimization strategies"
                    )
                
                elif metric.name == 'resource_utilization' and metric.value > self.thresholds['resource_utilization']:
                    recommendations.append(
                        f"⚠️  Resource utilization at {metric.value:.1%} - Clean up old data or increase capacity"
                    )
                
                elif metric.name == 'transaction_integrity' and metric.value < self.thresholds['transaction_integrity']:
                    recommendations.append(
                        f"🔧 Transaction integrity at {metric.value:.1%} - Run integrity repair immediately"
                    )
        
        # Anomaly-specific recommendations
        for anomaly in anomalies:
            if anomaly['severity'] in ['critical', 'high']:
                recommendations.append(
                    f"🚨 {anomaly['type'].upper()} detected in {anomaly['metric']} - Investigate immediately"
                )
        
        # General recommendations
        if not recommendations:
            recommendations.append("✅ All systems operating within normal parameters")
            recommendations.append("📊 Continue monitoring for early detection of issues")
        
        return recommendations
    
    def _save_health_report(self, report: HealthReport):
        """Save health report for historical tracking"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.metrics_dir / f"health_report_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report.to_dict(), f, indent=2)
        
        # Keep only last 100 reports
        reports = sorted(self.metrics_dir.glob("health_report_*.json"))
        if len(reports) > 100:
            for old_report in reports[:-100]:
                old_report.unlink()
        
        logger.info(f"💾 Health report saved: {report_file}")
    
    def update_baseline(self):
        """Update baseline metrics from recent healthy periods"""
        logger.info("📊 Updating baseline metrics...")
        
        # Collect metrics from recent healthy reports
        recent_reports = sorted(
            self.metrics_dir.glob("health_report_*.json"),
            key=os.path.getmtime
        )[-50:]
        
        if not recent_reports:
            logger.warning("No reports available for baseline update")
            return
        
        # Extract metrics from healthy reports only
        healthy_metrics = {}
        for report_file in recent_reports:
            try:
                with open(report_file) as f:
                    report = json.load(f)
                
                if report['overall_status'] == 'HEALTHY':
                    for metric in report['metrics']:
                        name = metric['name']
                        value = metric['value']
                        
                        if name not in healthy_metrics:
                            healthy_metrics[name] = []
                        healthy_metrics[name].append(value)
            except:
                continue
        
        # Calculate new baseline (median of healthy values)
        new_baseline = {}
        for name, values in healthy_metrics.items():
            if values:
                new_baseline[name] = statistics.median(values)
        
        if new_baseline:
            self.baseline_metrics.update(new_baseline)
            
            # Save updated baseline
            baseline_file = self.metrics_dir / "baseline.json"
            with open(baseline_file, 'w') as f:
                json.dump(self.baseline_metrics, f, indent=2)
            
            logger.info(f"✅ Baseline updated with {len(new_baseline)} metrics")
        else:
            logger.warning("No healthy metrics found for baseline update")


def main():
    """CLI for health monitoring"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Flow State Health Monitor')
    parser.add_argument('--flow-state-dir', default='.flow-state', help='Flow state directory')
    parser.add_argument('--update-baseline', action='store_true', help='Update baseline metrics')
    parser.add_argument('--output', default=None, help='Output file for report')
    
    args = parser.parse_args()
    
    monitor = HealthMonitor(flow_state_dir=args.flow_state_dir)
    
    if args.update_baseline:
        monitor.update_baseline()
        return
    
    # Run health check
    report = monitor.check_health()
    
    # Output report
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report.to_dict(), f, indent=2)
        logger.info(f"Report saved to {args.output}")
    else:
        print(json.dumps(report.to_dict(), indent=2))
    
    # Print summary
    print("\n" + "="*60)
    print("🏥 HEALTH CHECK SUMMARY")
    print("="*60)
    print(f"Overall Status: {report.overall_status.value}")
    print(f"Health Score: {report.health_score:.2%}")
    print(f"Metrics Checked: {len(report.metrics)}")
    print(f"Anomalies Detected: {len(report.anomalies)}")
    print("\n📋 Recommendations:")
    for rec in report.recommendations[:5]:
        print(f"  • {rec}")
    print("="*60)
    
    # Exit with appropriate code
    if report.overall_status == HealthStatus.CRITICAL:
        sys.exit(2)
    elif report.overall_status == HealthStatus.UNHEALTHY:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

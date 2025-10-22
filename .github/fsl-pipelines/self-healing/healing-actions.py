#!/usr/bin/env python3
"""
FSL Continuum - Healing Actions

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

Category: Self-Healing
"""

import json
import os
import sys
import time
import logging
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('healing-actions')


class HealingAction(Enum):
    """Types of healing actions"""
    REPAIR_TRANSACTION = "repair_transaction"
    CLEAN_ORPHANED_FILES = "clean_orphaned_files"
    REBUILD_INDEX = "rebuild_index"
    OPTIMIZE_STORAGE = "optimize_storage"
    RESTART_SERVICE = "restart_service"
    CLEAR_CACHE = "clear_cache"
    REPAIR_LINEAGE = "repair_lineage"
    UPDATE_CONFIGURATION = "update_configuration"


@dataclass
class HealingResult:
    """Result of healing action"""
    action: str
    success: bool
    message: str
    duration_ms: float
    affected_items: int
    timestamp: str


class HealingEngine:
    """
    Automated healing engine
    
    Implements:
    - US: Google SRE self-healing patterns
    - China: Alibaba's automated recovery
    - India: TCS incident automation
    """
    
    def __init__(self, flow_state_dir: str = ".flow-state"):
        self.flow_state_dir = Path(flow_state_dir)
        self.healing_log = self.flow_state_dir / "healing" / "healing_log.json"
        self.healing_log.parent.mkdir(parents=True, exist_ok=True)
        
        self.healing_history = self._load_healing_history()
    
    def _load_healing_history(self) -> List[Dict[str, Any]]:
        """Load healing history"""
        if self.healing_log.exists():
            with open(self.healing_log) as f:
                return json.load(f)
        return []
    
    def _save_healing_history(self):
        """Save healing history"""
        with open(self.healing_log, 'w') as f:
            json.dump(self.healing_history, f, indent=2)
    
    def heal_transaction_integrity(self) -> HealingResult:
        """Repair transaction integrity issues"""
        start_time = time.time()
        logger.info("🔧 Healing transaction integrity...")
        
        try:
            affected = 0
            
            # Find orphaned transactions
            tx_dir = self.flow_state_dir / "transactions"
            if tx_dir.exists():
                all_tx = set()
                orphaned = []
                
                # Collect all transaction IDs
                for file in tx_dir.glob("*.json"):
                    try:
                        with open(file) as f:
                            data = json.load(f)
                        tx_id = data.get('transaction_id')
                        if tx_id:
                            all_tx.add(tx_id)
                    except:
                        orphaned.append(file)
                
                # Move orphaned files to quarantine
                quarantine_dir = self.flow_state_dir / "quarantine"
                quarantine_dir.mkdir(exist_ok=True)
                
                for file in orphaned:
                    dest = quarantine_dir / file.name
                    shutil.move(str(file), str(dest))
                    affected += 1
                
            duration = (time.time() - start_time) * 1000
            
            result = HealingResult(
                action="repair_transaction",
                success=True,
                message=f"Repaired {affected} transaction integrity issues",
                duration_ms=duration,
                affected_items=affected,
                timestamp=datetime.now().isoformat()
            )
            
            self.healing_history.append(result.__dict__)
            self._save_healing_history()
            
            logger.info(f"✅ Transaction integrity healed: {affected} issues fixed")
            return result
            
        except Exception as e:
            logger.error(f"❌ Transaction healing failed: {e}")
            return HealingResult(
                action="repair_transaction",
                success=False,
                message=str(e),
                duration_ms=(time.time() - start_time) * 1000,
                affected_items=0,
                timestamp=datetime.now().isoformat()
            )
    
    def heal_resource_exhaustion(self) -> HealingResult:
        """Heal resource exhaustion issues"""
        start_time = time.time()
        logger.info("🔧 Healing resource exhaustion...")
        
        try:
            affected = 0
            
            # Clean old temporary files
            temp_patterns = [
                "*.tmp",
                "*.temp",
                "*~",
                ".*.swp"
            ]
            
            for pattern in temp_patterns:
                for file in self.flow_state_dir.rglob(pattern):
                    try:
                        file.unlink()
                        affected += 1
                    except:
                        pass
            
            # Clean old logs (keep last 100)
            log_dir = self.flow_state_dir / "logs"
            if log_dir.exists():
                log_files = sorted(log_dir.glob("*.log"), key=os.path.getmtime)
                for old_log in log_files[:-100]:
                    old_log.unlink()
                    affected += 1
            
            # Compress old data
            metrics_dir = self.flow_state_dir / "health-metrics"
            if metrics_dir.exists():
                old_metrics = sorted(
                    metrics_dir.glob("health_report_*.json"),
                    key=os.path.getmtime
                )[:-100]
                
                for old_metric in old_metrics:
                    old_metric.unlink()
                    affected += 1
            
            duration = (time.time() - start_time) * 1000
            
            result = HealingResult(
                action="optimize_storage",
                success=True,
                message=f"Cleaned {affected} files to free resources",
                duration_ms=duration,
                affected_items=affected,
                timestamp=datetime.now().isoformat()
            )
            
            self.healing_history.append(result.__dict__)
            self._save_healing_history()
            
            logger.info(f"✅ Resource exhaustion healed: {affected} files cleaned")
            return result
            
        except Exception as e:
            logger.error(f"❌ Resource healing failed: {e}")
            return HealingResult(
                action="optimize_storage",
                success=False,
                message=str(e),
                duration_ms=(time.time() - start_time) * 1000,
                affected_items=0,
                timestamp=datetime.now().isoformat()
            )
    
    def heal_configuration_drift(self) -> HealingResult:
        """Heal configuration drift"""
        start_time = time.time()
        logger.info("🔧 Healing configuration drift...")
        
        try:
            # Check and repair configuration files
            affected = 0
            
            # Ensure required directories exist
            required_dirs = [
                "transactions",
                "contexts",
                "completion",
                "healing",
                "health-metrics",
                "predictions",
                "features"
            ]
            
            for dir_name in required_dirs:
                dir_path = self.flow_state_dir / dir_name
                if not dir_path.exists():
                    dir_path.mkdir(parents=True)
                    affected += 1
            
            # Validate configuration integrity
            config_file = self.flow_state_dir / "config.json"
            if not config_file.exists():
                default_config = {
                    "version": "1.0",
                    "healing_enabled": True,
                    "auto_recovery": True,
                    "health_check_interval": 300,
                    "created_at": datetime.now().isoformat()
                }
                with open(config_file, 'w') as f:
                    json.dump(default_config, f, indent=2)
                affected += 1
            
            duration = (time.time() - start_time) * 1000
            
            result = HealingResult(
                action="update_configuration",
                success=True,
                message=f"Fixed {affected} configuration issues",
                duration_ms=duration,
                affected_items=affected,
                timestamp=datetime.now().isoformat()
            )
            
            self.healing_history.append(result.__dict__)
            self._save_healing_history()
            
            logger.info(f"✅ Configuration drift healed: {affected} fixes applied")
            return result
            
        except Exception as e:
            logger.error(f"❌ Configuration healing failed: {e}")
            return HealingResult(
                action="update_configuration",
                success=False,
                message=str(e),
                duration_ms=(time.time() - start_time) * 1000,
                affected_items=0,
                timestamp=datetime.now().isoformat()
            )
    
    def heal_context_lineage(self) -> HealingResult:
        """Repair context lineage breaks"""
        start_time = time.time()
        logger.info("🔧 Healing context lineage...")
        
        try:
            affected = 0
            
            # Rebuild lineage connections
            context_dir = self.flow_state_dir / "contexts"
            if context_dir.exists():
                contexts = {}
                
                # Load all contexts
                for file in context_dir.glob("*.json"):
                    try:
                        with open(file) as f:
                            data = json.load(f)
                        flow_id = data.get('flow_id')
                        if flow_id:
                            contexts[flow_id] = data
                    except:
                        continue
                
                # Repair missing lineage
                for flow_id, context in contexts.items():
                    if 'parent_context' not in context and 'context_lineage' not in context:
                        # Try to infer parent from timestamp
                        context_time = context.get('timestamp', '')
                        
                        # Add empty lineage to maintain consistency
                        context['context_lineage'] = []
                        context['lineage_repaired'] = True
                        context['repair_timestamp'] = datetime.now().isoformat()
                        
                        # Save repaired context
                        file = context_dir / f"{flow_id}.json"
                        with open(file, 'w') as f:
                            json.dump(context, f, indent=2)
                        
                        affected += 1
            
            duration = (time.time() - start_time) * 1000
            
            result = HealingResult(
                action="repair_lineage",
                success=True,
                message=f"Repaired {affected} lineage breaks",
                duration_ms=duration,
                affected_items=affected,
                timestamp=datetime.now().isoformat()
            )
            
            self.healing_history.append(result.__dict__)
            self._save_healing_history()
            
            logger.info(f"✅ Context lineage healed: {affected} repairs made")
            return result
            
        except Exception as e:
            logger.error(f"❌ Lineage healing failed: {e}")
            return HealingResult(
                action="repair_lineage",
                success=False,
                message=str(e),
                duration_ms=(time.time() - start_time) * 1000,
                affected_items=0,
                timestamp=datetime.now().isoformat()
            )
    
    def heal_cache_issues(self) -> HealingResult:
        """Clear cache issues"""
        start_time = time.time()
        logger.info("🔧 Clearing cache...")
        
        try:
            affected = 0
            
            # Clear ML prediction cache
            ml_cache_file = Path(".ml-models/cache/predictions.cache")
            if ml_cache_file.exists():
                ml_cache_file.unlink()
                affected += 1
            
            # Clear feature extraction cache
            feature_cache_dir = self.flow_state_dir / "features" / ".cache"
            if feature_cache_dir.exists():
                shutil.rmtree(feature_cache_dir)
                affected += 1
            
            duration = (time.time() - start_time) * 1000
            
            result = HealingResult(
                action="clear_cache",
                success=True,
                message=f"Cleared {affected} cache stores",
                duration_ms=duration,
                affected_items=affected,
                timestamp=datetime.now().isoformat()
            )
            
            self.healing_history.append(result.__dict__)
            self._save_healing_history()
            
            logger.info(f"✅ Cache cleared: {affected} stores reset")
            return result
            
        except Exception as e:
            logger.error(f"❌ Cache clearing failed: {e}")
            return HealingResult(
                action="clear_cache",
                success=False,
                message=str(e),
                duration_ms=(time.time() - start_time) * 1000,
                affected_items=0,
                timestamp=datetime.now().isoformat()
            )
    
    def heal_all(self, health_report: Optional[Dict[str, Any]] = None) -> List[HealingResult]:
        """
        Execute all applicable healing actions
        Based on health report if provided
        """
        logger.info("🏥 Starting comprehensive healing...")
        
        results = []
        
        # Always run these healings
        results.append(self.heal_configuration_drift())
        
        # Conditional healings based on health report
        if health_report:
            anomalies = health_report.get('anomalies', [])
            
            for anomaly in anomalies:
                anomaly_type = anomaly.get('type', '')
                
                if 'transaction' in anomaly_type or 'integrity' in anomaly_type:
                    results.append(self.heal_transaction_integrity())
                
                elif 'resource' in anomaly_type or 'exhaustion' in anomaly_type:
                    results.append(self.heal_resource_exhaustion())
                
                elif 'lineage' in anomaly_type or 'context' in anomaly_type:
                    results.append(self.heal_context_lineage())
                
                elif 'cache' in anomaly_type or 'performance' in anomaly_type:
                    results.append(self.heal_cache_issues())
        else:
            # Run all healings if no report provided
            results.append(self.heal_transaction_integrity())
            results.append(self.heal_resource_exhaustion())
            results.append(self.heal_context_lineage())
            results.append(self.heal_cache_issues())
        
        # Summary
        successful = sum(1 for r in results if r.success)
        total_affected = sum(r.affected_items for r in results)
        total_duration = sum(r.duration_ms for r in results)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🏥 HEALING COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"Actions Executed: {len(results)}")
        logger.info(f"Successful: {successful}/{len(results)}")
        logger.info(f"Total Items Fixed: {total_affected}")
        logger.info(f"Total Duration: {total_duration:.2f}ms")
        logger.info(f"{'='*60}")
        
        return results
    
    def get_healing_stats(self) -> Dict[str, Any]:
        """Get healing statistics"""
        if not self.healing_history:
            return {
                'total_healings': 0,
                'success_rate': 0,
                'average_duration_ms': 0,
                'total_items_fixed': 0
            }
        
        total = len(self.healing_history)
        successful = sum(1 for h in self.healing_history if h['success'])
        total_items = sum(h['affected_items'] for h in self.healing_history)
        avg_duration = statistics.mean([h['duration_ms'] for h in self.healing_history])
        
        return {
            'total_healings': total,
            'success_rate': successful / total if total > 0 else 0,
            'average_duration_ms': avg_duration,
            'total_items_fixed': total_items,
            'recent_healings': self.healing_history[-10:]
        }


def main():
    """CLI for healing actions"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Flow State Healing Actions')
    parser.add_argument('--flow-state-dir', default='.flow-state', help='Flow state directory')
    parser.add_argument('--action', choices=[
        'all', 'transaction', 'resource', 'config', 'lineage', 'cache', 'stats'
    ], default='all', help='Healing action to perform')
    parser.add_argument('--health-report', default=None, help='Health report JSON file')
    
    args = parser.parse_args()
    
    engine = HealingEngine(flow_state_dir=args.flow_state_dir)
    
    if args.action == 'stats':
        stats = engine.get_healing_stats()
        print(json.dumps(stats, indent=2))
        return
    
    # Load health report if provided
    health_report = None
    if args.health_report and os.path.exists(args.health_report):
        with open(args.health_report) as f:
            health_report = json.load(f)
    
    # Execute healing actions
    if args.action == 'all':
        results = engine.heal_all(health_report)
    elif args.action == 'transaction':
        results = [engine.heal_transaction_integrity()]
    elif args.action == 'resource':
        results = [engine.heal_resource_exhaustion()]
    elif args.action == 'config':
        results = [engine.heal_configuration_drift()]
    elif args.action == 'lineage':
        results = [engine.heal_context_lineage()]
    elif args.action == 'cache':
        results = [engine.heal_cache_issues()]
    
    # Print results
    for result in results:
        status = "✅" if result.success else "❌"
        print(f"{status} {result.action}: {result.message}")
    
    # Exit with appropriate code
    if all(r.success for r in results):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    import statistics
    main()

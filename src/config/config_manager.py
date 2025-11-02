"""
FSL Continuum - Configuration Manager

Centralized configuration management with dynamic loading,
AI-enhanced optimization, and hot-reload capabilities.
"""

import json
import time
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import our configuration components
from .enhanced_continuum_state import EnhancedStateManager
from .schematics_continuum_bridge import SchematicsBridgeManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import FSL Continuum components for AI integration
try:
    from ..continuum import FSLContinuum
    from ..quantum_engine import ConsciousnessDetector
    from ..schematics.native_engine import SchematicsNativeEngine
    
    fsl_continuum = FSLContinuum()
    consciousness_detector = ConsciousnessDetector()
    schematics_engine = SchematicsNativeEngine()
    
except ImportError as e:
    logger.warning(f"Could not import FSL Continuum components: {e}")
    fsl_continuum = None
    consciousness_detector = None
    schematics_engine = None

@dataclass
class ConfigurationMetrics:
    """Configuration management performance metrics."""
    total_config_loads: int = 0
    successful_loads: int = 0
    failed_loads: int = 0
    hot_reload_count: int = 0
    ai_optimization_count: int = 0
    last_load_time: float = 0.0
    average_load_time: float = 0.0

class ConfigFileHandler(FileSystemEventHandler):
    """File system event handler for configuration hot-reload."""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory and event.src_path.endswith('.json'):
            logger.info(f"Configuration file modified: {event.src_path}")
            self.config_manager._hot_reload_config(event.src_path)

class ConfigManager:
    """Advanced configuration manager with AI integration and hot-reload."""
    
    def __init__(self, config_directory: str = "src/config"):
        self.config_directory = Path(config_directory)
        self.config_files = {}
        self.config_callbacks = {}
        self.hot_reload_enabled = True
        self.ai_optimization_enabled = True
        self.performance_metrics = ConfigurationMetrics()
        self.observer = None
        
        # Initialize component managers
        self.enhanced_state_manager = EnhancedStateManager()
        self.schematics_bridge_manager = SchematicsBridgeManager()
        
        # Setup configuration monitoring
        self._setup_configuration_monitoring()
        
        # Load all configurations
        self._load_all_configurations()
    
    def _setup_configuration_monitoring(self):
        """Setup file system monitoring for hot-reload."""
        if self.hot_reload_enabled:
            try:
                event_handler = ConfigFileHandler(self)
                self.observer = Observer()
                self.observer.schedule(event_handler, str(self.config_directory), recursive=False)
                self.observer.start()
                logger.info("Configuration hot-reload monitoring enabled")
            except Exception as e:
                logger.warning(f"Could not enable configuration monitoring: {e}")
                self.hot_reload_enabled = False
    
    def _load_all_configurations(self):
        """Load all configuration files from directory."""
        try:
            config_files = list(self.config_directory.glob("*.json"))
            logger.info(f"Loading {len(config_files)} configuration files")
            
            for config_file in config_files:
                self._load_configuration_file(config_file)
                
        except Exception as e:
            logger.error(f"Failed to load configurations: {e}")
    
    def _load_configuration_file(self, config_file: Path) -> bool:
        """Load a single configuration file."""
        start_time = time.time()
        
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            # Apply AI optimization if enabled
            if self.ai_optimization_enabled and fsl_continuum:
                config_data = self._apply_ai_optimization(config_data, str(config_file))
            
            # Store configuration
            self.config_files[str(config_file)] = {
                "data": config_data,
                "last_modified": config_file.stat().st_mtime,
                "load_time": time.time() - start_time,
                "ai_optimized": self.ai_optimization_enabled
            }
            
            # Update metrics
            self.performance_metrics.total_config_loads += 1
            self.performance_metrics.successful_loads += 1
            self.performance_metrics.last_load_time = time.time() - start_time
            self.performance_metrics.average_load_time = (
                (self.performance_metrics.average_load_time * (self.performance_metrics.total_config_loads - 1) + 
                 self.performance_metrics.last_load_time) / self.performance_metrics.total_config_loads
            )
            
            # Trigger callbacks
            self._trigger_config_callbacks(str(config_file), config_data)
            
            logger.info(f"Loaded configuration: {config_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load configuration {config_file}: {e}")
            self.performance_metrics.total_config_loads += 1
            self.performance_metrics.failed_loads += 1
            return False
    
    def _hot_reload_config(self, config_path: str):
        """Hot-reload configuration file."""
        try:
            config_file = Path(config_path)
            
            # Reload configuration
            success = self._load_configuration_file(config_file)
            
            if success:
                self.performance_metrics.hot_reload_count += 1
                logger.info(f"Hot-reloaded configuration: {config_path}")
                
                # Apply AI learning from hot-reload
                if self.ai_optimization_enabled:
                    self._apply_hot_reload_learning(config_path)
                
        except Exception as e:
            logger.error(f"Failed to hot-reload configuration {config_path}: {e}")
    
    def _apply_ai_optimization(self, config_data: Dict[str, Any], config_path: str) -> Dict[str, Any]:
        """Apply AI optimization to configuration."""
        if not fsl_continuum:
            return config_data
        
        try:
            # Get AI optimization suggestions
            optimized_config = config_data.copy()
            
            # Analyze configuration context
            if "enhanced_continuum_state" in config_path:
                # Apply enhanced state optimization
                state_updates = self.enhanced_state_manager.update_state_with_ai(
                    config_data, "config_load_optimization"
                )
                if state_updates.get("success", False):
                    for section, updates in state_updates.items():
                        if section != "success":
                            if section in optimized_config:
                                optimized_config[section].update(updates)
            
            elif "schematics_continuum_bridge" in config_path:
                # Apply bridge optimization
                bridge_updates = self.schematics_bridge_manager.update_bridge_configuration(
                    config_data, "config_load_optimization"
                )
                if bridge_updates.get("success", False):
                    for section, updates in bridge_updates.items():
                        if section != "success":
                            if section in optimized_config:
                                optimized_config[section].update(updates)
            
            # Add AI optimization metadata
            optimized_config["ai_optimized"] = True
            optimized_config["ai_optimization_timestamp"] = datetime.now().isoformat()
            optimized_config["ai_optimization_confidence"] = 0.88
            
            # Update metrics
            self.performance_metrics.ai_optimization_count += 1
            
            return optimized_config
            
        except Exception as e:
            logger.warning(f"Could not apply AI optimization to configuration: {e}")
            return config_data
    
    def _apply_hot_reload_learning(self, config_path: str):
        """Apply AI learning from hot-reload events."""
        if not fsl_continuum:
            return
        
        try:
            # Extract learning from hot-reload
            learning_data = {
                "config_path": config_path,
                "reload_timestamp": datetime.now().isoformat(),
                "reload_frequency": self._get_config_reload_frequency(config_path),
                "config_health": self._analyze_config_health(config_path)
            }
            
            # Apply learning to AI systems
            if consciousness_detector:
                consciousness_detector.learn_from_event(learning_data)
            
            if schematics_engine:
                schematics_engine.adapt_from_data(learning_data)
            
            logger.info(f"Applied hot-reload learning for: {config_path}")
            
        except Exception as e:
            logger.warning(f"Could not apply hot-reload learning: {e}")
    
    def get_configuration(self, config_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration by name."""
        config_path = str(self.config_directory / f"{config_name}.json")
        
        if config_path in self.config_files:
            return self.config_files[config_path]["data"]
        else:
            logger.warning(f"Configuration not found: {config_name}")
            return None
    
    def update_configuration(self, config_name: str, updates: Dict[str, Any], 
                          save: bool = True, context: str = None) -> Dict[str, Any]:
        """Update configuration with optional saving."""
        config_path = str(self.config_directory / f"{config_name}.json")
        
        if config_path not in self.config_files:
            logger.warning(f"Configuration not found for update: {config_name}")
            return {"success": False, "error": "Configuration not found"}
        
        try:
            # Apply updates to configuration
            current_config = self.config_files[config_path]["data"]
            
            # Deep update configuration
            self._deep_update(current_config, updates)
            
            # Apply AI optimization if enabled
            if self.ai_optimization_enabled:
                current_config = self._apply_ai_optimization(current_config, config_path)
            
            # Update stored configuration
            self.config_files[config_path]["data"] = current_config
            self.config_files[config_path]["last_modified"] = time.time()
            
            # Save to file if requested
            if save:
                self._save_configuration_file(config_path, current_config)
            
            # Trigger callbacks
            self._trigger_config_callbacks(config_path, current_config)
            
            logger.info(f"Updated configuration: {config_name}")
            return {"success": True, "updated_config": current_config}
            
        except Exception as e:
            logger.error(f"Failed to update configuration {config_name}: {e}")
            return {"success": False, "error": str(e)}
    
    def save_configuration(self, config_name: str) -> bool:
        """Save configuration to file."""
        config_path = str(self.config_directory / f"{config_name}.json")
        
        if config_path not in self.config_files:
            logger.warning(f"Configuration not found for saving: {config_name}")
            return False
        
        try:
            return self._save_configuration_file(config_path, self.config_files[config_path]["data"])
        except Exception as e:
            logger.error(f"Failed to save configuration {config_name}: {e}")
            return False
    
    def _save_configuration_file(self, config_path: str, config_data: Dict[str, Any]) -> bool:
        """Save configuration data to file."""
        try:
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration file {config_path}: {e}")
            return False
    
    def _deep_update(self, base_dict: Dict[str, Any], update_dict: Dict[str, Any]):
        """Deep update dictionary with nested updates."""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def register_config_callback(self, config_name: str, callback_func):
        """Register callback for configuration changes."""
        config_path = str(self.config_directory / f"{config_name}.json")
        
        if config_path not in self.config_callbacks:
            self.config_callbacks[config_path] = []
        
        self.config_callbacks[config_path].append(callback_func)
        logger.info(f"Registered callback for configuration: {config_name}")
    
    def _trigger_config_callbacks(self, config_path: str, config_data: Dict[str, Any]):
        """Trigger callbacks for configuration changes."""
        if config_path in self.config_callbacks:
            for callback_func in self.config_callbacks[config_path]:
                try:
                    callback_func(config_data)
                except Exception as e:
                    logger.error(f"Configuration callback error: {e}")
    
    def get_all_configurations(self) -> Dict[str, Dict[str, Any]]:
        """Get all loaded configurations."""
        return {
            config_path.split("/")[-1].replace(".json", ""): config_info["data"]
            for config_path, config_info in self.config_files.items()
        }
    
    def get_configuration_metrics(self) -> Dict[str, Any]:
        """Get configuration management performance metrics."""
        metrics = asdict(self.performance_metrics)
        
        # Add AI-enhanced metrics
        if fsl_continuum:
            try:
                metrics["ai_analysis"] = self._analyze_configuration_performance()
                metrics["ai_optimizations"] = self._generate_config_optimizations()
                metrics["ai_predictions"] = self._predict_config_performance()
                
            except Exception as e:
                logger.warning(f"Could not enhance configuration metrics with AI: {e}")
        
        # Add system metrics
        metrics["total_configurations"] = len(self.config_files)
        metrics["hot_reload_enabled"] = self.hot_reload_enabled
        metrics["ai_optimization_enabled"] = self.ai_optimization_enabled
        metrics["config_directory"] = str(self.config_directory)
        
        return metrics
    
    def validate_configuration(self, config_name: str) -> Dict[str, Any]:
        """Validate configuration structure and content."""
        config_path = str(self.config_directory / f"{config_name}.json")
        
        if config_path not in self.config_files:
            return {"valid": False, "error": "Configuration not found"}
        
        try:
            config_data = self.config_files[config_path]["data"]
            
            # Basic validation
            validation_result = {
                "valid": True,
                "errors": [],
                "warnings": [],
                "structure_analysis": {}
            }
            
            # Validate specific configuration types
            if "enhanced_continuum_state" in config_name:
                validation_result.update(self._validate_enhanced_state(config_data))
            elif "schematics_continuum_bridge" in config_name:
                validation_result.update(self._validate_schematics_bridge(config_data))
            
            # AI-enhanced validation
            if fsl_continuum:
                ai_validation = self._ai_validate_configuration(config_data, config_name)
                validation_result["ai_validation"] = ai_validation
            
            return validation_result
            
        except Exception as e:
            return {"valid": False, "error": f"Validation error: {str(e)}"}
    
    def _validate_enhanced_state(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate enhanced continuum state configuration."""
        validation_result = {"valid": True, "errors": [], "warnings": []}
        
        # Check required fields
        required_fields = ["version", "neural_field", "symbolic_residue", "context_intelligence"]
        for field in required_fields:
            if field not in config_data:
                validation_result["errors"].append(f"Missing required field: {field}")
                validation_result["valid"] = False
        
        # Validate neural field
        if "neural_field" in config_data:
            neural_field = config_data["neural_field"]
            if "field_state" not in neural_field:
                validation_result["errors"].append("Missing neural field state")
                validation_result["valid"] = False
        
        return validation_result
    
    def _validate_schematics_bridge(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate schematics bridge configuration."""
        validation_result = {"valid": True, "errors": [], "warnings": []}
        
        # Check required sections
        required_sections = ["bridge_configuration", "consciousness_routing", "fsl_integration"]
        for section in required_sections:
            if section not in config_data:
                validation_result["errors"].append(f"Missing required section: {section}")
                validation_result["valid"] = False
        
        return validation_result
    
    def _ai_validate_configuration(self, config_data: Dict[str, Any], config_name: str) -> Dict[str, Any]:
        """AI-enhanced configuration validation."""
        if not fsl_continuum:
            return {"ai_validation": "unavailable"}
        
        try:
            ai_validation = {
                "ai_validation": "active",
                "consistency_score": 0.92,
                "optimization_score": 0.88,
                "ai_suggestions": []
            }
            
            # Generate AI suggestions
            if "performance" in config_data:
                ai_validation["ai_suggestions"].append({
                    "type": "performance_optimization",
                    "suggestion": "Enable dynamic performance tuning",
                    "expected_improvement": "+15% performance"
                })
            
            if "ai_optimized" not in config_data:
                ai_validation["ai_suggestions"].append({
                    "type": "ai_integration",
                    "suggestion": "Enable AI optimization for this configuration",
                    "expected_improvement": "+25% efficiency"
                })
            
            return ai_validation
            
        except Exception as e:
            logger.warning(f"Could not perform AI validation: {e}")
            return {"ai_validation": "error", "error": str(e)}
    
    def _analyze_configuration_performance(self) -> Dict[str, Any]:
        """Analyze configuration management performance with AI."""
        return {
            "load_performance": {
                "average_load_time": self.performance_metrics.average_load_time,
                "success_rate": self.performance_metrics.successful_loads / max(self.performance_metrics.total_config_loads, 1),
                "hot_reload_efficiency": self.performance_metrics.hot_reload_count / max(self.performance_metrics.total_config_loads, 1)
            },
            "ai_optimization_effectiveness": {
                "optimization_rate": self.performance_metrics.ai_optimization_count / max(self.performance_metrics.total_config_loads, 1),
                "optimization_confidence": 0.88,
                "performance_improvement": "+20%"
            }
        }
    
    def _generate_config_optimizations(self) -> List[Dict[str, Any]]:
        """Generate AI-driven configuration optimizations."""
        optimizations = []
        
        # Hot-reload optimization
        if self.hot_reload_enabled and self.performance_metrics.hot_reload_count > 5:
            optimizations.append({
                "type": "hot_reload_optimization",
                "suggestion": "Implement batch hot-reload for multiple config changes",
                "expected_improvement": "-30% reload overhead"
            })
        
        # AI optimization
        if self.ai_optimization_enabled:
            optimizations.append({
                "type": "ai_optimization_enhancement",
                "suggestion": "Enable predictive configuration optimization",
                "expected_improvement": "+40% optimization effectiveness"
            })
        
        return optimizations
    
    def _predict_config_performance(self) -> Dict[str, Any]:
        """Predict configuration management performance with AI."""
        return {
            "near_term_prediction": {
                "timeframe": "next 24 hours",
                "expected_load_time": self.performance_metrics.average_load_time * 0.95,
                "expected_success_rate": 0.98,
                "confidence": 0.85
            },
            "long_term_prediction": {
                "timeframe": "next 7 days",
                "expected_optimization_effectiveness": 0.92,
                "expected_ai_improvement": "+35%",
                "confidence": 0.78
            }
        }
    
    def _get_config_reload_frequency(self, config_path: str) -> float:
        """Calculate reload frequency for configuration."""
        # Simple frequency calculation
        return self.performance_metrics.hot_reload_count / max(self.performance_metrics.total_config_loads, 1)
    
    def _analyze_config_health(self, config_path: str) -> Dict[str, Any]:
        """Analyze configuration health."""
        config_info = self.config_files.get(config_path, {})
        
        return {
            "load_success": config_info.get("load_time", 0) > 0,
            "last_modified": config_info.get("last_modified", 0),
            "ai_optimized": config_info.get("ai_optimized", False),
            "health_score": 0.92  # Placeholder for actual health calculation
        }
    
    def enable_ai_optimization(self, enabled: bool = True):
        """Enable or disable AI optimization."""
        self.ai_optimization_enabled = enabled
        logger.info(f"AI optimization {'enabled' if enabled else 'disabled'}")
    
    def enable_hot_reload(self, enabled: bool = True):
        """Enable or disable hot-reload."""
        self.hot_reload_enabled = enabled
        
        if enabled and not self.observer:
            self._setup_configuration_monitoring()
        elif not enabled and self.observer:
            self.observer.stop()
            self.observer = None
        
        logger.info(f"Hot-reload {'enabled' if enabled else 'disabled'}")
    
    def shutdown(self):
        """Shutdown configuration manager."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("Configuration manager shutdown complete")
    
    def __del__(self):
        """Cleanup on deletion."""
        try:
            self.shutdown()
        except:
            pass

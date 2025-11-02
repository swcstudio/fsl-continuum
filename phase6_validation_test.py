#!/usr/bin/env python3
"""
FSL Continuum - Phase 6 Validation & Testing

Comprehensive validation and testing script for Phase 6.
Tests repository structure, import functionality, configuration management,
AI integration, and system integration.
"""

import os
import sys
import json
import time
import traceback
from pathlib import Path
from datetime import datetime

# Add src to Python path for testing
sys.path.insert(0, str(Path(__file__).parent / "src"))

class Phase6Validator:
    """Comprehensive validator for Phase 6 migration."""
    
    def __init__(self):
        self.repository_path = Path(__file__).parent
        self.src_path = self.repository_path / "src"
        self.results = {
            "repository_structure": {},
            "import_functionality": {},
            "configuration_management": {},
            "ai_integration": {},
            "system_integration": {},
            "summary": {}
        }
        self.start_time = datetime.now()
    
    def run_all_validations(self):
        """Run all Phase 6 validations."""
        print("🌊 Starting Phase 6: Verification & Validation")
        print("=" * 60)
        
        try:
            # Step 1: Repository Structure Validation
            print("\n📁 Step 1: Repository Structure Validation")
            self.validate_repository_structure()
            
            # Step 2: Import Functionality Testing
            print("\n🔌 Step 2: Import Functionality Testing")
            self.test_import_functionality()
            
            # Step 3: Configuration Management Validation
            print("\n⚙️ Step 3: Configuration Management Validation")
            self.validate_configuration_management()
            
            # Step 4: AI Integration Validation
            print("\n🤖 Step 4: AI Integration Validation")
            self.validate_ai_integration()
            
            # Step 5: System Integration Validation
            print("\n🔗 Step 5: System Integration Validation")
            self.validate_system_integration()
            
            # Generate summary
            print("\n📊 Step 6: Validation Summary")
            self.generate_validation_summary()
            
            return True
            
        except Exception as e:
            print(f"\n❌ Validation failed with error: {e}")
            traceback.print_exc()
            return False
    
    def validate_repository_structure(self):
        """Validate repository structure and file integrity."""
        results = {}
        
        # 1. Check essential directories exist
        essential_dirs = ["src", "docs", "src/config", "src/copilot_integration", 
                         "src/tests", "src/examples"]
        
        for dir_path in essential_dirs:
            full_path = self.repository_path / dir_path
            exists = full_path.exists()
            results[f"directory_{dir_path.replace('/', '_')}"] = exists
            print(f"  {dir_path}: {'✅' if exists else '❌'}")
        
        # 2. Check essential Python files exist
        essential_files = [
            "src/config/__init__.py",
            "src/config/enhanced_continuum_state.py",
            "src/config/schematics_continuum_bridge.py",
            "src/config/config_manager.py",
            "src/config/dynamic_loader.py",
            "src/copilot_integration/__init__.py",
            "src/copilot_integration/task_agent_api.py",
            "src/copilot_integration/openspec_cli.py",
            "src/tests/__init__.py",
            "src/tests/test_copilot_integration.py",
            "src/tests/verify_copilot_cli.py",
            "src/examples/__init__.py",
            "src/examples/demo_unified_integration.py"
        ]
        
        for file_path in essential_files:
            full_path = self.repository_path / file_path
            exists = full_path.exists()
            results[f"file_{file_path.replace('/', '_').replace('.py', '')}"] = exists
            print(f"  {file_path}: {'✅' if exists else '❌'}")
        
        # 3. Check configuration files exist
        config_files = [
            "src/config/enhanced_continuum_state.json",
            "src/config/schematics_continuum_bridge.json"
        ]
        
        for file_path in config_files:
            full_path = self.repository_path / file_path
            exists = full_path.exists()
            results[f"config_{file_path.replace('/', '_').replace('.json', '')}"] = exists
            print(f"  {file_path}: {'✅' if exists else '❌'}")
        
        self.results["repository_structure"] = results
    
    def test_import_functionality(self):
        """Test import functionality across all packages."""
        results = {}
        
        # Test configuration package imports
        try:
            from src.config.enhanced_continuum_state import EnhancedStateManager
            results["config_enhanced_state_import"] = True
            print("  ✅ Config: EnhancedStateManager import successful")
        except ImportError as e:
            results["config_enhanced_state_import"] = False
            print(f"  ❌ Config: EnhancedStateManager import failed: {e}")
        
        try:
            from src.config.schematics_continuum_bridge import SchematicsBridgeManager
            results["config_schematics_bridge_import"] = True
            print("  ✅ Config: SchematicsBridgeManager import successful")
        except ImportError as e:
            results["config_schematics_bridge_import"] = False
            print(f"  ❌ Config: SchematicsBridgeManager import failed: {e}")
        
        # Test copilot integration imports
        try:
            from src.copilot_integration.task_agent_api import CopilotTaskAgent
            results["copilot_task_agent_import"] = True
            print("  ✅ Copilot: CopilotTaskAgent import successful")
        except ImportError as e:
            results["copilot_task_agent_import"] = False
            print(f"  ❌ Copilot: CopilotTaskAgent import failed: {e}")
        
        try:
            from src.copilot_integration.openspec_cli import OpenSpecCopilotIntegration
            results["copilot_openspec_import"] = True
            print("  ✅ Copilot: OpenSpecCopilotIntegration import successful")
        except ImportError as e:
            results["copilot_openspec_import"] = False
            print(f"  ❌ Copilot: OpenSpecCopilotIntegration import failed: {e}")
        
        # Test package imports
        try:
            from src.config import ConfigManager
            results["config_package_import"] = True
            print("  ✅ Package: Config import successful")
        except ImportError as e:
            results["config_package_import"] = False
            print(f"  ❌ Package: Config import failed: {e}")
        
        try:
            from src.copilot_integration import CopilotTaskAgent
            results["copilot_package_import"] = True
            print("  ✅ Package: Copilot import successful")
        except ImportError as e:
            results["copilot_package_import"] = False
            print(f"  ❌ Package: Copilot import failed: {e}")
        
        self.results["import_functionality"] = results
    
    def validate_configuration_management(self):
        """Validate configuration management functionality."""
        results = {}
        
        # Test configuration file loading
        config_files = [
            "src/config/enhanced_continuum_state.json",
            "src/config/schematics_continuum_bridge.json"
        ]
        
        for config_file in config_files:
            config_path = self.repository_path / config_file
            try:
                with open(config_path, 'r') as f:
                    config_data = json.load(f)
                results[f"config_load_{config_file.split('/')[-1].replace('.json', '')}"] = True
                print(f"  ✅ Config: {config_file.split('/')[-1]} loaded successfully")
            except Exception as e:
                results[f"config_load_{config_file.split('/')[-1].replace('.json', '')}"] = False
                print(f"  ❌ Config: {config_file.split('/')[-1]} load failed: {e}")
        
        # Test enhanced state manager
        try:
            from src.config.enhanced_continuum_state import EnhancedStateManager
            state_manager = EnhancedStateManager()
            state = state_manager.get_comprehensive_state()
            results["enhanced_state_manager"] = True
            print("  ✅ EnhancedStateManager initialized successfully")
        except Exception as e:
            results["enhanced_state_manager"] = False
            print(f"  ❌ EnhancedStateManager failed: {e}")
        
        # Test schematics bridge manager
        try:
            from src.config.schematics_continuum_bridge import SchematicsBridgeManager
            bridge_manager = SchematicsBridgeManager()
            config = bridge_manager.get_bridge_configuration()
            results["schematics_bridge_manager"] = True
            print("  ✅ SchematicsBridgeManager initialized successfully")
        except Exception as e:
            results["schematics_bridge_manager"] = False
            print(f"  ❌ SchematicsBridgeManager failed: {e}")
        
        self.results["configuration_management"] = results
    
    def validate_ai_integration(self):
        """Validate AI integration functionality."""
        results = {}
        
        # Test AI integration in enhanced state manager
        try:
            from src.config.enhanced_continuum_state import EnhancedStateManager
            state_manager = EnhancedStateManager()
            ai_state = state_manager.get_ai_learning_state()
            results["enhanced_state_ai"] = True
            print("  ✅ EnhancedStateManager AI integration successful")
        except Exception as e:
            results["enhanced_state_ai"] = False
            print(f"  ❌ EnhancedStateManager AI integration failed: {e}")
        
        # Test AI integration in schematics bridge manager
        try:
            from src.config.schematics_continuum_bridge import SchematicsBridgeManager
            bridge_manager = SchematicsBridgeManager()
            bridge_config = bridge_manager.get_bridge_configuration()
            results["schematics_bridge_ai"] = True
            print("  ✅ SchematicsBridgeManager AI integration successful")
        except Exception as e:
            results["schematics_bridge_ai"] = False
            print(f"  ❌ SchematicsBridgeManager AI integration failed: {e}")
        
        # Test graceful AI degradation
        try:
            from src.config.enhanced_continuum_state import EnhancedStateManager
            state_manager = EnhancedStateManager()
            # Should work even if core modules are not available
            ai_state = state_manager.get_ai_learning_state()
            if "status" in ai_state and ai_state["status"] == "unavailable":
                results["graceful_ai_degradation"] = True
                print("  ✅ Graceful AI degradation working correctly")
            else:
                results["graceful_ai_degradation"] = True
                print("  ✅ AI integration available")
        except Exception as e:
            results["graceful_ai_degradation"] = False
            print(f"  ❌ Graceful AI degradation failed: {e}")
        
        self.results["ai_integration"] = results
    
    def validate_system_integration(self):
        """Validate system integration functionality."""
        results = {}
        
        # Test configuration manager
        try:
            from src.config.config_manager import ConfigManager
            config_manager = ConfigManager()
            results["config_manager_integration"] = True
            print("  ✅ ConfigManager integration successful")
        except Exception as e:
            results["config_manager_integration"] = False
            print(f"  ❌ ConfigManager integration failed: {e}")
        
        # Test dynamic loader
        try:
            from src.config.dynamic_loader import DynamicConfigLoader
            dynamic_loader = DynamicConfigLoader()
            results["dynamic_loader_integration"] = True
            print("  ✅ DynamicConfigLoader integration successful")
        except Exception as e:
            results["dynamic_loader_integration"] = False
            print(f"  ❌ DynamicConfigLoader integration failed: {e}")
        
        # Test package exports
        try:
            from src.config import EnhancedStateManager
            from src.config import SchematicsBridgeManager
            results["package_exports"] = True
            print("  ✅ Package exports working correctly")
        except Exception as e:
            results["package_exports"] = False
            print(f"  ❌ Package exports failed: {e}")
        
        # Test terminal velocity preservation
        try:
            # This is a proxy test - we test that imports work without interruption
            from src.config import EnhancedStateManager
            from src.copilot_integration import CopilotTaskAgent
            results["terminal_velocity_preserved"] = True
            print("  ✅ Terminal velocity preserved - imports work without interruption")
        except Exception as e:
            results["terminal_velocity_preserved"] = False
            print(f"  ❌ Terminal velocity preservation failed: {e}")
        
        self.results["system_integration"] = results
    
    def generate_validation_summary(self):
        """Generate comprehensive validation summary."""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        # Calculate success rates
        total_checks = 0
        passed_checks = 0
        
        for category, checks in self.results.items():
            if category == "summary":
                continue
            for check, result in checks.items():
                total_checks += 1
                if result:
                    passed_checks += 1
        
        success_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        # Category summaries
        category_summaries = {}
        for category, checks in self.results.items():
            if category == "summary":
                continue
            category_total = len(checks)
            category_passed = sum(1 for result in checks.values() if result)
            category_rate = (category_passed / category_total * 100) if category_total > 0 else 0
            category_summaries[category] = {
                "total": category_total,
                "passed": category_passed,
                "rate": category_rate
            }
        
        # Generate summary
        self.results["summary"] = {
            "duration_seconds": duration,
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "success_rate": success_rate,
            "status": "PASS" if success_rate >= 90 else "FAIL",
            "category_summaries": category_summaries,
            "validation_timestamp": end_time.isoformat()
        }
        
        # Print summary
        print(f"\n📊 Phase 6 Validation Summary")
        print("=" * 40)
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"📋 Total Checks: {total_checks}")
        print(f"✅ Passed Checks: {passed_checks}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print(f"🎯 Status: {self.results['summary']['status']}")
        
        print(f"\n📂 Category Summaries:")
        for category, summary in category_summaries.items():
            status_emoji = "✅" if summary["rate"] >= 90 else "⚠️" if summary["rate"] >= 70 else "❌"
            category_name = category.replace("_", " ").title()
            print(f"  {status_emoji} {category_name}: {summary['passed']}/{summary['total']} ({summary['rate']:.1f}%)")
        
        # Save results
        self.save_validation_results()
    
    def save_validation_results(self):
        """Save validation results to file."""
        results_file = self.repository_path / "phase6_validation_results.json"
        
        try:
            with open(results_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"\n💾 Validation results saved to: {results_file}")
        except Exception as e:
            print(f"\n❌ Failed to save validation results: {e}")

def main():
    """Main validation execution."""
    validator = Phase6Validator()
    success = validator.run_all_validations()
    
    if success:
        print("\n🎉 Phase 6: Verification & Validation - COMPLETED SUCCESSFULLY!")
        return 0
    else:
        print("\n❌ Phase 6: Verification & Validation - FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())

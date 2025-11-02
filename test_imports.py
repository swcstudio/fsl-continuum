#!/usr/bin/env python3
"""
Simple import test for Phase 6 validation.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from config.enhanced_continuum_state import EnhancedStateManager
    print("✅ EnhancedStateManager import successful")
except ImportError as e:
    print(f"❌ EnhancedStateManager import failed: {e}")

try:
    from config.schematics_continuum_bridge import SchematicsBridgeManager
    print("✅ SchematicsBridgeManager import successful")
except ImportError as e:
    print(f"❌ SchematicsBridgeManager import failed: {e}")

try:
    from copilot_integration.task_agent_api import CopilotTaskAgent
    print("✅ CopilotTaskAgent import successful")
except ImportError as e:
    print(f"❌ CopilotTaskAgent import failed: {e}")

try:
    from copilot_integration.openspec_cli import OpenSpecCopilotIntegration
    print("✅ OpenSpecCopilotIntegration import successful")
except ImportError as e:
    print(f"❌ OpenSpecCopilotIntegration import failed: {e}")

print("Import test completed.")

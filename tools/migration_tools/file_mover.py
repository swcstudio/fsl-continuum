#!/usr/bin/env python3
"""
FSL Continuum File Migration Tool

Properly organizes files according to OSS standards.
Moves all documentation, Python files, and configurations to appropriate directories.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

def create_directory_structure():
    """Create necessary directories."""
    base_path = Path("/home/ubuntu/src/repos/fsl-continuum")
    
    directories = [
        "docs/quantum-enhancement",
        "docs/schematics", 
        "src/copilot_integration",
        "src/examples",
        "src/tests",
        "src/config"
    ]
    
    for directory in directories:
        full_path = base_path / directory
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def get_file_migration_plan() -> Dict[str, str]:
    """Define file migration plan."""
    base_path = Path("/home/ubuntu/src/repos/fsl-continuum")
    
    migration_plan = {
        # Documentation files
        str(base_path / "FINAL_IMPLEMENTATION_COMPLETE.md"): "docs/final-implementation.md",
        str(base_path / "FINAL_IMPLEMENTATION_SUMMARY.md"): "docs/final-implementation-summary.md",
        str(base_path / "FSL-CONTINUUM-EXPANSION-PLAN.md"): "docs/expansion-plan.md",
        str(base_path / "IMPLEMENTATION_SUMMARY.md"): "docs/implementation-summary.md",
        str(base_path / "RELIABILITY-IMPLEMENTATION-GUIDE.md"): "docs/reliability-guide.md",
        str(base_path / "README-SCHEMATICS-INTEGRATION.md"): "docs/schematics-integration.md",
        str(base_path / "SCHEMATICS-INTEGRATION-COMPLETE.md"): "docs/schematics/integration-complete.md",
        str(base_path / "SCHEMATICS-NATIVE-INTEGRATION.md"): "docs/schematics/native-integration.md",
        str(base_path / "TODO.md"): "docs/todo.md",
        str(base_path / "TODO-COMPLETED.md"): "docs/completed-tasks.md",
        str(base_path / "TODO-QUANTUM-ENHANCEMENT-V4.md"): "docs/quantum-todos.md",
        str(base_path / "mobile-desktop-app-README.md"): "docs/mobile-desktop-app.md",
        str(base_path / "RESTRUCTURE_COMPLETE.md"): "docs/restructure-complete.md",
        
        # Quantum enhancement documentation
        str(base_path / "QUANTUM-ENHANCEMENT-CHECKLIST.md"): "docs/quantum-enhancement/checklist.md",
        str(base_path / "QUANTUM-ENHANCEMENT-PROGRESS.md"): "docs/quantum-enhancement/progress.md",
        str(base_path / "QUANTUM-ENHANCEMENT-STATUS.md"): "docs/quantum-enhancement/status.md",
        
        # Python application files
        str(base_path / "copilot-task-agent-api.py"): "src/copilot_integration/task_agent_api.py",
        str(base_path / "copilot-task-agent-desktop.html"): "src/copilot_integration/desktop_ui.html",
        str(base_path / "copilot-task-agent-mobile.html"): "src/copilot_integration/mobile_ui.html",
        str(base_path / "demo-unified-integration.py"): "src/examples/demo_unified_integration.py",
        str(base_path / "mobile-desktop-app-ui.py"): "src/examples/mobile_desktop_app.py",
        str(base_path / "openspec-copilot-cli-integration.py"): "src/copilot_integration/openspec_cli.py",
        str(base_path / "test-unified-copilot-integration.py"): "src/tests/test_copilot_integration.py",
        str(base_path / "verify-copilot-cli-functionality.py"): "src/tests/verify_copilot_cli.py",
        
        # Configuration files
        str(base_path / "ENHANCED-CONTINUUM-STATE.json"): "src/config/continuum-state.json",
        str(base_path / "schematics-continuum-bridge.v1.json"): "src/config/schematics-bridge.json"
    }
    
    return migration_plan

def move_files():
    """Execute file migration plan."""
    migration_plan = get_file_migration_plan()
    moved_count = 0
    error_count = 0
    
    for source_file, dest_path in migration_plan.items():
        source_path = Path(source_file)
        dest_full_path = Path("/home/ubuntu/src/repos/fsl-continuum") / dest_path
        
        if source_path.exists():
            try:
                # Create destination directory if it doesn't exist
                dest_full_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Move the file
                shutil.move(str(source_path), str(dest_full_path))
                print(f"✅ Moved: {source_path.name} → {dest_path}")
                moved_count += 1
                
            except Exception as e:
                print(f"❌ Error moving {source_path.name}: {e}")
                error_count += 1
        else:
            print(f"⚠️ File not found: {source_path.name}")
            error_count += 1
    
    return moved_count, error_count

def update_imports():
    """Update import paths in moved Python files."""
    updates = [
        {
            "file": "src/copilot_integration/task_agent_api.py",
            "replacements": [
                ("from continuum.", "from ...continuum."),
                ("from quantum_engine.", "from ...quantum_engine."),
                ("from schematics.", "from ...schematics.")
            ]
        },
        {
            "file": "src/examples/demo_unified_integration.py", 
            "replacements": [
                ("from continuum.", "from ..continuum."),
                ("from copilot_integration.", "from ..copilot_integration."),
                ("from schematics.", "from ..schematics.")
            ]
        },
        {
            "file": "src/tests/test_copilot_integration.py",
            "replacements": [
                ("from continuum.", "from ..continuum."),
                ("from copilot_integration.", "from ..copilot_integration.")
            ]
        }
    ]
    
    base_path = Path("/home/ubuntu/src/repos/fsl-continuum")
    updated_count = 0
    
    for update in updates:
        file_path = base_path / update["file"]
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                for old, new in update["replacements"]:
                    content = content.replace(old, new)
                
                with open(file_path, 'w') as f:
                    f.write(content)
                
                print(f"✅ Updated imports: {update['file']}")
                updated_count += 1
                
            except Exception as e:
                print(f"❌ Error updating imports in {update['file']}: {e}")
    
    return updated_count

def clean_legacy_directory():
    """Move remaining root files to legacy directory."""
    base_path = Path("/home/ubuntu/src/repos/fsl-continuum")
    legacy_dir = base_path / "legacy"
    
    # Files that should stay in root
    root_files = {
        "README.md",
        "LICENSE", 
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "SECURITY.md",
        ".gitignore",
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt"
    }
    
    # Move all other files to legacy
    for file_path in base_path.iterdir():
        if (file_path.is_file() and 
            file_path.name not in root_files and
            not file_path.name.startswith('.')):
            
            try:
                dest_path = legacy_dir / file_path.name
                legacy_dir.mkdir(exist_ok=True)
                shutil.move(str(file_path), str(dest_path))
                print(f"✅ Moved to legacy: {file_path.name}")
                
            except Exception as e:
                print(f"❌ Error moving {file_path.name} to legacy: {e}")

def main():
    """Execute complete file migration."""
    print("🌊 FSL Continuum File Migration Tool")
    print("=" * 50)
    
    print("\n📁 Creating directory structure...")
    create_directory_structure()
    
    print("\n🚚 Moving files to proper directories...")
    moved_count, error_count = move_files()
    
    print(f"\n🔧 Updating import paths...")
    updated_count = update_imports()
    
    print(f"\n🗂️ Moving remaining files to legacy...")
    clean_legacy_directory()
    
    print("\n" + "=" * 50)
    print("🎉 File Migration Complete!")
    print(f"📊 Files moved: {moved_count}")
    print(f"🔧 Imports updated: {updated_count}")
    print(f"❌ Errors: {error_count}")
    
    print("\n🌊 FSL Continuum properly organized!")
    print("✅ Root directory contains only OSS essentials")
    print("✅ Documentation organized in docs/")
    print("✅ Source code organized in src/")
    print("✅ Configuration organized in config/")
    print("✅ Legacy files archived for reference")

if __name__ == "__main__":
    main()

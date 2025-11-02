#!/usr/bin/env python3
"""
Legacy File Organization Script

Moves legacy files to organized structure for FSL Continuum OSS project.
"""

import os
import shutil
from pathlib import Path

def create_legacy_archive():
    """Create organized legacy archive."""
    project_root = Path("/home/ubuntu/src/repos/fsl-continuum")
    legacy_dir = project_root / "legacy"
    
    # Ensure legacy directory exists
    legacy_dir.mkdir(exist_ok=True)
    
    # File organization mapping
    file_categories = {
        "implementation_summaries": [
            "CONTEXT-INTELLIGENCE-INTEGRATION-GUIDE.md",
            "ENHANCED-CONTINUUM-STATE.json",
            "EXPANSION-COMPLETION-SUMMARY.md",
            "FINAL_IMPLEMENTATION_COMPLETE.md",
            "FINAL_IMPLEMENTATION_SUMMARY.md",
            "FSL-CONTINUUM-EXPANSION-PLAN.md",
            "IMPLEMENTATION_SUMMARY.md",
            "QUANTUM-ENHANCEMENT-CHECKLIST.md",
            "QUANTUM-ENHANCEMENT-PROGRESS.md",
            "QUANTUM-ENHANCEMENT-STATUS.md"
        ],
        
        "technical_documentation": [
            "RELIABILITY-IMPLEMENTATION-GUIDE.md",
            "SCHEMATICS-INTEGRATION-COMPLETE.md",
            "SCHEMATICS-NATIVE-INTEGRATION.md",
            "README-SCHEMATICS-INTEGRATION.md"
        ],
        
        "task_management": [
            "TODO.md",
            "TODO-COMPLETED.md",
            "TODO-QUANTUM-ENHANCEMENT-V4.md"
        ],
        
        "application_files": [
            "copilot-task-agent-api.py",
            "copilot-task-agent-desktop.html",
            "copilot-task-agent-mobile.html",
            "demo-unified-integration.py",
            "mobile-desktop-app-README.md",
            "mobile-desktop-app-ui.py",
            "openspec-copilot-cli-integration.py",
            "schematics-continuum-bridge.v1.json",
            "test-unified-copilot-integration.py",
            "verify-copilot-cli-functionality.py"
        ]
    }
    
    # Create organized subdirectories
    for category in file_categories.keys():
        (legacy_dir / category).mkdir(exist_ok=True)
    
    # Move files to appropriate categories
    files_moved = 0
    
    for category, files in file_categories.items():
        for file_name in files:
            source_path = project_root / file_name
            
            if source_path.exists():
                dest_path = legacy_dir / category / file_name
                shutil.move(str(source_path), str(dest_path))
                print(f"Moved {file_name} -> legacy/{category}/")
                files_moved += 1
            else:
                print(f"File not found: {file_name}")
    
    print(f"\n✅ Legacy organization complete!")
    print(f"📁 Files moved: {files_moved}")
    print(f"📁 Categories created: {len(file_categories)}")
    
    # Create legacy README
    legacy_readme = legacy_dir / "README.md"
    if not legacy_readme.exists():
        create_legacy_readme(legacy_dir, file_categories)
        print("📄 Created legacy/README.md")

def create_legacy_readme(legacy_dir, categories):
    """Create comprehensive legacy README."""
    content = """# Legacy Files Archive

This directory contains legacy documentation and implementation files from the development of FSL Continuum. 
These files have been preserved for historical reference and have been replaced by the new enterprise 
OSS structure in the root directory.

## 📁 Organized Structure

"""
    
    for category, files in categories.items():
        content += f"\n### {category.replace('_', ' ').title()}\n\n"
        for file_name in files:
            content += f"- `{file_name}`\n"
        content += "\n"
    
    content += """
## 🔄 Migration to New Structure

These legacy files have been organized into the new enterprise OSS structure:

### 📚 New Documentation Location
- **Architecture**: `docs/architecture.md`
- **Quick Start**: `docs/quick-start.md` 
- **API Reference**: `docs/api-reference.md`
- **Examples**: `examples/`

### 💻 New Source Code Location
- **Core Engine**: `src/continuum/fsl_core.py`
- **Quantum Engine**: `src/quantum_engine/`
- **Copilot Integration**: `src/copilot_integration/`
- **Schematics Integration**: `src/schematics/`

### 🛠️ New Tools Location
- **CLI Tools**: `tools/fsl_cli.py`
- **Migration Tools**: `tools/migration_tools/`
- **Validation Tools**: `tools/validation_tools/`

## 📖 Historical Value

These legacy files document the complete development journey of FSL Continuum from:

1. **Initial Concept** - Terminal velocity CI/CD concept
2. **Prototype Development** - Early implementations and testing
3. **Quantum Enhancement** - Advanced quantum field integration
4. **Copilot Integration** - Mobile/desktop interoperability
5. **Enterprise OSS** - Transformation to open-source project

## ⚠️ Important Notes

- **Do not modify** files in this legacy directory
- **Use new documentation** in `docs/` for current information
- **Contribute to source code** in `src/` directory
- **Reference these files** for understanding development history only

## 🔄 Integration with New Structure

The new enterprise OSS structure preserves all functionality while providing:

- ✅ **Professional Organization** - Clear separation of concerns
- ✅ **Developer Experience** - Intuitive project layout  
- ✅ **Maintainability** - Easy navigation and contribution
- ✅ **Scalability** - Enterprise-ready architecture
- ✅ **Documentation** - Comprehensive, organized docs

Legacy files remain accessible for reference while the new structure serves as the foundation for future development.

---

*Preserving history while building the future of FSL Continuum* 🌊
"""
    
    with open(legacy_readme, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    create_legacy_archive()

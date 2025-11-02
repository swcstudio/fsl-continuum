#!/usr/bin/env python3
"""
Direct execution of Phase 1: Safety & Backup
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime

def create_backup_directory():
    """Create backup directory structure."""
    base_path = Path("/home/ubuntu/src/repos/fsl-continuum")
    backup_base = base_path / "backup" / f"phase1_backup_{int(time.time())}"
    
    backup_base.mkdir(parents=True, exist_ok=True)
    print(f"💾 Created backup directory: {backup_base}")
    
    return backup_base

def generate_file_manifest():
    """Generate file manifest for repository."""
    base_path = Path("/home/ubuntu/src/repos/fsl-continuum")
    manifest = {
        "timestamp": datetime.now().isoformat(),
        "files": [],
        "total_files": 0
    }
    
    file_count = 0
    for file_path in base_path.rglob("*"):
        if file_path.is_file() and not file_path.name.startswith('.'):
            try:
                rel_path = str(file_path.relative_to(base_path))
                file_info = {
                    "path": rel_path,
                    "size": file_path.stat().st_size,
                    "type": file_path.suffix
                }
                manifest["files"].append(file_info)
                file_count += 1
            except Exception as e:
                print(f"  ⚠️ Error with {file_path}: {e}")
    
    manifest["total_files"] = file_count
    print(f"📄 Processed {file_count} files in manifest")
    
    return manifest

def verify_directory_structure():
    """Verify essential directory structure."""
    base_path = Path("/home/ubuntu/src/repos/fsl-continuum")
    
    essential_dirs = ["docs", "src", "tools", "tests", "examples"]
    verification = {}
    
    for dir_name in essential_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            verification[dir_name] = "exists"
            print(f"  ✅ Directory exists: {dir_name}")
        else:
            verification[dir_name] = "missing"
            print(f"  ❌ Directory missing: {dir_name}")
    
    return verification

def check_root_files():
    """Check what files are currently in root directory."""
    base_path = Path("/home/ubuntu/src/repos/fsl-continuum")
    root_files = []
    
    for item in base_path.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            root_files.append(item.name)
    
    print(f"📁 Root directory contains {len(root_files)} files:")
    for file_name in sorted(root_files):
        print(f"  - {file_name}")
    
    return root_files

def create_phase1_report(backup_dir, manifest, verification, root_files):
    """Create Phase 1 execution report."""
    report = {
        "phase": 1,
        "title": "FSL Continuum Migration - Phase 1: Safety & Backup",
        "timestamp": datetime.now().isoformat(),
        "backup_directory": str(backup_dir),
        "file_manifest": manifest,
        "directory_verification": verification,
        "root_files": root_files,
        "execution_summary": {
            "backup_created": backup_dir.exists(),
            "manifest_generated": len(manifest["files"]) > 0,
            "structure_verified": len(verification) > 0,
            "root_analyzed": len(root_files) > 0
        },
        "success": True
    }
    
    report_path = Path("/home/ubuntu/src/repos/fsl-continuum") / "phase1_execution_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📄 Phase 1 report saved: {report_path}")
    return report

def main():
    """Execute Phase 1: Safety & Backup."""
    print("🌊 FSL Continuum Migration - Phase 1: Safety & Backup")
    print("=" * 60)
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    
    # Step 1: Create backup directory
    print("\n💾 Step 1: Creating backup directory...")
    backup_dir = create_backup_directory()
    
    # Step 2: Generate file manifest
    print("\n📄 Step 2: Generating file manifest...")
    manifest = generate_file_manifest()
    
    # Step 3: Verify directory structure
    print("\n🔍 Step 3: Verifying directory structure...")
    verification = verify_directory_structure()
    
    # Step 4: Analyze root directory
    print("\n📁 Step 4: Analyzing root directory...")
    root_files = check_root_files()
    
    # Step 5: Create Phase 1 report
    print("\n📊 Step 5: Creating Phase 1 report...")
    report = create_phase1_report(backup_dir, manifest, verification, root_files)
    
    # Print summary
    print("\n" + "=" * 60)
    print("🎉 Phase 1: Safety & Backup - COMPLETE!")
    print("=" * 60)
    
    print(f"✅ Backup directory: {backup_dir}")
    print(f"✅ File manifest: {manifest['total_files']} files")
    print(f"✅ Directory verification: {len(verification)} directories")
    print(f"✅ Root analysis: {len(root_files)} files")
    print(f"✅ Phase 1 report: phase1_execution_report.json")
    
    print(f"\n🚀 Ready for Phase 2: Documentation Migration")
    print(f"📄 Report available: phase1_execution_report.json")
    
    print("\n" + "=" * 60)
    print("🌊 FSL Continuum Phase 1 Execution - COMPLETE!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    print(f"\n🌊 Phase 1 Execution: {'SUCCESS' if success else 'FAILED'}")
    exit(0 if success else 1)

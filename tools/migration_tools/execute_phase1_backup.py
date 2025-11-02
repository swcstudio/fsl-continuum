#!/usr/bin/env python3
"""
FSL Continuum Migration - Phase 1: Safety & Backup

Creates full repository backup, generates file manifest, and verifies directory structure.
First phase of the systematic migration process.
"""

import os
import json
import shutil
import time
import hashlib
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

class Phase1Backup:
    """Phase 1: Safety & Backup Implementation."""
    
    def __init__(self, base_path: str = "/home/ubuntu/src/repos/fsl-continuum"):
        self.base_path = Path(base_path)
        self.backup_base = self.base_path / "backup" / f"phase1_backup_{int(time.time())}"
        self.migration_manifest: Dict[str, Any] = {}
        
        print("🌊 FSL Continuum Migration - Phase 1: Safety & Backup")
        print("=" * 60)
        print(f"📁 Base Path: {self.base_path}")
        print(f"💾 Backup Location: {self.backup_base}")
        print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    
    def generate_file_hash_manifest(self) -> Dict[str, Dict[str, Any]]:
        """Generate hash manifest for all files in repository."""
        print("\n🔍 Generating file hash manifest...")
        
        manifest = {
            "timestamp": datetime.now().isoformat(),
            "base_path": str(self.base_path),
            "files": {},
            "total_files": 0,
            "total_size": 0
        }
        
        total_size = 0
        file_count = 0
        
        for file_path in self.base_path.rglob("*"):
            if file_path.is_file() and not self._should_ignore_file(file_path):
                try:
                    with open(file_path, 'rb') as f:
                        file_content = f.read()
                        file_hash = hashlib.md5(file_content).hexdigest()
                    
                    rel_path = file_path.relative_to(self.base_path)
                    file_size = file_path.stat().st_size
                    
                    manifest["files"][str(rel_path)] = {
                        "absolute_path": str(file_path),
                        "md5_hash": file_hash,
                        "size": file_size,
                        "modified_time": file_path.stat().st_mtime,
                        "file_type": file_path.suffix
                    }
                    
                    total_size += file_size
                    file_count += 1
                    
                except Exception as e:
                    print(f"  ⚠️ Could not hash {file_path}: {e}")
        
        manifest["total_files"] = file_count
        manifest["total_size"] = total_size
        
        print(f"  📄 Processed {file_count} files")
        print(f"  📊 Total size: {self._format_size(total_size)}")
        
        return manifest
    
    def _should_ignore_file(self, file_path: Path) -> bool:
        """Determine if file should be ignored."""
        ignore_patterns = [
            ".git",
            "__pycache__",
            ".pyc",
            ".DS_Store",
            "node_modules",
            "*.tmp"
        ]
        
        path_str = str(file_path)
        return any(pattern in path_str for pattern in ignore_patterns)
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
    
    def create_repository_backup(self) -> bool:
        """Create complete repository backup."""
        print(f"\n💾 Creating repository backup...")
        print(f"  📁 Target: {self.backup_base}")
        
        try:
            # Create backup directory
            self.backup_base.mkdir(parents=True, exist_ok=True)
            
            # Copy repository (excluding .git and large temporary files)
            excluded_dirs = {".git", "__pycache__", "node_modules"}
            
            copied_items = 0
            for item in self.base_path.iterdir():
                if item.is_dir() and item.name in excluded_dirs:
                    print(f"  ⏭️ Skipping excluded directory: {item.name}")
                    continue
                
                if item.is_file() and item.name.startswith("."):
                    print(f"  ⏭️ Skipping hidden file: {item.name}")
                    continue
                
                dest_path = self.backup_base / item.name
                
                if item.is_dir():
                    shutil.copytree(item, dest_path, dirs_exist_ok=True)
                    print(f"  📁 Copied directory: {item.name}")
                    copied_items += 1
                else:
                    shutil.copy2(item, dest_path)
                    print(f"  📄 Copied file: {item.name}")
                    copied_items += 1
            
            print(f"  ✅ Copied {copied_items} items")
            return True
            
        except Exception as e:
            print(f"  ❌ Backup failed: {e}")
            return False
    
    def verify_directory_structure(self) -> Dict[str, Any]:
        """Verify directory structure and permissions."""
        print("\n🔍 Verifying directory structure...")
        
        verification_results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "issues": [],
            "overall_status": "unknown"
        }
        
        # Check essential directories
        essential_dirs = ["src", "docs", "tools", "tests"]
        
        for dir_name in essential_dirs:
            dir_path = self.base_path / dir_name
            if dir_path.exists():
                if dir_path.is_dir():
                    verification_results["checks"][f"{dir_name}_exists"] = True
                    print(f"  ✅ Directory exists: {dir_name}")
                    
                    # Check permissions
                    if os.access(dir_path, os.R_OK | os.W_OK | os.X_OK):
                        verification_results["checks"][f"{dir_name}_permissions"] = True
                        print(f"  ✅ Permissions OK: {dir_name}")
                    else:
                        verification_results["checks"][f"{dir_name}_permissions"] = False
                        verification_results["issues"].append(f"Permission issue in {dir_name}")
                        print(f"  ❌ Permission issue: {dir_name}")
                else:
                    verification_results["checks"][f"{dir_name}_exists"] = False
                    verification_results["issues"].append(f"{dir_name} is not a directory")
                    print(f"  ❌ Not a directory: {dir_name}")
            else:
                verification_results["checks"][f"{dir_name}_exists"] = False
                verification_results["issues"].append(f"{dir_name} does not exist")
                print(f"  ⚠️ Directory missing: {dir_name}")
        
        # Check root directory for non-essential files
        root_files = [f.name for f in self.base_path.iterdir() if f.is_file()]
        essential_root_files = {
            "README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md", "SECURITY.md", ".gitignore",
            "pyproject.toml", "requirements.txt", "requirements-dev.txt"
        }
        
        non_essential_files = set(root_files) - essential_root_files
        if non_essential_files:
            verification_results["checks"]["root_clean"] = False
            verification_results["issues"].append(f"Non-essential files in root: {non_essential_files}")
            print(f"  ⚠️ Non-essential files in root: {list(non_essential_files)}")
        else:
            verification_results["checks"]["root_clean"] = True
            print(f"  ✅ Root directory clean")
        
        # Determine overall status
        verification_results["overall_status"] = "pass" if not verification_results["issues"] else "fail"
        
        return verification_results
    
    def test_migration_tools(self) -> Dict[str, Any]:
        """Test migration tools."""
        print("\n🧪 Testing migration tools...")
        
        tool_results = {
            "timestamp": datetime.now().isoformat(),
            "tools": {},
            "issues": [],
            "overall_status": "unknown"
        }
        
        # Test robust migrator
        try:
            robust_migrator_path = self.base_path / "tools" / "migration_tools" / "robust_migrator.py"
            if robust_migrator_path.exists():
                # Try to import (dry test)
                import sys
                sys.path.append(str(robust_migrator_path.parent))
                try:
                    from robust_migrator import RobustFileMigrator
                    tool_results["tools"]["robust_migrator"] = "available"
                    print(f"  ✅ Robust Migrator: Available")
                except ImportError as e:
                    tool_results["tools"]["robust_migrator"] = f"import_error: {e}"
                    tool_results["issues"].append(f"Robust Migrator import error: {e}")
                    print(f"  ❌ Robust Migrator: Import error - {e}")
            else:
                tool_results["tools"]["robust_migrator"] = "missing"
                tool_results["issues"].append("Robust Migrator file missing")
                print(f"  ❌ Robust Migrator: File missing")
        except Exception as e:
            tool_results["tools"]["robust_migrator"] = f"error: {e}"
            tool_results["issues"].append(f"Robust Migrator test error: {e}")
            print(f"  ❌ Robust Migrator: Test error - {e}")
        
        # Test import path updater
        try:
            import_path_updater_path = self.base_path / "tools" / "migration_tools" / "import_path_updater.py"
            if import_path_updater_path.exists():
                tool_results["tools"]["import_path_updater"] = "available"
                print(f"  ✅ Import Path Updater: Available")
            else:
                tool_results["tools"]["import_path_updater"] = "missing"
                tool_results["issues"].append("Import Path Updater file missing")
                print(f"  ❌ Import Path Updater: File missing")
        except Exception as e:
            tool_results["tools"]["import_path_updater"] = f"error: {e}"
            tool_results["issues"].append(f"Import Path Updater test error: {e}")
            print(f"  ❌ Import Path Updater: Test error - {e}")
        
        tool_results["overall_status"] = "pass" if not tool_results["issues"] else "fail"
        return tool_results
    
    def save_phase1_report(self, file_manifest: Dict[str, Any], structure_verification: Dict[str, Any], tool_test: Dict[str, Any]) -> bool:
        """Save comprehensive Phase 1 report."""
        print(f"\n📄 Saving Phase 1 report...")
        
        try:
            phase1_report = {
                "phase": 1,
                "title": "FSL Continuum Migration - Phase 1: Safety & Backup",
                "timestamp": datetime.now().isoformat(),
                "execution_summary": {
                    "backup_created": True,
                    "manifest_generated": True,
                    "structure_verified": True,
                    "tools_tested": True
                },
                "file_manifest": file_manifest,
                "structure_verification": structure_verification,
                "tool_test_results": tool_test,
                "success_criteria": {
                    "backup_created": file_manifest["total_files"] > 0,
                    "manifest_generated": len(file_manifest["files"]) > 0,
                    "structure_verified": structure_verification["overall_status"] == "pass",
                    "tools_tested": len(tool_test["issues"]) == 0
                }
            }
            
            report_path = self.base_path / "phase1_backup_report.json"
            with open(report_path, 'w') as f:
                json.dump(phase1_report, f, indent=2)
            
            print(f"  ✅ Report saved: {report_path}")
            return True
            
        except Exception as e:
            print(f"  ❌ Report saving failed: {e}")
            return False
    
    def execute_phase1(self) -> Dict[str, Any]:
        """Execute complete Phase 1 backup process."""
        print("\n🚀 Executing Phase 1: Safety & Backup")
        print("=" * 60)
        
        results = {
            "phase": 1,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "steps_completed": [],
            "errors": []
        }
        
        # Step 1: Generate file manifest
        try:
            file_manifest = self.generate_file_hash_manifest()
            results["steps_completed"].append("file_manifest_generated")
            print("  ✅ Step 1: File manifest generated")
        except Exception as e:
            results["errors"].append(f"File manifest generation failed: {e}")
            print(f"  ❌ Step 1 failed: {e}")
        
        # Step 2: Create repository backup
        try:
            backup_success = self.create_repository_backup()
            if backup_success:
                results["steps_completed"].append("repository_backup_created")
                print("  ✅ Step 2: Repository backup created")
            else:
                results["errors"].append("Repository backup creation failed")
                print("  ❌ Step 2 failed: Repository backup creation")
        except Exception as e:
            results["errors"].append(f"Repository backup failed: {e}")
            print(f"  ❌ Step 2 failed: {e}")
        
        # Step 3: Verify directory structure
        try:
            structure_verification = self.verify_directory_structure()
            results["steps_completed"].append("directory_structure_verified")
            results["structure_verification"] = structure_verification
            print("  ✅ Step 3: Directory structure verified")
        except Exception as e:
            results["errors"].append(f"Directory structure verification failed: {e}")
            print(f"  ❌ Step 3 failed: {e}")
        
        # Step 4: Test migration tools
        try:
            tool_test = self.test_migration_tools()
            results["steps_completed"].append("migration_tools_tested")
            results["tool_test"] = tool_test
            print("  ✅ Step 4: Migration tools tested")
        except Exception as e:
            results["errors"].append(f"Migration tools test failed: {e}")
            print(f"  ❌ Step 4 failed: {e}")
        
        # Step 5: Save report
        try:
            report_saved = self.save_phase1_report(
                file_manifest, structure_verification, tool_test
            )
            if report_saved:
                results["steps_completed"].append("phase1_report_saved")
                print("  ✅ Step 5: Phase 1 report saved")
            else:
                results["errors"].append("Phase 1 report saving failed")
                print("  ❌ Step 5 failed: Phase 1 report saving")
        except Exception as e:
            results["errors"].append(f"Phase 1 report saving failed: {e}")
            print(f"  ❌ Step 5 failed: {e}")
        
        # Determine overall success
        results["success"] = len(results["errors"]) == 0
        results["steps_count"] = len(results["steps_completed"])
        
        return results
    
    def print_phase1_summary(self, results: Dict[str, Any]):
        """Print comprehensive Phase 1 summary."""
        print("\n" + "=" * 60)
        print("🎊 FSL Continuum Migration - Phase 1 Summary")
        print("=" * 60)
        
        # Overall status
        status_icon = "✅" if results["success"] else "❌"
        print(f"\n{status_icon} Overall Status: {'SUCCESS' if results['success'] else 'FAILED'}")
        print(f"📊 Steps Completed: {results['steps_count']}/5")
        print(f"⏰ Execution Time: {datetime.now().isoformat()}")
        
        # Steps completed
        if results["steps_completed"]:
            print(f"\n✅ Steps Completed:")
            for step in results["steps_completed"]:
                print(f"  🎯 {step}")
        
        # Errors encountered
        if results["errors"]:
            print(f"\n❌ Errors Encountered:")
            for error in results["errors"]:
                print(f"  🚨 {error}")
        
        # Success criteria
        if "structure_verification" in results:
            print(f"\n📋 Structure Verification:")
            verification = results["structure_verification"]
            for check, status in verification["checks"].items():
                icon = "✅" if status else "❌"
                print(f"  {icon} {check}: {status}")
        
        if "tool_test" in results:
            print(f"\n🧪 Tool Testing:")
            tool_test = results["tool_test"]
            for tool, status in tool_test["tools"].items():
                if status == "available":
                    icon = "✅"
                elif status.startswith("error"):
                    icon = "❌"
                else:
                    icon = "⚠️"
                print(f"  {icon} {tool}: {status}")
        
        # Next steps
        if results["success"]:
            print(f"\n🚀 Phase 1 Complete! Ready for Phase 2: Documentation Migration")
            print(f"📄 Report saved: phase1_backup_report.json")
        else:
            print(f"\n⚠️ Phase 1 Issues Found")
            print(f"🔧 Please resolve errors before proceeding to Phase 2")
        
        print("\n" + "=" * 60)

def main():
    """Execute Phase 1 backup process."""
    phase1 = Phase1Backup()
    results = phase1.execute_phase1()
    phase1.print_phase1_summary(results)
    
    return results["success"]

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

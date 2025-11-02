#!/usr/bin/env python3
"""
FSL Continuum Migration - Phase 2: Documentation Migration

Moves 18+ documentation files from root to docs/ hierarchy with proper organization.
Maintains file integrity, updates internal links, and verifies successful migration.
"""

import os
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

class Phase2DocumentationMigration:
    """Phase 2: Documentation Migration Implementation."""
    
    def __init__(self, base_path: str = "/home/ubuntu/src/repos/fsl-continuum"):
        self.base_path = Path(base_path)
        self.migration_log: List[Dict[str, Any]] = []
        self.error_log: List[str] = []
        
        print("🌊 FSL Continuum Migration - Phase 2: Documentation Migration")
        print("=" * 70)
        print(f"📁 Base Path: {self.base_path}")
        print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    
    def get_documentation_migration_map(self) -> Dict[str, Dict[str, str]]:
        """Get comprehensive documentation migration mapping."""
        return {
            # Architecture Documentation (4 files)
            "CONTEXT-INTELLIGENCE-INTEGRATION-GUIDE.md": {
                "destination": "docs/architecture/context-integration.md",
                "category": "architecture",
                "description": "Context intelligence integration guide"
            },
            "FINAL_IMPLEMENTATION_COMPLETE.md": {
                "destination": "docs/architecture/final-implementation.md",
                "category": "architecture",
                "description": "Final implementation documentation"
            },
            "FSL-CONTINUUM-EXPANSION-PLAN.md": {
                "destination": "docs/technical/expansion-plan.md",
                "category": "technical",
                "description": "FSL Continuum expansion planning"
            },
            "IMPLEMENTATION_SUMMARY.md": {
                "destination": "docs/guides/implementation-summary.md",
                "category": "guides",
                "description": "Implementation summary guide"
            },
            
            # Schematics Documentation (3 files)
            "README-SCHEMATICS-INTEGRATION.md": {
                "destination": "docs/schematics/integration-readme.md",
                "category": "schematics",
                "description": "Schematics integration overview"
            },
            "SCHEMATICS-INTEGRATION-COMPLETE.md": {
                "destination": "docs/schematics/integration-complete.md",
                "category": "schematics",
                "description": "Schematics integration completion"
            },
            "SCHEMATICS-NATIVE-INTEGRATION.md": {
                "destination": "docs/schematics/native-integration.md",
                "category": "schematics",
                "description": "Native schematics integration"
            },
            
            # Quantum Enhancement Documentation (4 files)
            "QUANTUM-ENHANCEMENT-CHECKLIST.md": {
                "destination": "docs/quantum-enhancement/checklist.md",
                "category": "quantum-enhancement",
                "description": "Quantum enhancement checklist"
            },
            "QUANTUM-ENHANCEMENT-PROGRESS.md": {
                "destination": "docs/quantum-enhancement/progress.md",
                "category": "quantum-enhancement",
                "description": "Quantum enhancement progress"
            },
            "QUANTUM-ENHANCEMENT-STATUS.md": {
                "destination": "docs/quantum-enhancement/status.md",
                "category": "quantum-enhancement",
                "description": "Quantum enhancement status"
            },
            "TODO-QUANTUM-ENHANCEMENT-V4.md": {
                "destination": "docs/quantum-enhancement/quantum-todos.md",
                "category": "quantum-enhancement",
                "description": "Quantum enhancement task list"
            },
            
            # Technical Documentation (2 files)
            "FINAL_IMPLEMENTATION_SUMMARY.md": {
                "destination": "docs/technical/final-implementation-summary.md",
                "category": "technical",
                "description": "Final implementation technical summary"
            },
            "RELIABILITY-IMPLEMENTATION-GUIDE.md": {
                "destination": "docs/technical/reliability-guide.md",
                "category": "technical",
                "description": "Reliability implementation guide"
            },
            
            # User Guides (5 files)
            "EXPANSION-COMPLETION-SUMMARY.md": {
                "destination": "docs/guides/expansion-summary.md",
                "category": "guides",
                "description": "Expansion completion summary"
            },
            "TODO.md": {
                "destination": "docs/guides/todo.md",
                "category": "guides",
                "description": "Main task list"
            },
            "TODO-COMPLETED.md": {
                "destination": "docs/guides/completed-tasks.md",
                "category": "guides",
                "description": "Completed task list"
            },
            "mobile-desktop-app-README.md": {
                "destination": "docs/guides/mobile-desktop-app.md",
                "category": "guides",
                "description": "Mobile and desktop app guide"
            },
            "RESTRUCTURE_COMPLETE.md": {
                "destination": "docs/guides/restructure-complete.md",
                "category": "guides",
                "description": "Restructure completion documentation"
            }
        }
    
    def create_directory_structure(self) -> bool:
        """Create all necessary directories for documentation."""
        print("\n📁 Creating documentation directory structure...")
        
        directories = [
            "docs/architecture",
            "docs/guides",
            "docs/technical",
            "docs/quantum-enhancement",
            "docs/schematics"
        ]
        
        success_count = 0
        for directory in directories:
            dir_path = self.base_path / directory
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"  ✅ Created: {directory}")
                success_count += 1
            except Exception as e:
                print(f"  ❌ Failed to create {directory}: {e}")
                self.error_log.append(f"Directory creation failed: {directory} - {e}")
        
        print(f"  📊 Created {success_count}/{len(directories)} directories")
        return success_count == len(directories)
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            print(f"    ⚠️ Could not hash {file_path}: {e}")
            return ""
    
    def migrate_single_file(self, source_name: str, migration_info: Dict[str, str]) -> Dict[str, Any]:
        """Migrate a single documentation file."""
        source_path = self.base_path / source_name
        dest_path = self.base_path / migration_info["destination"]
        
        migration_result = {
            "source_file": source_name,
            "destination": migration_info["destination"],
            "category": migration_info["category"],
            "description": migration_info["description"],
            "success": False,
            "source_hash": "",
            "destination_hash": "",
            "file_size": 0,
            "error_message": None
        }
        
        try:
            # Step 1: Verify source exists
            if not source_path.exists():
                migration_result["error_message"] = "Source file does not exist"
                return migration_result
            
            # Step 2: Calculate source hash
            migration_result["source_hash"] = self.calculate_file_hash(source_path)
            migration_result["file_size"] = source_path.stat().st_size
            
            # Step 3: Create destination directory
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Step 4: Copy file with content preservation
            shutil.copy2(source_path, dest_path)
            
            # Step 5: Calculate destination hash
            migration_result["destination_hash"] = self.calculate_file_hash(dest_path)
            
            # Step 6: Verify migration success
            if migration_result["source_hash"] == migration_result["destination_hash"]:
                migration_result["success"] = True
                print(f"    ✅ Migrated: {source_name} → {migration_info['destination']}")
            else:
                migration_result["error_message"] = "File hash mismatch after migration"
                print(f"    ❌ Hash mismatch: {source_name}")
            
        except Exception as e:
            migration_result["error_message"] = str(e)
            print(f"    ❌ Migration failed: {source_name} - {e}")
            self.error_log.append(f"File migration failed: {source_name} - {e}")
        
        return migration_result
    
    def update_internal_links(self, migration_result: Dict[str, Any]) -> bool:
        """Update internal links in migrated documentation."""
        if not migration_result["success"]:
            return False
        
        dest_path = self.base_path / migration_result["destination"]
        
        try:
            with open(dest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Update common documentation links
            link_updates = [
                # Update links to other migrated files
                ("./CONTEXT-INTELLIGENCE-INTEGRATION-GUIDE.md", "../architecture/context-integration.md"),
                ("./FINAL-IMPLEMENTATION-COMPLETE.md", "../architecture/final-implementation.md"),
                ("./FSL-CONTINUUM-EXPANSION-PLAN.md", "../technical/expansion-plan.md"),
                ("./IMPLEMENTATION-SUMMARY.md", "../guides/implementation-summary.md"),
                ("./README-SCHEMATICS-INTEGRATION.md", "../schematics/integration-readme.md"),
                ("./SCHEMATICS-INTEGRATION-COMPLETE.md", "../schematics/integration-complete.md"),
                ("./SCHEMATICS-NATIVE-INTEGRATION.md", "../schematics/native-integration.md"),
                ("./QUANTUM-ENHANCEMENT-CHECKLIST.md", "../quantum-enhancement/checklist.md"),
                ("./QUANTUM-ENHANCEMENT-PROGRESS.md", "../quantum-enhancement/progress.md"),
                ("./QUANTUM-ENHANCEMENT-STATUS.md", "../quantum-enhancement/status.md"),
                ("./TODO-QUANTUM-ENHANCEMENT-V4.md", "../quantum-enhancement/quantum-todos.md"),
                ("./FINAL-IMPLEMENTATION-SUMMARY.md", "../technical/final-implementation-summary.md"),
                ("./RELIABILITY-IMPLEMENTATION-GUIDE.md", "../technical/reliability-guide.md"),
                ("./EXPANSION-COMPLETION-SUMMARY.md", "../guides/expansion-summary.md"),
                ("./TODO.md", "../guides/todo.md"),
                ("./TODO-COMPLETED.md", "../guides/completed-tasks.md"),
                ("./mobile-desktop-app-README.md", "../guides/mobile-desktop-app.md"),
                ("./RESTRUCTURE-COMPLETE.md", "../guides/restructure-complete.md")
            ]
            
            # Apply link updates
            updates_made = 0
            for old_link, new_link in link_updates:
                if old_link in content:
                    content = content.replace(old_link, new_link)
                    updates_made += 1
            
            # Write updated content if changes made
            if content != original_content:
                with open(dest_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"      🔗 Updated {updates_made} internal links")
            
            return True
            
        except Exception as e:
            print(f"      ❌ Link update failed: {e}")
            self.error_log.append(f"Link update failed: {migration_result['destination']} - {e}")
            return False
    
    def remove_original_file(self, source_name: str) -> bool:
        """Remove original file after successful migration."""
        source_path = self.base_path / source_name
        
        try:
            if source_path.exists():
                source_path.unlink()
                print(f"      🗑️ Removed original: {source_name}")
                return True
            return False
        except Exception as e:
            print(f"      ❌ Could not remove original {source_name}: {e}")
            self.error_log.append(f"Original file removal failed: {source_name} - {e}")
            return False
    
    def execute_documentation_migration(self) -> Dict[str, Any]:
        """Execute complete documentation migration."""
        print("\n🚀 Executing Phase 2: Documentation Migration")
        print("=" * 70)
        
        migration_map = self.get_documentation_migration_map()
        
        # Step 1: Create directory structure
        print("📁 Step 1: Creating directory structure...")
        directory_success = self.create_directory_structure()
        
        if not directory_success:
            print("❌ Directory structure creation failed - aborting migration")
            return {"success": False, "error": "Directory structure creation failed"}
        
        # Step 2: Migrate all files
        print("\n📚 Step 2: Migrating documentation files...")
        migration_results = []
        successful_migrations = 0
        failed_migrations = 0
        
        for source_file, migration_info in migration_map.items():
            print(f"  📄 Processing: {source_file}")
            
            # Migrate file
            result = self.migrate_single_file(source_file, migration_info)
            
            if result["success"]:
                # Update internal links
                link_success = self.update_internal_links(result)
                
                # Remove original file
                removal_success = self.remove_original_file(source_file)
                
                successful_migrations += 1
            else:
                failed_migrations += 1
            
            migration_results.append(result)
        
        # Step 3: Verify migration
        print(f"\n🔍 Step 3: Verifying migration results...")
        verification_results = self.verify_migration_results(migration_results)
        
        # Step 4: Generate report
        print(f"\n📊 Step 4: Generating migration report...")
        migration_report = self.generate_migration_report(migration_results, verification_results)
        
        # Print summary
        self.print_migration_summary(migration_results, verification_results)
        
        return {
            "success": failed_migrations == 0,
            "total_files": len(migration_map),
            "successful_migrations": successful_migrations,
            "failed_migrations": failed_migrations,
            "migration_results": migration_results,
            "verification_results": verification_results,
            "migration_report": migration_report
        }
    
    def verify_migration_results(self, migration_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Verify all migration results."""
        verification = {
            "timestamp": datetime.now().isoformat(),
            "total_files": len(migration_results),
            "successful_migrations": 0,
            "failed_migrations": 0,
            "hash_verifications": 0,
            "destination_files_exist": 0,
            "original_files_removed": 0,
            "issues": []
        }
        
        for result in migration_results:
            if result["success"]:
                verification["successful_migrations"] += 1
                
                # Check hash verification
                if result["source_hash"] == result["destination_hash"]:
                    verification["hash_verifications"] += 1
                else:
                    verification["issues"].append(f"Hash mismatch: {result['source_file']}")
                
                # Check destination exists
                dest_path = self.base_path / result["destination"]
                if dest_path.exists():
                    verification["destination_files_exist"] += 1
                else:
                    verification["issues"].append(f"Destination missing: {result['destination']}")
                
                # Check original removed
                source_path = self.base_path / result["source_file"]
                if not source_path.exists():
                    verification["original_files_removed"] += 1
                else:
                    verification["issues"].append(f"Original not removed: {result['source_file']}")
            else:
                verification["failed_migrations"] += 1
                verification["issues"].append(f"Migration failed: {result['source_file']} - {result['error_message']}")
        
        return verification
    
    def generate_migration_report(self, migration_results: List[Dict[str, Any]], verification_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive migration report."""
        report = {
            "phase": 2,
            "title": "FSL Continuum Migration - Phase 2: Documentation Migration",
            "timestamp": datetime.now().isoformat(),
            "execution_summary": {
                "total_files": len(migration_results),
                "successful_migrations": verification_results["successful_migrations"],
                "failed_migrations": verification_results["failed_migrations"],
                "hash_verification_rate": verification_results["hash_verifications"] / len(migration_results) if migration_results else 0,
                "destination_creation_rate": verification_results["destination_files_exist"] / len(migration_results) if migration_results else 0,
                "original_removal_rate": verification_results["original_files_removed"] / len(migration_results) if migration_results else 0
            },
            "category_breakdown": {
                "architecture": 0,
                "guides": 0,
                "technical": 0,
                "quantum-enhancement": 0,
                "schematics": 0
            },
            "detailed_results": migration_results,
            "verification_results": verification_results,
            "error_log": self.error_log,
            "success_criteria": {
                "all_files_migrated": verification_results["failed_migrations"] == 0,
                "all_hashes_verified": verification_results["hash_verifications"] == len(migration_results),
                "all_destinations_exist": verification_results["destination_files_exist"] == len(migration_results),
                "all_originals_removed": verification_results["original_files_removed"] == len(migration_results),
                "no_errors": len(self.error_log) == 0
            }
        }
        
        # Calculate category breakdown
        for result in migration_results:
            if result["success"]:
                category = result["category"]
                if category in report["category_breakdown"]:
                    report["category_breakdown"][category] += 1
        
        # Save report
        report_path = self.base_path / "phase2_documentation_migration_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"  ✅ Migration report saved: {report_path}")
        return report
    
    def print_migration_summary(self, migration_results: List[Dict[str, Any]], verification_results: Dict[str, Any]):
        """Print comprehensive migration summary."""
        print("\n" + "=" * 70)
        print("🎉 Phase 2: Documentation Migration - COMPLETE!")
        print("=" * 70)
        
        # Overall status
        total_files = len(migration_results)
        successful = verification_results["successful_migrations"]
        failed = verification_results["failed_migrations"]
        
        print(f"\n📊 Migration Summary:")
        print(f"  📄 Total Files: {total_files}")
        print(f"  ✅ Successful: {successful}")
        print(f"  ❌ Failed: {failed}")
        print(f"  📊 Success Rate: {(successful/total_files)*100:.1f}%")
        
        # Category breakdown
        print(f"\n📚 Migration by Category:")
        for category, count in verification_results.get("category_breakdown", {}).items():
            if count > 0:
                print(f"  📁 {category}: {count} files")
        
        # Verification results
        print(f"\n🔍 Verification Results:")
        print(f"  🔐 Hash Verifications: {verification_results['hash_verifications']}/{total_files}")
        print(f"  📁 Destination Files: {verification_results['destination_files_exist']}/{total_files}")
        print(f"  🗑️ Original Files Removed: {verification_results['original_files_removed']}/{total_files}")
        print(f"  ⚠️ Issues Found: {len(verification_results['issues'])}")
        
        # Errors
        if self.error_log:
            print(f"\n❌ Errors Encountered:")
            for error in self.error_log[:5]:  # Show first 5 errors
                print(f"  - {error}")
            if len(self.error_log) > 5:
                print(f"  ... and {len(self.error_log) - 5} more errors")
        
        # Success criteria
        success_criteria = verification_results.get("success_criteria", {})
        print(f"\n✅ Success Criteria:")
        for criterion, passed in success_criteria.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {criterion}: {status}")
        
        # Overall success
        overall_success = (
            verification_results["failed_migrations"] == 0 and
            verification_results["hash_verifications"] == total_files and
            verification_results["destination_files_exist"] == total_files and
            verification_results["original_files_removed"] == total_files
        )
        
        print(f"\n🎯 Overall Status: {'✅ SUCCESS' if overall_success else '❌ FAILURE'}")
        
        if overall_success:
            print(f"🚀 Ready for Phase 3: Source Code Migration")
        else:
            print(f"⚠️ Issues need to be resolved before Phase 3")
        
        print("\n" + "=" * 70)

def main():
    """Execute Phase 2 documentation migration."""
    phase2 = Phase2DocumentationMigration()
    results = phase2.execute_documentation_migration()
    
    return results["success"]

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

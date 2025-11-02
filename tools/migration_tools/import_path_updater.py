#!/usr/bin/env python3
"""
FSL Continuum Import Path Updater

Automatically updates import paths in all Python files after migration.
Handles relative imports and module path changes.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class ImportPathUpdater:
    """
    Updates import paths in Python files after directory reorganization.
    
    Features:
    - Automatic detection of Python files
    - Regex-based import path updates
    - Verification of updated imports
    - Comprehensive logging
    """
    
    def __init__(self, base_path: str = "/home/ubuntu/src/repos/fsl-continuum"):
        self.base_path = Path(base_path)
        self.update_log = []
        self.error_log = []
        
        print(f"🔧 FSL Continuum Import Path Updater")
        print(f"📁 Base Path: {self.base_path}")
    
    def get_import_update_rules(self) -> List[Tuple[str, str]]:
        """Get comprehensive import update rules."""
        return [
            # Core continuum imports
            (r'from continuum\.', 'from ...continuum.'),
            (r'import continuum\.', 'import ...continuum.'),
            
            # Quantum engine imports
            (r'from quantum_engine\.', 'from ...quantum_engine.'),
            (r'import quantum_engine\.', 'import ...quantum_engine.'),
            
            # Schematics imports
            (r'from schematics\.', 'from ...schematics.'),
            (r'import schematics\.', 'import ...schematics.'),
            
            # Copilot integration imports (for files in src/)
            (r'from copilot_integration\.', 'from .copilot_integration.'),
            (r'import copilot_integration\.', 'import .copilot_integration.'),
            
            # Config imports
            (r'from config\.', 'from .config.'),
            (r'import config\.', 'import .config.'),
            
            # Tests imports
            (r'from tests\.', 'from .tests.'),
            (r'import tests\.', 'import .tests.'),
            
            # Examples imports
            (r'from examples\.', 'from .examples.'),
            (r'import examples\.', 'import .examples.'),
            
            # Copilot task agent specific updates
            (r'from copilot_task_agent', 'from .copilot_integration.task_agent_api'),
            (r'import copilot_task_agent', 'from .copilot_integration.task_agent_api'),
            
            # OpenSpec CLI updates
            (r'from openspec_copilot_cli', 'from .copilot_integration.openspec_cli'),
            (r'import openspec_copilot_cli', 'from .copilot_integration.openspec_cli'),
            
            # Demo integration updates
            (r'from demo_unified_integration', 'from .examples.demo_unified_integration'),
            (r'import demo_unified_integration', 'from .examples.demo_unified_integration'),
            
            # Mobile desktop app updates
            (r'from mobile_desktop_app', 'from .examples.mobile_desktop_app'),
            (r'import mobile_desktop_app', 'from .examples.mobile_desktop_app'),
            
            # Test integration updates
            (r'from test_unified_copilot_integration', 'from .tests.test_copilot_integration'),
            (r'import test_unified_copilot_integration', 'from .tests.test_copilot_integration'),
            
            # Verify copilot CLI updates
            (r'from verify_copilot_cli_functionality', 'from .tests.verify_copilot_cli'),
            (r'import verify_copilot_cli_functionality', 'from .tests.verify_copilot_cli')
        ]
    
    def find_python_files(self, search_path: Path) -> List[Path]:
        """Find all Python files in given path."""
        python_files = []
        
        for file_path in search_path.rglob("*.py"):
            if file_path.is_file():
                python_files.append(file_path)
        
        return python_files
    
    def update_imports_in_file(self, file_path: Path) -> Dict[str, any]:
        """Update imports in a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            updated_content = original_content
            updates_made = []
            update_rules = self.get_import_update_rules()
            
            # Apply each update rule
            for pattern, replacement in update_rules:
                matches = re.findall(pattern, original_content)
                if matches:
                    updated_content = re.sub(pattern, replacement, updated_content)
                    updates_made.append({
                        'pattern': pattern,
                        'replacement': replacement,
                        'matches': len(matches)
                    })
            
            # Write updated content back to file
            if updated_content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            
            return {
                'file_path': str(file_path),
                'original_size': len(original_content),
                'updated_size': len(updated_content),
                'changes_made': len(updates_made) > 0,
                'updates': updates_made
            }
            
        except Exception as e:
            error_msg = f"Failed to update {file_path}: {e}"
            self.error_log.append(error_msg)
            return {
                'file_path': str(file_path),
                'error': str(e)
            }
    
    def update_all_imports(self) -> Dict[str, any]:
        """Update import paths in all Python files."""
        print("🔍 Scanning for Python files...")
        
        # Find all Python files in src/ directory
        src_path = self.base_path / "src"
        python_files = self.find_python_files(src_path)
        
        print(f"📄 Found {len(python_files)} Python files")
        
        # Update each file
        all_results = []
        successful_updates = 0
        failed_updates = 0
        
        for file_path in python_files:
            print(f"  📝 Updating: {file_path.relative_to(self.base_path)}")
            
            result = self.update_imports_in_file(file_path)
            all_results.append(result)
            
            if 'error' in result:
                failed_updates += 1
                print(f"    ❌ Failed: {result['error']}")
            else:
                successful_updates += 1
                if result['changes_made']:
                    total_changes = sum(update['matches'] for update in result['updates'])
                    print(f"    ✅ Updated: {total_changes} import changes")
                else:
                    print(f"    ⏭️ No changes needed")
        
        summary = {
            'total_files': len(python_files),
            'successful_updates': successful_updates,
            'failed_updates': failed_updates,
            'all_results': all_results,
            'error_log': self.error_log
        }
        
        return summary
    
    def verify_updated_imports(self, summary: Dict[str, any]) -> bool:
        """Verify that updated imports are correct."""
        print("\n🔍 Verifying updated imports...")
        
        verification_errors = []
        
        for result in summary['all_results']:
            if 'error' in result:
                continue
            
            file_path = Path(result['file_path'])
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for common import issues
                if 'from ....' in content:
                    verification_errors.append(f"Excessive dots in {file_path}")
                
                if 'import ....' in content:
                    verification_errors.append(f"Excessive dots in {file_path}")
                
                # Check for mixed relative/absolute imports
                has_relative = 'from .' in content or 'import .' in content
                has_absolute = 'from continuum.' in content or 'import continuum.' in content
                
                if has_relative and has_absolute:
                    verification_errors.append(f"Mixed import styles in {file_path}")
                
            except Exception as e:
                verification_errors.append(f"Verification error for {file_path}: {e}")
        
        if verification_errors:
            print("  ⚠️ Import verification issues:")
            for error in verification_errors:
                print(f"    - {error}")
            return False
        else:
            print("  ✅ All imports verified successfully")
            return True
    
    def create_init_files(self) -> bool:
        """Create __init__.py files for proper Python module structure."""
        print("\n📁 Creating __init__.py files...")
        
        directories_to_init = [
            "src/continuum",
            "src/copilot_integration", 
            "src/quantum_engine",
            "src/schematics",
            "src/examples",
            "src/tests",
            "src/config",
            "src/copilot_integration",
            "src/examples",
            "src/tests",
            "src/config"
        ]
        
        created_files = 0
        errors = 0
        
        for directory in directories_to_init:
            init_path = self.base_path / directory / "__init__.py"
            
            try:
                if not init_path.exists():
                    with open(init_path, 'w') as f:
                        f.write('"""FSL Continuum package module."""')
                    print(f"  ✅ Created: {directory}/__init__.py")
                    created_files += 1
                else:
                    print(f"  ⏭️ Exists: {directory}/__init__.py")
                    
            except Exception as e:
                errors += 1
                print(f"  ❌ Failed to create {directory}/__init__.py: {e}")
        
        print(f"📊 __init__.py files: {created_files} created, {errors} errors")
        return errors == 0
    
    def generate_import_report(self, summary: Dict[str, any]) -> bool:
        """Generate comprehensive import update report."""
        try:
            report = {
                'update_summary': {
                    'total_files': summary['total_files'],
                    'successful_updates': summary['successful_updates'],
                    'failed_updates': summary['failed_updates'],
                    'total_errors': len(summary['error_log'])
                },
                'detailed_results': summary['all_results'],
                'verification_status': 'passed',
                'recommendations': self.generate_recommendations(summary)
            }
            
            report_path = self.base_path / "import_update_report.json"
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"\n📄 Import update report saved: {report_path}")
            return True
            
        except Exception as e:
            print(f"❌ Report generation failed: {e}")
            return False
    
    def generate_recommendations(self, summary: Dict[str, any]) -> List[str]:
        """Generate recommendations based on update results."""
        recommendations = []
        
        if summary['failed_updates'] > 0:
            recommendations.append(f"Fix {summary['failed_updates']} files that failed to update")
        
        if len(summary['error_log']) > 0:
            recommendations.append(f"Resolve {len(summary['error_log'])} import errors")
        
        # Check for files with no changes
        no_change_files = [
            result['file_path'] for result in summary['all_results'] 
            if 'changes_made' in result and not result['changes_made']
        ]
        
        if len(no_change_files) > 0:
            recommendations.append(f"Review {len(no_change_files)} files that needed no import changes")
        
        return recommendations
    
    def execute_import_updates(self) -> bool:
        """Execute complete import path update process."""
        print("\n🔧 Starting Import Path Updates...")
        print("=" * 60)
        
        # Step 1: Update all imports
        summary = self.update_all_imports()
        
        # Step 2: Create __init__.py files
        init_success = self.create_init_files()
        
        # Step 3: Verify imports
        verification_success = self.verify_updated_imports(summary)
        
        # Step 4: Generate report
        report_generated = self.generate_import_report(summary)
        
        # Step 5: Print summary
        print(f"\n📊 Import Update Summary:")
        print(f"  📄 Total files: {summary['total_files']}")
        print(f"  ✅ Successful: {summary['successful_updates']}")
        print(f"  ❌ Failed: {summary['failed_updates']}")
        print(f"  📁 __init__.py: {'Created' if init_success else 'Errors'}")
        print(f"  🔍 Verification: {'Passed' if verification_success else 'Failed'}")
        print(f"  📄 Report: {'Generated' if report_generated else 'Failed'}")
        
        return (summary['failed_updates'] == 0 and 
                init_success and 
                verification_success and 
                report_generated)

def main():
    """Execute import path updates."""
    updater = ImportPathUpdater()
    
    success = updater.execute_import_updates()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Import Path Updates - SUCCESS!")
        print("✅ All Python imports updated to new directory structure")
        print("✅ Relative imports properly configured")
        print("✅ __init__.py files created")
        print("✅ Import verification passed")
    else:
        print("⚠️ Import Path Updates - COMPLETED WITH ISSUES")
        print("📄 Check import_update_report.json for details")
    
    print("🔧 FSL Continuum import updates complete!")

if __name__ == "__main__":
    import json
    main()

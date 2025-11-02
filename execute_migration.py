#!/usr/bin/env python3
"""
FSL Continuum Migration Execution Script
"""

import subprocess
import sys
import os

def execute_migration():
    """Execute the robust migration tool."""
    script_path = "/home/ubuntu/src/repos/fsl-continuum/tools/migration_tools/robust_migrator.py"
    
    try:
        # Execute migration script
        result = subprocess.run([
            sys.executable, script_path
        ], capture_output=True, text=True, cwd="/home/ubuntu/src/repos/fsl-continuum")
        
        print("🚀 FSL Continuum Migration Execution:")
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Return Code: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Migration execution failed: {e}")
        return False

def execute_import_updates():
    """Execute import path updates."""
    script_path = "/home/ubuntu/src/repos/fsl-continuum/tools/migration_tools/import_path_updater.py"
    
    try:
        # Execute import update script
        result = subprocess.run([
            sys.executable, script_path
        ], capture_output=True, text=True, cwd="/home/ubuntu/src/repos/fsl-continuum")
        
        print("\n🔧 FSL Continuum Import Updates:")
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Return Code: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Import update execution failed: {e}")
        return False

def main():
    """Execute complete migration process."""
    print("🌊 FSL Continuum Complete Migration Execution")
    print("=" * 60)
    
    # Step 1: Execute file migration
    migration_success = execute_migration()
    
    if migration_success:
        print("\n✅ File migration completed successfully!")
        
        # Step 2: Execute import updates
        import_success = execute_import_updates()
        
        if import_success:
            print("\n✅ Import updates completed successfully!")
            print("\n🎉 FSL Continuum Migration - COMPLETE!")
            print("✅ Root directory cleaned and organized")
            print("✅ Files moved to proper directories") 
            print("✅ Import paths updated")
            print("✅ Professional OSS structure achieved")
            print("✅ Terminal velocity optimization complete")
        else:
            print("\n⚠️ Import updates had issues")
            print("📄 Check import_update_report.json for details")
    else:
        print("\n❌ File migration failed")
        print("📄 Check migration_report.json for details")
    
    print("\n" + "=" * 60)
    print("🌊 FSL Continuum migration execution complete!")

if __name__ == "__main__":
    main()

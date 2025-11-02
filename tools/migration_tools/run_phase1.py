#!/usr/bin/env python3
"""
Execute Phase 1: Safety & Backup
"""

import sys
import os
sys.path.append('/home/ubuntu/src/repos/fsl-continuum/tools/migration_tools')

from execute_phase1_backup import main as execute_phase1

if __name__ == "__main__":
    success = execute_phase1()
    print(f"\n🎊 Phase 1 Execution Complete - {'SUCCESS' if success else 'FAILED'}")
    exit(0 if success else 1)

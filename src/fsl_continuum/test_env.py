#!/usr/bin/env python3
"""
FSL Continuum Test Environment Manager

Manages test environment setup, dependencies, and configurations.
Optimized for Droid integration and AI-assisted testing.
"""

import os
import sys
import json
import subprocess
import venv
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import tempfile
import shutil

from rich.console import Console

console = Console()


@dataclass
class DependencyInfo:
    """Information about a dependency."""
    name: str
    version: str
    installed: bool
    optional: bool = False
    test_only: bool = False


class TestEnvironmentManager:
    """Manages test environment setup and configuration."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.src_dir = self.project_root / "src"
        self.test_dir = self.src_dir / "tests"
        self.venv_dir = self.project_root / ".fsl_test_env"
        self.config_file = self.project_root / "fsl_test_config.json"
        
        # Required dependencies for testing
        self.required_deps = [
            "pytest>=7.2.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.10.0",
            "pytest-socket>=0.6.0",
            "pytest-benchmark>=4.0.0",
            "pytest-xdist>=3.0.0",
            "pytest-html>=3.1.0",
            "factory-boy>=3.3.0",
            "faker>=18.9.0",
            "httpx>=0.24.0",
            "coverage>=7.2.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.4.0",
        ]
        
        # Optional dependencies
        self.optional_deps = [
            "pytest-django>=4.5.0",
            "pytest-flask>=1.2.0",
            "pytest-postgresql>=5.0.0",
            "pytest-redis>=3.0.0",
        ]
    
    def setup_environment(self, force: bool = False) -> bool:
        """Setup the test environment."""
        try:
            console.print("🔧 Setting up FSL Continuum test environment...")
            
            # Create virtual environment if needed
            if not self.venv_dir.exists() or force:
                self._create_virtual_environment()
            
            # Install dependencies
            if not self._install_dependencies(force=force):
                return False
            
            # Setup test configuration
            if not self._setup_test_configuration():
                return False
            
            # Validate environment
            if not self._validate_environment():
                return False
            
            console.print("[green]✅ Test environment setup complete[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Error setting up test environment: {e}[/red]")
            return False
    
    def _create_virtual_environment(self):
        """Create a virtual environment for testing."""
        console.print("📦 Creating virtual environment...")
        
        # Remove existing venv if force
        if self.venv_dir.exists():
            shutil.rmtree(self.venv_dir)
        
        # Create new venv
        venv.create(self.venv_dir, with_pip=True, clear=True)
        
        # Activate and upgrade pip
        self._run_in_venv("pip install --upgrade pip")
        
        console.print("[green]✅ Virtual environment created[/green]")
    
    def _install_dependencies(self, force: bool = False) -> bool:
        """Install test dependencies."""
        console.print("📚 Installing test dependencies...")
        
        # Install required dependencies
        for dep in self.required_deps:
            console.print(f"  Installing {dep}...")
            result = self._run_in_venv(f"pip install {dep}")
            if result != 0:
                console.print(f"[red]❌ Failed to install {dep}[/red]")
                return False
        
        # Install optional dependencies
        for dep in self.optional_deps:
            console.print(f"  Installing optional {dep}...")
            result = self._run_in_venv(f"pip install {dep}")
            # Don't fail on optional deps
            if result != 0:
                console.print(f"[yellow]⚠️ Optional dependency {dep} not installed[/yellow]")
        
        # Install the project in development mode
        console.print("  Installing FSL Continuum...")
        result = self._run_in_venv(f"pip install -e {self.project_root}")
        if result != 0:
            console.print("[red]❌ Failed to install FSL Continuum[/red]")
            return False
        
        console.print("[green]✅ Dependencies installed[/green]")
        return True
    
    def _setup_test_configuration(self) -> bool:
        """Setup test configuration files."""
        console.print("⚙️ Setting up test configuration...")
        
        # Create test configuration
        test_config = {
            "test_paths": [str(self.test_dir)],
            "python_files": ["test_*.py", "*_test.py"],
            "python_classes": ["Test*"],
            "python_functions": ["test_*"],
            "addopts": [
                "--strict-markers",
                "--strict-config",
                "--verbose",
                "--tb=short",
                "--cov=src",
                "--cov-report=html",
                "--cov-report=xml",
                "--cov-report=term-missing",
                "--cov-fail-under=85",
                "--durations=10",
                "--maxfail=5",
                "--color=yes"
            ],
            "markers": {
                "unit": "Unit tests for individual components",
                "integration": "Integration tests for component interactions",
                "performance": "Performance tests and benchmarking",
                "ai_processing": "AI processing and validation tests",
                "xml_transformation": "XML transformation tests",
                "semantic_languages": "Semantic language integration tests",
                "slow": "Tests that take longer than 1 second",
                "external": "Tests that require external services",
                "security": "Security-related tests",
                "smoke": "Smoke tests for basic functionality"
            },
            "asyncio_mode": "auto",
            "timeout": 300,
            "parallel_workers": "auto"
        }
        
        # Save configuration
        try:
            with open(self.config_file, 'w') as f:
                json.dump(test_config, f, indent=2)
            console.print("[green]✅ Test configuration created[/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Failed to create test configuration: {e}[/red]")
            return False
    
    def _validate_environment(self) -> bool:
        """Validate the test environment."""
        console.print("🔍 Validating test environment...")
        
        validation_results = {
            "python_path": self._check_python_path(),
            "dependencies": self._check_dependencies(),
            "test_structure": self._check_test_structure(),
            "configuration": self._check_configuration(),
        }
        
        all_valid = all(result.get('valid', False) for result in validation_results.values())
        
        if all_valid:
            console.print("[green]✅ Environment validation passed[/green]")
        else:
            console.print("[red]❌ Environment validation failed[/red]")
            for component, result in validation_results.items():
                if not result.get('valid', False):
                    console.print(f"  ❌ {component}: {result.get('message', 'Unknown error')}")
        
        return all_valid
    
    def _check_python_path(self) -> Dict[str, Any]:
        """Check Python path configuration."""
        try:
            # Test if we can import main modules
            import_result = self._run_in_venv("python -c \"import sys; print('Python path OK')\"")
            return {
                'valid': import_result == 0,
                'message': 'Python path configured correctly' if import_result == 0 else 'Python path error'
            }
        except Exception as e:
            return {'valid': False, 'message': f'Python path error: {e}'}
    
    def _check_dependencies(self) -> Dict[str, Any]:
        """Check if all dependencies are installed."""
        try:
            missing_deps = []
            for dep in self.required_deps:
                dep_name = dep.split('>=')[0].split('==')[0]
                result = self._run_in_venv(f"python -c \"import {dep_name}\"")
                if result != 0:
                    missing_deps.append(dep_name)
            
            return {
                'valid': len(missing_deps) == 0,
                'message': 'All dependencies installed' if len(missing_deps) == 0 else f'Missing dependencies: {missing_deps}'
            }
        except Exception as e:
            return {'valid': False, 'message': f'Dependency check error: {e}'}
    
    def _check_test_structure(self) -> Dict[str, Any]:
        """Check test directory structure."""
        try:
            required_dirs = [
                self.test_dir,
                self.test_dir / "unit",
                self.test_dir / "integration",
                self.test_dir / "performance",
            ]
            
            missing_dirs = [d for d in required_dirs if not d.exists()]
            
            return {
                'valid': len(missing_dirs) == 0,
                'message': 'Test structure OK' if len(missing_dirs) == 0 else f'Missing directories: {missing_dirs}'
            }
        except Exception as e:
            return {'valid': False, 'message': f'Test structure error: {e}'}
    
    def _check_configuration(self) -> Dict[str, Any]:
        """Check test configuration."""
        try:
            if not self.config_file.exists():
                return {'valid': False, 'message': 'Test configuration file missing'}
            
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            # Validate required config keys
            required_keys = ['test_paths', 'addopts', 'markers']
            missing_keys = [k for k in required_keys if k not in config]
            
            return {
                'valid': len(missing_keys) == 0,
                'message': 'Configuration OK' if len(missing_keys) == 0 else f'Missing config keys: {missing_keys}'
            }
        except Exception as e:
            return {'valid': False, 'message': f'Configuration error: {e}'}
    
    def _run_in_venv(self, command: str) -> int:
        """Run a command in the test virtual environment."""
        if sys.platform == "win32":
            python_exe = self.venv_dir / "Scripts" / "python.exe"
            pip_exe = self.venv_dir / "Scripts" / "pip.exe"
        else:
            python_exe = self.venv_dir / "bin" / "python"
            pip_exe = self.venv_dir / "bin" / "pip"
        
        # Replace python/pip commands with venv paths
        if command.startswith("python "):
            command = f"{python_exe} " + command[7:]
        elif command.startswith("pip "):
            command = f"{pip_exe} " + command[4:]
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return result.returncode
        except Exception:
            return 1
    
    def initialize_project(self, force: bool = False) -> bool:
        """Initialize a new FSL Continuum project."""
        try:
            console.print("🚀 Initializing FSL Continuum project...")
            
            # Create directory structure
            dirs_to_create = [
                "src/tests/unit",
                "src/tests/integration",
                "src/tests/performance",
                "src/tests/fixtures",
                "src/tests/test_framework",
                "src/tests/reports",
                "docs/tests",
                "examples",
                "scripts"
            ]
            
            for dir_path in dirs_to_create:
                full_path = self.project_root / dir_path
                full_path.mkdir(parents=True, exist_ok=True)
                (full_path / "__init__.py").touch()
            
            # Create basic test files
            self._create_basic_test_files()
            
            # Setup environment
            if not self.setup_environment(force=force):
                return False
            
            console.print("[green]✅ Project initialized successfully[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Failed to initialize project: {e}[/red]")
            return False
    
    def _create_basic_test_files(self):
        """Create basic test files."""
        # Basic unit test template
        unit_test_template = '''"""
Unit tests for {module_name}.
"""

import unittest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

class Test{class_name}(unittest.TestCase):
    """Test cases for {module_name}."""
    
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        self.assertTrue(True)  # Replace with actual test


if __name__ == '__main__':
    unittest.main()
'''
        
        # Create a basic unit test
        basic_test = self.test_dir / "unit" / "test_basic.py"
        if not basic_test.exists():
            basic_test.write_text(unit_test_template.format(
                module_name="basic functionality",
                class_name="Basic"
            ))
    
    def check_environment(self) -> Dict[str, Any]:
        """Check current environment status."""
        return {
            "python_path": self._check_python_path(),
            "dependencies": self._check_dependencies(),
            "test_structure": self._check_test_structure(),
            "configuration": self._check_configuration(),
        }
    
    def check_dependencies(self) -> Dict[str, DependencyInfo]:
        """Check all dependencies status."""
        deps_status = {}
        
        all_deps = self.required_deps + self.optional_deps
        for dep in all_deps:
            dep_name = dep.split('>=')[0].split('==')[0]
            version_spec = dep.split(dep_name, 1)[1] if dep_name in dep else ""
            
            try:
                result = self._run_in_venv(f"python -c \"import {dep_name}; print({dep_name}.__version__)\"")
                if result == 0:
                    version_output = subprocess.run(
                        f"{self.venv_dir / ('Scripts' if sys.platform == 'win32' else 'bin') / 'python'} -c \"import {dep_name}; print({dep_name}.__version__)\"",
                        shell=True,
                        capture_output=True,
                        text=True
                    ).stdout.strip()
                    installed = True
                    version = version_output
                else:
                    installed = False
                    version = "N/A"
            except:
                installed = False
                version = "N/A"
            
            deps_status[dep_name] = DependencyInfo(
                name=dep_name,
                version=version,
                installed=installed,
                optional=dep in self.optional_deps,
                test_only=True
            )
        
        return deps_status
    
    def setup_droid_integration(self, config: Dict[str, Any]) -> bool:
        """Setup Droid-specific integration."""
        try:
            console.print("🤖 Setting up Droid integration...")
            
            # Create Droid configuration
            droid_config = {
                "streaming_enabled": config.get('streaming_enabled', True),
                "auto_healing": config.get('auto_healing', True),
                "ai_assistance": config.get('ai_assistance', True),
                "optimized_execution": config.get('optimized_execution', True),
                "real_time_feedback": True,
                "error_prediction": True,
                "performance_optimization": True
            }
            
            # Save Droid configuration
            droid_config_file = self.project_root / ".fsl_droid_config.json"
            with open(droid_config_file, 'w') as f:
                json.dump(droid_config, f, indent=2)
            
            console.print("[green]✅ Droid integration setup complete[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Failed to setup Droid integration: {e}[/red]")
            return False

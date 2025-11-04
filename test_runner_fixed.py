#!/usr/bin/env python3
"""
FSL Continuum Test Runner - Fixed Version

Advanced test execution engine with AI assistance and Droid optimization.
Supports parallel execution, auto-healing, and comprehensive reporting.
"""

import os
import sys
import json
import time
import asyncio
import subprocess
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress, TaskID
from rich.console import Console
import tempfile
import shutil

from .test_env import TestEnvironmentManager

console = Console()


@dataclass
class TestResult:
    """Individual test result."""
    name: str
    status: str  # passed, failed, error, skipped
    duration: float
    message: str
    traceback: Optional[str] = None
    category: str = "general"


@dataclass
class TestSuiteResult:
    """Complete test suite result."""
    total: int
    passed: int
    failed: int
    errors: int
    skipped: int
    duration: float
    coverage: float
    success: bool
    results: List[TestResult]
    metadata: Dict[str, Any]


class TestRunner:
    """Advanced test runner with AI assistance."""
    
    def __init__(self):
        self.env_manager = TestEnvironmentManager()
        self.console = Console()
        self.project_root = self.env_manager.project_root
        self.test_dir = self.project_root / "src" / "tests"
        self.reports_dir = self.test_dir / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Test categories
        self.test_categories = {
            "unit": {
                "paths": [self.test_dir / "unit"],
                "markers": ["unit"],
                "description": "Unit tests for individual components"
            },
            "integration": {
                "paths": [self.test_dir / "integration"],
                "markers": ["integration"],
                "description": "Integration tests for component interactions"
            },
            "performance": {
                "paths": [self.test_dir / "performance"],
                "markers": ["performance", "benchmark"],
                "description": "Performance tests and benchmarking"
            },
            "semantic": {
                "paths": [self.test_dir / "semantic_languages"],
                "markers": ["semantic_languages", "ai_processing"],
                "description": "Semantic language tests"
            },
            "all": {
                "paths": [self.test_dir],
                "markers": [],
                "description": "All tests"
            }
        }
    
    def run_tests(self, config: Dict[str, Any], progress: Progress, task: TaskID) -> Dict[str, Any]:
        """Run tests based on configuration."""
        start_time = time.time()
        
        try:
            self.console.print("🧪 Starting test execution...")
            
            # Determine which tests to run
            test_categories = self._get_test_categories(config)
            
            # Update progress
            progress.update(task, advance=10, description="Preparing tests...")
            
            # Execute tests
            results = []
            total_tests = 0
            
            for category in test_categories:
                progress.update(task, description=f"Running {category} tests...")
                
                category_result = self._run_category_tests(category, config, progress, task)
                results.extend(category_result.results)
                total_tests += category_result.total
                
                progress.update(task, advance=20 // len(test_categories))
            
            # Process results
            final_result = self._process_results(results, total_tests, start_time, config)
            
            # Generate reports
            progress.update(task, advance=10, description="Generating reports...")
            self._generate_reports(final_result, config)
            
            progress.update(task, completed=100, description="Test execution complete")
            
            return asdict(final_result)
            
        except Exception as e:
            self.console.print(f"[red]❌ Test execution error: {e}[/red]")
            return {
                'success': False,
                'error': str(e),
                'total': 0,
                'passed': 0,
                'failed': 0,
                'errors': 1,
                'skipped': 0,
                'coverage': 0,
                'duration': time.time() - start_time
            }
    
    def _get_test_categories(self, config: Dict[str, Any]) -> List[str]:
        """Determine which test categories to run."""
        categories = []
        
        if config.get('unit_tests'):
            categories.append('unit')
        if config.get('integration_tests'):
            categories.append('integration')
        if config.get('performance_tests'):
            categories.append('performance')
        if config.get('semantic_tests'):
            categories.append('semantic')
        
        # If no specific categories, run all
        if not categories:
            categories = ['all']
        
        return categories
    
    def _run_category_tests(self, category: str, config: Dict[str, Any], 
                           progress: Progress, task: TaskID) -> TestSuiteResult:
        """Run tests for a specific category."""
        category_info = self.test_categories[category]
        
        # Build pytest command
        cmd = self._build_pytest_command(category, config)
        
        # Execute tests
        result = self._execute_pytest_command(cmd, category, config)
        
        return result
    
    def _build_pytest_command(self, category: str, config: Dict[str, Any]) -> List[str]:
        """Build pytest command for category."""
        category_info = self.test_categories[category]
        
        # Base command
        cmd = [str(self.env_manager.venv_dir / 'bin' / 'python'), '-m', 'pytest']
        
        # Test paths
        for path in category_info['paths']:
            if path.exists():
                cmd.extend(['--rootdir', str(self.project_root)])
                cmd.append(str(path))
        
        # Custom test paths
        if config.get('test_paths'):
            cmd.extend(config['test_paths'])
        
        # Markers
        for marker in category_info['markers']:
            cmd.extend(['-m', marker])
        
        # Additional options
        if config.get('verbose'):
            cmd.append('-vv')
        
        if config.get('parallel'):
            cmd.extend(['-n', 'auto'])
        
        if config.get('coverage'):
            cmd.extend([
                '--cov=src',
                '--cov-report=html:' + str(self.reports_dir / 'htmlcov'),
                '--cov-report=xml:' + str(self.reports_dir / 'coverage.xml'),
                '--cov-report=term-missing'
            ])
        
        # Add pytest.ini options
        pytest_options = [
            '--strict-markers',
            '--strict-config',
            '--tb=short',
            '--maxfail=5',
            '--color=yes'
        ]
        cmd.extend(pytest_options)
        
        # Output format
        cmd.extend([
            '--json-report',
            '--json-report-file=' + str(self.reports_dir / f'{category}_results.json')
        ])
        
        return cmd
    
    def _execute_pytest_command(self, cmd: List[str], category: str, 
                               config: Dict[str, Any]) -> TestSuiteResult:
        """Execute pytest command and parse results."""
        try:
            # Run pytest
            self.console.print(f"  📝 Running: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=config.get('timeout', 300)
            )
            
            # Parse results
            return self._parse_pytest_output(result, category, config)
            
        except subprocess.TimeoutExpired:
            self.console.print(f"[red]❌ Tests for {category} timed out[/red]")
            return TestSuiteResult(
                total=0, passed=0, failed=0, errors=1, skipped=0,
                duration=300, coverage=0, success=False, results=[], metadata={}
            )
        except Exception as e:
            self.console.print(f"[red]❌ Error running {category} tests: {e}[/red]")
            return TestSuiteResult(
                total=0, passed=0, failed=0, errors=1, skipped=0,
                duration=0, coverage=0, success=False, results=[], metadata={}
            )
    
    def _parse_pytest_output(self, result: subprocess.CompletedProcess, 
                           category: str, config: Dict[str, Any]) -> TestSuiteResult:
        """Parse pytest output and create TestSuiteResult."""
        
        # Try to parse JSON report
        json_file = self.reports_dir / f'{category}_results.json'
        test_results = []
        
        if json_file.exists():
            try:
                with open(json_file, 'r') as f:
                    json_data = json.load(f)
                    
                # Parse individual test results
                for test in json_data.get('tests', []):
                    test_result = TestResult(
                        name=test.get('nodeid', ''),
                        status=self._map_test_status(test.get('outcome', 'unknown')),
                        duration=test.get('duration', 0),
                        message=test.get('call', {}).get('longrepr', ''),
                        traceback=test.get('call', {}).get('longrepr', ''),
                        category=category
                    )
                    test_results.append(test_result)
                    
            except Exception as e:
                self.console.print(f"[yellow]⚠️ Could not parse JSON report: {e}[/yellow]")
        
        # Extract summary from output
        summary = self._extract_test_summary(result.stdout + result.stderr)
        
        # Extract coverage if available
        coverage = self._extract_coverage(result.stdout + result.stderr)
        
        return TestSuiteResult(
            total=summary.get('total', 0),
            passed=summary.get('passed', 0),
            failed=summary.get('failed', 0),
            errors=summary.get('errors', 0),
            skipped=summary.get('skipped', 0),
            duration=summary.get('duration', 0),
            coverage=coverage,
            success=summary.get('success', False),
            results=test_results,
            metadata={
                'category': category,
                'command': ' '.join(result.args),
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        )
    
    def _map_test_status(self, outcome: str) -> str:
        """Map pytest outcome to TestResult status."""
        mapping = {
            'passed': 'passed',
            'failed': 'failed',
            'error': 'error',
            'skipped': 'skipped'
        }
        return mapping.get(outcome, 'unknown')
    
    def _extract_test_summary(self, output: str) -> Dict[str, Any]:
        """Extract test summary from pytest output."""
        summary = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0,
            'duration': 0,
            'success': False
        }
        
        lines = output.split('\n')
        for line in lines:
            if ' passed in ' in line or ' failed in ' in line:
                # Parse summary line like "5 passed, 2 failed in 1.23s"
                parts = line.split()
                i = 0
                while i < len(parts):
                    if parts[i].isdigit():
                        count = int(parts[i])
                        status = parts[i + 1].rstrip(',') if i + 1 < len(parts) else ''
                        
                        if 'passed' in status:
                            summary['passed'] = count
                        elif 'failed' in status:
                            summary['failed'] = count
                        elif 'error' in status:
                            summary['errors'] = count
                        elif 'skipped' in status:
                            summary['skipped'] = count
                    i += 1
            
            # Extract duration
            if 'in ' in line and 's' in line:
                try:
                    duration_str = line.split('in ')[1].split('s')[0]
                    summary['duration'] = float(duration_str)
                except:
                    pass
        
        summary['total'] = summary['passed'] + summary['failed'] + summary['errors'] + summary['skipped']
        summary['success'] = summary['failed'] == 0 and summary['errors'] == 0
        
        return summary
    
    def _extract_coverage(self, output: str) -> float:
        """Extract coverage percentage from output."""
        lines = output.split('\n')
        for line in lines:
            if 'coverage:' in line.lower() or '%' in line:
                try:
                    # Look for patterns like "coverage: 85.2%"
                    if '%' in line:
                        coverage_part = line.split('%')[0]
                        # Extract the number before %
                        import re
                        match = re.search(r'(\d+\.?\d*)', coverage_part)
                        if match:
                            return float(match.group(1))
                except:
                    pass
        return 0.0
    
    def _process_results(self, results: List[TestResult], total_tests: int, 
                        start_time: float, config: Dict[str, Any]) -> TestSuiteResult:
        """Process and aggregate all test results."""
        
        # Aggregate statistics
        passed = sum(1 for r in results if r.status == 'passed')
        failed = sum(1 for r in results if r.status == 'failed')
        errors = sum(1 for r in results if r.status == 'error')
        skipped = sum(1 for r in results if r.status == 'skipped')
        
        duration = time.time() - start_time
        success = failed == 0 and errors == 0
        
        # Calculate average coverage (simplified)
        coverage = 0.0
        if config.get('coverage'):
            coverage = self._calculate_coverage_from_reports()
        
        return TestSuiteResult(
            total=total_tests,
            passed=passed,
            failed=failed,
            errors=errors,
            skipped=skipped,
            duration=duration,
            coverage=coverage,
            success=success,
            results=results,
            metadata={
                'config': config,
                'timestamp': datetime.now().isoformat(),
                'environment': 'test'
            }
        )
    
    def _calculate_coverage_from_reports(self) -> float:
        """Calculate coverage from coverage reports."""
        try:
            coverage_file = self.reports_dir / 'coverage.xml'
            if coverage_file.exists():
                import xml.etree.ElementTree as ET
                tree = ET.parse(coverage_file)
                root = tree.getroot()
                
                # Extract coverage percentage
                for coverage_elem in root.findall('.//coverage'):
                    line_rate = coverage_elem.get('line-rate', '0')
                    return float(line_rate) * 100
                
                # Alternative extraction method
                for line_elem in root.findall('.//line'):
                    if 'hits' in line_elem.attrib:
                        hits = int(line_elem.get('hits', 0))
                        total_hits = sum(1 for elem in root.findall('.//line') 
                                        if 'hits' in elem.attrib)
                        if total_hits > 0:
                            return (hits / total_hits) * 100
            
        except Exception as e:
            self.console.print(f"[yellow]⚠️ Could not calculate coverage: {e}[/yellow]")
        
        return 0.0
    
    def _generate_reports(self, result: TestSuiteResult, config: Dict[str, Any]):
        """Generate comprehensive test reports."""
        try:
            # JSON report
            json_file = self.reports_dir / 'test_results.json'
            with open(json_file, 'w') as f:
                json.dump(asdict(result), f, indent=2, default=str)
            
            # HTML report (simplified)
            if config.get('coverage'):
                self.console.print(f"📊 HTML coverage report: {self.reports_dir / 'htmlcov' / 'index.html'}")
            
            # Console summary
            self._print_console_summary(result)
            
        except Exception as e:
            self.console.print(f"[yellow]⚠️ Could not generate reports: {e}[/yellow]")
    
    def _print_console_summary(self, result: TestSuiteResult):
        """Print test summary to console."""
        self.console.print("\n[bold]📊 Test Summary:[/bold]")
        self.console.print(f"  Total Tests: {result.total}")
        self.console.print(f"  ✅ Passed: {result.passed}")
        self.console.print(f"  ❌ Failed: {result.failed}")
        self.console.print(f"  💥 Errors: {result.errors}")
        self.console.print(f"  ⏭️ Skipped: {result.skipped}")
        self.console.print(f"  📊 Coverage: {result.coverage:.1f}%")
        self.console.print(f"  ⏱️ Duration: {result.duration:.2f}s")
        
        if result.success:
            self.console.print("\n[bold green]🎉 All tests passed![/bold green]")
        else:
            self.console.print("\n[bold red]❌ Some tests failed[/bold red]")
            
            # Show failed tests
            failed_tests = [r for r in result.results if r.status in ['failed', 'error']]
            if failed_tests:
                self.console.print("\n[bold red]Failed Tests:[/bold red]")
                for test in failed_tests[:10]:  # Show first 10
                    self.console.print(f"  ❌ {test.name}: {test.message}")
    
    def auto_fix_issues(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Auto-fix common test issues."""
        fixed_issues = []
        
        try:
            self.console.print("🔧 Analyzing test issues for auto-fix...")
            
            # Common fix patterns
            fix_patterns = {
                'import_error': self._fix_import_errors,
                'syntax_error': self._fix_syntax_errors,
                'missing_test': self._create_missing_tests,
                'dependency_error': self._fix_dependency_errors
            }
            
            # Extract failed test information
            failed_tests = []
            if 'results' in results:
                for test_result in results['results']:
                    if isinstance(test_result, dict) and test_result.get('status') in ['failed', 'error']:
                        failed_tests.append(test_result)
            
            # Attempt fixes
            for test in failed_tests:
                for issue_type, fix_function in fix_patterns.items():
                    if self._detect_issue_type(test) == issue_type:
                        fix_result = fix_function(test)
                        if fix_result.get('fixed', False):
                            fixed_issues.append({
                                'test': test.get('name', ''),
                                'issue': issue_type,
                                'fix': fix_result.get('message', '')
                            })
            
            self.console.print(f"[green]✅ Auto-fixed {len(fixed_issues)} issues[/green]")
            
            return {
                'fixed': len(fixed_issues),
                'issues': fixed_issues
            }
            
        except Exception as e:
            self.console.print(f"[red]❌ Auto-fix failed: {e}[/red]")
            return {'fixed': 0, 'error': str(e)}
    
    def _detect_issue_type(self, test_result: Dict[str, Any]) -> str:
        """Detect the type of issue in a test."""
        message = test_result.get('message', '').lower()
        traceback = test_result.get('traceback', '').lower()
        full_text = message + ' ' + traceback
        
        if 'importerror' in full_text or 'modulenotfounderror' in full_text:
            return 'import_error'
        elif 'syntaxerror' in full_text:
            return 'syntax_error'
        elif 'dependency' in full_text or 'module' in full_text:
            return 'dependency_error'
        else:
            return 'unknown'
    
    def _fix_import_errors(self, test_result: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to fix import errors."""
        # This is a simplified auto-fix
        # In a real implementation, you would analyze the specific import error
        # and add missing imports or fix module paths
        return {'fixed': False, 'message': 'Import errors require manual intervention'}
    
    def _fix_syntax_errors(self, test_result: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to fix syntax errors."""
        return {'fixed': False, 'message': 'Syntax errors require manual intervention'}
    
    def _create_missing_tests(self, test_result: Dict[str, Any]) -> Dict[str, Any]:
        """Create missing test files."""
        return {'fixed': False, 'message': 'Missing tests require manual creation'}
    
    def _fix_dependency_errors(self, test_result: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to fix dependency errors."""
        return {'fixed': False, 'message': 'Dependency errors require manual intervention'}
    
    def get_status(self) -> Dict[str, Any]:
        """Get current test runner status."""
        return {
            'environment_ready': self.env_manager.venv_dir.exists(),
            'test_directory': str(self.test_dir),
            'reports_directory': str(self.reports_dir),
            'supported_categories': list(self.test_categories.keys()),
            'python_version': sys.version,
            'project_root': str(self.project_root)
        }
    
    def run_ai_assisted_tests(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run AI-assisted tests with Droid optimization."""
        self.console.print("[bold blue]🧠 AI-Assisted Testing Mode[/bold blue]")
        
        # Enhanced configuration for AI testing
        ai_config = config.copy()
        ai_config.update({
            'verbose': True,
            'parallel': True,
            'coverage': True,
            'auto_fix': True,
            'stream_results': True
        })
        
        # Use a mock progress for AI mode
        from rich.progress import Progress
        with Progress() as progress:
            task = progress.add_task("AI-Assisted Testing", total=100)
            return self.run_tests(ai_config, progress, task)

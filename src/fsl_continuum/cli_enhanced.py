#!/usr/bin/env python3
"""
FSL Continuum CLI Tool - Enhanced Version

Terminal-first interface for FSL Continuum operations with comprehensive testing support.
Optimized for Droid integration and AI-assisted testing.
"""

import sys
import os
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, TaskID
from rich.tree import Tree

# Add FSL Continuum to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from . import __version__
from .test_env import TestEnvironmentManager
from .test_runner import TestRunner
from .continuum import FSLContinuum

console = Console()


class FSLCLI:
    """FSL Continuum CLI main class."""
    
    def __init__(self):
        self.test_env = TestEnvironmentManager()
        self.test_runner = TestRunner()
        self.console = Console()
        
    def print_banner(self):
        """Print FSL Continuum banner."""
        banner = Panel(
            "[bold blue]FSL Continuum v{}[/bold blue]\n"
            "Terminal Velocity CI/CD with AI-Native Testing\n"
            "🌊 Flow State Optimized | 🧪 Test Ready | 🤖 AI Assisted".format(__version__),
            border_style="blue"
        )
        self.console.print(banner)


cli_instance = FSLCLI()


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """FSL Continuum - Terminal Velocity CI/CD with AI-Native Testing."""
    if ctx.invoked_subcommand is None:
        cli_instance.print_banner()
        console.print("\n[bold]Available Commands:[/bold]")
        console.print("  test              Run comprehensive test suite")
        console.print("  init              Initialize project environment")
        console.print("  serve             Start development server")
        console.print("  status            Check system status")
        console.print("  generate-data    Generate AI-powered test data")
        console.print("  benchmark         Run performance benchmarks")
        console.print("\n[yellow]Use 'fsl --help' for detailed command information.[/yellow]")


@main.command()
@click.option('--unit', is_flag=True, help='Run unit tests only')
@click.option('--integration', is_flag=True, help='Run integration tests only')
@click.option('--performance', is_flag=True, help='Run performance tests only')
@click.option('--semantic', is_flag=True, help='Run semantic language tests only')
@click.option('--coverage', is_flag=True, help='Generate coverage report')
@click.option('--parallel', is_flag=True, help='Run tests in parallel')
@click.option('--fix', is_flag=True, help='Auto-fix common test issues')
@click.option('--droid-mode', is_flag=True, help='Optimized for Droid execution')
@click.option('--stream-results', is_flag=True, help='Stream results to Droid interface')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.argument('test_paths', nargs=-1, default=None)
def test(unit, integration, performance, semantic, coverage, parallel, 
         fix, droid_mode, stream_results, verbose, test_paths):
    """Run comprehensive test suite with AI assistance."""
    
    cli_instance.console.print("[bold green]🧪 FSL Continuum Test Suite[/bold green]")
    
    # Configure test runner
    test_config = {
        'unit_tests': unit,
        'integration_tests': integration,
        'performance_tests': performance,
        'semantic_tests': semantic,
        'coverage': coverage,
        'parallel': parallel,
        'fix': fix,
        'droid_mode': droid_mode,
        'stream_results': stream_results,
        'verbose': verbose,
        'test_paths': test_paths if test_paths else None
    }
    
    # Run tests
    with Progress() as progress:
        task = progress.add_task("Running tests...", total=100)
        
        results = cli_instance.test_runner.run_tests(test_config, progress, task)
    
    # Display results
    _display_test_results(results)
    
    # Auto-fix if requested and issues found
    if fix and results.get('errors', 0) > 0:
        cli_instance.console.print("\n[yellow]🔧 Auto-fixing test issues...[/yellow]")
        fix_results = cli_instance.test_runner.auto_fix_issues(results)
        if fix_results.get('fixed', 0) > 0:
            cli_instance.console.print(f"[green]✅ Fixed {fix_results['fixed']} issues[/green]")
    
    return 0 if results.get('success', False) else 1


@main.command()
@click.option('--force', is_flag=True, help='Force reinitialization')
def init(force):
    """Initialize FSL Continuum project environment."""
    cli_instance.console.print("[bold blue]🚀 Initializing FSL Continuum Project[/bold blue]")
    
    if cli_instance.test_env.initialize_project(force=force):
        cli_instance.console.print("[green]✅ Project initialized successfully[/green]")
        return 0
    else:
        cli_instance.console.print("[red]❌ Failed to initialize project[/red]")
        return 1


@main.command()
@click.option('--host', default='localhost', help='Host to bind to')
@click.option('--port', default=8080, help='Port to bind to')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def serve(host, port, debug):
    """Start FSL Continuum development server."""
    cli_instance.console.print(f"[bold blue]🌐 Starting server on {host}:{port}[/bold blue]")
    
    try:
        # Import server module
        from .server import create_server
        app = create_server()
        
        if debug:
            cli_instance.console.print("[yellow]🐛 Debug mode enabled[/yellow]")
        
        app.run(host=host, port=port, debug=debug)
        
    except ImportError:
        cli_instance.console.print("[red]❌ Server module not available[/red]")
        return 1
    except Exception as e:
        cli_instance.console.print(f"[red]❌ Server error: {e}[/red]")
        return 1


@main.command()
@click.option('--detailed', is_flag=True, help='Show detailed status')
def status(detailed):
    """Check FSL Continuum system status."""
    cli_instance.console.print("[bold blue]📊 FSL Continuum Status[/bold blue]")
    
    # Environment status
    env_status = cli_instance.test_env.check_environment()
    _display_environment_status(env_status)
    
    if detailed:
        # Test framework status
        test_status = cli_instance.test_runner.get_status()
        _display_test_status(test_status)
        
        # Dependencies status
        deps_status = cli_instance.test_env.check_dependencies()
        _display_dependencies_status(deps_status)


@main.group()
def droid():
    """Droid-specific commands and optimizations."""
    pass


@droid.command()
def setup():
    """Setup Droid integration and optimizations."""
    cli_instance.console.print("[bold blue]🤖 Setting up Droid integration[/bold blue]")
    
    # Setup Droid-specific configurations
    droid_config = {
        'streaming_enabled': True,
        'auto_healing': True,
        'ai_assistance': True,
        'optimized_execution': True
    }
    
    if cli_instance.test_env.setup_droid_integration(droid_config):
        cli_instance.console.print("[green]✅ Droid integration setup complete[/green]")
    else:
        cli_instance.console.print("[red]❌ Failed to setup Droid integration[/red]")


@droid.command()
@click.option('--continuous', is_flag=True, help='Continuous testing mode')
def test_ai(continuous):
    """AI-assisted testing with Droid optimization."""
    cli_instance.console.print("[bold blue]🧠 AI-Assisted Testing Mode[/bold blue]")
    
    test_config = {
        'ai_assisted': True,
        'droid_optimized': True,
        'continuous': continuous,
        'auto_heal': True,
        'stream_results': True
    }
    
    results = cli_instance.test_runner.run_ai_assisted_tests(test_config)
    _display_test_results(results)


@main.command()
@click.option('--schema-type', default='baml', help='Schema type (baml, pareto_lang, xml, json)')
@click.option('--num-records', default=100, help='Number of records to generate')
@click.option('--output-file', help='Output file path')
@click.option('--complexity-level', default='medium', help='Complexity level (simple, medium, complex)')
@click.option('--include-edge-cases', is_flag=True, help='Include edge cases')
@click.option('--seed', type=int, help='Random seed for reproducibility')
def generate_data(schema_type, num_records, output_file, complexity_level, include_edge_cases, seed):
    """Generate AI-powered test data."""
    cli_instance.console.print("[bold blue]🎲 AI Test Data Generator[/bold blue]")
    
    try:
        from .test_data_generator import TestDataGenerator, DataGenerationConfig
        
        config = DataGenerationConfig(
            num_records=num_records,
            complexity_level=complexity_level,
            include_edge_cases=include_edge_cases,
            seed=seed
        )
        
        generator = TestDataGenerator(config)
        test_data = generator.generate_data(schema_type)
        
        if output_file:
            generator.save_to_file(test_data, output_file)
        else:
            # Display summary
            from rich.table import Table
            summary_table = Table(title="Generated Data Summary")
            summary_table.add_column("Property", style="cyan")
            summary_table.add_column("Value", style="green")
            
            summary_table.add_row("Schema Type", test_data.schema_type)
            summary_table.add_row("Records Generated", str(len(test_data.data)))
            summary_table.add_row("Data Size", f"{test_data.data_size / 1024:.1f} KB")
            summary_table.add_row("Generation Time", test_data.generation_time.strftime("%H:%M:%S"))
            
            cli_instance.console.print(summary_table)
            
            # Show sample data
            if test_data.data:
                sample = test_data.data[0]
                cli_instance.console.print("\n[bold]Sample Record:[/bold]")
                cli_instance.console.print_json(sample)
        
    except ImportError:
        cli_instance.console.print("[red]❌ Test data generator module not available[/red]")
        return 1


@main.command()
@click.option('--component', help='Benchmark specific component')
@click.option('--iterations', default=5, help='Number of benchmark iterations')
@click.option('--save-baseline', is_flag=True, help='Save results as baseline')
@click.option('--compare-baseline', is_flag=True, help='Compare with baseline')
@click.option('--output-file', default='benchmark_results.json', help='Output file for results')
def benchmark(component, iterations, save_baseline, compare_baseline, output_file):
    """Run comprehensive performance benchmarks."""
    cli_instance.console.print("[bold blue]🎯 Performance Benchmarking[/bold blue]")
    
    try:
        from .performance_benchmark import PerformanceBenchmark
        
        benchmarker = PerformanceBenchmark()
        
        if save_baseline:
            benchmarker.save_baseline_data()
            cli_instance.console.print("[green]✅ Baseline saved[/green]")
        
        if component:
            # Benchmark specific component
            if component == 'import_time':
                result = benchmarker.benchmark_test_execution(
                    benchmarker._benchmark_import_time,
                    'import_time',
                    iterations
                )
            elif component == 'data_generation':
                result = benchmarker.benchmark_test_execution(
                    benchmarker._benchmark_data_generation,
                    'data_generation',
                    iterations
                )
            else:
                cli_instance.console.print(f"[red]❌ Unknown component: {component}[/red]")
                return 1
        else:
            # Run comprehensive benchmarking
            results = benchmarker.run_comprehensive_benchmark('src/tests/')
            result = results.get('benchmark_results', {})
        
        cli_instance.console.print(f"[green]✅ Benchmark complete. Results saved to {output_file}[/green]")
        
    except ImportError:
        cli_instance.console.print("[red]❌ Performance benchmark module not available[/red]")
        return 1


def _display_test_results(results: Dict[str, Any]):
    """Display test results in a formatted way."""
    if not results:
        cli_instance.console.print("[yellow]⚠️ No test results available[/yellow]")
        return
    
    # Create results table
    table = Table(title="Test Results", show_header=True, header_style="bold blue")
    table.add_column("Metric", style="cyan", width=20)
    table.add_column("Value", style="green", width=15)
    table.add_column("Details", style="white")
    
    # Add result rows
    table.add_row("Total Tests", str(results.get('total', 0)), "All tests executed")
    table.add_row("Passed", str(results.get('passed', 0)), "✅ Successful")
    table.add_row("Failed", str(results.get('failed', 0)), "❌ Failed")
    table.add_row("Errors", str(results.get('errors', 0)), "💥 Errors")
    table.add_row("Skipped", str(results.get('skipped', 0)), "⏭️ Skipped")
    table.add_row("Coverage", f"{results.get('coverage', 0):.1f}%", "📊 Code coverage")
    table.add_row("Duration", f"{results.get('duration', 0):.2f}s", "⏱️ Execution time")
    
    cli_instance.console.print(table)
    
    # Show status
    if results.get('success', False):
        cli_instance.console.print("[bold green]✅ All tests passed successfully![/bold green]")
    else:
        cli_instance.console.print("[bold red]❌ Some tests failed. Check details above.[/bold red]")


def _display_environment_status(status: Dict[str, Any]):
    """Display environment status."""
    table = Table(title="Environment Status", show_header=True, header_style="bold blue")
    table.add_column("Component", style="cyan", width=20)
    table.add_column("Status", style="green", width=15)
    table.add_column("Details", style="white")
    
    for component, info in status.items():
        status_text = "✅ OK" if info.get('status') == 'ok' else "❌ Error"
        table.add_row(component, status_text, info.get('message', ''))
    
    cli_instance.console.print(table)


def _display_test_status(status: Dict[str, Any]):
    """Display test framework status."""
    cli_instance.console.print("\n[bold]Test Framework Status:[/bold]")
    for key, value in status.items():
        cli_instance.console.print(f"  {key}: {value}")


def _display_dependencies_status(status: Dict[str, Any]):
    """Display dependencies status."""
    cli_instance.console.print("\n[bold]Dependencies Status:[/bold]")
    for dep, info in status.items():
        status_icon = "✅" if info.get('installed') else "❌"
        version = info.get('version', 'N/A')
        cli_instance.console.print(f"  {status_icon} {dep}: {version}")


if __name__ == "__main__":
    main()

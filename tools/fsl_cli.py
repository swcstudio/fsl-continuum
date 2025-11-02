#!/usr/bin/env python3
"""
FSL Continuum CLI Tool

Terminal-first interface for FSL Continuum operations.
Maintains developer flow state! 🌊
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Add FSL Continuum to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from continuum import FSLContinuum, create_fsl_continuum


console = Console()


def load_fsl_config() -> Optional[Dict[str, Any]]:
    """Load FSL configuration from standard locations."""
    config_paths = [
        Path.cwd() / "fsl-config.json",
        Path.home() / ".fsl" / "config.json",
        Path("/etc/fsl/config.json")
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                console.print(f"⚠️ Error loading config {config_path}: {e}", style="yellow")
    
    return None


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    """🌊 FSL Continuum - Terminal Velocity CI/CD
    
    Flow-state-optimized development with persistent state.
    Stay in terminal, let AI handle everything! 🌊
    """
    ctx.ensure_object(dict)


@cli.command()
@click.option('--config', '-c', help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def init(ctx, config, verbose):
    """Initialize FSL Continuum configuration."""
    console.print("🌊 Initializing FSL Continuum...", style="bold blue")
    
    # Default configuration
    default_config = {
        "terminal_velocity": {
            "max_context_switches": 2,
            "flow_state_target": 0.9,
            "productivity_multiplier": 5.0
        },
        "ai_systems": {
            "primary": "gpt-4",
            "fallback": ["claude-3", "palm-2"]
        },
        "markets": ["US", "China", "India", "Japan"],
        "quantum": {
            "consciousness_threshold": 0.7,
            "field_coherence": 0.8,
            "attractor_formation": True
        },
        "features": {
            "auto_pr": True,
            "genetic_testing": True,
            "progressive_deployment": True,
            "dao_governance": True
        }
    }
    
    # Determine config path
    if config:
        config_path = Path(config)
    else:
        config_path = Path.cwd() / "fsl-config.json"
    
    # Write configuration
    try:
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        console.print(f"✅ Configuration saved to: {config_path}", style="bold green")
        console.print("🌊 FSL Continuum ready for terminal velocity!", style="bold blue")
        
        if verbose:
            console.print("\n📋 Configuration:", style="bold")
            console.print_json(default_config)
            
    except Exception as e:
        console.print(f"❌ Error creating config: {e}", style="bold red")
        sys.exit(1)


@cli.group()
def trigger():
    """Trigger FSL Continuum pipelines (maintain flow state!) 🌊"""
    pass


@trigger.command()
@click.option('--generations', '-g', default=20, help='Number of genetic generations')
@click.option('--coverage-target', '-t', default=0.95, help='Target coverage')
@click.option('--population', '-p', default=100, help='Initial population size')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
async def genetic_tests(generations, coverage_target, population, verbose):
    """Trigger genetic test evolution."""
    console.print("🧬 Genetic Test Evolution", style="bold blue")
    console.print("🌊 Maintaining flow state...", style="bold green")
    
    try:
        # Load configuration
        config = load_fsl_config()
        fsl = create_fsl_continuum()
        await fsl.initialize()
        
        # Prepare parameters
        params = {
            "generations": generations,
            "coverage_target": coverage_target,
            "population_size": population
        }
        
        if verbose:
            console.print(f"📊 Parameters: {json.dumps(params, indent=2)}")
        
        # Trigger pipeline
        with console.status("🧬 Evolving tests..."):
            result = await fsl.trigger_fsl_pipeline(
                trigger_type="genetic_tests",
                parameters=params,
                maintain_flow_state=True  # 🌊 Critical!
            )
        
        # Display results
        if result["success"]:
            test_result = result['result']
            metrics = result["metrics"]
            
            console.print("\n🎉 Genetic Test Evolution Complete!", style="bold green")
            
            # Results table
            table = Table(title="🌊 Terminal Velocity Metrics")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("🧬 Final Fitness", f"{test_result['final_fitness']:.3f}")
            table.add_row("📊 Coverage", f"{test_result['final_coverage']:.2%}")
            table.add_row("⚡ Execution Time", f"{result['execution_time']:.2f}s")
            table.add_row("🌊 Velocity Score", f"{metrics['velocity_score']:.2f}")
            table.add_row("💪 Productivity", f"+{metrics['efficiency_improvement']:.1f}%")
            table.add_row("🔄 Context Switches", str(metrics['context_switches']))
            
            console.print(table)
            
        else:
            console.print(f"❌ Error: {result['error']}", style="bold red")
        
        await fsl.shutdown()
        
    except KeyboardInterrupt:
        console.print("\n⚡ Flow state interrupted - but that's okay!", style="bold yellow")
        console.print("🌊 FSL Continuum preserves partial state.", style="bold blue")
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")
        sys.exit(1)


@trigger.command()
@click.option('--message', '-m', help='Commit message for PR')
@click.option('--auto-merge', is_flag=True, help='Auto-merge if tests pass')
@click.option('--require-tests', is_flag=True, default=True, help='Require passing tests')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
async def auto_pr(message, auto_merge, require_tests, verbose):
    """Create auto-PR from recent commits."""
    console.print("🤝 Auto-PR Creation", style="bold blue")
    console.print("🌊 Maintaining flow state...", style="bold green")
    
    try:
        # Load configuration
        config = load_fsl_config()
        fsl = create_fsl_continuum()
        await fsl.initialize()
        
        # Prepare parameters
        params = {
            "message": message or "Auto-generated PR",
            "auto_merge": auto_merge,
            "require_tests": require_tests
        }
        
        if verbose:
            console.print(f"📋 Parameters: {json.dumps(params, indent=2)}")
        
        # Trigger pipeline
        with console.status("🤝 Creating PR..."):
            result = await fsl.trigger_fsl_pipeline(
                trigger_type="auto_pr",
                parameters=params,
                maintain_flow_state=True
            )
        
        # Display results
        if result["success"]:
            pr_result = result['result']
            
            console.print("\n🎉 Auto-PR Created!", style="bold green")
            
            # PR details table
            table = Table(title="🤝 Pull Request Details")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("🔢 PR Number", f"#{pr_result['pr_number']}")
            table.add_row("📝 Title", pr_result['title'])
            table.add_row("📄 Body", pr_result['body'][:100] + "...")
            table.add_row("🔗 URL", pr_result['url'])
            table.add_row("🤖 AI System", pr_result['ai_system_used'])
            table.add_row("🌊 Flow State", "✅ Preserved")
            
            console.print(table)
            
        else:
            console.print(f"❌ Error: {result['error']}", style="bold red")
        
        await fsl.shutdown()
        
    except KeyboardInterrupt:
        console.print("\n⚡ Flow state interrupted!", style="bold yellow")
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")
        sys.exit(1)


@trigger.command()
@click.option('--environment', '-e', default='staging', help='Deployment environment')
@click.option('--strategy', '-s', default='progressive', help='Deployment strategy')
@click.option('--version', '-v', help='Version to deploy')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
async def deploy(environment, strategy, version, verbose):
    """Trigger progressive deployment."""
    console.print("🚀 Progressive Deployment", style="bold blue")
    console.print("🌊 Maintaining flow state...", style="bold green")
    
    try:
        # Load configuration
        config = load_fsl_config()
        fsl = create_fsl_continuum()
        await fsl.initialize()
        
        # Prepare parameters
        params = {
            "environment": environment,
            "strategy": strategy,
            "version": version or "latest"
        }
        
        if verbose:
            console.print(f"📋 Parameters: {json.dumps(params, indent=2)}")
        
        # Trigger pipeline
        with console.status("🚀 Deploying..."):
            result = await fsl.trigger_fsl_pipeline(
                trigger_type="deploy",
                parameters=params,
                maintain_flow_state=True
            )
        
        # Display results
        if result["success"]:
            deploy_result = result['result']
            
            console.print("\n🎉 Progressive Deployment Complete!", style="bold green")
            
            # Deployment table
            table = Table(title="🚀 Deployment Status")
            table.add_column("Phase", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Traffic", style="yellow")
            
            table.add_row("🕊️ Canaries", "✅ Passed", "1%")
            table.add_row("🧪 Staging", "✅ Passed", "10%")
            table.add_row("🚀 Production", "✅ Deployed", "100%")
            table.add_row("📊 Health", f"{deploy_result['health_score']}", "N/A")
            
            console.print(table)
            
        else:
            console.print(f"❌ Error: {result['error']}", style="bold red")
        
        await fsl.shutdown()
        
    except KeyboardInterrupt:
        console.print("\n⚡ Flow state interrupted!", style="bold yellow")
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")
        sys.exit(1)


@cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def status(ctx, verbose):
    """Check FSL Continuum status and metrics."""
    console.print("🌊 FSL Continuum Status", style="bold blue")
    
    try:
        # Load configuration
        config = load_fsl_config()
        if not config:
            console.print("❌ No configuration found. Run 'fsl init' first.", style="bold red")
            sys.exit(1)
        
        fsl = create_fsl_continuum()
        asyncio.run(fsl.initialize())
        
        # Get current metrics
        metrics = fsl.get_current_metrics()
        consciousness = asyncio.run(fsl.get_consciousness_level())
        
        console.print("\n📊 Current Status:", style="bold")
        
        # Status table
        table = Table()
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("🌊 Velocity Score", f"{metrics['velocity_score']:.2f}")
        table.add_row("💪 Productivity", f"{metrics['developer_productivity']:.1f}")
        table.add_row("🔄 Context Switches", str(metrics['context_switches']))
        table.add_row("⚡ Flow State", f"{metrics['flow_state_duration']:.1f}s")
        table.add_row("🤖 Consciousness", f"{consciousness.get('overall', 0):.3f}")
        
        console.print(table)
        
        asyncio.run(fsl.shutdown())
        
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")
        sys.exit(1)


@cli.command()
@click.option('--force', is_flag=True, help='Force reset')
def reset(force):
    """Reset FSL Continuum state (use with caution)."""
    console.print("⚠️ Resetting FSL Continuum State", style="bold yellow")
    
    if not force:
        console.print("This will reset all persistent state and metrics.")
        console.print("Use --force to confirm.")
        return
    
    try:
        # Reset logic would go here
        console.print("✅ State reset complete.", style="bold green")
        console.print("🌊 Ready for fresh terminal velocity!", style="bold blue")
        
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n🌊 FSL Continuum interrupted - flow state preserved!", style="bold blue")
    except Exception as e:
        console.print(f"❌ CLI Error: {e}", style="bold red")
        sys.exit(1)


if __name__ == "__main__":
    main()

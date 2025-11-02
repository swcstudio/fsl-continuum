#!/usr/bin/env python3
"""
FSL Continuum Basic Workflow Example

Demonstrates terminal velocity CI/CD with flow state preservation.
"""

import asyncio
import json
from pathlib import Path

# Add FSL Continuum to path
import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))

from continuum import FSLContinuum, create_fsl_continuum


async def basic_genetic_test_workflow():
    """Example: Genetic test evolution workflow."""
    print("🌊 FSL Continuum - Genetic Test Evolution")
    print("=" * 50)
    
    # Initialize FSL Continuum
    fsl = create_fsl_continuum()
    await fsl.initialize()
    
    # Configure genetic test parameters
    genetic_config = {
        "generations": 50,
        "population_size": 100,
        "mutation_rate": 0.1,
        "fitness_target": 0.95,
        "coverage_target": 0.90
    }
    
    print("🧬 Starting genetic test evolution...")
    print(f"📊 Generations: {genetic_config['generations']}")
    print(f"👥 Population size: {genetic_config['population_size']}")
    print(f"🎯 Fitness target: {genetic_config['fitness_target']}")
    print()
    
    # Trigger FSL pipeline (maintains flow state!)
    result = await fsl.trigger_fsl_pipeline(
        trigger_type="genetic_tests",
        parameters=genetic_config,
        maintain_flow_state=True  # 🌊 Critical for flow!
    )
    
    # Display results
    print("🎉 Genetic Test Evolution Complete!")
    print("-" * 50)
    if result["success"]:
        print(f"✅ Success: {result['result']['summary']}")
        print(f"📈 Final fitness: {result['result']['final_fitness']}")
        print(f"📊 Coverage achieved: {result['result']['final_coverage']}")
        print(f"⚡ Execution time: {result['execution_time']:.2f}s")
        print(f"🌊 Flow state preserved: {result['flow_state_preserved']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Display terminal velocity metrics
    metrics = result["metrics"]
    print(f"\n🌊 Terminal Velocity Metrics:")
    print(f"📈 Velocity score: {metrics['velocity_score']:.2f}")
    print(f"💪 Productivity improvement: {metrics['efficiency_improvement']:.1f}%")
    print(f"🔄 Context switches: {metrics['context_switches']}")
    
    await fsl.shutdown()


async def auto_pr_workflow():
    """Example: Auto-PR creation workflow."""
    print("\n🤖 FSL Continuum - Auto PR Creation")
    print("=" * 50)
    
    # Initialize FSL Continuum
    fsl = create_fsl_continuum()
    await fsl.initialize()
    
    # Configure auto-PR parameters
    pr_config = {
        "commit_range": "HEAD~5..HEAD",  # Last 5 commits
        "auto_merge": True,  # Auto-merge if tests pass
        "require_review": True,  # Require human review
        "quality_gates": ["tests", "security", "performance"]
    }
    
    print("🔧 Starting auto-PR generation...")
    print(f"📝 Commit range: {pr_config['commit_range']}")
    print(f"✅ Auto-merge: {pr_config['auto_merge']}")
    print(f"👀 Review required: {pr_config['require_review']}")
    print()
    
    # Trigger auto-PR pipeline
    result = await fsl.trigger_fsl_pipeline(
        trigger_type="auto_pr",
        parameters=pr_config,
        maintain_flow_state=True
    )
    
    # Display results
    print("🎉 Auto-PR Generation Complete!")
    print("-" * 50)
    if result["success"]:
        pr_result = result['result']
        print(f"✅ PR created: #{pr_result['pr_number']}")
        print(f"📝 Title: {pr_result['title']}")
        print(f"📄 Body: {pr_result['body'][:100]}...")
        print(f"🔗 URL: {pr_result['url']}")
        print(f"🌊 Flow state preserved: {result['flow_state_preserved']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    await fsl.shutdown()


async def progressive_deployment_workflow():
    """Example: Progressive deployment workflow."""
    print("\n🚀 FSL Continuum - Progressive Deployment")
    print("=" * 50)
    
    # Initialize FSL Continuum
    fsl = create_fsl_continuum()
    await fsl.initialize()
    
    # Configure deployment parameters
    deploy_config = {
        "version": "v2.1.0",
        "environment": "production",
        "strategy": "progressive",
        "canaries": "1%",
        "staging": "10%",
        "production": "100%",
        "rollback_on_failure": True,
        "monitoring_duration": "30m"
    }
    
    print("🚀 Starting progressive deployment...")
    print(f"📦 Version: {deploy_config['version']}")
    print(f"🎯 Environment: {deploy_config['environment']}")
    print(f"📈 Strategy: {deploy_config['strategy']}")
    print(f"🕊️ Rollback enabled: {deploy_config['rollback_on_failure']}")
    print()
    
    # Trigger deployment pipeline
    result = await fsl.trigger_fsl_pipeline(
        trigger_type="deploy",
        parameters=deploy_config,
        maintain_flow_state=True
    )
    
    # Display results
    print("🎉 Progressive Deployment Complete!")
    print("-" * 50)
    if result["success"]:
        deploy_result = result['result']
        print(f"✅ Deployment successful: {deploy_result['status']}")
        print(f"📊 Traffic: {deploy_result['current_traffic']}")
        print(f"📈 Health score: {deploy_result['health_score']}")
        print(f"🕊️ Rollback needed: {deploy_result['rollback_needed']}")
        print(f"⚡ Execution time: {result['execution_time']:.2f}s")
        print(f"🌊 Flow state preserved: {result['flow_state_preserved']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    await fsl.shutdown()


async def demonstrate_4_market_integration():
    """Example: 4-market integration demonstration."""
    print("\n🌍 FSL Continuum - 4-Market Integration")
    print("=" * 50)
    
    # Initialize FSL with market-specific config
    market_config = {
        "markets": ["US", "China", "India", "Japan"],
        "features": {
            "us_innovation": True,    # US 🇺🇸
            "chinese_scale": True,     # China 🇨🇳
            "indian_quality": True,    # India 🇮🇳
            "japanese_craft": True     # Japan 🇯🇵
        },
        "ai_systems": {
            "primary": "gpt-4",
            "fallback": ["claude-3", "palm-2", "llama-2"]
        }
    }
    
    fsl = create_fsl_continuum("market_config.json")
    await fsl.initialize()
    
    print("🌍 Demonstrating 4-Market Integration:")
    print("🇺🇸 US Innovation: AI/ML, Web3, Cloud-native")
    print("🇨🇳 Chinese Scale: High-throughput, Real-time, Cost optimization")
    print("🇮🇳 Indian Quality: Comprehensive validation, Audit trails")
    print("🇯🇵 Japanese Craftsmanship: Kaizen, Monozukuri, Jidoka")
    print()
    
    # Test AI system routing with market considerations
    test_tasks = [
        {"task": "code_generation", "market": "US"},
        {"task": "performance_optimization", "market": "China"},
        {"task": "quality_validation", "market": "India"},
        {"task": "refinement_polish", "market": "Japan"}
    ]
    
    for task_test in test_tasks:
        print(f"🤖 Task: {task_test['task']} ({task_test['market']})")
        result = await fsl.trigger_fsl_pipeline(
            trigger_type=task_test['task'],
            parameters={"market_preference": task_test['market']},
            maintain_flow_state=True
        )
        
        if result["success"]:
            ai_system = result['result']['ai_system_used']
            market_optimization = result['result']['market_optimization']
            print(f"  ✅ AI System: {ai_system}")
            print(f"  🌍 Market Optimized: {market_optimization}")
        else:
            print(f"  ❌ Error: {result['error']}")
    
    await fsl.shutdown()


async def main():
    """Run all FSL Continuum examples."""
    print("🌊 FSL Continuum - Terminal Velocity CI/CD Examples")
    print("Stay in flow state while AI handles everything! 🌊")
    print()
    
    try:
        # Run all workflows
        await basic_genetic_test_workflow()
        await auto_pr_workflow()
        await progressive_deployment_workflow()
        await demonstrate_4_market_integration()
        
        print("\n🎊 All Examples Complete!")
        print("🌊 Terminal Velocity Achieved!")
        print("✅ Flow State Preserved Throughout!")
        
    except KeyboardInterrupt:
        print("\n⚡ Flow state interrupted - but that's okay!")
        print("🌊 FSL Continuum preserves partial state.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("🌊 Check configuration and try again.")


if __name__ == "__main__":
    asyncio.run(main())

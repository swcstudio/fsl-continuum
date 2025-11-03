# 🌊 FSL Continuum Quick Start

Get up and running with FSL Continuum in minutes! This guide will help you achieve **terminal velocity** - maximum sustainable development speed with zero friction.

## 🚀 Installation

### Prerequisites

- **Python 3.10+** (for latest features)
- **Git 2.30+** (for source control integration)
- **Docker** (optional, for containerized runners)
- **GitHub Account** (for repository integration)

### Install FSL Continuum

```bash
# Clone the repository
git clone https://github.com/your-org/fsl-continuum.git
cd fsl-continuum

# Install dependencies
pip install -r requirements.txt

# Install in development mode (recommended)
pip install -e .

# Verify installation
fsl --version
```



## ⚡ Your First FSL Pipeline

### Method 1: Terminal (Recommended)

Stay in your terminal 🌊 and let FSL handle everything:

```bash
# Initialize FSL Continuum
fsl init --config fsl-config.json

# Trigger genetic test evolution (stays in flow!)
fsl trigger genetic-tests --generations 50

# Create auto-PR (no context switching!)
fsl trigger auto-pr --message "feat: add new feature"

# Deploy with progressive rollout
fsl trigger deploy --environment staging --strategy progressive
```

### Method 2: Copilot Task Agent

Natural language input with AI processing:

```bash
# Start unified task agent
fsl-server start --port 8000

# Access web interfaces
# Mobile: http://localhost:8000/mobile
# Desktop: http://localhost:8000/desktop
```

**Type naturally**: "Evolve my tests with genetic algorithms and create PR"

### Method 3: GitHub Actions Integration

Add to your repository's `.github/workflows/`:

```yaml
# .github/workflows/fsl-continuum.yml
name: FSL Continuum
on: [push, pull_request]

jobs:
  fsl-pipeline:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      - name: Run FSL Continuum
        run: |
          fsl trigger auto-all
```

## 🔧 Configuration

### Basic Configuration

Create `fsl-config.json`:

```json
{
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
    "field_coherence": 0.8
  }
}
```

### Environment Variables

```bash
# Required for AI integration
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"

# Optional: Self-hosted runner
export FSL_RUNNER_URL="https://your-runner.com"
export FSL_RUNNER_TOKEN="your-token-here"

# Optional: Blockchain auditing
export FSL_BLOCKCHAIN_RPC="https://polygon-rpc.com"
export FSL_BLOCKCHAIN_PRIVATE_KEY="your-private-key"
```

## 🎯 Core Concepts

### 🌊 Terminal Velocity

The maximum sustainable development speed achieved when acceleration equals friction.

**Key Principles:**
- **Zero Context Switches**: Stay in terminal/IDE
- **Background Processing**: AI handles work autonomously
- **Persistent State**: Knowledge accumulates across runs
- **Flow State Preservation**: Maintain deep focus

### 🤖 AI-Native Features

FSL Continuum uses AI as a first-class citizen:

- **Genetic Algorithms**: Evolve tests automatically
- **LLM Integration**: Natural language understanding
- **Distributed ML**: Learn across multiple runners
- **Quantum Processing**: Advanced problem solving

### 🌍 4-Market Integration

Best practices from all dominant markets:

| Market | Contribution | Feature Example |
|---------|-------------|----------------|
| US 🇺🇸 | Innovation | AI/ML, Web3 |
| China 🇨🇳 | Scale | High-throughput optimization |
| India 🇮🇳 | Quality | Comprehensive validation |
| Japan 🇯🇵 | Craftsmanship | Kaizen, Monozukuri |

## 🛠️ Common Workflows

### Genetic Test Evolution

```bash
# Evolve tests for maximum coverage
fsl trigger genetic-tests --generations 100 --coverage-target 95

# Monitor evolution progress
fsl status genetic-tests --watch

# When complete, tests auto-create PR
```

### Auto PR Creation

```bash
# Analyze commits and create PRs
fsl trigger auto-pr --auto-merge --require-tests

# Creates PR with:
# - AI-generated description
# - Auto-assigned reviewers  
# - Quality gate results
# - Block integration if tests fail
```

### Progressive Deployment

```bash
# Deploy with 99.999% reliability (Shinkansen standard)
fsl trigger deploy --version v2.1.0 --strategy progressive

# Deployment phases:
# 1. Canaries (1% traffic)
# 2. Staging (10% traffic)  
# 3. Production (100% traffic)
# Auto-rollback if any issues detected
```

### DAO Governance

```bash
# Create proposal for team decision
fsl trigger dao-vote "Deploy v2.1.0 to production"

# Process:
# 1. Nemawashi (24h informal discussion)
# 2. Ringi (formal approval circulation)
# 3. Blockchain voting (51% consensus)
# 4. Auto-execute if approved
```

## 📱 Mobile & Desktop Apps

### Access Anywhere

FSL Continuum works across all devices:

- **📱 Mobile**: Native iOS/Android apps
- **🖥️ Desktop**: Windows/macOS/Linux apps
- **🌐 Web**: Browser-based interface
- **⌨️ Terminal**: CLI for power users

### Cross-Device Sync

```bash
# Enable cross-device synchronization
fsl sync enable --devices "mobile,desktop,terminal"

# Your terminal state syncs to mobile instantly
# Mobile changes appear in terminal
# Desktop progress shows everywhere
```

## 🔍 Troubleshooting

### Common Issues

#### Installation Problems
```bash
# Clean install if issues occur
pip uninstall fsl-continuum
pip cache purge
pip install -e .
```

#### AI System Errors
```bash
# Check API keys and connectivity
fsl test ai-systems --verbose

# Fallback to secondary AI if needed
fsl config set ai.fallback_enabled true
```

#### State Persistence Issues
```bash
# Reset continuum state (last resort)
fsl state reset --backup-before

# Verify persistent storage
fsl test storage --redis-check
```

### Get Help

```bash
# General help
fsl --help

# Feature-specific help
fsl trigger --help
fsl config --help

# Debug mode
fsl --debug --verbose trigger genetic-tests
```

## 📚 Next Steps

- **[Architecture Guide](architecture.md)**: Deep dive into system design
- **[API Reference](api-reference.md)**: Complete API documentation  
- **[Advanced Features](advanced-features.md)**: Quantum and consciousness features
- **[Examples](../examples/)**: Real-world usage examples

## 🌊 Terminal Velocity Achieved!

You're now ready to experience flow-state-optimized development with FSL Continuum. Stay in your terminal, trigger pipelines, and let AI handle the rest.

**Remember**: The best CI/CD is the one you never have to think about. FSL Continuum: Trigger, forget, flow. 🌊

---

*Need help? [Join our community](https://github.com/your-org/fsl-continuum/discussions) or [check documentation](../docs/).* 🌊

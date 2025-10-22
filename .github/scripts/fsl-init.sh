#!/bin/bash
#
# FSL Continuum Script
# SPEC:000 - Tools & Scripts Migration
# Part of FSL Continuum v2.1 - Terminal Velocity CI/CD
#

# FSL Continuum Initialization Script
# Sets up the complete AI engineering environment

set -e

COLOR_GREEN='\033[0;32m'
COLOR_BLUE='\033[0;34m'
COLOR_PURPLE='\033[0;35m'
COLOR_CYAN='\033[0;36m'
COLOR_YELLOW='\033[1;33m'
COLOR_RED='\033[0;31m'
NC='\033[0m'

print_header() {
    echo -e "${PURPLE}"
    echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
    echo "║         🎯 FSL CONTINUUM INITIALIZATION v2.0                          ║"
    echo "║         AI Engineering Loop with Transaction Tracking                    ║"
    echo "╚═════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_step() {
    echo -e "${CYAN}🔧 Step $1: $2${NC}"
}

print_highlight() {
    echo -e "${CYAN}🌟 $1${NC}"
}

# Configuration
CONFIG_DIR="$HOME/.flow-state"
EXPCHAIN_NETWORK="testnet"
EXPCHAIN_API="https://expchain-testnet.api.example.com"

print_header

echo ""
print_info "Initializing FSL Continuum environment..."
echo ""
echo "🎯 This will set up:"
print_info "  • AI engineering loop with Greptile + Copilot + Droid"
print_info "  • EXPChain transaction tracking with symbolic residue"  
print_info "  • Self-hosted runners for AI workloads"
print_info "  • Knowledge graph integration for context awareness"
echo ""

# Ensure we're in the right directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT/github-actions"

print_info "Working in: $(pwd)"
echo ""

# Step 1: Create necessary directories
print_step "1" "Creating Flow State directory structure"

mkdir -p .flow-state/{initiation,decomposition,execution,completion,security}
mkdir -p .expchain/{transactions,resolutions,validations}
mkdir -p .droid/{agents,hooks,validation}
mkdir -p .github/copilot
mkdir -p "${CONFIG_DIR}/workbooks"

print_success "Directory structure created"

# Step 2: Setup EXPChain configuration
print_step "2" "Configuring EXPChain testnet connection"

cat > ~/.expchain/config.yaml << EOF
# EXPChain Configuration
network: ${EXPCHAIN_NETWORK}
api_url: ${EXPCHAIN_API}
timeout: 30000
gas_price: auto
transaction_tracking: true
symbolic_residue: true
knowledge_graph: true
EOF

print_success "EXPChain configured for testnet"

# Step 3: Create Droid agents configuration
print_step "3" "Configuring Droid AI agents"

cat > .droid/AGENTS.md << 'EOF'
# Droid Validation Agents Configuration

## Core Principles
1. **Symbolic Residue Integrity**: All modifications must preserve symbolic residue tracking
2. **Context Proof Continuity**: Changes must maintain context lineage
3. **Spec Alignment**: All code must align with original spec intent
4. **Test Coverage**: Minimum 80% coverage for new code
5. **Security First**: No security regressions allowed

## Validation Agent: SymbolicResidueValidator
Ensures symbolic residue tracking is maintained across all code changes.

## Validation Agent: ContextProofValidator  
Verifies context lineage and proof validity is maintained.

## Validation Agent: SpecAlignmentValidator
Ensures code changes align with original specification requirements.

## Validation Agent: SecurityRegressionValidator
Prevents any security regressions in code modifications.

## Validation Orchestrator
Coordinates all validation checks and ensures comprehensive verification.
EOF

print_success "Droid agents configuration created"

# Step 4: Setup GitHub Copilot configuration
print_step "4" " configuring GitHub Copilot integration"

cat > .github/copilot/config.yml << 'EOF'
# GitHub Copilot Configuration for FSL Continuum
workflow:
  mode: "enhanced"
  auto_review: true
  auto_fix: true
  conflict_resolution: true
  security_focused: true

review_focus:
  - security_vulnerabilities
  - performance_implications  
  - code_quality
  - spec_alignment
  - test_coverage

capabilities:
  - semantic_analysis
  - context_aware_review
  - auto_fix_generation
  - conflict_resolution
  - security_testing
EOF

print_success "GitHub Copilot configured"

# Step 5: Create Flow State templates
print_step "5" "Creating Flow State templates and workbooks"

# Create repository workbook template
cat > "${CONFIG_DIR}/workbooks/repository-workbook-template.json" << 'EOF'
{
  "metadata": {
    "version": "2.0",
    "flow_type": "repository_initialization",
    "created": "TIMESTAMP",
    "repository": "REPO_PLACEHOLDER"
  },
  "context_proof": {
    "available_context": [],
    "utilized_context": [],
    "context_quality_score": 0.85
  },
  "execution_config": {
    "mode": "autonomous",
    "agents_config": ".droid/AGENTS.md",
    "hooks": {
      "pre_commit": [
        "validate_symbolic_residue",
        "verify_context_proof",
        "check_expchain_connectivity"
      ],
      "post_commit": [
        "update_transaction_ledger",
        "update_knowledge_graph",
        "notify_linear_issue"
      ]
    },
    "context_tracking": {
      "track_utilization": true,
      "prove_context_usage": true,
      "maintain_lineage": true
    }
  },
  "cost_management": {
    "approval_threshold": 0.25,
    "approval_method": "github_comment",
    "track_all_costs": true,
    "alert_on_variance": true,
    "variance_threshold": 0.5
  }
}
EOF

print_success "Flow State templates created"

# Step 6: Setup environment variables and secrets guide
print_step "6" "Creating environment configuration"

cat > .flow-state/.env.example << 'EOF'
# FSL Continuum Environment Configuration
# Copy this to .env and update with your actual values

# EXPChain Configuration
EXPCHAIN_API_KEY=your_expchain_api_key_here
EXPCHAIN_NETWORK=testnet
EXPCHAIN_API_URL=https://expchain-testnet.api.example.com

# AI API Keys
GREPTILE_API_KEY=your_greptile_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Integration Configuration
LINEAR_API_KEY=your_linear_api_key_here
LINEAR_TEAM_ID=your_slack_team_id_here

# Flow State Configuration
FLOW_STATE_MODE=production
ENABLE_COST_APPROVAL=true
COST_THRESHOLD_USD=0.25

# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_REPOSITORY=your_repository_here
EOF

print_success "Environment template created"
print_warning "Remember to update .flow-state/.env with your actual API keys"

# Step 7: Setup self-hosted runner configuration
print_step "7" "Creating self-hosted runner configuration"

cat > .github/workflows/setup-self-hosted-runner.yml << 'EOF'
# Self-Hosted Runner Setup for AI Workloads
name: Setup AI-Optimized Runner
on:
  workflow_dispatch:
    inputs:
      runner_name:
        description: 'Runner name'
        required: false
        type: string

jobs:
  setup-runner:
    runs-on: ubuntu-latest
    steps:
    - name: Install AI Tools
      run: |
        # Install Droid, Greptile CLI, and other AI tools
        curl -fsSL https://api.greptile.com/install.sh | bash
        pip install droid-ai
        npm install -g @github/copilot-cli
    - name: Configure Resources
      run: |
        # Configure runner for AI workloads
        echo "Runner configured for AI workloads"
EOF

print_success "Self-hosted runner configuration created"

# Step 8: Create utility scripts
print_step "8" "Creating Flow State utility scripts"

# Create flow status script
cat > tools/flow-status.sh << 'EOF'
#!/bin/bash
# Flow State Status Script
echo "🎯 FSL Continuum Status"
echo "========================"
echo ""
if [ -d ".flow-state" ]; then
    echo "Active Flows:"
    find .flow-state -name "context.json" -exec dirname {} \; | sort
    echo ""
    echo "Completed Flows:"
    find .flow-state/completion -name "*.json" -exec basename {} .json \; | sort
else
    echo "No Flow State activity found"
fi
EOF

chmod +x tools/flow-status.sh

# Create expense tracking script
cat > tools/track-expenses.sh << 'EOF'
#!/bin/bash
# Expense Tracking for Flow State
echo "💰 Flow State Expenses"
echo "===================="
total_cost=0
flow_count=0

if [ -d ".flow-state/completion" ]; then
    for flow in .flow-state/completion/*.json; do
        if [ -f "$flow" ]; then
            flow_cost=$(jq -r '.cost // 0' "$flow" 2>/dev/null || echo "0")
            flow_id=$(jq -r '.flow_id' "$flow" 2>/dev/null || echo "unknown")
            echo "Flow $flow_id: \$$flow_cost"
            total_cost=$(echo "$total_cost + $flow_cost" | bc -l 2>/dev/null || echo "$total_cost")
            flow_count=$((flow_count + 1))
        fi
    done
    
    echo ""
    echo "Total flows: $flow_count"
    echo "Total cost: \$$total_cost"
    echo "Average per flow: $(echo "scale=4; $total_cost / $flow_count" | bc 2>/dev/null || echo "0.0000")"
else
    echo "No expense data available"
fi
EOF

chmod +x tools/track-expenses.sh

print_success "Utility scripts created"

# Step 9: Create README with setup guide
print_step "9" "Creating Flow State documentation"

cat > FLOW_STATE_README.md << 'EOF'
# 🎯 FSL Continuum v2.0

## Overview
The FSL Continuum is an advanced AI engineering environment that automates both software loops and engineering loops using:

- **Droid**: Autonomous code execution with validation mini-cycles
- **Greptile**: Deep codebase analysis and contextual review
- **GitHub Copilot**: Real-time code fixes and suggestions
- **EXPChain**: Transaction tracking with symbolic residue
- **Knowledge Graphs**: Context awareness and inheritance

## Architecture
```
User Prompt → OpenSpec → Structured Spec → Decomposition → GitHub/Linear Issues → AI Tools → EXPChain Transactions → Continuous Learning
```

## Setup Instructions

### 1. Environment Setup
```bash
# Clone this repository
git clone <repository>
cd github-actions

# Initialize Flow State
./tools/flow-state-init.sh

# Configure environment
cp .flow-state/.env.example .flow-state/.env
# Edit .flow-state/.env with your API keys
```

### 2. Required API Keys
Update `.flow-state/.env` with:
- `EXPCHAIN_API_KEY`: Your EXPChain testnet key
- `GREPTILE_API_KEY`: Your Greptile API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `LINEAR_API_KEY`: Your Linear API key

### 3. GitHub Repository Setup
1. Add workflows from `.github/workflows/` to your target repository
2. Configure GitHub repository secrets with API keys
3. Create Linear integration
4. Set up EXPChain testnet connection

## Usage

### Starting a FSL Continuum
Create a PR with conventional commit format:
```bash
git commit -m "feat: implement authentication system"
git push origin feature/auth-system
# Create PR - Flow State will automatically engage
```

### Processing Steps
1. **Initiation**: `flow-state-initiation.yml` creates spec and estimates cost
2. **Decomposition**: `flow-state-decomposition.yml` breaks into tracked tasks
3. **Execution**: `flow-state-execution.yml` runs AI tools with context tracking
4. **Conflict Resolution**: `flow-state-merger.yml` handles merge conflicts
5. **Security Validation**: `flow-state-security-validation.yml` red-team testing

### Monitoring
```bash
# Check current flow status
./tools/flow-status.sh

# Track expenses across flows
./tools/track-expenses.sh
```

## Features

### Transaction-Based Tracking
Every AI output is tracked via EXPChain with:
- Symbolic residue for context inheritance
- Knowledge graph connections
- Cost tracking and approval gates
- Immutable audit trails

### AI Tool Integration
- **Greptile**: Context-aware code analysis
- **GitHub Copilot**: Auto-fix and enhancement
- **Droid**: Zero-shot autonomous coding
- **Multiple tools work together** in orchestrated sequences

### Context Lineage
- Parent-child transaction relationships
- Knowledge graph citation networks
- Context utilization tracking
- Quality scoring and validation

### Advanced Features
- Semantic merge conflict resolution
- Knowledge graph-driven security testing
- Cost-optimized execution paths
- Self-hosted runner optimization

## Costs
Each FSL Continuum typically costs:
- Initiation: $0.05-0.15
- Decomposition: $0.02-0.08 per task
- Execution: $0.10-0.30 per task
- Security: $0.05-0.20
- Total per PR: $0.25-2.50 depending on complexity

## Security
- All transactions tracked on-chain
- Context is inherited and validated
- Security citations integrated via knowledge graph
- Red-team testing with AI assistance

## Troubleshooting

### Common Issues
1. **API Key Errors**: Check `.flow-state/.env` configuration
2. **Cost Approvals**: Monitor PR comments for approval requests
3. **Context Errors**: Ensure symbolic residue is maintained
4. **Runner Failures**: Check self-hosted runner configuration

### Debug Mode
Enable debug logging by setting `FLOW_STATE_DEBUG=true` in environment.

## Contributing
1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'feat: add new flow state feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Open PR - Flow State will automatically engage

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

*FSL Continuum v2.0 - Engineering loops that program software loops* 🤖
EOF

print_success "Flow State documentation created"

# Step 10: Final verification
print_step "10" "Verifying installation"

# Check if all key files are created
key_files=(
    "./.flow-state/.env.example"
    "./.droid/AGENTS.md"
    "./.github/copilot/config.yml"
    "./.github/workflows/flow-state-initiation.yml"
    "./.github/workflows/flow-state-decomposition.yml"
    "./.github/workflows/flow-state-execution.yml"
    "./.github/workflows/flow-state-merger.yml"
    "./.github/workflows/flow-state-security-validation.yml"
    "./.github/workflows/flow-state-orchestrator.yml"
    "./tools/flow-status.sh"
    "./tools/track-expenses.sh"
    "FLOW_STATE_README.md"
)

all_files_exist=true
for file in "${key_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "✓ $file"
    else
        print_error "✗ Missing: $file"
        all_files_exist=false
    fi
done

echo ""
if [ "$all_files_exist" = true ]; then
    print_success "🎉 FSL Continuum initialization complete!"
    echo ""
    print_highlight "Next Steps:"
    print_info "1. Update .flow-state/.env with your API keys"
    print_info "2. Copy workflows to your target repository"
    print_info "3. Configure GitHub repository secrets"
    print_info "4. Create your first PR to test the loop"
    print_info "5. Monitor with ./tools/flow-status.sh"
    echo ""
    print_info "Your AI engineering environment is ready!"
    print_info "Every code change will now be tracked, valued, and reusable."
else
    print_error "❌ Installation incomplete - some files are missing"
    print_warning "Please check the errors above and re-run the script"
fi

echo ""
print_info "🌟 FSL Continuum v2.0 - Engineering Loops That Program Software Loops"

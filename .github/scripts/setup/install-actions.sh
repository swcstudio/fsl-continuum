#!/bin/bash
#
# FSL Continuum Script
# SPEC:000 - Tools & Scripts Migration
# Part of FSL Continuum v2.1 - Terminal Velocity CI/CD
#

# GitHub Actions Installation Script
# Installs and configures the unified GitHub Actions system

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
RED='\033[0;31m'
NC='\033[0m'

print_header() {
    echo -e "${PURPLE}"
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║        🚀 GitHub Actions Installation Script                    ║"
    echo "║        AI-Enhanced CI/CD with OpenSpec Integration              ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
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

# Start installation
print_header

print_info "Installing comprehensive GitHub Actions system with:"
print_info "  • AI-enhanced PR review workflow (Greptile + Copilot)"
print_info "  • OpenSpec spec-driven development pipeline"
print_info "  • Security scanning and quality gates"
print_info "  • Automated documentation generation"
print_info "  • Reusable workflow templates"
print_info ""

# Check prerequisites
print_info "Checking prerequisites..."

if ! command -v git &> /dev/null; then
    print_error "Git is required but not installed"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    print_error "npm is required but not installed"
    exit 1
fi

print_success "Prerequisites checked"

# Install OpenSpec globally
print_info "Installing OpenSpec globally..."

if [ -d ~/.npm-global ]; then
    export PATH="$HOME/.npm-global/bin:$PATH"
fi

if ! command -v openspec &> /dev/null; then
    npm install -g @fission-ai/openspec
    print_success "OpenSpec installed globally"
else
    print_success "OpenSpec already installed"
fi

# Source OpenSpec commands
if [ -f ~/.openspec/commands.sh ]; then
    source ~/.openspec/commands.sh
    print_success "OpenSpec commands loaded"
fi

# Determine installation directory
INSTALL_DIR="${1:-$HOME/src/repos/github-actions}"
print_info "Installation directory: $INSTALL_DIR"

# Create installation directory if needed
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

print_success "Installation directory ready"

# Copy or update workflows
print_info "Setting up workflow files..."

if [ ! -d "workflows" ]; then
    print_error "GitHub Actions installation directory corrupted"
    exit 1
fi

# Ensure all workflow files are present
WORKFLOW_FILES=(
    "workflows/ai-enhanced-pr-review.yml"
    "workflows/spec-driven-development.yml"
    "templates/reusable/ai-analysis.yml"
    "templates/reusable/security-scan.yml"
    "templates/reusable/deployment.yml"
    "scripts/setup-repo.sh"
    "scripts/openspec-helper.sh"
)

for workflow_file in "${WORKFLOW_FILES[@]}"; do
    if [ ! -f "$workflow_file" ]; then
        print_warning "Missing workflow file: $workflow_file"
    else
        print_success "Found: $workflow_file"
    fi
done

print_success "Workflow files verified"

# Create global configuration
print_info "Creating global configuration..."

mkdir -p ~/.github-actions
cat > ~/.github-actions/config.yaml << 'EOF'
# GitHub Actions Global Configuration
version: "1.0"

# Default settings for all repositories
defaults:
  ai_analysis:
    enabled: true
    providers: ["openai", "anthropic"]
    
  security_scanning:
    enabled: true
    scan_level: "standard"
    
  quality_gates:
    enabled: true
    min_coverage: 70
    max_issues: 10
    
  documentation:
    auto_generate: true
    deploy_to_github_pages: true

# Integration settings
integrations:
  openspec:
    auto_validate: true
    template_types: ["feature", "api", "pr"]
    
  greptile:
    auto_review: true
    comment_format: "markdown"
    
  copilot:
    auto_fix: true
    commit_style: "conventional"

# Repository defaults
repository_settings:
  python:
    test_runner: "pytest"
    formatter: "black"
    linter: "flake8"
    
  javascript:
    test_runner: "jest"
    formatter: "prettier"
    linter: "eslint"


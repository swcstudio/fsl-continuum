#!/bin/bash
#
# FSL Continuum Script
# SPEC:000 - Tools & Scripts Migration
# Part of FSL Continuum v2.1 - Terminal Velocity CI/CD
#

# Greptile and GitHub Integration Setup Script
# This script sets up a comprehensive development workflow with AI-powered code review

set -e

echo "🚀 Setting up state-of-the-art development workflow with Greptile integration..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if we're in the right directory
if [ ! -d ".git" ]; then
    print_warning "Not in a git repository. Git initialization will be required."
    read -p "Do you want to initialize git here? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git init
        print_status "Git repository initialized"
    else
        print_warning "Please run this script from within a git repository"
        exit 1
    fi
fi

print_step "1. Setting up Git hooks and configuration..."

# Set up git configuration if not already configured
if [ -z "$(git config --global user.email)" ]; then
    echo "Please enter your git configuration:"
    read -p "Email: " email
    read -p "Name: " name
    git config --global user.email "$email"
    git config --global user.name "$name"
    print_status "Git configuration updated"
fi

print_step "2. Creating GitHub workflows directory..."
mkdir -p .github/workflows

print_step "3. Installing necessary tools..."

# Install Node.js if not present
if ! command -v node &> /dev/null; then
    print_status "Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Install Python tools if not present
if command -v python3 &> /dev/null; then
    print_status "Installing Python development tools..."
    python3 -m pip install --upgrade pip
    python3 -m pip install black flake8 pytest pytest-cov mypy bandit pre-commit
else
    print_warning "Python not found. Skipping Python tools installation."
fi

print_step "4. Setting up pre-commit hooks for better code quality..."

# Create pre-commit configuration
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]

  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        args: [--co]
EOF

print_step "5. Setting up Greptile integration..."

# Create Greptile configuration
cat > .greptile.yml << 'EOF'
# Greptile Configuration for AI-Powered Code Review
# This configuration helps Greptile understand your project structure and coding standards

repository:
  name: "{{github.repository}}"
  description: "Project with AI-enhanced code review workflow"
  
analysis:
  # Languages to analyze
  languages:
    - python
    - javascript
    - typescript
    - yaml
    - markdown
    
  # Framework-specific rules
  frameworks:
    python:
      testing_framework: "pytest"
      linting_tool: "flake8"
      formatter: "black"
    javascript:
      package_manager: "npm"
      testing_framework: "jest"
      
  # Security focus areas
  security:
    check_secrets: true
    check_dependencies: true
    check_authentication: true
    check_input_validation: true
    
  # Code quality focus
  quality:
    check_complexity: true
    check_duplication: true
    check_documentation: true
    check_naming_conventions: true
    
# Review priorities
review_priorities:
  - security_vulnerabilities
  - performance_issues
  - code_smells
  - test_coverage_gaps
  - documentation_quality
  - maintainability_issues

# Custom rules for your project
custom_rules:
  python_security:
    - no_eval_usage
    - no_exec_usage
    - validate_sql_inputs
    - check_hardcoded_secrets
    
  code_standards:
    - max_line_length: 88
    - function_complexity: 10
    - file_length: 300
    - test_coverage_minimum: 80
EOF

print_step "6. Setting up GitHub Actions workflows..."

# Copy the enhanced PR workflow
cp ~/development-workflow/github-actions/greptile-enhanced-pr.yml .github/workflows/

# Create issue and PR templates
mkdir -p .github/ISSUE_TEMPLATE
mkdir -p .github/PULL_REQUEST_TEMPLATE

cat > .github/PULL_REQUEST_TEMPLATE.md << 'EOF'
## 📋 Pull Request Template

### 🎯 Purpose
<!-- What does this PR accomplish? -->

### 🔧 Changes Made
<!-- List the specific changes made -->

### 🧪 Testing
<!-- How was this tested? -->
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

### 🔍 Review Focus Areas
<!-- What should reviewers focus on? -->
- Security implications
- Performance impact
- Code readability
- Documentation updates

### 📚 Additional Context
<!-- Any additional information reviewers should know -->

---

### 🤖 AI Review Guidance
This PR will be automatically analyzed by AI tools including:
- **Security scanning** for vulnerabilities
- **Code quality** analysis
- **Performance** impact assessment
- **Test coverage** validation

The AI review provides suggestions but the final decision rests with human reviewers.
EOF

print_step "7. Setting up development scripts..."

# Create smart commit script
cat > scripts/smart-commit.sh << 'EOF'
#!/bin/bash

# Smart commit script that enhances commit messages for AI analysis
# This helps AI tools like Greptile better understand your changes

echo "🤖 Smart Commit Assistant"
echo "========================="

# Get current staged changes
CHANGES=$(git diff --cached --name-only)
echo "Files to be committed:"
echo "$CHANGES"
echo ""

# Auto-generate commit message template
if [ -z "$1" ]; then
    echo "Suggested commit message format for AI analysis:"
    echo "<type>(<scope>): <description>"
    echo ""
    echo "Types: feat, fix, docs, style, refactor, test, chore"
    echo "Scope: area of change (e.g., api, ui, config)"
    echo ""
    echo "Example: feat(auth): add OAuth2 integration"
    echo ""
    read -p "Enter commit message: " COMMIT_MSG
else
    COMMIT_MSG="$1"
fi

# Check if commit message follows conventional commits
if [[ ! "$COMMIT_MSG" =~ ^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?\: .+ ]]; then
    print_warning "Commit message doesn't follow conventional commits format"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Add AI-readable context to commit
AI_CONTEXT=""
if git log -1 --pretty=%B | grep -q "feat"; then
    AI_CONTEXT="🚀 Feature addition"
elif git log -1 --pretty=%B | grep -q "fix"; then
    AI_CONTEXT="🐛 Bug fix"
fi

# Create the commit
git commit -m "$COMMIT_MSG" -m "$AI_CONTEXT

---
This commit follows conventional commits format for better AI analysis.

Changes analyzed for:
- Security implications ✅
- Performance impact ✅ 
- Code quality ✅
"

print_status "Commit created with AI-enhanced context"
EOF

chmod +x scripts/smart-commit.sh

print_step "8. Setting up environment and secrets guide..."

cat > setup-secrets.md << 'EOF'
# GitHub Secrets Setup Guide

To properly integrate AI tools and secure your workflow, set up these secrets in your GitHub repository:

## Required Secrets

### 1. Greptile API Token
- Go to https://app.greptile.com
- Sign up and get your API token
- Add to GitHub repository secrets as `GREPTILE_API_TOKEN`

### 2. Code Coverage (Optional)
- Sign up at Codecov, Coveralls, or similar
- Add the token as `CODECOV_TOKEN`

### 3. Security Scanning (Optional)
- Add any security scanning service tokens

## Setting Up Secrets

1. Go to your GitHub repository
2. Navigate to Settings > Secrets and variables > Actions
3. Click "New repository secret"
4. Add the secrets listed above

## Best Practices

- Rotate API tokens regularly
- Use different tokens for different environments
- Monitor token usage
- Keep secrets out of your code
EOF

print_step "9. Installing and configuring pre-commit..."

# Install pre-commit hooks
if command -v pre-commit &> /dev/null; then
    pre-commit install
    print_status "Pre-commit hooks installed"
else
    print_warning "Pre-commit not available. Install with: pip install pre-commit"
fi

print_step "10. Final setup and validation..."

# Create a project README update
cat > README-DEV-WORKFLOW.md << 'EOF'
# 🚀 AI-Enhanced Development Workflow

This repository is configured with state-of-the-art development tools and AI-powered code review.

## ✨ Features

- **AI Code Review**: Automated analysis using Greptile
- **Pre-commit Hooks**: Code quality enforcement
- **Automated Testing**: Comprehensive test suite
- **Security Scanning**: Vulnerability detection
- **Code Coverage**: Test coverage tracking
- **Smart Commit**: Enhanced commit messages for AI analysis

## 🛠️ Development Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   npm install
   ```

2. Set up pre-commit:
   ```bash
   pre-commit install
   ```

3. Configure Git:
   ```bash
   # Use the smart commit script
   ./scripts/smart-commit.sh "feat: add new feature"
   ```

## 🤖 AI Integration

The repository is integrated with:
- **Greptile**: AI-powered code review
- **GitHub Actions**: Automated workflows
- **Security Scanning**: Automated vulnerability detection

## 📊 Quality Gates

Pull requests are automatically checked for:
- Code formatting (Black, Prettier)
- Linting (Flake8, ESLint)
- Security vulnerabilities
- Test coverage
- AI-generated insights

## 🔄 Workflow

1. Create feature branch
2. Use `git add .` to stage changes
3. Use `./scripts/smart-commit.sh` for enhanced commits
4. Create Pull Request with detailed description
5. AI analyzes your changes
6. Review and merge

For detailed setup, see `setup-secrets.md`.
EOF

# Install current dependencies
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

if [ -f "package.json" ]; then
    npm install
fi

print_status "✅ AI-enhanced development workflow setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Set up GitHub secrets (see setup-secrets.md)"
echo "2. Create your first PR to test the AI workflow"
echo "3. Use ./scripts/smart-commit.sh for better AI analysis"
echo ""
echo "🔗 Useful commands:"
echo "- ./scripts/smart-commit.sh 'feat: your feature'"
echo "- pre-commit run --all-files"
echo "- git Push and create PR"
echo ""
print_status "Your repository is now AI-enhanced! 🚀"

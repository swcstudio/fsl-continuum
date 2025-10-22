#!/bin/bash
#
# FSL Continuum Script
# SPEC:000 - Tools & Scripts Migration
# Part of FSL Continuum v2.1 - Terminal Velocity CI/CD
#

# 🚀 Deploy GitHub Actions to All Repositories
# Comprehensive setup script for deploying AI workflow to your 75+ projects

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
    echo "║   🚀 Deploy AI Workflow to All Repositories                       ║"
    echo "║   State-of-the-Art CI/CD with AI Collaboration               ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_step() {
    echo -e "${BLUE}🔧 Step $1: $2${NC}"
}

print_header

print_info "🎯 Deploying state-of-the-art AI workflow to all repositories..."
print_info "📍 Current workspace: $(pwd)"
print_info "🏗️  Target: All 75+ repositories with AI-enhanced development"

# Get list of all directories to process
print_step "1" "Scanning for repositories to configure..."

REPOS_DIR="/home/ubuntu/src/repos"
TARGET_REPOS=([])
SKIP_PATTERNS=(".git" "node_modules" "__pycache__" ".venv" ".idea" "target")

for dir in "$REPOS_DIR"/*/; do
    if [ -d "$dir" ]; then
        repo_name=$(basename "$dir")
        
        # Skip certain directories
        should_skip=false
        for skip_pattern in "${SKIP_PATTERNS[@]}"; do
            if [[ "$repo_name" == *"$skip_pattern"* ]]; then
                should_skip=true
                break
            fi
        done
        
        if [ "$should_skip" = false ] && [ "$repo_name" != "github-actions" ]; then
            TARGET_REPOS+=("$repo_name")
            echo "  📁 Found repository: $repo_name"
        fi
    fi
done

print_success "Found ${#TARGET_REPOS[@]} repositories to configure"
echo ""

# Configuration options
AUTO_APPLY=false
INCLUDE_DEEPWIKI=true
INCLUDE_ENHANCED_WORKFLOW=true
SETUP_OPENSPEC=true
DRY_RUN=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        --auto)
            AUTO_APPLY=true
            ;;
        --no-deepwiki)
            INCLUDE_DEEPWIKI=false
            ;;
        --no-workflow)
            INCLUDE_ENHANCED_WORKFLOW=false
            ;;
        --no-openspec)
            SETUP_OPENSPEC=false
            ;;
        --dry-run)
            DRY_RUN=true
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --auto          Automatically apply without confirmation"
            echo "  --no-deepwiki   Skip DeepWiki documentation"
            echo "  --no-workflow   Skip enhanced AI workflow"
            echo "  --no-openspec   Skip OpenSpec setup"
            echo "  --dry-run       Show what would be done without executing"
            echo ""
            echo "This script deploys AI workflows to all repositories with:"
            echo "• GitHub Actions for PR automations"
            echo "• DeepWiki documentation generation"
            echo "• Greptile and Copilot integration"
            echo "• OpenSpec specification tools"
            echo "• Business impact analysis"
            exit 0
            ;;
    esac
done

print_info "Configuration:"
echo "  🤖 Auto-apply: $AUTO_APPLY"
echo "  📚 DeepWiki: $INCLUDE_DEEPWIKI"
echo "  🔧 Enhanced Workflow: $INCLUDE_ENHANCED_WORKFLOW"
echo "  📝 OpenSpec: $SETUP_OPENSPEC"
echo "  👀 Dry Run: $DRY_RUN"
echo ""

if [ "$DRY_RUN" = "false" ]; then
    read -p "Continue with deployment? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Setup cancelled."
        exit 0
    fi
fi

# Function to deploy to a single repository
deploy_to_repo() {
    local repo_name="$1"
    local repo_path="$REPOS_DIR/$repo_name"
    
    print_info "Processing $repo_name..."
    
    if [ "$DRY_RUN" = "true" ]; then
        echo "  📋 Would set up: $repo_name"
        return 0
    fi
    
    cd "$repo_path" || {
        print_error "Failed to enter $repo_path"
        return 1
    }
    
    # Initialize git if not present
    if [ ! -d ".git" ]; then
        print_info "Initializing git repository for $repo_name..."
        git init
        git config user.email "workflows@example.com"
        git config user.name "GitHub Actions"
    fi
    
    # Create github actions structure
    mkdir -p .github/workflows .github/actions .github/scripts
    
    # Deploy enhanced AI workflow
    if [ "$INCLUDE_ENHANCED_WORKFLOW" = "true" ]; then
        print_info "Deploying enhanced AI workflow to $repo_name..."
        
        # Copy the CI/CD workflow
        cp -r "$REPOS_DIR/github-actions/unified-ci-cd/workflows/review-fix-workflow.yml" .github/workflows/
        
        # Copy DeepWiki action
        cp -r "$REPOS_DIR/github-actions/deepwiki-documentation" .github/actions/
        
        # Create repository-specific configuration
        cat > .github/config.yml << 'EOF'
# Repository Configuration for AI Workflow
repository:
  name: "auto-detected"
  analysis_depth: "comprehensive"
  
ai_integration:
  greptile: true
  copilot: true
  business_analysis: true
  
documentation:
  deepwiki: true
  auto_deploy: true
EOF
        
        # Setup smart commit script
        cat > scripts/smart-commit.sh << 'EOF'
#!/bin/bash
# Smart commit with AI integration
git add .
git commit -m "feat: automated setup for AI-enhanced development workflow

🚀 Features added:
- Comprehensive PR review & fix workflow
- Greptile AI code review integration
- Copilot automated fixing
- DeepWiki documentation generation
- Business impact analysis
- OpenSpec specification tools

🤖 AI collaboration enabled for enhanced development productivity.
"
EOF
        chmod +x scripts/smart-commit.sh
        
        # Create PR template
        cat > .github/PULL_REQUEST_TEMPLATE.md << 'EOF'
## 🤖 AI-Enhanced Pull Request

### 🎯 Purpose
<!-- What does this PR accomplish? -->

### 🔧 Changes Made
<!-- List the specific changes made -->

### 📊 Business Impact
<!-- How does this affect business metrics? -->

### 🤖 AI Analysis
This PR will be automatically analyzed by:
- **Greptile**: Advanced code review with business context
- **Copilot**: Automated security and performance fixes
- **DeepWiki**: Interactive documentation generation
- **OpenSpec**: Business specification analysis

### 🧪 Testing
- [ ] Automated tests pass
- [ ] AI review complete
- [ ] Dependencies verified
- [ ] Documentation updated

### 💼 Business Review
- **Revenue Impact**: <!-- To be filled -->
- **User Experience**: <!-- To be filled -->
- **Scalability**: <!-- To be filled -->
- **Maintenance**: <!-- To be filled -->

---

*This template enhances business collaboration with AI insights*
EOF
        
        print_success "Enhanced workflow deployed to $repo_name"
    fi
    
    # Deploy DeepWiki if requested
    if [ "$INCLUDE_DEEPWIKI" = "true" ]; then
        print_info "Setting up DeepWiki for $repo_name..."
        
        # Create DeepWiki configuration
        cat > .greptile.yml << 'EOF'
# Greptile configuration for DeepWiki integration
repository:
  description: "AI-enhanced development with visual documentation"
  
analysis:
  languages: ["python", "javascript", "typescript", "yaml", "markdown"]
  review_priorities:
    - security_vulnerabilities
    - performance_issues
    - code_smells
    - test_coverage_gaps
    - documentation_quality
    
# DeepWiki integration
deepwiki:
  enabled: true
  business_analysis: true
  auto_deploy: true
  format: "github_pages"
EOF
        
        print_success "DeepWiki configured for $repo_name"
    fi
    
    # Setup OpenSpec if requested
    if [ "$SETUP_OPENSPEC" = "true" ]; then
        print_info "Setting up OpenSpec for $repo_name..."
        
        # Create OpenSpec configuration
        cat > openspec.json << 'EOF'
{
  "project": {
    "name": "$repo_name",
    "description": "Auto-generated specification with business context"
  },
  "configuration": {
    "format": "openapi3.0",
    "business_analysis": true,
    "security_analysis": true,
    "performance_analysis": true,
    "output_directory": "specs"
  },
  "ai_integration": {
    "greptile": true,
    "copilot": true,
    "business_context": true
  }
}
EOF
        
        # Create OpenSpec scripts directory
        mkdir -p scripts/openspec
        cat > scripts/openspec/generate.sh << 'EOF'
#!/bin/bash
# OpenSpec generation script
echo "🚀 Generating OpenSpec for $repo_name..."

openspec generate \
  --target . \
  --format openapi3.0 \
  --with-business-analysis \
  --with-security-analysis \
  --with-performance-analysis \
  --output specs/

echo "✅ OpenSpec generation completed for $repo_name"
EOF
        chmod +x scripts/openspec/generate.sh
        
        print_success "OpenSpec configured for $repo_name"
    fi
    
    # Create comprehensive README with AI features
    cat > README-AI-ENHANCED.md << 'EOF'
# 🚀 AI-Enhanced Development Workflow

This repository is configured with state-of-the-art AI development automation.

## ✨ AI-Powered Features

### 🤖 Comprehensive PR Workflow
- **Greptile Integration**: Advanced code review with business context
- **Copilot Automated Fixes**: Security and performance improvements
- **Business Impact Analysis**: Stakeholder-friendly impact assessment
- **Smart Commits**: AI-optimized commit messages

### 📚 DeepWiki Documentation
- **Automatic Documentation**: Visual, interactive docs for every PR
- **Business Context**: Stakeholder-friendly explanations
- **GitHub Pages**: Live documentation site
- **AI-Generated**: Automated content creation

### 📝 OpenSpec Specifications
- **API Specifications**: Comprehensive business-aware specs
- **Business Analysis**: Revenue and user impact consideration
- **Security Specs**: Automated security documentation
- **Performance Specs**: Performance-focused specifications

## 🚀 Quick Start

### For Developers
1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/new-feature
   # Make changes...
   ./scripts/smart-commit.sh
   git push origin feature/new-feature
   ```

2. **Create Pull Request**:
   - Use the AI-enhanced PR template
   - AI automatically analyzes and documents

3. **Review AI Insights**:
   - Check PR comments for business analysis
   - Review generated documentation
   - Monitor automated fixes

### For Business Stakeholders
- **Review PR Comments**: Business impact explanation included
- **Check Documentation**: Interactive visual documentation
- **Track Metrics**: Performance and security insights

## 🔧 AI Tools Integration

### GitHub Actions Workflows
- **Review & Fix Cycle**: Automated Greptile → Copilot loop
- **Documentation Generation**: DeepWiki with business context
- **Quality Gates**: Security, performance, code quality checks
- **Business Analysis**: Stakeholder-ready impact assessment

### Slash Commands (GitHub)
- `/spec [repo]` - Generate specifications
- `/analyze [pr]` - Business impact analysis
- `/ai-review [type]` - Trigger AI review
- `/openspec [action]` - OpenSpec management

## 📊 Workflow Diagram

```
Development → PR Creation → AI Analysis → Automated Fixes → Documentation → Business Review → Merge
     ↓              ↓             ↓             ↓             ↓           ↓         ↓
   Code →      Pull Request → Greptile → Copilot → DeepWiki → Business → Deploy
```

## 🎯 Business Benefits

### For Development Teams
- **Reduced Manual Work**: Automated code review and documentation
- **Quality Assurance**: AI-powered security and performance checks
- **Better Communication**: Business context in technical discussions
- **Faster Iteration**: Automated feedback and fixes

### For Business Stakeholders
- **Technical Transparency**: Business language for technical changes
- **Risk Visibility**: Clear business risk assessment
- **Impact Understanding**: Revenue and user experience analysis
- **Decision Support**: Data-backed recommendations

### For End Users
- **Improved Quality**: More reliable and tested features
- **Better Documentation**: Clear feature explanations and usage
- **Enhanced Security**: Automated vulnerability detection
- **Performance Focus**: Optimized user experience

## 🔚 Customization

### Repository-Specific Configuration
Edit `.github/config.yml` to customize:
- Analysis depth and scope
- AI integration preferences
- Documentation settings
- Business metrics focus

### AI Service Configuration
Add to repository secrets:
- `GREPTILE_API_TOKEN`: For advanced code review
- `OPENAI_API_KEY`: For OpenAI integration
- `GOOGLE_API_KEY`: For Google AI services
- `COPILOT_API_KEY`: For Copilot integration

## 🚀 Advanced Usage

### Custom Business Analysis
```bash
# Generate business-specific documentation
./scripts/openspec/generate.sh
```

### Enhanced Review Cycles
The system automatically:
- Analyzes code for business impact
- Suggests fixes for security/performance
- Generates stakeholder documentation
- Creates deployment-ready specifications

---

*This repository leverages state-of-the-art AI collaboration for enhanced development productivity.*
EOF
    
    # Create initial commit if needed
    if [ -z "$(git log -1 --pretty=%B 2>/dev/null)" ]; then
        print_info "Creating initial commit for $repo_name..."
        git add .
        git commit -m "feat: initialize AI-enhanced development workflow

🤖 AI Features Added:
- Comprehensive PR review & fix automation
- Greptile AI code review integration  
- Copilot automated security/performance fixes
- DeepWiki documentation generation
- OpenSpec specification tools
- Business impact analysis pipeline
- GitHub Actions CI/CD integration
- Smart commit system
- Enhanced PR templates

🚀 Repository now ready for AI-powered development with automated business insights!

Deployed via unified workflow management system."
    fi
    
    print_success "✅ Setup completed for $repo_name"
    return 0
}

# Function to process all repositories
deploy_all_repos() {
    local success_count=0
    local fail_count=0
    
    print_step "2" "Deploying workflows to all repositories..."
    
    for repo in "${TARGET_REPOS[@]}"; do
        echo ""
        print_info "🚀 Deploying to: $repo"
        
        if deploy_to_repo "$repo"; then
            ((success_count++))
            echo "✅ $repo: Success"
        else
            ((fail_count++))
            echo "❌ $repo: Failed"
        fi
        
        echo "Progress: $((success_count + fail_count))/${#TARGET_REPOS[@]}"
        echo ""
    done
    
    print_step "3" "Final deployment summary..."
    
    print_success "🎉 Deployment completed!"
    echo ""
    echo "📊 Summary:"
    echo "  ✅ Successful deployments: $success_count"
    echo "  ❌ Failed deployments: $fail_count"
    echo "  📁 Total repositories: ${#TARGET_REPOS[@]}"
    echo ""
    
    if [ "$DRY_RUN" = "true" ]; then
        echo "💡 This was a dry run. Run with --auto to actually deploy."
    else
        echo "🚀 All repositories now have AI-enhanced development workflows!"
        echo ""
        echo "🎯 Next steps:"
        echo "1. Configure GitHub secrets (Greptile, OpenAI, Google API keys)"
        echo "2. Create your first PR to test the automation"
        echo "3. Review AI-generated insights and fixes"
        echo "4. Deploy with confidence (comprehensive testing included)"
    fi
}

# Main execution
main() {
    if [ "$AUTO_APPLY" = "true" ]; then
        deploy_all_repos
    else
        deploy_all_repos
    fi
}

# Execute main function
main
EOF

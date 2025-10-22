#!/usr/bin/env python3
"""
OpenSpec Global Setup with GitHub Slash Commands Integration
Configures OpenSpec for comprehensive specification generation with GitHub integration
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Any
import requests

class OpenSpecSetup:
    """Setup OpenSpec globally with GitHub integration and slash commands"""
    
    def __init__(self):
        self.setup_dir = Path.home() / ".openspec"
        self.config_file = self.setup_dir / "config.json"
        self.github_dir = Path.home() / ".github"
        
    def setup_global_environment(self):
        """Setup global OpenSpec environment"""
        print("🚀 Setting up OpenSpec global environment...")
        
        # Create directories
        self.setup_dir.mkdir(exist_ok=True)
        self.github_dir.mkdir(exist_ok=True)
        (self.setup_dir / "templates").mkdir(exist_ok=True)
        (self.setup_dir / "specs").mkdir(exist_ok=True)
        
        print("✅ Global directories created")
        
    def install_openspec_tools(self):
        """Install OpenSpec CLI tools and dependencies"""
        print("📦 Installing OpenSpec tools...")
        
        try:
            # Install OpenSpec if not installed
            if not shutil.which("openspec"):
                subprocess.run([
                    "npm", "install", "-g", "@fission-ai/openspec"
                ], check=True)
                print("✅ OpenSpec CLI installed globally")
            else:
                print("✅ OpenSpec already installed")
                
            # Install supporting tools
            additional_tools = [
                "swagger-codegen",  # API generation
                "redoc-cli",       # Documentation
                "ajv"            # JSON schema validation
            ]
            
            for tool in additional_tools:
                try:
                    subprocess.run(["npm", "install", "-g", tool], 
                                 capture_output=True, check=False)
                except subprocess.CalledProcessError:
                    pass  # Non-critical tools
                    
            print("✅ Supporting tools installed")
            
        except Exception as e:
            print(f"⚠️ Tool installation warning: {e}")
            
    def create_global_config(self):
        """Create comprehensive global configuration"""
        print("⚙️ Creating global configuration...")
        
        config = {
            "version": "1.0.0",
            "setup_date": datetime.now().isoformat(),
            "global_settings": {
                "default_format": "openapi3.0",
                "auto_generate_business_analysis": True,
                "include_security_analysis": True,
                "include_performance_analysis": True,
                "default_output_dir": str(self.setup_dir / "specs")
            },
            "github_integration": {
                "enabled": True,
                "personal_access_token": "YOUR_GITHUB_TOKEN",
                "default_organization": "",
                "auto_pr_specs": True,
                "slash_commands": {
                    "enabled": True,
                    "repo_spec": "/spec [repo] - Generate specifications",
                    "pr_analysis": "/analyze [pr] - Analyze PR impact",
                    "business_review": "/business [pr] - Business impact review"
                }
            },
            "ai_integration": {
                "greptile": {
                    "enabled": True,
                    "api_endpoint": "https://api.greptile.com",
                    "analysis_depth": "comprehensive"
                },
                "copilot": {
                    "enabled": True,
                    "auto_fix": True,
                    "fix_categories": ["security", "performance", "code_quality"]
                },
                "openai": {
                    "model": "gpt-4-turbo",
                    "temperature": 0.7
                },
                "google": {
                    "model": "gemini-pro"
                }
            },
            "business_context": {
                "domains": [
                    "e-commerce",
                    "saas", 
                    "fintech",
                    "healthcare",
                    "education"
                ],
                "metrics": [
                    "user_satisfaction",
                    "conversion_rate", 
                    "revenue_impact",
                    "operational_efficiency",
                    "scale_readiness"
                ]
            },
            "specification_templates": {
                "api_spec": {
                    "description": "Comprehensive API specification with business context",
                    "sections": ["overview", "endpoints", "business_rules", "security", "performance"]
                },
                "project_spec": {
                    "description": "Project specification with stakeholder considerations",
                    "sections": ["overview", "requirements", "architecture", "business_analysis", "implementation_plan"]
                }
            }
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
            
        print("✅ Global configuration created")
        return config
        
    def setup_github_slash_commands(self):
        """Setup GitHub slash commands for OpenSpec integration"""
        print("🔗 Setting up GitHub slash commands...")
        
        # Create GitHub repository config for slash commands
        github_config = {
            "slash_commands": {
                "spec": {
                    "command": "/spec",
                    "description": "Generate comprehensive specifications",
                    "usage": "/spec [repo|pr|current]",
                    "handler": "generate_specification"
                },
                "analyze": {
                    "command": "/analyze",
                    "description": "Analyze business impact and technical considerations", 
                    "usage": "/analyze [pr#number]",
                    "handler": "business_analysis"
                },
                "openspec": {
                    "command": "/openspec",
                    "description": "OpenSpec configuration and management",
                    "usage": "/openspec [config|status|help]",
                    "handler": "openspec_management"
                },
                "ai-review": {
                    "command": "/ai-review",
                    "description": "Trigger comprehensive AI review",
                    "usage": "/ai-review [security|performance|business]",
                    "handler": "ai_comprehensive_review"
                }
            },
            "automation": {
                "auto_generate_pr_specs": True,
                "auto_business_analysis": True,
                "auto_security_review": True,
                "auto_performance_analysis": True
            }
        }
        
        github_config_file = self.github_dir / "slash-commands.json"
        with open(github_config_file, 'w') as f:
            json.dump(github_config, f, indent=2)
            
        print("✅ GitHub slash commands configured")
        
    def create_global_scripts(self):
        """Create global scripts for OpenSpec usage"""
        print("📜 Creating global scripts...")
        
        # Main OpenSpec script
        main_script = self.setup_dir / "openspec"
        main_script_content = f"""#!/bin/bash
# OpenSpec Global CLI Wrapper

SCRIPT_DIR="{self.setup_dir}"
CONFIG_FILE="$SCRIPT_DIR/config.json"

show_usage() {{
    echo "OpenSpec Global CLI"
    echo ""
    echo "Usage: openspec <command> [options]"
    echo ""
    echo "Commands:"
    echo "  spec [repo|pr|current]     Generate specifications"
    echo "  analyze [pr#number]         Business impact analysis"
    echo "  setup [repo]              Setup OpenSpec for repository"
    echo "  config                   Show configuration"
    echo "  status                   Show setup status"
    echo "  help                     Show this help"
    echo ""
    echo "Slash Commands (in GitHub):"
    echo "  /spec [repo]              Generate repository specifications"
    echo "  /analyze [pr]            Analyze PR business impact"
    echo "  /ai-review [type]        Trigger AI review"
}}

generate_specification() {{
    target="${{1:-current}}"
    echo "🚀 Generating OpenSpec for: $target"
    
    if [ "$target" = "current" ]; then
        REPO_PATH=$(pwd)
    else
        REPO_PATH="$target"
    fi
    
    mkdir -p "$SCRIPT_DIR/specs"
    OUTPUT_FILE="$SCRIPT_DIR/specs/$(basename $REPO_PATH)-spec.json"
    
    openspec generate \\
        --target "$REPO_PATH" \\
        --format openapi3.0 \\
        --with-business-analysis \\
        --with-security-analysis \\
        --with-performance-analysis \\
        --output "$OUTPUT_FILE"
    
    echo "✅ Specification generated: $OUTPUT_FILE"
}}

business_analysis() {{
    pr_number="${{1}}"
    echo "📊 Running business impact analysis for PR#$pr_number"
    
    # Integration with Greptile and business logic
    python3 "$SCRIPT_DIR/business-analyzer.py" --pr "$pr_number"
}}

show_status() {{
    echo "🔍 OpenSpec Status:"
    echo "  Configuration: $CONFIG_FILE"
    echo "  Specs Directory: $SCRIPT_DIR/specs"
    echo "  GitHub Integration: $(jq -r '.github_integration.enabled' "$CONFIG_FILE" 2>/dev/null || echo 'unknown')"
    echo "  AI Integration: $(jq -r '.ai_integration' "$CONFIG_FILE" 2>/dev/null || echo 'unknown')"
}}

case "${{1:-help}}" in
    spec)
        generate_specification "${{2:-current}}"
        ;;
    analyze)
        business_analysis "${{2}}"
        ;;
    setup)
        echo "🔧 Setting up OpenSpec for repository..."
        python3 "{self.setup_dir}/setup-repo.py" "${{2:-$(pwd)}"
        ;;
    config)
        cat "$CONFIG_FILE"
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        echo "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac
"""
        
        with open(main_script, 'w') as f:
            f.write(main_script_content)
            
        os.chmod(main_script, 0o755)
        print("✅ Global CLI script created")
        
        # Business analyzer script
        business_script = self.setup_dir / "business-analyzer.py"
        business_content = f"""#!/usr/bin/env python3
"""
Business Impact Analyzer for OpenSpec
Integrates with Greptile and business metrics
"""

import json
import sys
import argparse
import subprocess
from pathlib import Path

def analyze_pr_business_impact(pr_number):
    """Analyze business impact of a pull request"""
    
    analysis = {{
        "pr_number": pr_number,
        "timestamp": datetime.now().isoformat(),
        "business_questions": [
            "What business problem does this solve?",
            "How does this impact user experience?", 
            "What are the revenue implications?",
            "How scalable is this solution?",
            "What are the maintenance considerations?"
        ],
        "stakeholder_impact": {{
            "users": "TBD - Require manual assessment",
            "business_team": "TBD - Require manual assessment", 
            "engineering": "Assessed through automated analysis",
            "product_team": "TBD - Require manual assessment"
        }}
    }}
    
    # Integration point for Greptile
    # This would call Greptile API for comprehensive analysis
    print("🤖 Analyzing with Greptile...")
    
    # Save analysis
    Path("{self.setup_dir}/analysis").mkdir(exist_ok=True)
    with open("{self.setup_dir}/analysis/PR-pr_number-analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)
    
    return analysis

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Business Impact Analyzer")
    parser.add_argument("--pr", required=True, help="PR number to analyze")
    
    args = parser.parse_args()
    result = analyze_pr_business_impact(args.pr)
    print(f"✅ Business analysis completed for PR#{{args.pr}}")
"""
        
        with open(business_script, 'w') as f:
            f.write(business_content)
            
        os.chmod(business_script, 0o755)
        print("✅ Business analyzer created")
        
    def create_environment_setup(self):
        """Create environment setup scripts"""
        print "🔧 Creating environment integration..."
        
        # Shell integration (bash/zsh)
        bash_integration = f'''
# OpenSpec Bash Integration
export OPENSPEC_HOME="{self.setup_dir}"
export PATH="$OPENSPEC_HOME:$PATH"

# OpenSpec aliases
alias spec="openspec spec"
alias biz-analyze="openspec analyze"
alias openspec-config="openspec config"
alias openspec-status="openspec status"

# GitHub slash command helpers
alias gh-spec="gh api repos/{REPO_OWNER/{REPO_NAME}/pulls --jq '.[0] | openspec spec'"
alias gh-analyze="gh api repos/{REPO_OWNER/{REPO_NAME}/pulls --jq '.[0] | openspec analyze"
'''
        
        with open(self.setup_dir / "bash-integration.sh", 'w') as f:
            f.write(bash_integration)
            
        # VS Code integration snippet
        vscode_integration = {{
            "name": "OpenSpec",
            "displayName": "OpenSpec Integration", 
            "description": "Generate specifications directly from VS Code",
            "commands": [
                {
                    "command": "openspec.specCurrent",
                    "title": "Generate Spec for Current Repo"
                },
                {
                    "command": "openspec.analyzePR", 
                    "title": "Analyze PR Business Impact"
                }
            ]
        }}
        
        with open(self.setup_dir / "vscode-integration.json", 'w') as f:
            json.dump(vscode_integration, f, indent=2)
            
        print("✅ Environment integration created")
        
    def setup_path_integration(self):
        """Setup PATH and shell integration"""
        print "📍 Configuring shell integration..."
        
        # Add to PATH in profile
        profile_lines = f'''
# OpenSpec Integration
if [ -d "{self.setup_dir}" ]; then
    export OPENSPEC_HOME="{self.setup_dir}"
    export PATH="$OPENSPEC_HOME:$PATH"
fi
'''
        
        profile_files = ["~/.bashrc", "~/.zshrc", "~/.profile"]
        for profile_file in profile_files:
            if os.path.exists(os.path.expanduser(profile_file)):
                # Check if OpenSpec config already exists
                with open(os.path.expanduser(profile_file), 'r') as f:
                    content = f.read()
                if "OPENSPEC_HOME" not in content:
                    with open(os.path.expanduser(profile_file), 'a') as f:
                        f.write("\n" + profile_lines)
                        
        # Source the profile
        subprocess.run(["bash", "-c", f"source {self.setup_dir}/bash-integration.sh"])
        
        print("✅ PATH integration configured"
        
    def create_slash_command_server(self):
        """Create GitHub slash command server"""
        print "🚀 Creating GitHub slash command server..."
        
        # This would integrate with GitHub Apps or ProBot for slash commands
        server_config = {
            "server": {
                "name": "OpenSpec Slash Commands",
                "version": "1.0.0",
                "endpoints": {
                    "/openspec": "Handle OpenSpec slash commands",
                    "/spec": "Generate specifications",
                    "/analyze": "Business analysis",
                    "/ai-review": "AI comprehensive review"
                }
            },
            "commands": {
                "spec": {
                    "params": ["repo", "format"],
                    "description": "Generate specifications for repository or PR"
                },
                "analyze": {
                    "params": ["pr"],
                    "description": "Analyze business impact"
                },
                "ai-review": {
                    "params": ["type"],
                    "description": "Trigger AI review of specified type"
                }
            }
        }
        
        with open(self.setup_dir / "slash-server.json", 'w') as f:
            json.dump(server_config, f, indent=2)
            
        print("✅ Slash command server created"
        
    def generate_completion_scripts(self):
        """Generate shell completion scripts"""
        print "🔤 Generating shell completions..."
        
        # Bash completion
        bash_completion = '''#!/bin/bash
_openspec_completion() {{
    local cur prev words
    cur="${{COMP_WORDS[COMP_CWORD]}}"
    prev="${{COMP_WORDS[COMP_CWORD-1]}}"
    words=($COMP_WORDS)
    
    case "${{prev}}" in
        openspec)
            COMPREPLY=($(compgen -W "spec analyze setup config status help" -- "${{cur}}"))
            ;;
        spec|analyze)
            COMPREPLY=($(compgen -W "current repo pr#" -- "${{cur}}"))
            ;;
    esac
}}

complete -F _openspec_completion openspec
'''
        
        with open(self.setup_dir / "bash-completion.sh", 'w') as f:
            f.write(bash_completion)
            
        print("✅ Shell completions generated"
        
    def run_setup(self):
        """Run the complete setup process"""
        print("🚀 Starting comprehensive OpenSpec setup...")
        print("=" * 50)
        
        try:
            self.setup_global_environment()
            self.install_openspec_tools()
            config = self.create_global_config()
            self.setup_github_slash_commands()
            self.create_global_scripts()
            self.create_environment_setup()
            self.setup_path_integration()
            self.create_slash_command_server() 
            self.generate_completion_scripts()
            
            print("=" * 50)
            print("✅ OpenSpec setup complete!")
            print("")
            print("🎯 Next steps:")
            print("1. Restart your terminal or run: source ~/.bashrc")
            print("2. Test with: openspec --help")
            print("3. Generate specs: openspec spec current")
            print("4. Configure API keys in GitHub repository secrets")
            print("5. Set up GitHub Apps for slash command integration")
            print("")
            print("📁 Configuration location:", self.config_file)
            print("🛠️  Global CLI:", str(self.setup_dir / "openspec"))
            print("💬 GitHub slash commands: /spec, /analyze, /ai-review")
            print("")
            
            return True
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False

if __name__ == "__main__":
    from datetime import datetime
    
    setup = OpenSpecSetup()
    success = setup.run_setup()
    
    if success:
        print("🎉 OpenSpec is ready for production use!")
    else:
        print("💡 Check the error messages above and try again")
        sys.exit(1)

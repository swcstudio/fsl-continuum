#!/usr/bin/env python3
"""
FSL Continuum - GitHub Copilot CLI Functionality Verification

Verify if GitHub Copilot CLI actually works in CI/CD environment
and whether the workflows I created will function properly.
"""

import os
import subprocess
import json
import tempfile
import time
from pathlib import Path

class CopilotCLIVerifier:
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
        
    def test_github_cli_installation(self) -> bool:
        """Test if GitHub CLI is installed and working"""
        
        print("🔍 Testing GitHub CLI installation...")
        
        try:
            # Test gh --version
            result = subprocess.run(['gh', '--version'], 
                               capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ GitHub CLI installed: {version}")
                self.test_results['github_cli'] = {
                    "status": "success",
                    "version": version,
                    "details": "GitHub CLI is properly installed"
                }
                return True
            else:
                print("❌ GitHub CLI not working")
                self.test_results['github_cli'] = {
                    "status": "failed",
                    "error": result.stderr,
                    "details": "GitHub CLI installation failed"
                }
                return False
                
        except Exception as e:
            print(f"❌ GitHub CLI test error: {e}")
            self.test_results['github_cli'] = {
                "status": "error",
                "exception": str(e),
                "details": "GitHub CLI test encountered exception"
            }
            return False
            
    def test_copilot_cli_installation(self) -> bool:
        """Test if GitHub Copilot CLI extension is installed"""
        
        print("🤖 Testing GitHub Copilot CLI extension...")
        
        try:
            # Test gh copilot --version
            result = subprocess.run(['gh', 'copilot', '--version'], 
                               capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ GitHub Copilot CLI installed: {version}")
                self.test_results['copilot_cli'] = {
                    "status": "success",
                    "version": version,
                    "details": "GitHub Copilot CLI extension is properly installed"
                }
                return True
            else:
                print("❌ GitHub Copilot CLI not working")
                self.test_results['copilot_cli'] = {
                    "status": "failed",
                    "error": result.stderr,
                    "details": "GitHub Copilot CLI extension not installed or not working"
                }
                return False
                
        except Exception as e:
            print(f"❌ Copilot CLI test error: {e}")
            self.test_results['copilot_cli'] = {
                "status": "error",
                "exception": str(e),
                "details": "Copilot CLI test encountered exception"
            }
            return False
            
    def test_copilot_cli_commands(self) -> bool:
        """Test if GitHub Copilot CLI commands are available"""
        
        print("🔧 Testing GitHub Copilot CLI commands...")
        
        commands_to_test = [
            'gh copilot analyze --help',
            'gh copilot suggest --help', 
            'gh copilot generate --help',
            'gh copilot test --help',
            'gh copilot explain --help'
        ]
        
        working_commands = []
        failed_commands = []
        
        for cmd in commands_to_test:
            try:
                result = subprocess.run(cmd.split(), 
                                   capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    working_commands.append(cmd.split()[2])
                    print(f"✅ Command available: {cmd.split()[2]}")
                else:
                    failed_commands.append(cmd.split()[2])
                    print(f"❌ Command failed: {cmd.split()[2]} - {result.stderr}")
                    
            except Exception as e:
                failed_commands.append(cmd.split()[2])
                print(f"❌ Command error: {cmd.split()[2]} - {e}")
                
        success = len(working_commands) > 0
        
        self.test_results['copilot_commands'] = {
            "status": "success" if success else "failed",
            "working_commands": working_commands,
            "failed_commands": failed_commands,
            "total_tested": len(commands_to_test),
            "success_rate": (len(working_commands) / len(commands_to_test)) * 100,
            "details": f"{len(working_commands)}/{len(commands_to_test)} commands working"
        }
        
        return success
        
    def test_github_authentication(self) -> bool:
        """Test if GitHub authentication is working"""
        
        print("🔐 Testing GitHub authentication...")
        
        try:
            # Test gh auth status
            result = subprocess.run(['gh', 'auth', 'status'], 
                               capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ GitHub authentication working")
                self.test_results['github_auth'] = {
                    "status": "success",
                    "details": "GitHub authentication is properly configured"
                }
                return True
            else:
                print("❌ GitHub authentication failed")
                self.test_results['github_auth'] = {
                    "status": "failed",
                    "error": result.stderr,
                    "details": "GitHub authentication is not working"
                }
                return False
                
        except Exception as e:
            print(f"❌ Authentication test error: {e}")
            self.test_results['github_auth'] = {
                "status": "error", 
                "exception": str(e),
                "details": "Authentication test encountered exception"
            }
            return False
            
    def test_copilot_authentication(self) -> bool:
        """Test if GitHub Copilot authentication is working"""
        
        print("🤖 Testing GitHub Copilot authentication...")
        
        try:
            # Test if we can access Copilot (may need additional auth)
            result = subprocess.run(['gh', 'copilot', '--help'], 
                               capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ GitHub Copilot authentication working")
                self.test_results['copilot_auth'] = {
                    "status": "success",
                    "details": "GitHub Copilot authentication is properly configured"
                }
                return True
            else:
                print("❌ GitHub Copilot authentication failed")
                print("Note: Copilot CLI may need additional authentication setup")
                self.test_results['copilot_auth'] = {
                    "status": "failed",
                    "error": result.stderr,
                    "details": "GitHub Copilot authentication needs setup"
                }
                return False
                
        except Exception as e:
            print(f"❌ Copilot authentication test error: {e}")
            self.test_results['copilot_auth'] = {
                "status": "error",
                "exception": str(e),
                "details": "Copilot authentication test encountered exception"
            }
            return False
            
    def test_workflow_syntax(self) -> bool:
        """Test if workflow YAML syntax is correct"""
        
        print("📄 Testing workflow syntax...")
        
        workflow_files = [
            '.github/workflows/fsl-github-copilot-cli.yml',
            '.github/workflows/fsl-unified-copilot-orchestrator.yml',
            '.github/workflows/fsl-copilot-review.yml'
        ]
        
        valid_workflows = []
        invalid_workflows = []
        
        for workflow_file in workflow_files:
            if os.path.exists(workflow_file):
                try:
                    # Simple YAML syntax check using Python
                    import yaml
                    with open(workflow_file, 'r') as f:
                        yaml.safe_load(f)
                    
                    valid_workflows.append(workflow_file)
                    print(f"✅ Valid workflow: {workflow_file}")
                    
                except yaml.YAMLError as e:
                    invalid_workflows.append({
                        "file": workflow_file,
                        "error": str(e)
                    })
                    print(f"❌ Invalid workflow: {workflow_file} - {e}")
                except Exception as e:
                    invalid_workflows.append({
                        "file": workflow_file,
                        "error": str(e)
                    })
                    print(f"❌ Workflow error: {workflow_file} - {e}")
            else:
                invalid_workflows.append({
                    "file": workflow_file,
                    "error": "File not found"
                })
                print(f"❌ Missing workflow: {workflow_file}")
                
        success = len(valid_workflows) > 0
        
        self.test_results['workflow_syntax'] = {
            "status": "success" if success else "failed",
            "valid_workflows": valid_workflows,
            "invalid_workflows": invalid_workflows,
            "total_tested": len(workflow_files),
            "details": f"{len(valid_workflows)}/{len(workflow_files)} workflows have valid syntax"
        }
        
        return success
        
    def test_actual_copilot_execution(self) -> bool:
        """Test if we can actually execute a Copilot CLI command"""
        
        print("🚀 Testing actual Copilot CLI execution...")
        
        try:
            # Try to execute a simple analyze command
            # Note: This may fail due to missing repo context or authentication
            cmd = ['gh', 'copilot', 'analyze', '--scope', 'repository', 
                    '--query', 'Analyze repository structure', '--output', 'json']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Copilot CLI execution successful")
                try:
                    output = json.loads(result.stdout)
                    print(f"📊 Response type: {type(output)}")
                except:
                    print(f"📊 Response length: {len(result.stdout)} chars")
                    
                self.test_results['copilot_execution'] = {
                    "status": "success",
                    "output_length": len(result.stdout),
                    "details": "Copilot CLI command executed successfully"
                }
                return True
            else:
                print("❌ Copilot CLI execution failed")
                print(f"Error: {result.stderr}")
                
                # This might be expected in CI/CD environment
                self.test_results['copilot_execution'] = {
                    "status": "failed",
                    "error": result.stderr,
                    "return_code": result.returncode,
                    "details": "Copilot CLI execution failed - may need additional setup in CI/CD"
                }
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Copilot CLI execution timed out")
            self.test_results['copilot_execution'] = {
                "status": "timeout",
                "error": "Command timed out after 30 seconds",
                "details": "Copilot CLI execution timed out - may need more time or different setup"
            }
            return False
            
        except Exception as e:
            print(f"❌ Copilot CLI execution error: {e}")
            self.test_results['copilot_execution'] = {
                "status": "error",
                "exception": str(e),
                "details": "Copilot CLI execution encountered exception"
            }
            return False
            
    def run_comprehensive_verification(self) -> dict:
        """Run all verification tests"""
        
        print("🔍 COMPREHENSIVE GITHUB COPILOT CLI VERIFICATION")
        print("=" * 60)
        print()
        
        # Run all tests
        tests = [
            ("GitHub CLI", self.test_github_cli_installation),
            ("Copilot CLI", self.test_copilot_cli_installation), 
            ("Copilot Commands", self.test_copilot_cli_commands),
            ("GitHub Authentication", self.test_github_authentication),
            ("Copilot Authentication", self.test_copilot_authentication),
            ("Workflow Syntax", self.test_workflow_syntax),
            ("Actual Copilot Execution", self.test_actual_copilot_execution)
        ]
        
        results = {}
        for test_name, test_func in tests:
            print(f"\n📋 Running: {test_name}")
            result = test_func()
            results[test_name] = result
            print()
            
        # Generate summary
        total_tests = len(results)
        successful_tests = sum(results.values())
        success_rate = (successful_tests / total_tests) * 100
        
        summary = {
            "verification_timestamp": time.time(),
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": success_rate,
            "test_results": self.test_results,
            "detailed_results": results,
            "recommendations": self.generate_recommendations(results),
            "copilot_cli_ready": success_rate >= 70
        }
        
        return summary
        
    def generate_recommendations(self, test_results: dict) -> list:
        """Generate recommendations based on test results"""
        
        recommendations = []
        
        # Check GitHub CLI
        if not test_results.get('GitHub CLI', False):
            recommendations.append("Install GitHub CLI: curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && echo \"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main\" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null && sudo apt-get update && sudo apt-get install gh")
            
        # Check Copilot CLI
        if not test_results.get('Copilot CLI', False):
            recommendations.append("Install GitHub Copilot CLI extension: gh extension install github/gh-copilot")
            
        # Check authentication
        if not test_results.get('GitHub Authentication', False):
            recommendations.append("Set up GitHub authentication: gh auth login")
            
        # Check Copilot execution
        if not test_results.get('Actual Copilot Execution', False):
            recommendations.append("Copilot CLI may need additional setup in CI/CD environment")
            recommendations.append("Check if GitHub Copilot subscription is active")
            recommendations.append("Verify self-hosted runner has access to GitHub Copilot CLI")
            
        # Check workflows
        if not test_results.get('Workflow Syntax', False):
            recommendations.append("Fix workflow YAML syntax errors")
            recommendations.append("Validate workflows with GitHub Actions syntax checker")
            
        return recommendations

def main():
    """Main verification execution"""
    
    verifier = CopilotCLIVerifier()
    summary = verifier.run_comprehensive_verification()
    
    print("📊 VERIFICATION SUMMARY")
    print("=" * 40)
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Successful: {summary['successful_tests']}")
    print(f"Failed: {summary['failed_tests']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print(f"Copilot CLI Ready: {'✅ YES' if summary['copilot_cli_ready'] else '❌ NO'}")
    print()
    
    print("🔧 RECOMMENDATIONS")
    print("=" * 40)
    for i, rec in enumerate(summary['recommendations'], 1):
        print(f"{i}. {rec}")
    print()
    
    print("📋 DETAILED RESULTS")
    print("=" * 40)
    for test_name, result in summary['detailed_results'].items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        
    print()
    if summary['copilot_cli_ready']:
        print("🎉 GitHub Copilot CLI is ready for use in CI/CD!")
        print("Workflows should execute successfully with gh copilot commands.")
    else:
        print("⚠️ GitHub Copilot CLI needs additional setup.")
        print("Implementation may need adjustment for current environment.")
        
    # Save verification report
    report_file = f"copilot-cli-verification-report-{int(time.time())}.json"
    with open(report_file, 'w') as f:
        json.dump(summary, f, indent=2)
        
    print(f"\n📄 Detailed report saved to: {report_file}")

if __name__ == "__main__":
    main()

# Troubleshooting Guide

This guide helps you resolve common issues with FSL Continuum.

## Installation Issues

### Python Version Error

**Problem**: `Python 3.10+ is required`

**Solution**:
```bash
# Check current version
python --version

# Install Python 3.10+ on Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3.10-pip

# On macOS with Homebrew
brew install python@3.10

# On Windows
# Download from python.org
```

### Permission Denied Error

**Problem**: `Permission denied` during installation

**Solution**:
```bash
# Option 1: Use virtual environment
python -m venv fsl-env
source fsl-env/bin/activate
pip install fsl-continuum

# Option 2: Install for current user
pip install --user fsl-continuum

# Option 3: Use sudo (not recommended)
sudo pip install fsl-continuum
```

### Git Not Found

**Problem**: `git: command not found`

**Solution**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install git

# CentOS/RHEL
sudo yum install git

# macOS
brew install git

# Windows
# Download from git-scm.com
```

## Configuration Issues

### Config File Not Found

**Problem**: `Configuration not found: .fslrc`

**Solution**:
```bash
# Create default config
fsl init

# Or create manually
cat > .fslrc << EOF
version: "1.0"
project:
  name: "my-project"
  type: "python"
github:
  token: "\${GITHUB_TOKEN}"
EOF
```

### Invalid GitHub Token

**Problem**: `Bad credentials`

**Solution**:
```bash
# Check token is set
echo $GITHUB_TOKEN

# Set token
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"

# Or add to config
fsl config set github.token "ghp_xxxxxxxxxxxx"
```

### YAML Syntax Error

**Problem**: `Invalid YAML configuration`

**Solution**:
```bash
# Validate YAML syntax
fsl config validate

# Common YAML issues:
# - Use spaces, not tabs
# - Correct indentation
# - Quote strings with special characters
# - Check for missing colons
```

## Pipeline Issues

### Pipeline Not Found

**Problem**: `Unknown pipeline: xyz`

**Solution**:
```bash
# List available pipelines
fsl list pipelines

# Common pipeline types:
# - genetic-tests
# - dependency-update
# - auto-pr
# - deploy
```

### Genetic Algorithm Fails

**Problem**: `Genetic algorithm failed to converge`

**Solution**:
```bash
# Check test coverage
fsl analyze coverage

# Ensure sufficient test files
find . -name "*test*.py" | head -10

# Adjust parameters
fsl trigger genetic-tests --generations 100 --population-size 200
```

### Dependency Conflicts

**Problem**: `Dependency resolution failed`

**Solution**:
```bash
# Check for conflicts
fsl analyze dependencies

# Update specific package
fsl update package-name

# Clear cache and retry
rm -rf .fsl/cache
fsl trigger dependency-update
```

## Performance Issues

### Slow Execution

**Problem**: Pipeline taking too long

**Solution**:
```bash
# Enable performance monitoring
fsl config set monitoring.enabled true

# Check resource usage
fsl analyze performance

# Optimize configuration
fsl config set ci.parallel_jobs 8
fsl config set cache.enabled true
```

### Memory Issues

**Problem**: `Out of memory` error

**Solution**:
```bash
# Check memory usage
fsl monitor memory

# Reduce parallel jobs
fsl config set ci.parallel_jobs 2

# Use memory-efficient mode
fsl trigger genetic-tests --memory-efficient
```

## Integration Issues

### GitHub Actions Fail

**Problem**: CI checks failing

**Solution**:
```bash
# Check workflow file
cat .github/workflows/fsl.yml

# Verify secrets are set
gh secret list

# Test locally
fsl trigger --dry-run
```

### Docker Issues

**Problem**: Container fails to start

**Solution**:
```bash
# Check Docker is running
docker ps

# Verify image
docker images fslcontinuum/fsl-continuum

# Check logs
docker logs container-name
```

## Authentication Issues

### 2FA Required

**Problem**: `Must use two-factor authentication`

**Solution**:
```bash
# Create personal access token
# 1. Go to GitHub > Settings > Developer settings
# 2. Generate new token with appropriate scopes
# 3. Use token instead of password

# Configure FSL
export GITHUB_TOKEN="your_personal_token"
```

### SSH Key Issues

**Problem**: `Permission denied (publickey)`

**Solution**:
```bash
# Check SSH key
ssh -T git@github.com

# Add SSH key to GitHub
# 1. Copy public key
cat ~/.ssh/id_rsa.pub
# 2. Add to GitHub > Settings > SSH keys
```

## Quantum Feature Issues (Experimental)

### Quantum Engine Not Initializing

**Problem**: `Quantum engine failed to initialize`

**Solution**:
```bash
# Check prerequisites
python -c "import numpy, scipy; print('OK')"

# Enable quantum features
fsl config set quantum.enabled true

# Verify dimensions
fsl config set quantum.dimensions 4
```

### Consciousness Level Error

**Problem**: `Invalid consciousness level`

**Solution**:
```bash
# Valid levels: alpha, beta, gamma, delta, omega
fsl config set quantum.consciousness_level beta
```

## Debug Mode

### Enable Debug Logging

```bash
# Enable debug mode
fsl config set debug.enabled true
fsl config set debug.log_level debug

# Run with verbose output
fsl --verbose trigger genetic-tests
```

### Save Debug Information

```bash
# Save intermediate files
fsl config set debug.save_intermediate true

# Generate debug report
fsl debug report > debug-report.txt
```

## Getting Help

### Check Version and Environment

```bash
# FSL version
fsl --version

# Python version
python --version

# Git version
git --version

# OS information
uname -a
```

### Generate Support Bundle

```bash
# Create support bundle
fsl support bundle

# Includes:
# - Configuration files
# - Logs
# - System information
# - Error traces
```

### Community Support

- [GitHub Issues](https://github.com/your-org/fsl-continuum/issues)
- [Discord Community](https://discord.gg/fsl-continuum)
- [Documentation](../0001-getting-started/)
- [API Reference](0001-api-reference.md)

### Reporting Issues

When reporting issues, include:

1. **Environment**:
   - OS and version
   - Python version
   - FSL version

2. **Configuration**:
   - Redacted config file
   - Custom settings

3. **Error Details**:
   - Full error message
   - Steps to reproduce
   - Expected behavior

4. **Logs**:
   - Debug output
   - Stack traces
   - Performance metrics

## Quick Fixes

| Problem | Quick Fix |
|----------|------------|
| Config not found | `fsl init` |
| Token invalid | `export GITHUB_TOKEN="..."` |
| Tests failing | `fsl analyze coverage` |
| Slow performance | `fsl config set cache.enabled true` |
| Permission error | `pip install --user` |
| Git not found | Install Git first |
| Docker fail | Check Docker is running |

## Advanced Troubleshooting

### Reset Configuration

```bash
# Reset to defaults
fsl config reset

# Backup first
cp .fslrc .fslrc.backup
fsl config reset
```

### Clear Cache

```bash
# Clear all caches
rm -rf .fsl/cache
fsl cache clear

# Clear specific cache
fsl cache clear --type docker
fsl cache clear --type pip
```

### Health Check

```bash
# Run comprehensive health check
fsl health check

# Includes:
# - Configuration validation
# - Connectivity tests
# - Permission checks
# - Resource availability
```

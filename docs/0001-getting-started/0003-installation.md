# Installation Guide

This guide will help you install and set up FSL Continuum on your system.

## Prerequisites

- **Python 3.10+** (for latest features)
- **Git 2.30+** (for source control integration)
- **Docker** (optional, for containerized runners)
- **GitHub Account** (for repository integration)

## Standard Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-org/fsl-continuum.git
cd fsl-continuum
```

### 2. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

### 3. Install FSL Continuum

```bash
# Install in development mode (recommended for contributors)
pip install -e .

# Or install from PyPI (when available)
pip install fsl-continuum
```

### 4. Verify Installation

```bash
fsl --version
```

## Quick Setup with Installer

For a faster, one-command setup:

```bash
# Download and run installer
curl -sSL https://install.fsl-continuum.sh | bash

# Or download first
wget https://install.fsl-continuum.sh
chmod +x install.fsl-continuum.sh
./install.fsl-continuum.sh
```

## Docker Installation

```bash
# Pull the image
docker pull fslcontinuum/fsl-continuum:latest

# Run with mounted volume
docker run -v $(pwd):/workspace fslcontinuum/fsl-continuum:latest
```

## Development Setup

If you plan to contribute to FSL Continuum:

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/fsl-continuum.git
cd fsl-continuum

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Install in development mode
pip install -e .

# 5. Set up pre-commit hooks
pre-commit install
```

## Configuration

FSL Continuum looks for configuration in this order:

1. `./.fslrc` (project-specific)
2. `~/.fsl/config.yml` (user-specific)
3. `/etc/fsl/config.yml` (system-wide)

### Basic Configuration

```yaml
# ~/.fsl/config.yml
github:
  token: your_github_token
  default_branch: main

ci:
  platform: github
  cache_enabled: true
  
ai:
  model: gpt-4
  temperature: 0.7
```

## Next Steps

1. [Quick Start Guide](0002-quick-start.md) - Run your first pipeline
2. [User Guides](../0002-guides/) - Learn advanced features
3. [Architecture](../0003-architecture/) - Understand the system

## Troubleshooting

### Common Issues

**Python version error**: Ensure you're using Python 3.10 or higher
```bash
python --version  # Should show 3.10.x or higher
```

**Permission denied**: Use virtual environment or install with user flag
```bash
pip install --user -e .
```

**Git not found**: Install Git first
```bash
# Ubuntu/Debian
sudo apt-get install git

# macOS
brew install git

# Windows
# Download from git-scm.com
```

### Getting Help

- Check [Common Issues](../0005-reference/0003-troubleshooting.md)
- Open an issue on GitHub
- Join our Discord community

# Contributing to FSL Continuum

We love your input! We want to make contributing to FSL Continuum as easy and transparent as possible, whether it's:

- 🐛 A bug report
- 🚀 A feature request  
- 📚 Documentation improvements
- 🧬 A genetic algorithm optimization
- 🌊 A flow state enhancement

## 🚀 Quick Start for Contributors

### Prerequisites

- Python 3.10+
- Git 2.30+
- GitHub account (for PRs)

### Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/fsl-continuum.git
cd fsl-continuum

# 2. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Install in development mode
pip install -e .

# 4. Set up pre-commit hooks
pre-commit install
```

## 📝 How to Contribute

### 🐛 Reporting Bugs

1. Use the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md)
2. Include:
   - OS and Python version
   - FSL Continuum version
   - Steps to reproduce
   - Expected vs actual behavior

### 🚀 Suggesting Features

1. Check [existing issues](https://github.com/your-org/fsl-continuum/issues)
2. Use the [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)
3. Describe the use case and problem it solves

### 📚 Documentation

- Fix typos: `docs/quick-start.md`
- Add examples: `examples/`
- API docs: `docs/api-reference.md`

### 🧬 Code Contributions

#### Coding Standards

We follow [PEP 8](https://pep8.org/) with these additions:

```python
# ✅ Good: Descriptive names
def calculate_terminal_velocity(developer_productivity: float, context_switches: int) -> float:
    """Calculate terminal velocity metric."""
    return developer_productivity / (1 + context_switches)

# ❌ Bad: Unclear abbreviations
def calc_tv(dp: float, cs: int) -> float:
    return dp / (1 + cs)
```

#### Testing

All contributions must include tests:

```bash
# Run tests
pytest tests/unit/ -v

# Run with coverage
pytest --cov=src tests/unit/

# Run integration tests
pytest tests/integration/ -v
```

#### Git Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make changes and commit
git commit -m "feat: add terminal velocity calculation"

# 3. Push and create PR
git push origin feature/your-feature-name
# Then create Pull Request on GitHub
```

### 🎨 Contribution Areas

We welcome contributions in all areas:

#### 🌊 Core FSL Engine
- Terminal velocity algorithms
- State management optimizations
- AI orchestration improvements

#### 🤖 AI-Native Features
- Genetic algorithm enhancements
- ML model optimizations
- Quantum field manipulations

#### 🌍 4-Market Integration
- US innovation patterns
- Chinese scale optimizations
- Indian quality standards
- Japanese craftsmanship principles

#### 🛠️ Tooling & Integration
- GitHub Actions workflows
- Copilot integration features
- Schematics native engine

#### 📚 Documentation & Examples
- Architecture explanations
- Quick start guides
- Real-world usage examples

## 🤝 Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

## 📋 Review Process

1. **Automated Checks**: CI/CD runs tests and quality gates
2. **Code Review**: Maintainer review for architecture and standards
3. **DAO Vote**: For major features (Ringi consensus)
4. **Merge**: When all checks pass and consensus achieved

## 🏆 Recognition

All contributors are recognized in:
- README.md contributors section
- CHANGELOG.md release notes
- Annual contributor highlights

## 🚀 Get Started

Ready to contribute? 

1. Pick an [issue](https://github.com/your-org/fsl-continuum/issues)
2. Create a discussion for questions
3. Open a PR for your changes

Thank you for helping make FSL Continuum better! 🌊

---

*"The best CI/CD is the one we build together."*

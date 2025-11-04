"""
FSL Continuum Setup Script

Legacy setup script for compatibility with older pip versions and build systems.
New installations should use pyproject.toml (PEP 517/518).
"""

from setuptools import setup, find_packages
import os

# Read version from pyproject.toml
def get_version():
    try:
        with open('pyproject.toml', 'r') as f:
            content = f.read()
            for line in content.split('\n'):
                if line.startswith('version = '):
                    return line.split('=')[1].strip().strip('"\'')
    except FileNotFoundError:
        pass
    
    # Fallback version
    return "3.0.0"

# Read requirements
def get_requirements():
    requirements = []
    try:
        with open('requirements.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
    except FileNotFoundError:
        pass
    
    return requirements

# Read long description
def get_long_description():
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Terminal Velocity CI/CD with persistent state and AI-native features"

# Get package data
def get_package_data():
    package_data = {
        '': [
            'LICENSE',
            'README.md',
            'CHANGELOG.md',
            'CONTRIBUTING.md',
            'SECURITY.md',
            'CODE_OF_CONDUCT.md',
            'requirements.txt',
            'requirements-dev.txt',
            'pyproject.toml',
            'setup.py',
        ],
        'docs': [
            '*.md',
            '*.yaml',
            '*.yml',
            '*.json',
        ],
        'config': [
            '*.json',
            '*.yaml',
            '*.yml',
        ],
    }
    
    # Add all files recursively
    for root, dirs, files in os.walk('src'):
        for file in files:
            if not file.endswith('.pyc'):
                rel_path = os.path.relpath(os.path.join(root, file), 'src')
                package_data[''].append(rel_path)
    
    return package_data

# Setup configuration
setup(
    name='fsl-continuum',
    version=get_version(),
    description='Terminal Velocity CI/CD with persistent state and AI-native features',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='FSL Continuum Team',
    author_email='team@fsl-continuum.org',
    maintainer='FSL Continuum Team',
    maintainer_email='team@fsl-continuum.org',
    url='https://github.com/your-org/fsl-continuum',
    project_urls={
        'Documentation': 'https://github.com/your-org/fsl-continuum/docs',
        'Source': 'https://github.com/your-org/fsl-continuum',
        'Tracker': 'https://github.com/your-org/fsl-continuum/issues',
        'Changelog': 'https://github.com/your-org/fsl-continuum/blob/main/CHANGELOG.md',
        'Discussions': 'https://github.com/your-org/fsl-continuum/discussions',
    },
    license='MIT',
    license_files=('LICENSE',),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Software Distribution',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Framework :: Flask',
        'Framework :: Pydantic',
        'Natural Language :: English',
    ],
    keywords=[
        'ci-cd',
        'devops', 
        'terminal-velocity',
        'flow-state',
        'persistent-state',
        'ai-native',
        'quantum-computing',
        'blockchain',
        '4-market-integration',
        'baml',
        'pareto-lang',
        'xml-transformation',
        'semantic-languages',
    ],
    python_requires='>=3.9',
    install_requires=get_requirements(),
    packages=find_packages(where='src', exclude=['tests*']),
    package_dir={'': 'src'},
    package_data=get_package_data(),
    data_files=[
        ('share/fsl-continuum/docs', ['docs/*.md']),
        ('share/fsl-continuum/config', ['config/*.json', 'config/*.yaml', 'config/*.yml']),
        ('share/fsl-continuum/examples', ['examples/*.py', 'examples/*.yaml', 'examples/*.md']),
    ],
    entry_points={
        'console_scripts': [
            'fsl=fsl_continuum.cli:main',
            'fsl-continuum=fsl_continuum.cli:main',
            'fsl-trigger=fsl_continuum.cli.trigger_cli:main',
            'fsl-monitor=fsl_continuum.cli.monitor_cli:main',
            'fsl-config=fsl_continuum.cli.config_cli:main',
        ],
        'gui_scripts': [
            'fsl-desktop=fsl_continuum.desktop.app:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    platforms=['any'],
    test_suite='tests',
    tests_require=[
        'pytest>=7.2.0',
        'pytest-asyncio>=0.21.0',
        'pytest-cov>=4.1.0',
        'pytest-mock>=3.10.0',
    ],
    extras_require={
        'dev': [
            'black>=23.0.0',
            'isort>=5.12.0',
            'flake8>=6.0.0',
            'mypy>=1.4.0',
            'pre-commit>=3.4.0',
        ],
        'docs': [
            'mkdocs>=1.5.0',
            'mkdocs-material>=9.1.0',
            'mkdocstrings[python]>=0.21.0',
        ],
        'test': [
            'pytest>=7.2.0',
            'pytest-asyncio>=0.21.0',
            'pytest-cov>=4.1.0',
            'pytest-mock>=3.10.0',
            'factory-boy>=3.3.0',
            'faker>=18.9.0',
            'httpx>=0.24.0',
        ],
        'ai': [
            'openai>=0.27.0',
            'anthropic>=0.3.0',
            'transformers>=4.21.0',
            'torch>=2.0.0',
            'numpy>=1.24.0',
            'scikit-learn>=1.3.0',
            'pandas>=2.0.0',
        ],
        'quantum': [
            'qiskit>=0.43.0',
            'cirq>=1.0.0',
            'sympy>=1.12',
        ],
        'blockchain': [
            'blockchain>=1.0.2',
            'cryptography>=3.4.0',
            'web3>=6.0.0',
        ],
        'monitoring': [
            'prometheus-client>=0.14.0',
            'grafana-api>=1.0.3',
            'psutil>=5.9.0',
            'sentry-sdk>=1.15.0',
        ],
    },
    project_urls={
        'Documentation': 'https://fsl-continuum.readthedocs.io/',
        'Source': 'https://github.com/your-org/fsl-continuum',
        'Tracker': 'https://github.com/your-org/fsl-continuum/issues',
        'Changelog': 'https://github.com/your-org/fsl-continuum/blob/main/CHANGELOG.md',
        'Discord': 'https://discord.gg/fsl-continuum',
    },
)

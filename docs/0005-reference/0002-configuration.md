# Configuration Reference

This document provides comprehensive configuration options for FSL Continuum.

## Configuration Sources

FSL Continuum loads configuration from multiple sources in priority order:

1. `.fslrc` (Project root)
2. `~/.fsl/config.yml` (User config)
3. `/etc/fsl/config.yml` (System config)
4. Environment variables
5. Command-line arguments

## Project Configuration

### Basic Project Setup

```yaml
# .fslrc
version: "1.0"
project:
  name: "my-awesome-project"
  type: "python"  # python, typescript, docker, microservice
  source_root: "src"
  test_root: "tests"
  build_root: "dist"
```

### Advanced Project Options

```yaml
project:
  # Custom paths
  source_paths:
    - "src"
    - "lib"
  test_paths:
    - "tests"
    - "spec"
  ignore_paths:
    - "*.min.js"
    - "dist/**"
  
  # Build configuration
  build:
    command: "npm run build"
    artifacts:
      - "dist/*"
  
  # Test configuration
  test:
    framework: "pytest"  # pytest, jest, mocha
    coverage:
      enabled: true
      threshold: 80
```

## GitHub Integration

### Repository Configuration

```yaml
github:
  # Authentication
  token: "${GITHUB_TOKEN}"  # Environment variable
  api_url: "https://api.github.com"
  
  # Repository
  owner: "my-org"
  repo: "my-repo"
  default_branch: "main"
  
  # Pull Request settings
  auto_merge: false
  require_review: true
  reviewers:
    - "team-leads"
```

### Branch Protection

```yaml
github:
  branch_protection:
    main:
      require_status_checks: true
      required_status_checks:
        - "ci/test"
        - "ci/quality"
        - "ci/security"
      enforce_admins: true
      restrictions: null
```

## CI/CD Pipeline

### Pipeline Configuration

```yaml
ci:
  # Platform
  platform: "github"  # github, gitlab, azure, jenkins
  cache_enabled: true
  parallel_jobs: 4
  
  # Stages
  stages:
    - name: "lint"
      command: "flake8 src/"
    - name: "test"
      command: "pytest --cov=src"
    - name: "build"
      command: "npm run build"
    - name: "security"
      command: "npm audit"
  
  # Artifact handling
  artifacts:
    retention_days: 30
    paths:
      - "dist/*"
      - "coverage/*"
```

### Deployment Strategy

```yaml
deployment:
  # Strategy type
  strategy: "progressive"  # progressive, rolling, blue-green, canary
  
  # Environments
  environments:
    - name: "staging"
      url: "https://staging.example.com"
      auto_promote: true
    - name: "production"
      url: "https://example.com"
      require_approval: true
  
  # Progressive deployment
  progressive:
    phases:
      - percentage: 10
        duration: "5m"
        monitor: true
      - percentage: 50
        duration: "15m"
        monitor: true
      - percentage: 100
        duration: "30m"
        monitor: true
```

## AI Configuration

### Language Model Settings

```yaml
ai:
  # Model configuration
  model: "gpt-4"  # gpt-3.5-turbo, gpt-4, claude-3
  temperature: 0.7
  max_tokens: 4096
  timeout: 30
  
  # Feature flags
  features:
    code_review: true
    test_generation: true
    documentation: true
    refactoring: true
  
  # API endpoints
  api_base: "https://api.openai.com/v1"
  api_version: "2023-06-01"
```

### Genetic Algorithms

```yaml
ai:
  genetic:
    # Test generation
    population_size: 100
    generations: 50
    mutation_rate: 0.1
    crossover_rate: 0.8
    
    # Fitness evaluation
    fitness_metrics:
      - "coverage"
      - "performance"
      - "complexity"
    
    # Selection strategy
    selection: "tournament"  # tournament, roulette, rank
    tournament_size: 5
```

## Quantum Features (Experimental)

### Quantum Field Configuration

```yaml
quantum:
  enabled: false  # Enable quantum features
  dimensions: 4
  field_type: "unified"
  
  # Consciousness levels
  consciousness_level: "beta"  # alpha, beta, gamma, delta, omega
  
  # Quantum gates
  gates:
    - "hadamard"
    - "cnot"
    - "phase"
  
  # Entanglement
  entanglement:
    enabled: false
    max_distance: 42
    fidelity_threshold: 0.95
```

## Monitoring & Analytics

### Performance Metrics

```yaml
monitoring:
  # Metrics collection
  enabled: true
  interval: 60  # seconds
  
  # Metrics to track
  metrics:
    - "build_time"
    - "test_duration"
    - "deployment_frequency"
    - "change_failure_rate"
  
  # DORA metrics
  dora:
    deployment_frequency: true
    lead_time_for_changes: true
    mean_time_to_recovery: true
    change_failure_rate: true
```

### Notifications

```yaml
notifications:
  # Channels
  slack:
    webhook_url: "${SLACK_WEBHOOK}"
    channel: "#ci-cd"
  discord:
    webhook_url: "${DISCORD_WEBHOOK}"
  email:
    enabled: true
    recipients:
      - "team@example.com"
  
  # Triggers
  on_success: true
  on_failure: true
  on_deployment: true
```

## Security Configuration

### Access Control

```yaml
security:
  # Authentication
  auth_required: true
  token_expiry: 86400  # seconds
  
  # Permissions
  rbac:
    enabled: true
    roles:
      - name: "admin"
        permissions: ["*"]
      - name: "developer"
        permissions: ["read", "execute"]
      - name: "viewer"
        permissions: ["read"]
```

### Vulnerability Scanning

```yaml
security:
  scanning:
    enabled: true
    tools:
      - "snyk"
      - "bandit"
      - "semgrep"
    
    # Schedule
    schedule: "0 2 * * *"  # Daily at 2 AM
    
    # Severity thresholds
    fail_on_severity:
      - "critical"
      - "high"
```

## Caching Configuration

### Cache Settings

```yaml
cache:
  enabled: true
  backend: "redis"  # redis, filesystem, memory
  
  # Redis configuration
  redis:
    host: "localhost"
    port: 6379
    db: 0
    ttl: 3600
    
  # Filesystem cache
  filesystem:
    path: ".fsl/cache"
    max_size: "1GB"
    cleanup_policy: "lru"
```

## Advanced Options

### Experimental Features

```yaml
experimental:
  # Beta features
  features:
    - "quantum_field_optimization"
    - "ai_consciousness_detection"
    - "real_time_collaboration"
  
  # Feature flags
  flags:
    quantum_enabled: false
    consciousness_enabled: false
    collab_enabled: true
```

### Debug Mode

```yaml
debug:
  enabled: false
  log_level: "debug"  # debug, info, warn, error
  verbose: true
  
  # Debug outputs
  show_stack_traces: true
  show_timing: true
  save_intermediate: false
```

## Environment Variables

All configuration values can be overridden with environment variables:

```bash
# Project
export FSL_PROJECT_NAME="my-project"
export FSL_PROJECT_TYPE="python"

# GitHub
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
export FSL_GITHUB_OWNER="my-org"

# AI
export FSL_AI_MODEL="gpt-4"
export FSL_AI_TEMPERATURE="0.7"

# Quantum
export FSL_QUANTUM_ENABLED="true"
export FSL_QUANTUM_DIMENSIONS="4"
```

## Validation

### Schema Validation

FSL validates configuration against JSON schema:

```bash
fsl config validate
```

### Test Configuration

Test your configuration without running pipelines:

```bash
fsl config test
```

### Common Issues

1. **Token not found**: Ensure `GITHUB_TOKEN` is set
2. **Invalid YAML**: Check indentation and syntax
3. **Permission denied**: Verify file permissions
4. **Cache errors**: Check Redis connection or disk space

## Migration Guide

When upgrading FSL versions, migrate your configuration:

```bash
# Backup current config
cp .fslrc .fslrc.backup

# Migrate to new version
fsl config migrate --from-version 3.0 --to-version 4.0
```

## More Information

- [API Reference](0001-api-reference.md)
- [Getting Started](../0001-getting-started/)
- [Troubleshooting](0003-troubleshooting.md)

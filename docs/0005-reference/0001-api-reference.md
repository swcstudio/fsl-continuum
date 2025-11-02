# API Reference

This section provides comprehensive API documentation for FSL Continuum.

## Core CLI Commands

### fsl

Main command-line interface for FSL Continuum.

```bash
fsl [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS]
```

#### Global Options

- `--config PATH`: Specify configuration file
- `--verbose`: Enable verbose output
- `--version`: Show version information

### Commands

#### trigger
Trigger automated CI/CD pipelines.

```bash
fsl trigger [PIPELINE_TYPE] [OPTIONS]
```

**Pipeline Types:**
- `genetic-tests`: Run genetic algorithm test generation
- `dependency-update`: Update project dependencies
- `auto-pr`: Create pull request from commits
- `deploy`: Deploy to staging/production

**Options:**
- `--generations N`: Number of genetic iterations (default: 50)
- `--target ENV`: Target environment (staging/production)
- `--dry-run`: Preview without execution

#### analyze
Analyze codebase and generate insights.

```bash
fsl analyze [ANALYSIS_TYPE] [OPTIONS]
```

**Analysis Types:**
- `performance`: Performance bottleneck analysis
- `security`: Security vulnerability scan
- `dependencies`: Dependency health check
- `quality`: Code quality metrics

#### config
Manage FSL configuration.

```bash
fsl config [get|set|list] [KEY] [VALUE]
```

#### init
Initialize FSL in project directory.

```bash
fsl init [TEMPLATE]
```

**Templates:**
- `python`: Python project template
- `typescript`: TypeScript/Node.js template
- `docker`: Docker-based project
- `microservice`: Microservice template

## Python API

### Core Classes

#### FSLContinuum

Main orchestrator class for FSL operations.

```python
from fsl_continuum import FSLContinuum

# Initialize
fsl = FSLContinuum(config_path=".fslrc")

# Trigger pipeline
result = fsl.trigger("genetic-tests", generations=100)
```

#### GeneticTestEngine

Manages genetic algorithm-based test generation.

```python
from fsl_continuum import GeneticTestEngine

engine = GeneticTestEngine()
engine.evolve(generations=50, population_size=100)
```

#### DependencyUpdater

Automated dependency management.

```python
from fsl_continuum import DependencyUpdater

updater = DependencyUpdater()
updates = updater.check_for_updates()
updater.apply_updates(updates)
```

## Configuration

### Configuration File Format

FSL uses YAML configuration files.

```yaml
# .fslrc
version: "1.0"
project:
  name: "my-project"
  type: "python"
  
github:
  token: "${GITHUB_TOKEN}"
  owner: "my-org"
  repo: "my-repo"
  
ci:
  platform: "github"
  cache_enabled: true
  parallel_jobs: 4
  
ai:
  model: "gpt-4"
  temperature: 0.7
  max_tokens: 4096
  
quantum:
  enabled: false
  dimensions: 4
  consciousness_level: "alpha"
  
deployment:
  strategy: "progressive"
  environments:
    - staging
    - production
  gates:
    - quality_check
    - security_scan
    - performance_test
```

### Environment Variables

- `FSL_CONFIG_PATH`: Path to configuration file
- `GITHUB_TOKEN`: GitHub API token
- `FSL_LOG_LEVEL`: Logging level (debug/info/warn/error)
- `FSL_CACHE_DIR`: Cache directory path

## Events and Hooks

### Pre-trigger Hooks

Execute before pipeline triggers:

```python
def pre_trigger_hook(pipeline_type, options):
    print(f"Starting {pipeline_type} pipeline")
    # Custom logic here
    return options
```

### Post-trigger Hooks

Execute after pipeline completion:

```python
def post_trigger_hook(result):
    if result.success:
        notify_success(result)
    else:
        notify_failure(result)
```

## Error Codes

| Code | Description | Resolution |
|-------|-------------|------------|
| 1001 | Configuration not found | Create .fslrc file |
| 1002 | Invalid GitHub token | Check GITHUB_TOKEN env var |
| 1003 | Pipeline not found | Verify pipeline type |
| 2001 | Genetic algorithm failed | Check test coverage |
| 2002 | Dependency conflict | Review requirements.txt |
| 3001 | Deployment failed | Check deployment gates |

## SDKs

### Python SDK

```python
from fsl_continuum import FSL, Pipeline

# Using SDK
fsl = FSL(token="your-token")

# Create custom pipeline
pipeline = fsl.create_pipeline("custom")
pipeline.add_step("build", command="npm run build")
pipeline.add_step("test", command="npm test")
pipeline.execute()
```

### JavaScript/TypeScript SDK

```typescript
import { FSLContinuum } from '@fsl/continuum-js';

const fsl = new FSLContinuum({
  token: process.env.GITHUB_TOKEN,
  config: './.fslrc'
});

await fsl.trigger('genetic-tests');
```

## Extensions

### Creating Custom Extensions

```python
from fsl_continuum import Extension

class MyExtension(Extension):
    def __init__(self):
        super().__init__("my-extension", "1.0.0")
    
    def execute(self, context):
        # Custom logic
        return result

# Register extension
fsl.register_extension(MyExtension())
```

## More Information

- [Getting Started Guide](../0001-getting-started/)
- [Architecture](../0003-architecture/)
- [User Guides](../0002-guides/)
- [Community](https://github.com/your-org/fsl-continuum/discussions)

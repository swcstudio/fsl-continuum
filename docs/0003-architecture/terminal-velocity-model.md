# Terminal Velocity Model

## Overview

The Terminal Velocity system in FSL Continuum uses a **growth-based model** where velocity increases over time, representing momentum building as the system operates continuously. This design is intuitive: **higher velocity values indicate better performance**.

## Key Concepts

### Growth-Based Velocity

Unlike traditional models where velocity decreases over time (inverse relationship), FSL Continuum's velocity **increases** with uptime:

```
velocity = BASE_VELOCITY + (uptime * acceleration)
```

This represents:
- **Momentum Building**: Longer runtime = higher velocity
- **Continuous Improvement**: System gets faster as it maintains state
- **Intuitive Metrics**: Higher numbers = better performance

### Flow State Multiplier

When the system enters "flow state" (optimal operation mode), velocity receives a **1.5x multiplier**:

```
if in_flow_state:
    velocity *= 1.5
```

This represents the productivity boost from uninterrupted, focused work.

## Configuration Parameters

### Acceleration Factor

Controls how quickly velocity grows over time:

```python
# Slow growth (0.5x)
tv = TerminalVelocity(acceleration=0.5)

# Normal growth (1.0x - default)
tv = TerminalVelocity()

# Fast growth (2.0x)
tv = TerminalVelocity(acceleration=2.0)
```

**Use cases:**
- **Low acceleration (0.1-0.5)**: Long-running services that need stable velocity
- **Normal acceleration (1.0)**: Standard CI/CD pipelines
- **High acceleration (2.0-10.0)**: Short-lived tasks that need quick ramp-up

### Maximum Velocity Cap

Prevents unbounded growth by capping velocity at a maximum value:

```python
# Cap at 50
tv = TerminalVelocity(max_velocity=50.0)

# Cap at 100 (default)
tv = TerminalVelocity()

# Cap at 500 (for high-performance scenarios)
tv = TerminalVelocity(max_velocity=500.0)
```

**Use cases:**
- **Low cap (10-50)**: Resource-constrained environments
- **Normal cap (100)**: Standard deployments
- **High cap (200-1000)**: High-performance computing, real-time systems

## API Reference

### Initialization

```python
from fsl_continuum.continuum.terminal_velocity import TerminalVelocity

# Use defaults
tv = TerminalVelocity()

# Custom configuration
tv = TerminalVelocity(
    acceleration=2.0,      # Faster velocity growth
    max_velocity=200.0     # Higher velocity cap
)
```

### Getting Velocity

```python
# Get current velocity
velocity = tv.get_velocity()
print(f"Current velocity: {velocity}")

# Get full status including configuration
status = tv.get_status()
print(f"Velocity: {status['velocity']}")
print(f"Uptime: {status['uptime']}")
print(f"Config: {status['config']}")
```

### Flow State Management

```python
# Enter flow state (1.5x velocity boost)
tv.enter_flow_state()

# Exit flow state
tv.exit_flow_state()
```

### Runtime Configuration

```python
# Update acceleration factor
tv.set_acceleration(5.0)

# Update max velocity cap
tv.set_max_velocity(300.0)

# Get current configuration
config = tv.get_config()
print(f"Acceleration: {config['acceleration']}")
print(f"Max velocity: {config['max_velocity']}")
```

## Example Scenarios

### Scenario 1: CI/CD Pipeline

```python
# Standard CI/CD with normal acceleration
tv = TerminalVelocity(acceleration=1.0, max_velocity=100.0)

# Start pipeline
tv.enter_flow_state()  # Enter flow for focused execution

# After 10 seconds of uptime
# velocity ≈ 1.0 + (10 * 1.0) = 11.0
# With flow state: 11.0 * 1.5 = 16.5
```

### Scenario 2: Long-Running Service

```python
# Stable, long-running service with slow growth
tv = TerminalVelocity(acceleration=0.1, max_velocity=50.0)

# After 100 seconds of uptime
# velocity ≈ 1.0 + (100 * 0.1) = 11.0
# Eventually caps at 50.0 for stability
```

### Scenario 3: High-Performance Batch Job

```python
# Fast ramp-up for batch processing
tv = TerminalVelocity(acceleration=10.0, max_velocity=500.0)

# After 5 seconds
# velocity ≈ 1.0 + (5 * 10.0) = 51.0
# Reaches high velocity quickly
```

## Velocity Interpretation

| Velocity Range | Interpretation | Typical Scenario |
|----------------|----------------|------------------|
| 0-10 | Starting up | Fresh start, < 10s uptime |
| 10-50 | Building momentum | Normal operation, stabilizing |
| 50-100 | High velocity | Sustained operation, flow state |
| 100+ | Terminal velocity | Maximum performance, capped |

## Migration from Legacy Model

The legacy model used inverse velocity calculation:

```python
# OLD: velocity = 1.0 / uptime (decreases over time)
# NEW: velocity = base + (uptime * acceleration) (increases over time)
```

**Key differences:**
1. **Direction**: New model increases (not decreases) with time
2. **Intuitive**: Higher values = better performance
3. **Configurable**: Acceleration and cap are adjustable
4. **Flow state**: Explicit multiplier for flow state boost

**Backward compatibility**: The new model maintains the same API (`get_velocity()`), so existing code continues to work, but the semantics have changed to be more intuitive.

## Best Practices

1. **Choose appropriate acceleration** based on your use case:
   - Short tasks: Higher acceleration (2.0-10.0)
   - Long services: Lower acceleration (0.1-0.5)

2. **Set realistic velocity caps** to prevent resource exhaustion:
   - Development: 100 (default)
   - Production: 200-500
   - Critical systems: Custom based on monitoring

3. **Use flow state** for focused execution:
   - Enter flow state during critical operations
   - Exit flow state during idle/maintenance periods

4. **Monitor velocity trends** over time:
   - Velocity should grow steadily
   - Sudden drops indicate issues
   - Caps being hit indicate optimization opportunities

## Related Documentation

- [System Architecture](0001-system-architecture.md)
- [State Management](../../src/fsl_continuum/continuum/state_management.py)
- [Metrics Collection](../../src/fsl_continuum/continuum/metrics.py)

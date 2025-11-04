# Terminal Velocity Quick Reference

## Basic Usage

```python
from fsl_continuum.continuum.terminal_velocity import TerminalVelocity

# Create instance
tv = TerminalVelocity()

# Get velocity (increases over time)
velocity = tv.get_velocity()

# Enter flow state (1.5x boost)
tv.enter_flow_state()

# Exit flow state
tv.exit_flow_state()
```

## Configuration

```python
# Custom acceleration and max velocity
tv = TerminalVelocity(
    acceleration=2.0,      # Faster growth
    max_velocity=200.0     # Higher cap
)

# Change at runtime
tv.set_acceleration(5.0)
tv.set_max_velocity(300.0)

# View configuration
config = tv.get_config()
```

## Velocity Formula

```
velocity = BASE_VELOCITY + (uptime * acceleration)

If in flow state:
    velocity *= 1.5

Final velocity = min(velocity, max_velocity)
```

## Default Values

- `BASE_VELOCITY`: 1.0
- `DEFAULT_ACCELERATION`: 1.0
- `DEFAULT_MAX_VELOCITY`: 100.0
- `FLOW_STATE_MULTIPLIER`: 1.5

## Key Principle

**Higher velocity = Better performance**

Velocity increases as the system runs longer, representing momentum building. This is intuitive and easy to understand.

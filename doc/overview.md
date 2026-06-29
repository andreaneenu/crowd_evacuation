# Crowd Evacuation Simulation — Code Overview

## What this project does

Simulates emergency crowd evacuation using the **Social Force Model (SFM)**, a physics-based
approach where agents are treated as particles subject to psychological and physical forces.
Agents navigate toward an exit while avoiding walls, circular obstacles, and each other.

Based on: https://github.com/fschur/Evacuation-Bottleneck

---

## File Structure

| File | Role |
|------|------|
| `running_code.py` | Entry point — configure and launch a simulation |
| `Simulation_class.py` | Orchestrator — holds all state, wires components together |
| `Room.py` | Room geometry — walls, doors, spawn zones, destinations |
| `diff_equation.py` | Social Force Model — computes per-agent accelerations |
| `Integrators.py` | Numerical integration — advances simulation forward in time |
| `steps_function_quit.py` | Visualization — pygame animation + matplotlib graphs |

---

## Execution Pipeline

```
running_code.py
  └─ Simulation(...)          # configure parameters
       ├─ Room(...)           # build room geometry (walls, door, spawn zone)
       └─ Diff_Equ(...)       # set up physics engine with SFM constants

  └─ sim.fill_room()          # place agents randomly in spawn zone (no-overlap check)
  └─ sim.run()                # run leap-frog integration over all timesteps
       └─ leap_frog(...)      # advance position/velocity each timestep
            └─ Diff_Equ.f()  # compute accelerations via SFM forces
  └─ sim.show(...)            # animate with pygame, save MP4 + graphs
```

---

## Social Force Model (diff_equation.py)

Each agent `i` has three force contributions:

1. **Driving force** — pulls agent toward the exit at desired speed `v_0 = 1.5 m/s`
2. **Agent–agent interaction** — exponential repulsion + sliding friction when agents overlap
3. **Wall/obstacle repulsion** — same exponential + friction model applied to walls and circular obstacles

Total acceleration at each step:

```
a_i = (v_0 * e_i - v_i) * 0.1 / tau  +  Σ_j f_ij / m_i  +  Σ_W f_iW / m_i  +  Σ_obs f_i_obs / m_i
```

### SFM Constants

| Constant | Value | Physical meaning |
|----------|-------|-----------------|
| `A` | 2000 N | Repulsion interaction strength |
| `B` | 0.08 m | Repulsion decay length |
| `k` | 1.2×10⁵ kg/s² | Body compression stiffness |
| `kap` | 2.4×10⁵ kg/(m·s) | Sliding friction coefficient |

---

## Agent Statuses (tracked per timestep in `status` array)

| Code | Meaning |
|------|---------|
| `4` | Pre-simulation settling phase (~0.7 s; agents placed but not moving toward exit) |
| `1` | Alive and moving toward the exit |
| `3` | Reached exit zone; waiting `delay` seconds before collecting |
| `2` | Collected / escaped (moves away from crowd) |
| `0` | Dead — pressure on agent exceeded threshold (`pressure > 10800`) |

---

## Numerical Integration — Leap-Frog (Integrators.py)

Leap-frog is a symplectic (energy-conserving) integrator. The velocity is staggered by half a timestep:

```
v[k+0.5] = v[k-0.5] + dt * a[k]     # velocity at half-step
y[k+1]   = y[k]     + dt * v[k+0.5] # position at full step
```

This gives better long-term stability than Euler at the same computational cost.
The integrator also handles:
- **Escape detection**: agent enters `collection_radius` → status `3` → countdown → status `2`
- **Pressure-based death**: cumulative force per unit radius exceeds threshold → status `0`

---

## Obstacle Placement (Simulation_class.py)

Circular obstacles are placed in front of the exit, symmetrically around the room's vertical midline:

```
# 2-obstacle config
center_x = collection_radius + obs_dis + obs_rad
center_y = room_size/2 ± (obs_gap/2 + obs_rad)
```

This creates a **bottleneck**: agents must squeeze through the gap between the two obstacles to reach the exit, which leads to crowd pressure buildup and potential deaths.

---

## Room Types (Room.py)

| Room | Description |
|------|-------------|
| `square` | Open square room, one exit on the left wall (x=0) |
| `long_room` | Narrow rectangle (5× longer than wide), one exit on the left |
| `long_room_v2` | Same rectangle but exits on both ends; agents split between them |
| `edu_1` | Square with one vertical internal wall (partial obstruction) |
| `edu_room` | Square with two diagonal internal walls forming a funnel |

Walls are stored as arrays of endpoint pairs `[[x1,y1], [x2,y2]]`.

---

## Key Parameters

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `num_individuals` | 40 | Number of agents |
| `total_time` | 24 s | Simulation duration |
| `tau` | 0.02 s | Timestep (smaller = more accurate, slower) |
| `room_size` | 11 m | Square room side length |
| `num_obs` | 2 | Number of circular obstacles (0, 1, or 2) |
| `obs_rad` | 1.2 m | Obstacle radius |
| `obs_gap` | 2.2 m | Gap between two obstacles |
| `obs_dis` | 0.5 m | Obstacle distance from exit wall |
| `collection_radius` | 2 m | Radius of the exit collection zone |
| `delay` | 0.5 s | Time an agent waits at exit before escaping |

---

## Output

| Output | Description |
|--------|-------------|
| Pygame window | Real-time animation (color-coded by agent status) |
| `*recording.mp4` | Saved screen recording of the animation |
| `* graph.png` | Plot of escape count and death count over time |
| `death.txt` | Appends total dead count per run (for batch experiments) |

### Agent colors in visualization

| Color | Status |
|-------|--------|
| Red | Alive, moving to exit |
| Orange | Reached exit, waiting |
| Blue | Escaped |
| Lavender | Pre-simulation settling |
| Black | Dead |

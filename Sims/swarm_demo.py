#!/usr/bin/env python3
"""
Drone Force One: Swarm Demo Sim (CLI Mode)
Quick viz for spirals + pings. Tweak mode/drones below.
"""

import numpy as np
import matplotlib.pyplot as plt
from ai.core.swarm import SwarmCoordinator  # Assumes swarm.py in path

# Config (tweak here!)
mode = 'wildfire'  # Or 'earthquake', etc.
origin = (0, 0)
radius_km = 3
drones = 5

print("Swarm launching in {} mode...".format(mode))
coord = SwarmCoordinator(mode=mode)
spiral_points = coord.launch_spiral(origin, radius_km, drones)
print("Spiral points: {}".format(spiral_points))

# Plot the Spiral Coverage
fig, ax = plt.subplots(1, 1, figsize=(8, 8))
ax.set_xlim(-radius_km, radius_km)
ax.set_ylim(-radius_km, radius_km)
ax.set_title('Drone Force One: Fibonacci Spiral Launch')
ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')

# Plot points & path
x_points = [p[0] for p in spiral_points]
y_points = [p[1] for p in spiral_points]
ax.scatter(x_points, y_points, c='red', s=100, marker='^', label='Spotter Drones')
ax.plot([origin[0]] + x_points, [origin[1]] + y_points, 'b--', alpha=0.5, label='Spiral Path')

# Mock coverage (thermal radius)
for px, py in spiral_points:
    circle = plt.Circle((px, py), 0.5, color='orange', fill=False, alpha=0.3)
    ax.add_patch(circle)

ax.legend()
plt.grid(True, alpha=0.3)
plt.show(block=False)  # Non-blocking for multi-plot

# Simulate Ping Cascade & Heatmap
ping_coords = (1.2, 0.8)
heat_sig = 0.92  # Above threshold for cascade

ping_result = coord.handle_ping(ping_coords, heat_sig)
print("Ping result: {}".format(ping_result))

# Fake heatmap viz
x_grid, y_grid = np.meshgrid(np.linspace(-3, 3, 100), np.linspace(-3, 3, 100))
heat_map = np.exp(-((x_grid - ping_coords[0])**2 + (y_grid - ping_coords[1])**2) / (2 * 0.5**2))

fig2, ax2 = plt.subplots(1, 1, figsize=(8, 8))
im = ax2.imshow(heat_map, extent=[-3, 3, -3, 3], origin='lower', cmap='hot', alpha=0.8)
ax2.scatter(ping_coords[0], ping_coords[1], c='white', s=200, marker='*', label='Thermal Ping Hit')
ax2.set_title('Mock Thermal Heatmap: Ping Cascade Triggered')
ax2.set_xlabel('X (km)')
ax2.set_ylabel('Y (km)')
plt.colorbar(im, ax=ax2, label='Heat Intensity')
ax2.legend()
plt.grid(True, alpha=0.2)
plt.show()

print("Sim complete: Swarm covers ~{} km², pings locked—giggity!".format(np.pi * radius_km**2))

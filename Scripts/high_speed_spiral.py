# scripts/high_speed_spiral.py
# Multi-Drone High-Speed Coordination Sim
# Integrates real SwarmCoordinator + Archimedean bursts for Peregreen mode

import numpy as np
import matplotlib.pyplot as plt
import random
from ai.core.swarm import SwarmCoordinator
from swarm_handshake import check_battery

# Config
MODE = 'wildfire'
DRONES = 8
RADIUS_KM = 3.0

coord = SwarmCoordinator(mode=MODE)

plt.figure(figsize=(12, 12))

for drone_id in range(1, DRONES + 1):
    battery = check_battery(drone_id)
    if battery < 20:
        print(f"Drone-{drone_id}: Low battery - grounded")
        continue

    print(f"Drone-{drone_id}: Launching high-speed Archimedean burst")

    # Archimedean (offset per drone for multi-coverage)
    theta = np.linspace(0, 8 * np.pi, 1500) + (drone_id * np.pi / 4)  # Phase offset
    a = 0.05
    b = 0.7
    r = a + b * theta
    x = r * np.cos(theta) * 1000  # Meters
    y = r * np.sin(theta) * 1000

    plt.plot(x, y, linewidth=1.5, label=f'Drone-{drone_id} Path' if drone_id <= 3 else "")

    # Victims (shared)
    if drone_id == 1:
        victims = [(random.uniform(-2000, 2000), random.uniform(-2000, 2000)) for _ in range(7)]
        detected_global = []
        plt.scatter([v[0] for v in victims], [v[1] for v in victims], c='orange', s=120, label='Hidden Victims')

    # Detection
    detected = []
    for vx, vy in victims:
        dist = np.sqrt((x - vx)**2 + (y - vy)**2)
        if np.min(dist) < 600:
            detected.append((vx, vy))
            detected_global.append((vx, vy))
            print(f"Drone-{drone_id}: Victim detected!")

    if detected:
        plt.scatter([d[0] for d in detected], [d[1] for d in detected], c='red', s=200, edgecolors='black')

plt.scatter(0, 0, c='g', s=400, marker='*', label='Backpack Hive')
plt.title('Drone Force One: Multi-Drone High-Speed Archimedean Coordination')
plt.xlabel('Meters')
plt.ylabel('Meters')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.axis('equal')
plt.tight_layout()
plt.show()

print(f"Swarm search complete: {len(set(detected_global))} unique victims located.")

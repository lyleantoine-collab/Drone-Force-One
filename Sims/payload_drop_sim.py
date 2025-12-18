# sims/payload_drop_sim.py
# Payload Drop Simulation for Disaster Scenarios
# Integrates SwarmCoordinator for mode + spirals, battery check, multi-drone coordination

import numpy as np
import matplotlib.pyplot as plt
import random
from ai.core.swarm import SwarmCoordinator, EMERGENCY_MODES
from swarm_handshake import check_battery

# Config
MODE = 'flood'  # 'flood', 'tornado', 'wildfire', 'missing_persons'
DRONES = 10  # 7 scouts + 3 haulers
RADIUS_M = 2000  # Search radius

coord = SwarmCoordinator(mode=MODE)
payload = EMERGENCY_MODES[MODE]['payload']  # Mode-specific drop (e.g., 'life vests')

# Simulate victims/targets
victims = [(random.uniform(-RADIUS_M, RADIUS_M), random.uniform(-RADIUS_M, RADIUS_M)) for _ in range(5)]

plt.figure(figsize=(12, 12))

scout_paths = []
hauler_drops = []
detected = []

for drone_id in range(1, DRONES + 1):
    battery = check_battery(drone_id)
    if battery < 20:
        print(f"Drone-{drone_id}: Low battery - grounded")
        continue

    is_hauler = drone_id > 7  # Last 3 are dedicated haulers

    if is_hauler:
        print(f"Hauler-{drone_id}: On standby for drop queue")
        continue

    print(f"Scout-{drone_id}: Launching high-speed Archimedean search")

    # Archimedean spiral (offset per scout)
    theta = np.linspace(0, 10 * np.pi, 1500) + (drone_id * np.pi / 3)
    a = 0.1
    b = 0.5
    r = a + b * theta
    x = r * np.cos(theta) * RADIUS_M / 10  # Scale
    y = r * np.sin(theta) * RADIUS_M / 10

    scout_paths.append((x, y))
    plt.plot(x, y, linewidth=1.2, label=f'Scout-{drone_id} Path' if drone_id <= 3 else "")

    # Detection
    for vx, vy in victims:
        dist = np.sqrt((x - vx)**2 + (y - vy)**2)
        if np.min(dist) < 400 and (vx, vy) not in detected:  # Avoid double-detect
            detected.append((vx, vy))
            print(f"Scout-{drone_id}: Target detected at ({vx:.0f}m, {vy:.0f}m) - queuing {payload} drop")
            # Sim drop: Hauler deploys to coord
            drop_x, drop_y = vx + random.uniform(-50, 50), vy + random.uniform(-50, 50)  # Hover offset
            hauler_drops.append((drop_x, drop_y))
            coord._queue_payload((vx, vy), payload)  # Use your queue

plt.scatter(0, 0, c='g', s=400, marker='*', label='Backpack Hive')
plt.scatter([v[0] for v in victims], [v[1] for v in victims], c='orange', s=120, label='Targets/Victims')
if detected:
    plt.scatter([d[0] for d in detected], [d[1] for d in detected], c='red', s=200, edgecolors='black', label=f'Detected ({len(detected)})')
if hauler_drops:
    plt.scatter([h[0] for h in hauler_drops], [h[1] for h in hauler_drops], c='blue', s=150, marker='x', label='Payload Drops')

plt.title(f'Drone Force One: Multi-Drone Payload Drop Sim ({MODE.capitalize()} Scenario)')
plt.xlabel('Meters')
plt.ylabel('Meters')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.axis('equal')
plt.tight_layout()
plt.show()

print(f"Sim complete: {len(detected)} targets located, {len(hauler_drops)} payloads deployed.")


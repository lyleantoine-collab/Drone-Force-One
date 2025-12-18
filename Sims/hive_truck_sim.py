# sims/hive_truck_sim.py
# Hive Truck Simulation: F350 Mod Utility Box Deployment
# Deploys signal boosters + scouts, chains signals, LAAT-inspired emergency sound cue

import numpy as np
import matplotlib.pyplot as plt
import random
from ai.core.swarm import SwarmCoordinator
from swarm_handshake import check_battery

# Config
MODE = 'flood'
TRUCK_POS = (0, 0)
RADIUS_M = 4000  # Expanded with boosters
SCOUTS = 6
BOOSTERS = 4  # Signal repeaters

coord = SwarmCoordinator(mode=MODE)

plt.figure(figsize=(12, 12))

# Simulate LAAT emergency sound cue
print("Hive Truck: EMERGENCY DEPLOY SOUND - [LAAT whine + roar] (WAV playback stub)")

deployed = []
chain_links = [TRUCK_POS]  # Signal chain starts at truck

for drone_id in range(1, BOOSTERS + SCOUTS + 1):
    is_booster = drone_id <= BOOSTERS
    role = 'Booster' if is_booster else 'Scout'

    battery = check_battery(drone_id)
    if battery < 20:
        print(f"{role}-{drone_id}: Low battery - stays in hive")
        continue

    print(f"{role}-{drone_id}: Deploying from F350 utility box")

    # Position: Boosters chain outward, scouts spiral from ends
    if is_booster:
        # Linear chain for signal boost
        offset = drone_id * (RADIUS_M / BOOSTERS)
        bx, by = TRUCK_POS[0] + offset, TRUCK_POS[1] + random.uniform(-200, 200)
        chain_links.append((bx, by))
        plt.scatter(bx, by, c='purple', s=250, marker='s', label=f'Booster-{drone_id}' if drone_id == 1 else "")
    else:
        # Scouts from last booster
        base = chain_links[-1]
        # Archimedean spiral from base
        theta = np.linspace(0, 6 * np.pi, 1000) + random.uniform(0, 2*np.pi)
        a = 0.1
        b = 0.4
        r = a + b * theta
        x = base[0] + r * np.cos(theta) * 500
        y = base[1] + r * np.sin(theta) * 500
        deployed.append((x, y))
        plt.plot(x, y, linewidth=1.2, label=f'Scout-{drone_id - BOOSTERS} Path' if (drone_id - BOOSTERS) <= 2 else "")

    # Victims (shared)
    if drone_id == 1:
        victims = [(random.uniform(-RADIUS_M, RADIUS_M), random.uniform(-RADIUS_M, RADIUS_M)) for _ in range(8)]
        detected = []
        plt.scatter([v[0] for v in victims], [v[1] for v in victims], c='orange', s=120, label='Targets')

# Detection (scouts only)
for x_path, y_path in deployed:
    for vx, vy in victims:
        dist = np.sqrt((x_path - vx)**2 + (y_path - vy)**2)
        if np.min(dist) < 400 and (vx, vy) not in detected:
            detected.append((vx, vy))
            print(f"Scout detected target - queuing payload drop")

plt.scatter(TRUCK_POS[0], TRUCK_POS[1], c='black', s=500, marker='o', label='F350 Hive Truck')
plt.plot([p[0] for p in chain_links], [p[1] for p in chain_links], 'm--', linewidth=2, label='Signal Chain')
if detected:
    plt.scatter([d[0] for d in detected], [d[1] for d in detected], c='red', s=200, edgecolors='black', label=f'Detected ({len(detected)})')

plt.title(f'Drone Force One: Hive Truck Deployment & Signal Boost Chain ({MODE.capitalize()})')
plt.xlabel('Meters')
plt.ylabel('Meters')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.axis('equal')
plt.tight_layout()
plt.show()

print(f"Expanded search complete: {len(detected)} targets located over boosted radius.")

import numpy as np
import matplotlib.pyplot as plt

# Archimedean spiral for optimal search coverage
theta = np.linspace(0, 10*np.pi, 1000)  # Tight spirals for speed
a = 0.5  # Spacing
b = 0.1  # Growth rate
r = a + b * theta

x = r * np.cos(theta)
y = r * np.sin(theta)

# Simulate LIDAR "hits" (victim flags)
victim_x, victim_y = 5, 3  # Example survivor coord

plt.figure(figsize=(8,8))
plt.plot(x, y, 'b-', label='Drone Spiral Path (300+ km/h burst)')
plt.scatter(0, 0, c='g', label='Deploy Point (Backpack)')
plt.scatter(victim_x, victim_y, c='r', s=100, label='Detected Victim (LIDAR/Thermal)')
plt.title('Drone Force One: High-Speed Spiral Search Pattern')
plt.legend()
plt.axis('equal')
plt.show()

# Next: Integrate with pygame for real-time swarm sim + collision avoid

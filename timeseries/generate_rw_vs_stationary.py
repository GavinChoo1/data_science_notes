import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('assets', exist_ok=True)

np.random.seed(42)
t = np.arange(100)
shocks = np.random.choice([-1, 1], size=100) # Coin flips
random_walk = np.cumsum(shocks)

fig, axes = plt.subplots(2, 1, figsize=(10, 8))

# Stationary Error
axes[0].plot(t, shocks, color='green', marker='o', linestyle='none', markersize=4)
axes[0].axhline(0, color='black', linestyle='--', linewidth=1)
axes[0].set_title('Stationary Error (Coin Flips: +1 or -1)')
axes[0].set_ylim(-2, 2)

# Random Walk
axes[1].plot(t, random_walk, color='blue', linewidth=2)
axes[1].axhline(0, color='black', linestyle='--', linewidth=1)
axes[1].set_title('Random Walk (Running Total of Coin Flips)')

plt.tight_layout()
plt.savefig('assets/rw_vs_stationary.png')
plt.close()

print("Graph generated successfully.")

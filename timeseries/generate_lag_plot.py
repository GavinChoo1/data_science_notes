import numpy as np
import matplotlib.pyplot as plt
import os

# Create assets dir
os.makedirs('assets', exist_ok=True)

# Sample data
Y = np.array([2, 4, 5, 4, 5])
Y_t = Y[1:]      # Today's values:    [4, 5, 4, 5]
Y_lag1 = Y[:-1]   # Yesterday's values: [2, 4, 5, 4]

# --- Figure: Lag 1 Scatter Plot ---
fig, ax = plt.subplots(figsize=(7, 6))

# Scatter points
ax.scatter(Y_lag1, Y_t, s=120, color='#8e44ad', zorder=5, edgecolors='white', linewidths=1.5)

# Annotate each point with its time index
annotations = [
    (2, 4, '$t=2$'),
    (4, 5, '$t=3$'),
    (5, 4, '$t=4$'),
    (4, 5, '$t=5$'),
]

# t=3 and t=5 overlap at (4, 5), offset them
offsets = {
    2: (0.15, -0.25),   # t=2: (2,4)
    3: (-0.15, 0.25),   # t=3: (4,5) - offset up-left
    4: (0.15, -0.25),   # t=4: (5,4)
    5: (0.15, -0.25),   # t=5: (4,5) - offset down-right
}

for i, (x, y, label) in enumerate(annotations):
    t_idx = i + 2
    dx, dy = offsets[t_idx]
    ax.annotate(label, (x, y), textcoords="data", xytext=(x + dx, y + dy),
                fontsize=12, fontweight='bold', color='#2c3e50',
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0e6f6', edgecolor='#8e44ad', alpha=0.8))

# Highlight that (4,5) has two overlapping points
ax.annotate('(×2)', (4, 5), textcoords="offset points", xytext=(30, 12),
            fontsize=10, color='#8e44ad', fontstyle='italic',
            arrowprops=dict(arrowstyle='->', color='#8e44ad', lw=1.2))

# Reference diagonal line (perfect correlation)
diag_range = np.linspace(1.5, 5.5, 50)
ax.plot(diag_range, diag_range, '--', color='#bdc3c7', linewidth=1.5, alpha=0.7, label='Perfect correlation line')

# Mean lines
mean_val = 4
ax.axhline(y=mean_val, color='#e74c3c', linestyle=':', linewidth=1.2, alpha=0.6, label=r'Mean $\bar{Y} = 4$')
ax.axvline(x=mean_val, color='#e74c3c', linestyle=':', linewidth=1.2, alpha=0.6)

# Style
ax.set_xlabel(r'Yesterday: $Y_{t-1}$', fontsize=14, fontweight='bold', color='#2c3e50')
ax.set_ylabel(r'Today: $Y_t$', fontsize=14, fontweight='bold', color='#2c3e50')
ax.set_title(r'Lag 1 Scatter Plot — Does Today Depend on Yesterday?', fontsize=15, fontweight='bold', color='#2c3e50', pad=15)
ax.set_xlim(1.5, 5.5)
ax.set_ylim(1.5, 5.5)
ax.set_xticks([2, 3, 4, 5])
ax.set_yticks([2, 3, 4, 5])
ax.set_aspect('equal')
ax.legend(loc='lower right', fontsize=10, framealpha=0.9)
ax.grid(True, alpha=0.3)

# Annotation box explaining the result
ax.text(0.03, 0.03,
        r'$\rho_1 = 0$' + '\nNo linear pattern → Zero autocorrelation',
        transform=ax.transAxes, fontsize=11, verticalalignment='bottom',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#eafaf1', edgecolor='#27ae60', alpha=0.9),
        color='#27ae60', fontweight='bold')

plt.tight_layout()
plt.savefig('assets/acf_lag1_scatter.png', dpi=150, bbox_inches='tight')
plt.close()

print("Lag plot generated: assets/acf_lag1_scatter.png")

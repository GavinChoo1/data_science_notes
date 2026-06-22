import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
import os

os.makedirs('assets', exist_ok=True)

# Generate an AR(1) process: Y_t = 0.8 * Y_{t-1} + noise
np.random.seed(42)
n = 150
phi = 0.8
Y = np.zeros(n)
noise = np.random.normal(0, 1, n)
for t in range(1, n):
    Y[t] = phi * Y[t-1] + noise[t]

# Build the lag matrix
Y_t    = Y[2:]      # Current value
Y_t1   = Y[1:-1]    # Lag 1 (yesterday)
Y_t2   = Y[:-2]     # Lag 2 (two days ago)

# --- Fit the multiple linear regression: Y_t = a * Y_{t-1} + b * Y_{t-2} + c ---
X_reg = np.column_stack([Y_t1, Y_t2])
reg = LinearRegression().fit(X_reg, Y_t)
coef_lag1, coef_lag2 = reg.coef_
intercept = reg.intercept_

# --- Create the 3D figure ---
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# Regression plane (draw first so points sit on top)
lag2_grid = np.linspace(Y_t2.min() - 0.3, Y_t2.max() + 0.3, 30)
lag1_grid = np.linspace(Y_t1.min() - 0.3, Y_t1.max() + 0.3, 30)
L2, L1 = np.meshgrid(lag2_grid, lag1_grid)
Z_plane = intercept + coef_lag1 * L1 + coef_lag2 * L2

ax.plot_surface(L2, L1, Z_plane, alpha=0.35, color='#3498db',
                edgecolor='#2980b9', linewidth=0.3, shade=True,
                rstride=3, cstride=3)

# Scatter: data points colored by Y_t value for depth
scatter = ax.scatter(Y_t2, Y_t1, Y_t, c=Y_t, cmap='plasma', s=40, alpha=0.75,
                     edgecolors='white', linewidths=0.5, depthshade=True,
                     label='Observed data points')

# Residual lines from some points to the plane (to show error)
np.random.seed(7)
sample_idx = np.random.choice(len(Y_t), 15, replace=False)
for i in sample_idx:
    z_pred = intercept + coef_lag1 * Y_t1[i] + coef_lag2 * Y_t2[i]
    ax.plot([Y_t2[i], Y_t2[i]], [Y_t1[i], Y_t1[i]], [Y_t[i], z_pred],
            color='#e74c3c', linewidth=0.8, alpha=0.5)

# Labels
ax.set_xlabel(r'$Y_{t-2}$  (2 days ago)', fontsize=13, fontweight='bold',
              color='#2c3e50', labelpad=12)
ax.set_ylabel(r'$Y_{t-1}$  (yesterday)', fontsize=13, fontweight='bold',
              color='#2c3e50', labelpad=12)
ax.set_zlabel(r'$Y_t$  (today)', fontsize=13, fontweight='bold',
              color='#2c3e50', labelpad=10)

ax.set_title('PACF as Multiple Linear Regression\n'
             r'$Y_t = \phi_{21}\,Y_{t-1} + \phi_{22}\,Y_{t-2} + \varepsilon_t$',
             fontsize=15, fontweight='bold', color='#2c3e50', pad=20)

# Set a good viewing angle
ax.view_init(elev=22, azim=225)

# Annotation text box with regression results
textstr = (
    f'Regression coefficients:\n'
    f'  $\\phi_{{21}}$ (Lag 1) = {coef_lag1:.3f}  ← strong direct effect\n'
    f'  $\\phi_{{22}}$ (Lag 2) = {coef_lag2:.3f}  ← near zero (PACF at Lag 2)\n'
    f'\n'
    f'The plane tilts steeply along $Y_{{t-1}}$\n'
    f'but is nearly flat along $Y_{{t-2}}$.\n'
    f'This proves $Y_{{t-2}}$ adds no unique\n'
    f'information once $Y_{{t-1}}$ is controlled.'
)

fig.text(0.02, 0.02, textstr, fontsize=10.5, fontfamily='monospace',
         verticalalignment='bottom',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#eaf2f8',
                   edgecolor='#2980b9', alpha=0.95),
         color='#2c3e50')

plt.tight_layout(rect=[0.0, 0.15, 1.0, 1.0])
plt.savefig('assets/pacf_3d_regression.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"3D plot saved. Coefficients: lag1={coef_lag1:.4f}, lag2={coef_lag2:.4f}")

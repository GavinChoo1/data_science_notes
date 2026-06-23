import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

os.makedirs('assets', exist_ok=True)

# ── Dataset ───────────────────────────────────────────────────────
X = np.array([2, 4, 6, 2, 1])
Y = np.array([10, 11, 15, 19, 11])
T = len(X)
t = np.arange(1, T + 1)

x_bar = np.mean(X)   # 3.0
y_bar = np.mean(Y)   # 13.2

dx = X - x_bar        # deviations
dy = Y - y_bar

# Variances
c_xx0 = np.sum(dx**2) / T   # 3.2
c_yy0 = np.sum(dy**2) / T   # 11.36
denom = np.sqrt(c_xx0 * c_yy0)

# Cross-correlations at multiple lags
max_lag = 4
lags = np.arange(-max_lag, max_lag + 1)
ccf_vals = []
for k in lags:
    if k >= 0:
        pairs = [(dx[tt], dy[tt + k]) for tt in range(T - k)]
    else:
        pairs = [(dx[tt], dy[tt + k]) for tt in range(-k, T)]
    c_xy_k = sum(a * b for a, b in pairs) / T
    r_xy_k = c_xy_k / denom
    ccf_vals.append(r_xy_k)

ccf_vals = np.array(ccf_vals)

# Print for verification
print("=" * 60)
print("CCF Calculation Results")
print("=" * 60)
print(f"X = {X},  mean = {x_bar}")
print(f"Y = {Y},  mean = {y_bar}")
print(f"c_xx(0) = {c_xx0:.2f},  c_yy(0) = {c_yy0:.2f}")
print(f"sqrt(c_xx(0)*c_yy(0)) = {denom:.4f}")
for lag, val in zip(lags, ccf_vals):
    print(f"  r_xy({lag:+d}) = {val:.4f}")

# ── Colours ───────────────────────────────────────────────────────
c_x     = '#3498db'
c_y     = '#e74c3c'
c_bar   = '#8e44ad'
c_sig   = '#1abc9c'
c_lag   = '#e67e22'
grey    = '#95a5a6'

# ── Figure: 2x2 ──────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 10))
gs = gridspec.GridSpec(2, 2, hspace=0.42, wspace=0.3)

# ── Panel 1: Both time series ────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(t, X, 'o-', color=c_x, linewidth=2.5, markersize=10, label='$X_t$ (Marketing)', zorder=3)
ax1.plot(t, Y, 's-', color=c_y, linewidth=2.5, markersize=10, label='$Y_t$ (Sales)', zorder=3)
for i in range(T):
    ax1.annotate(f'{X[i]}', (t[i], X[i]), textcoords="offset points",
                 xytext=(-12, -14), ha='center', fontsize=11, fontweight='bold', color=c_x)
    ax1.annotate(f'{Y[i]}', (t[i], Y[i]), textcoords="offset points",
                 xytext=(12, 10), ha='center', fontsize=11, fontweight='bold', color=c_y)
ax1.set_title('Step 1: The Two Time Series', fontsize=13, fontweight='bold')
ax1.set_xlabel('Week ($t$)', fontsize=11)
ax1.set_ylabel('Value', fontsize=11)
ax1.set_xticks(t)
ax1.legend(fontsize=10, loc='upper left')
ax1.grid(True, alpha=0.3)

# ── Panel 2: Deviations from mean ────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
width = 0.35
ax2.bar(t - width/2, dx, width=width, color=c_x, alpha=0.7, label='$x_t - \\bar{x}$', zorder=3)
ax2.bar(t + width/2, dy, width=width, color=c_y, alpha=0.7, label='$y_t - \\bar{y}$', zorder=3)
ax2.axhline(0, color=grey, linestyle='--', linewidth=1.2)
for i in range(T):
    off_x = -16 if dx[i] < 0 else 10
    off_y = -16 if dy[i] < 0 else 10
    ax2.annotate(f'{dx[i]:+.0f}', (t[i] - width/2, dx[i]), textcoords="offset points",
                 xytext=(0, off_x), ha='center', fontsize=9, fontweight='bold', color=c_x)
    ax2.annotate(f'{dy[i]:+.1f}', (t[i] + width/2, dy[i]), textcoords="offset points",
                 xytext=(0, off_y), ha='center', fontsize=9, fontweight='bold', color=c_y)
ax2.set_title('Step 1: Deviations from Mean', fontsize=13, fontweight='bold')
ax2.set_xlabel('Week ($t$)', fontsize=11)
ax2.set_ylabel('Deviation', fontsize=11)
ax2.set_xticks(t)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

# ── Panel 3: Lag 0 vs Lag 1 pairing ─────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])

# Lag 0: scatter of (x_t, y_t)
ax3.scatter(dx, dy, color=c_bar, s=120, zorder=4, edgecolors='white', linewidth=1.5,
            label='Lag 0 pairs $(x_t, y_t)$')
# Lag 1: scatter of (x_t, y_{t+1})
dx_lag1 = dx[:T-1]
dy_lag1 = dy[1:]
ax3.scatter(dx_lag1, dy_lag1, color=c_lag, s=120, marker='D', zorder=4, edgecolors='white',
            linewidth=1.5, label='Lag +1 pairs $(x_t, y_{t+1})$')
ax3.axhline(0, color=grey, linestyle='--', linewidth=0.8)
ax3.axvline(0, color=grey, linestyle='--', linewidth=0.8)
ax3.set_title('Step 3–4: Scatter of Paired Deviations', fontsize=13, fontweight='bold')
ax3.set_xlabel('$x_t - \\bar{x}$', fontsize=11)
ax3.set_ylabel('$y_{t+k} - \\bar{y}$', fontsize=11)
ax3.legend(fontsize=9, loc='upper left')
ax3.grid(True, alpha=0.3)

# ── Panel 4: CCF Plot ────────────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])

# 95% confidence interval
ci = 1.96 / np.sqrt(T)

colors_ccf = [c_sig if abs(v) > ci else '#bdc3c7' for v in ccf_vals]
bars4 = ax4.bar(lags, ccf_vals, color=colors_ccf, width=0.6, edgecolor='white',
                linewidth=1.5, zorder=3)
ax4.axhline(0, color=grey, linestyle='-', linewidth=1)
ax4.axhline(ci, color=c_sig, linestyle='--', linewidth=1.2, alpha=0.7, label=f'95% CI ($\\pm{ci:.2f}$)')
ax4.axhline(-ci, color=c_sig, linestyle='--', linewidth=1.2, alpha=0.7)
ax4.fill_between([-max_lag - 0.5, max_lag + 0.5], -ci, ci, alpha=0.08, color=c_sig)

# Annotate key values
for i, (lag, val) in enumerate(zip(lags, ccf_vals)):
    if abs(val) > 0.1:
        offset = 12 if val >= 0 else -16
        ax4.annotate(f'{val:.2f}', (lag, val), textcoords="offset points",
                     xytext=(0, offset), ha='center', fontsize=10, fontweight='bold')

ax4.set_title('CCF Plot: $r_{xy}(k)$', fontsize=13, fontweight='bold')
ax4.set_xlabel('Lag ($k$)', fontsize=11)
ax4.set_ylabel('Cross-Correlation', fontsize=11)
ax4.set_xticks(lags)
ax4.set_ylim(-1.1, 1.1)
ax4.legend(fontsize=10)
ax4.grid(True, alpha=0.3)

# Highlight lag +1
ax4.annotate('Strongest!\nX leads Y by 1 week',
             xy=(1, ccf_vals[lags == 1][0]),
             xytext=(2.5, 0.95),
             fontsize=10, fontweight='bold', color=c_lag,
             arrowprops=dict(arrowstyle='->', color=c_lag, lw=2),
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#fef9e7', edgecolor=c_lag))

plt.savefig('assets/ccf_step_by_step.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nGraph saved to assets/ccf_step_by_step.png")

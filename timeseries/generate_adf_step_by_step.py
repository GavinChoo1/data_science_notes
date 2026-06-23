import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

os.makedirs('assets', exist_ok=True)

# ── The dataset from the user's ADF example ───────────────────────
y = np.array([10, 12, 11, 15, 14, 18])
T = len(y)
t = np.arange(1, T + 1)

# ── Step 1: First differences ────────────────────────────────────
delta_y = np.diff(y)  # [2, -1, 4, -1, 4]

# ── Build the regression matrix (p=1, with constant, no trend) ───
# Usable rows: t = 3,4,5,6 (indices 2-5 in 0-based)
# Dependent:   Δy_t    for t=3..6 → delta_y[2], delta_y[3], delta_y[4]  → [-1, 4, -1, 4]
# Wait, let me re-check. With p=1 lag of differences:
# t=3: Δy3=-1,  y_{t-1}=y2=12,  Δy_{t-1}=Δy2=2
# t=4: Δy4=4,   y_{t-1}=y3=11,  Δy_{t-1}=Δy3=-1
# t=5: Δy5=-1,  y_{t-1}=y4=15,  Δy_{t-1}=Δy4=4
# t=6: Δy6=4,   y_{t-1}=y5=14,  Δy_{t-1}=Δy5=-1

# Usable observations (t=3 to t=6, so 4 data points)
dep_y = delta_y[1:]              # Δy for t=3..6: [-1, 4, -1, 4]
x_yt1 = y[1:-1]                  # y_{t-1} for t=3..6: [12, 11, 15, 14]
x_dyt1 = delta_y[:-1]            # Δy_{t-1} for t=3..6: [2, -1, 4, -1]

# OLS: Δy_t = α + γ * y_{t-1} + δ₁ * Δy_{t-1}
n_obs = len(dep_y)
X = np.column_stack([np.ones(n_obs), x_yt1, x_dyt1])
Y = dep_y

# β = (X'X)^{-1} X'Y
XtX = X.T @ X
XtX_inv = np.linalg.inv(XtX)
beta_hat = XtX_inv @ (X.T @ Y)
alpha_hat, gamma_hat, delta1_hat = beta_hat

# Fitted values and residuals
Y_hat = X @ beta_hat
residuals = Y - Y_hat

# Residual variance
k = 3  # number of parameters
s_sq = np.sum(residuals**2) / (n_obs - k)

# Variance-covariance matrix of coefficients
var_cov = s_sq * XtX_inv

# Standard error of gamma
se_gamma = np.sqrt(var_cov[1, 1])

# ADF t-statistic
t_adf = gamma_hat / se_gamma

print("=" * 60)
print("ADF Test Step-by-Step Calculation")
print("=" * 60)
print(f"y = {y}")
print(f"delta_y = {delta_y}")
print(f"\nUsable observations (t=3..6):")
print(f"  Dep (delta_y_t)  = {dep_y}")
print(f"  y_t-1            = {x_yt1}")
print(f"  delta_y_t-1      = {x_dyt1}")
print(f"\nOLS Coefficients:")
print(f"  alpha  (intercept) = {alpha_hat:.4f}")
print(f"  gamma  (y_t-1)     = {gamma_hat:.4f}")
print(f"  delta1 (delta_y_t-1) = {delta1_hat:.4f}")
print(f"\nFitted values: {Y_hat}")
print(f"Residuals:     {residuals}")
print(f"Residual variance s^2 = {s_sq:.4f}")
print(f"SE(gamma) = {se_gamma:.4f}")
print(f"\nt_ADF = gamma / SE(gamma) = {gamma_hat:.4f} / {se_gamma:.4f} = {t_adf:.4f}")

# ── Colours ───────────────────────────────────────────────────────
c_data   = '#3498db'
c_diff   = '#1abc9c'
c_reg    = '#e67e22'
c_resid  = '#e74c3c'
c_stat   = '#8e44ad'
grey     = '#95a5a6'

# ── Figure: 2x2 ──────────────────────────────────────────────────
fig = plt.figure(figsize=(15, 10))
gs = gridspec.GridSpec(2, 2, hspace=0.4, wspace=0.35)

# ── Panel 1: Raw Time Series ─────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(t, y, 'o-', color=c_data, linewidth=2.5, markersize=10, zorder=3)
for i in range(T):
    ax1.annotate(f'{y[i]}', (t[i], y[i]), textcoords="offset points",
                 xytext=(0, 14), ha='center', fontsize=12, fontweight='bold', color=c_data)
ax1.set_title('Step 1: Raw Data $y_t$', fontsize=13, fontweight='bold')
ax1.set_xlabel('Time ($t$)', fontsize=11)
ax1.set_ylabel('$y_t$', fontsize=11)
ax1.set_xticks(t)
ax1.set_ylim(7, 21)
ax1.grid(True, alpha=0.3)

# ── Panel 2: First Differences ───────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
t_diff = np.arange(2, T + 1)
colors_bar = [('#e74c3c' if v < 0 else c_diff) for v in delta_y]
bars = ax2.bar(t_diff, delta_y, color=colors_bar, width=0.5, edgecolor='white',
               linewidth=1.5, zorder=3)
ax2.axhline(0, color=grey, linestyle='--', linewidth=1.2)
for i in range(len(delta_y)):
    offset = -18 if delta_y[i] < 0 else 12
    ax2.annotate(f'{delta_y[i]:+d}', (t_diff[i], delta_y[i]), textcoords="offset points",
                 xytext=(0, offset), ha='center', fontsize=12, fontweight='bold')
ax2.set_title('Step 1: First Differences $\\Delta y_t = y_t - y_{t-1}$', fontsize=13, fontweight='bold')
ax2.set_xlabel('Time ($t$)', fontsize=11)
ax2.set_ylabel('$\\Delta y_t$', fontsize=11)
ax2.set_xticks(t_diff)
ax2.set_ylim(-3, 6)
ax2.grid(True, alpha=0.3)

# ── Panel 3: OLS Regression (Actual vs Fitted) ──────────────────
ax3 = fig.add_subplot(gs[1, 0])
t_usable = np.array([3, 4, 5, 6])
ax3.bar(t_usable - 0.15, dep_y, width=0.3, color=c_diff, alpha=0.7, label='Actual $\\Delta y_t$', zorder=3)
ax3.bar(t_usable + 0.15, Y_hat, width=0.3, color=c_reg, alpha=0.7, label='Fitted $\\hat{\\Delta y}_t$', zorder=3)
ax3.axhline(0, color=grey, linestyle='--', linewidth=1.2)
for i in range(n_obs):
    ax3.annotate(f'{dep_y[i]:+.0f}', (t_usable[i] - 0.15, dep_y[i]),
                 textcoords="offset points",
                 xytext=(0, 12 if dep_y[i] >= 0 else -16), ha='center', fontsize=10, fontweight='bold', color=c_diff)
    ax3.annotate(f'{Y_hat[i]:+.1f}', (t_usable[i] + 0.15, Y_hat[i]),
                 textcoords="offset points",
                 xytext=(0, 12 if Y_hat[i] >= 0 else -16), ha='center', fontsize=10, fontweight='bold', color=c_reg)
ax3.set_title('Step 2: OLS Regression (Actual vs. Fitted)', fontsize=13, fontweight='bold')
ax3.set_xlabel('Time ($t$)', fontsize=11)
ax3.set_ylabel('$\\Delta y_t$', fontsize=11)
ax3.set_xticks(t_usable)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)

# Coefficient box
ax3.text(0.97, 0.05,
    f'$\\hat{{\\alpha}} = {alpha_hat:.2f}$\n'
    f'$\\hat{{\\gamma}} = {gamma_hat:.4f}$\n'
    f'$\\hat{{\\delta}}_1 = {delta1_hat:.2f}$',
    transform=ax3.transAxes, fontsize=10,
    verticalalignment='bottom', horizontalalignment='right',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='#fef9e7', edgecolor=c_reg, alpha=0.95))

# ── Panel 4: Test Statistic Result ───────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_xlim(-6, 2)
ax4.set_ylim(0, 1)
ax4.set_yticks([])

# Draw a horizontal number line
ax4.axhline(0.5, color=grey, linewidth=2, zorder=1)

# Critical values
crit_1 = -3.75   # ~1% for constant, small sample
crit_5 = -3.00   # ~5%
crit_10 = -2.63  # ~10%

for cv, label, yoff in [(crit_1, '1%', 0.15), (crit_5, '5%', 0.15), (crit_10, '10%', 0.15)]:
    ax4.axvline(cv, color='#bdc3c7', linestyle='--', linewidth=1.5, ymin=0.3, ymax=0.7)
    ax4.annotate(f'{label}\n({cv:.2f})', (cv, 0.5 + yoff), ha='center', fontsize=10, color=grey)

# Mark the test statistic
ax4.plot(t_adf, 0.5, 'D', color=c_stat, markersize=16, zorder=5)
ax4.annotate(f'$t_{{ADF}} = {t_adf:.2f}$', (t_adf, 0.5), textcoords="offset points",
             xytext=(0, -30), ha='center', fontsize=13, fontweight='bold', color=c_stat,
             arrowprops=dict(arrowstyle='->', color=c_stat, lw=2))

# Shade rejection region
ax4.axvspan(-6, crit_5, alpha=0.08, color=c_stat, zorder=0)
ax4.text(-5.5, 0.85, 'Reject $H_0$\n(Stationary)', fontsize=11, color=c_stat,
         ha='left', fontweight='bold')
ax4.text(0.5, 0.85, 'Fail to Reject $H_0$\n(Non-Stationary)', fontsize=11, color=c_resid,
         ha='center', fontweight='bold')

# More negative ← → Less negative
ax4.annotate('← More negative', (-5.8, 0.38), fontsize=9, color=grey)
ax4.annotate('Less negative →', (0.6, 0.38), fontsize=9, color=grey)

ax4.set_title('Step 5: Compare $t_{ADF}$ to Critical Values', fontsize=13, fontweight='bold')
ax4.set_xlabel('ADF $t$-statistic', fontsize=11)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
ax4.spines['left'].set_visible(False)

plt.savefig('assets/adf_step_by_step.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"\nGraph saved to assets/adf_step_by_step.png")

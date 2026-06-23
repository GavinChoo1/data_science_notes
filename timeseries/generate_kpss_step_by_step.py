import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

os.makedirs('assets', exist_ok=True)

# ── The same tiny dataset from the ACF / PACF notes ───────────────
y = np.array([2, 4, 5, 4, 5])
T = len(y)
t = np.arange(1, T + 1)

# ── Step 1: OLS regression on a constant (mean) ──────────────────
y_bar = np.mean(y)            # = 4.0
e = y - y_bar                 # residuals

# ── Step 2: Cumulative sum S_t ────────────────────────────────────
S = np.cumsum(e)

# ── Step 3: S_t^2 ────────────────────────────────────────────────
S_sq = S ** 2

# ── Step 4: Long-run variance (simple, lag 0 only for tiny sample)
sigma_sq = (1 / T) * np.sum(e ** 2)   # = 1.2

# ── Step 5: LM statistic ─────────────────────────────────────────
LM = np.sum(S_sq) / (T**2 * sigma_sq)

# Print all intermediate values for the markdown
print("=" * 50)
print("Hand-Calculated KPSS Example")
print("=" * 50)
print(f"y       = {y}")
print(f"y_bar   = {y_bar}")
print(f"e_t     = {e}")
print(f"S_t     = {S}")
print(f"S_t^2   = {S_sq}")
print(f"sum(S_t^2) = {np.sum(S_sq)}")
print(f"sigma^2 = {sigma_sq}")
print(f"T^2 * sigma^2 = {T**2 * sigma_sq}")
print(f"LM      = {LM:.4f}")

# ── Colours ───────────────────────────────────────────────────────
c_data  = '#3498db'
c_resid = '#1abc9c'
c_cusum = '#8e44ad'
c_sq    = '#e67e22'
grey    = '#95a5a6'

# ── Figure: 2x2 grid ─────────────────────────────────────────────
fig = plt.figure(figsize=(14, 9))
gs = gridspec.GridSpec(2, 2, hspace=0.4, wspace=0.35)

# ── Panel 1: Raw Data ────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(t, y, 'o-', color=c_data, linewidth=2.5, markersize=10, zorder=3)
ax1.axhline(y_bar, color=grey, linestyle='--', linewidth=1.2, label=f'$\\bar{{y}} = {y_bar:.0f}$')
for i in range(T):
    ax1.annotate(f'{y[i]}', (t[i], y[i]), textcoords="offset points",
                 xytext=(0, 14), ha='center', fontsize=12, fontweight='bold', color=c_data)
ax1.set_title('Step 1: Raw Data & Mean', fontsize=13, fontweight='bold')
ax1.set_xlabel('Time ($t$)', fontsize=11)
ax1.set_ylabel('$y_t$', fontsize=11)
ax1.set_xticks(t)
ax1.set_ylim(0.5, 7)
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# ── Panel 2: Residuals e_t ───────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
colors_bar = [('#e74c3c' if v < 0 else c_resid) for v in e]
bars = ax2.bar(t, e, color=colors_bar, width=0.5, edgecolor='white', linewidth=1.5, zorder=3)
ax2.axhline(0, color=grey, linestyle='--', linewidth=1.2)
for i in range(T):
    offset = -18 if e[i] < 0 else 12
    ax2.annotate(f'{e[i]:+.0f}', (t[i], e[i]), textcoords="offset points",
                 xytext=(0, offset), ha='center', fontsize=12, fontweight='bold')
ax2.set_title('Step 2: Residuals $e_t = y_t - \\bar{y}$', fontsize=13, fontweight='bold')
ax2.set_xlabel('Time ($t$)', fontsize=11)
ax2.set_ylabel('$e_t$', fontsize=11)
ax2.set_xticks(t)
ax2.set_ylim(-3, 2.5)
ax2.grid(True, alpha=0.3)

# ── Panel 3: Cumulative Sum S_t ──────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(t, S, 'o-', color=c_cusum, linewidth=2.5, markersize=10, zorder=3)
ax3.fill_between(t, 0, S, alpha=0.15, color=c_cusum)
ax3.axhline(0, color=grey, linestyle='--', linewidth=1.2)
for i in range(T):
    offset = -18 if S[i] < 0 else 12
    ax3.annotate(f'{S[i]:+.0f}', (t[i], S[i]), textcoords="offset points",
                 xytext=(0, offset), ha='center', fontsize=12, fontweight='bold', color=c_cusum)
ax3.set_title('Step 3: Cumulative Sum $S_t = \\sum_{i=1}^{t} e_i$', fontsize=13, fontweight='bold')
ax3.set_xlabel('Time ($t$)', fontsize=11)
ax3.set_ylabel('$S_t$', fontsize=11)
ax3.set_xticks(t)
ax3.grid(True, alpha=0.3)

# ── Panel 4: S_t^2 and LM ───────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
bars4 = ax4.bar(t, S_sq, color=c_sq, width=0.5, edgecolor='white', linewidth=1.5, zorder=3)
for i in range(T):
    ax4.annotate(f'{S_sq[i]:.0f}', (t[i], S_sq[i]), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=12, fontweight='bold', color=c_sq)
ax4.set_title('Step 4: $S_t^2$ → Sum to get LM', fontsize=13, fontweight='bold')
ax4.set_xlabel('Time ($t$)', fontsize=11)
ax4.set_ylabel('$S_t^2$', fontsize=11)
ax4.set_xticks(t)
ax4.grid(True, alpha=0.3)

# Annotation box with final calculation
ax4.text(0.97, 0.95,
    f'$\\sum S_t^2 = {int(np.sum(S_sq))}$\n'
    f'$T^2 \\cdot \\hat{{\\sigma}}^2 = {T**2 * sigma_sq:.0f}$\n'
    f'$LM = {int(np.sum(S_sq))} \\div {T**2 * sigma_sq:.0f} = {LM:.4f}$',
    transform=ax4.transAxes, fontsize=11,
    verticalalignment='top', horizontalalignment='right',
    bbox=dict(boxstyle='round,pad=0.6', facecolor='#fef9e7', edgecolor=c_sq, alpha=0.95))

plt.savefig('assets/kpss_step_by_step.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nGraph saved to assets/kpss_step_by_step.png")

import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import kpss
import os

# Create assets dir if it doesn't exist
os.makedirs('assets', exist_ok=True)

# Set seed for reproducibility
np.random.seed(42)
T = 200

# ── Generate Data ──────────────────────────────────────────────────
# Scenario 1: Stationary series (white noise around a constant mean)
stationary = np.random.normal(loc=5, scale=1.5, size=T)

# Scenario 2: Non-stationary series (random walk)
random_walk = np.cumsum(np.random.normal(0, 1, T))

# ── Compute OLS residuals & cumulative sums ────────────────────────
def ols_residuals_and_cusum(y):
    """Regress y on a constant, return residuals and their cumulative sum."""
    y_mean = np.mean(y)
    e = y - y_mean          # residuals from OLS on a constant
    S = np.cumsum(e)        # cumulative sum S_t
    return e, S

e_stat, S_stat = ols_residuals_and_cusum(stationary)
e_rw, S_rw = ols_residuals_and_cusum(random_walk)

# ── Run actual KPSS tests ──────────────────────────────────────────
kpss_stat_stat, kpss_p_stat, _, kpss_crit_stat = kpss(stationary, regression='c', nlags='auto')
kpss_stat_rw, kpss_p_rw, _, kpss_crit_rw = kpss(random_walk, regression='c', nlags='auto')

# ── Colours ────────────────────────────────────────────────────────
c_stat = '#1abc9c'   # teal for stationary
c_rw   = '#e74c3c'   # red for random walk
c_cusum = '#8e44ad'  # purple for cumulative sum
c_sq    = '#e67e22'  # orange for S_t^2
grey    = '#95a5a6'

t = np.arange(T)

# ── Figure ─────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(18, 9))

# ─── Row 1: Stationary Series ─────────────────────────────────────
# Col 1 – Time series
axes[0, 0].plot(t, stationary, color=c_stat, linewidth=1.2, alpha=0.85)
axes[0, 0].axhline(np.mean(stationary), color=grey, linestyle='--', linewidth=1)
axes[0, 0].set_title('Stationary Series (White Noise)', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Time')
axes[0, 0].set_ylabel('Value')

# Col 2 – Residuals & cumulative sum
ax_r = axes[0, 1]
ax_r.bar(t, e_stat, color=c_stat, alpha=0.35, width=1.0, label='Residuals $e_t$')
ax_r.plot(t, S_stat, color=c_cusum, linewidth=2, label='Cumulative Sum $S_t$')
ax_r.axhline(0, color=grey, linestyle='--', linewidth=0.8)
ax_r.set_title('Residuals & Cumulative Sum $S_t$', fontsize=12, fontweight='bold')
ax_r.set_xlabel('Time')
ax_r.set_ylabel('Value')
ax_r.legend(fontsize=9)

# Col 3 – S_t^2
axes[0, 2].fill_between(t, 0, S_stat**2, color=c_sq, alpha=0.5)
axes[0, 2].plot(t, S_stat**2, color=c_sq, linewidth=1.5)
axes[0, 2].set_title('$S_t^2$  (stays small → low LM)', fontsize=12, fontweight='bold')
axes[0, 2].set_xlabel('Time')
axes[0, 2].set_ylabel('$S_t^2$')

# Add annotation with test result
axes[0, 2].text(0.97, 0.95,
    f'LM = {kpss_stat_stat:.4f}\np-value = {kpss_p_stat:.2f}\n→ Stationary ✓',
    transform=axes[0, 2].transAxes, fontsize=10,
    verticalalignment='top', horizontalalignment='right',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=c_stat, alpha=0.9))

# ─── Row 2: Non-Stationary Series (Random Walk) ───────────────────
# Col 1 – Time series
axes[1, 0].plot(t, random_walk, color=c_rw, linewidth=1.2, alpha=0.85)
axes[1, 0].axhline(np.mean(random_walk), color=grey, linestyle='--', linewidth=1)
axes[1, 0].set_title('Non-Stationary Series (Random Walk)', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Time')
axes[1, 0].set_ylabel('Value')

# Col 2 – Residuals & cumulative sum
ax_r2 = axes[1, 1]
ax_r2.bar(t, e_rw, color=c_rw, alpha=0.35, width=1.0, label='Residuals $e_t$')
ax_r2.plot(t, S_rw, color=c_cusum, linewidth=2, label='Cumulative Sum $S_t$')
ax_r2.axhline(0, color=grey, linestyle='--', linewidth=0.8)
ax_r2.set_title('Residuals & Cumulative Sum $S_t$', fontsize=12, fontweight='bold')
ax_r2.set_xlabel('Time')
ax_r2.set_ylabel('Value')
ax_r2.legend(fontsize=9)

# Col 3 – S_t^2
axes[1, 2].fill_between(t, 0, S_rw**2, color=c_sq, alpha=0.5)
axes[1, 2].plot(t, S_rw**2, color=c_sq, linewidth=1.5)
axes[1, 2].set_title('$S_t^2$  (explodes → high LM)', fontsize=12, fontweight='bold')
axes[1, 2].set_xlabel('Time')
axes[1, 2].set_ylabel('$S_t^2$')

# Add annotation with test result
axes[1, 2].text(0.97, 0.95,
    f'LM = {kpss_stat_rw:.4f}\np-value = {kpss_p_rw:.2f}\n→ Non-Stationary ✗',
    transform=axes[1, 2].transAxes, fontsize=10,
    verticalalignment='top', horizontalalignment='right',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=c_rw, alpha=0.9))

# ── Layout ─────────────────────────────────────────────────────────
plt.tight_layout()
plt.savefig('assets/kpss_examples.png', dpi=150)
plt.close()

# ── Print numerical results for the markdown example ───────────────
print("=" * 60)
print("KPSS Test Results")
print("=" * 60)
print(f"\nStationary Series:")
print(f"  LM Statistic = {kpss_stat_stat:.4f}")
print(f"  p-value      = {kpss_p_stat:.4f}")
print(f"  Critical Values: {kpss_crit_stat}")
print(f"\nRandom Walk (Non-Stationary):")
print(f"  LM Statistic = {kpss_stat_rw:.4f}")
print(f"  p-value      = {kpss_p_rw:.4f}")
print(f"  Critical Values: {kpss_crit_rw}")
print("\nKPSS examples graph generated successfully.")

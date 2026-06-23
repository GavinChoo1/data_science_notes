import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

os.makedirs('assets', exist_ok=True)

# ── Dataset ───────────────────────────────────────────────────────
x = np.array([1, 2, 1, 0])
N = len(x)
n = np.arange(N)

# ── Compute DFT manually ─────────────────────────────────────────
X = np.fft.fft(x)
magnitudes = np.abs(X)

print("=" * 60)
print("FFT Step-by-Step Results")
print("=" * 60)
print(f"x = {x}")
print(f"X = {X}")
print(f"|X| = {magnitudes}")
for k in range(N):
    print(f"  X[{k}] = {X[k].real:+.1f} {X[k].imag:+.1f}j  ->  |X[{k}]| = {magnitudes[k]:.1f}")

# ── Colours ───────────────────────────────────────────────────────
c_time  = '#3498db'
c_freq  = '#e67e22'
c_real  = '#1abc9c'
c_imag  = '#e74c3c'
c_mag   = '#8e44ad'
grey    = '#95a5a6'

# ── Figure: 2x2 ──────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 10))
gs = gridspec.GridSpec(2, 2, hspace=0.45, wspace=0.3)

# ── Panel 1: Time-domain signal ──────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(n, x, 'o-', color=c_time, linewidth=2.5, markersize=12, zorder=3)
for i in range(N):
    ax1.annotate(f'$x_{i} = {x[i]}$', (n[i], x[i]), textcoords="offset points",
                 xytext=(12, 10), ha='left', fontsize=12, fontweight='bold', color=c_time)
ax1.axhline(0, color=grey, linestyle='--', linewidth=0.8)
ax1.set_title('Input: Time-Domain Signal $x_n$', fontsize=13, fontweight='bold')
ax1.set_xlabel('Sample index ($n$)', fontsize=11)
ax1.set_ylabel('Amplitude', fontsize=11)
ax1.set_xticks(n)
ax1.set_ylim(-0.5, 3)
ax1.grid(True, alpha=0.3)

# ── Panel 2: Unit circle / twiddle factors for k=1 ──────────────
ax2 = fig.add_subplot(gs[0, 1])
theta = np.linspace(0, 2 * np.pi, 200)
ax2.plot(np.cos(theta), np.sin(theta), color=grey, linewidth=1.5, alpha=0.4)
ax2.axhline(0, color=grey, linewidth=0.5)
ax2.axvline(0, color=grey, linewidth=0.5)

# Plot twiddle factors W_N^(kn) for k=1
colors_tw = ['#2ecc71', '#3498db', '#e74c3c', '#9b59b6']
labels_tw = ['$n=0$: $(1, 0)$', '$n=1$: $(0, -1)$', '$n=2$: $(-1, 0)$', '$n=3$: $(0, 1)$']
for nn in range(N):
    angle = -2 * np.pi * 1 * nn / N   # k=1
    re = np.cos(angle)
    im = np.sin(angle)
    ax2.plot(re, im, 'o', color=colors_tw[nn], markersize=14, zorder=5)
    # Arrow from origin
    ax2.annotate('', xy=(re, im), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color=colors_tw[nn], lw=2))
    # Label
    offset_x = 15 if re >= 0 else -15
    offset_y = 15 if im >= 0 else -15
    ha = 'left' if re >= 0 else 'right'
    ax2.annotate(labels_tw[nn], (re, im), textcoords="offset points",
                 xytext=(offset_x, offset_y), ha=ha, fontsize=10, fontweight='bold',
                 color=colors_tw[nn])

ax2.set_title('Euler\'s Formula: Twiddle Factors for $k=1$\n$e^{-j 2\\pi kn/N}$ on the Unit Circle',
              fontsize=12, fontweight='bold')
ax2.set_xlabel('Real', fontsize=11)
ax2.set_ylabel('Imaginary', fontsize=11)
ax2.set_xlim(-1.8, 1.8)
ax2.set_ylim(-1.8, 1.8)
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.3)

# ── Panel 3: Real & Imaginary parts of X_k ──────────────────────
ax3 = fig.add_subplot(gs[1, 0])
k_vals = np.arange(N)
width = 0.35
bars_re = ax3.bar(k_vals - width/2, X.real, width=width, color=c_real, alpha=0.8,
                  label='Real part', edgecolor='white', linewidth=1.5, zorder=3)
bars_im = ax3.bar(k_vals + width/2, X.imag, width=width, color=c_imag, alpha=0.8,
                  label='Imaginary part', edgecolor='white', linewidth=1.5, zorder=3)
ax3.axhline(0, color=grey, linestyle='--', linewidth=1)

for i in range(N):
    re_off = 12 if X[i].real >= 0 else -16
    im_off = 12 if X[i].imag >= 0 else -16
    ax3.annotate(f'{X[i].real:+.0f}', (k_vals[i] - width/2, X[i].real),
                 textcoords="offset points", xytext=(0, re_off), ha='center',
                 fontsize=11, fontweight='bold', color=c_real)
    if X[i].imag != 0:
        ax3.annotate(f'{X[i].imag:+.0f}j', (k_vals[i] + width/2, X[i].imag),
                     textcoords="offset points", xytext=(0, im_off), ha='center',
                     fontsize=11, fontweight='bold', color=c_imag)
    else:
        ax3.annotate('0j', (k_vals[i] + width/2, 0),
                     textcoords="offset points", xytext=(0, 10), ha='center',
                     fontsize=11, fontweight='bold', color=c_imag)

ax3.set_title('Output: Real & Imaginary Parts of $X_k$', fontsize=13, fontweight='bold')
ax3.set_xlabel('Frequency index ($k$)', fontsize=11)
ax3.set_ylabel('Value', fontsize=11)
ax3.set_xticks(k_vals)
ax3.set_xticklabels([f'$X_{k}$' for k in range(N)])
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)

# ── Panel 4: Magnitude spectrum ──────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
bars4 = ax4.bar(k_vals, magnitudes, color=c_mag, width=0.5, edgecolor='white',
                linewidth=1.5, zorder=3, alpha=0.85)
for i in range(N):
    ax4.annotate(f'{magnitudes[i]:.0f}', (k_vals[i], magnitudes[i]),
                 textcoords="offset points", xytext=(0, 10), ha='center',
                 fontsize=13, fontweight='bold', color=c_mag)

# Symmetry arrow
ax4.annotate('', xy=(3, magnitudes[3] + 0.3), xytext=(1, magnitudes[1] + 0.3),
             arrowprops=dict(arrowstyle='<->', color=c_freq, lw=2.5))
ax4.text(2, magnitudes[1] + 0.6, 'Mirror symmetry!', ha='center', fontsize=11,
         fontweight='bold', color=c_freq,
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#fef9e7', edgecolor=c_freq))

ax4.set_title('Magnitude Spectrum $|X_k| = \\sqrt{\\mathrm{Re}^2 + \\mathrm{Im}^2}$',
              fontsize=13, fontweight='bold')
ax4.set_xlabel('Frequency index ($k$)', fontsize=11)
ax4.set_ylabel('Magnitude $|X_k|$', fontsize=11)
ax4.set_xticks(k_vals)
ax4.set_xticklabels([f'$X_{k}$' for k in range(N)])
ax4.set_ylim(0, 5.5)
ax4.grid(True, alpha=0.3)

plt.savefig('assets/fft_step_by_step.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nGraph saved to assets/fft_step_by_step.png")

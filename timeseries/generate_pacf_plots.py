import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import os

# Create assets dir
os.makedirs('assets', exist_ok=True)

np.random.seed(42)
n_samples = 200

# 1. AR(1) Process: Y_t = 0.75 * Y_{t-1} + e_t
ar_coeff = 0.75
ar_data = np.zeros(n_samples)
errors = np.random.normal(0, 1, n_samples)
for t in range(1, n_samples):
    ar_data[t] = ar_coeff * ar_data[t-1] + errors[t]

# 2. MA(1) Process: Y_t = e_t + 0.75 * e_{t-1}
ma_coeff = 0.75
ma_data = np.zeros(n_samples)
for t in range(1, n_samples):
    ma_data[t] = errors[t] + ma_coeff * errors[t-1]

# Create plot
fig, axes = plt.subplots(2, 2, figsize=(14, 8))

# Color styles
color_ar = '#8e44ad'  # Purple
color_ma = '#16a085'  # Teal

# Row 1: AR(1)
plot_acf(ar_data, ax=axes[0, 0], lags=20, color=color_ar, vlines_kwargs={'colors': color_ar}, title='AR(1) Process: ACF (Decays/Tails Off)')
plot_pacf(ar_data, ax=axes[0, 1], lags=20, color=color_ar, vlines_kwargs={'colors': color_ar}, title='AR(1) Process: PACF (Cuts Off after Lag 1)')

# Row 2: MA(1)
plot_acf(ma_data, ax=axes[1, 0], lags=20, color=color_ma, vlines_kwargs={'colors': color_ma}, title='MA(1) Process: ACF (Cuts Off after Lag 1)')
plot_pacf(ma_data, ax=axes[1, 1], lags=20, color=color_ma, vlines_kwargs={'colors': color_ma}, title='MA(1) Process: PACF (Decays/Tails Off)')

for ax in axes.flat:
    ax.set_xlabel('Lag')
    ax.set_ylabel('Correlation')

plt.tight_layout()
plt.savefig('assets/pacf_examples.png', dpi=150)
plt.close()

print("PACF examples graph generated successfully.")

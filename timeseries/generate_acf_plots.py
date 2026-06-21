import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf
import os

# Create assets dir if it doesn't exist
os.makedirs('assets', exist_ok=True)

# Set seed for reproducibility
np.random.seed(42)
n_samples = 100
t = np.arange(n_samples)

# Scenario 1: Pure Random Noise (Stationary/White Noise)
white_noise = np.random.normal(0, 1, n_samples)

# Scenario 2: Strong Trend (Non-Stationary)
trend = 0.15 * t
trended_data = trend + np.random.normal(0, 1, n_samples)

# Scenario 3: Seasonality (Weekly Cycle of 7 days)
seasonality = 2.0 * np.sin(2 * np.pi * t / 7)
seasonal_data = seasonality + np.random.normal(0, 0.5, n_samples)

# Create Plot
fig, axes = plt.subplots(3, 2, figsize=(14, 10))

# Custom styles
color_noise = '#1abc9c'
color_trend = '#3498db'
color_season = '#e67e22'

# Row 1: White Noise
axes[0, 0].plot(t, white_noise, color=color_noise, linewidth=1.5)
axes[0, 0].axhline(0, color='gray', linestyle='--', linewidth=0.8)
axes[0, 0].set_title('1. Time Series: Pure Random Noise (Stationary)')
axes[0, 0].set_xlabel('Time')
axes[0, 0].set_ylabel('Value')

plot_acf(white_noise, ax=axes[0, 1], lags=30, color=color_noise, vlines_kwargs={'colors': color_noise}, title='ACF: Pure Random Noise')
axes[0, 1].set_xlabel('Lag')
axes[0, 1].set_ylabel('Autocorrelation')

# Row 2: Trend
axes[1, 0].plot(t, trended_data, color=color_trend, linewidth=1.5)
axes[1, 0].plot(t, trend, color='#e74c3c', linestyle=':', label='True Trend', linewidth=1.5)
axes[1, 0].set_title('2. Time Series: Data with Strong Trend (Non-Stationary)')
axes[1, 0].set_xlabel('Time')
axes[1, 0].set_ylabel('Value')
axes[1, 0].legend()

plot_acf(trended_data, ax=axes[1, 1], lags=30, color=color_trend, vlines_kwargs={'colors': color_trend}, title='ACF: Strong Trend (Tailing Off)')
axes[1, 1].set_xlabel('Lag')
axes[1, 1].set_ylabel('Autocorrelation')

# Row 3: Seasonality
axes[2, 0].plot(t, seasonal_data, color=color_season, linewidth=1.5)
axes[2, 0].set_title('3. Time Series: Data with Seasonality (7-Day Period)')
axes[2, 0].set_xlabel('Time')
axes[2, 0].set_ylabel('Value')

plot_acf(seasonal_data, ax=axes[2, 1], lags=30, color=color_season, vlines_kwargs={'colors': color_season}, title='ACF: Seasonality (Periodic Spikes)')
axes[2, 1].set_xlabel('Lag')
axes[2, 1].set_ylabel('Autocorrelation')

# Clean up layout
plt.tight_layout()
plt.savefig('assets/acf_examples.png', dpi=150)
plt.close()

print("ACF examples graph generated successfully.")

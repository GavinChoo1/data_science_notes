import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import statsmodels.api as sm
import os

# Create assets dir
os.makedirs('assets', exist_ok=True)

# Helper for plotting
def plot_before_after(original, trend, detrended, title, filename):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Before
    axes[0].plot(original, label='Original Data', color='blue')
    if trend is not None:
        axes[0].plot(trend, label='Fitted Trend', color='red', linestyle='--')
    axes[0].set_title(f'{title} (Before)')
    axes[0].legend()
    
    # After
    axes[1].plot(detrended, label='Detrended Data', color='green')
    axes[1].axhline(0, color='black', linestyle='--', linewidth=0.8)
    axes[1].set_title(f'{title} (After)')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig(f'assets/{filename}.png')
    plt.close()

np.random.seed(42)
t = np.arange(100)

# A. Linear Trend
noise = np.random.normal(0, 1, 100)
linear_trend = 0.5 * t
linear_data = linear_trend + noise

model = LinearRegression()
model.fit(t.reshape(-1, 1), linear_data)
linear_trend_fit = model.predict(t.reshape(-1, 1))
linear_detrended = linear_data - linear_trend_fit

plot_before_after(linear_data, linear_trend_fit, linear_detrended, 'A. Linear Trend', 'linear_trend')

# B. Non-Linear / Polynomial Trend
poly_trend = 0.05 * (t - 50)**2
poly_data = poly_trend + noise

poly = PolynomialFeatures(degree=2)
t_poly = poly.fit_transform(t.reshape(-1, 1))
model = LinearRegression()
model.fit(t_poly, poly_data)
poly_trend_fit = model.predict(t_poly)
poly_detrended = poly_data - poly_trend_fit

plot_before_after(poly_data, poly_trend_fit, poly_detrended, 'B. Non-Linear Trend', 'poly_trend')

# C. Changing / Non-Parametric Trend
changing_trend = np.sin(t / 10) * 10
changing_data = changing_trend + noise

# Using HP filter
cycle, trend_hp = sm.tsa.filters.hpfilter(changing_data, 1600)
changing_detrended = changing_data - trend_hp

plot_before_after(changing_data, trend_hp, changing_detrended, 'C. Changing Trend', 'changing_trend')

# D. Stochastic Trend (Random Walk)
random_walk = np.cumsum(np.random.normal(0, 1, 100))
# Detrending by differencing
rw_detrended = np.diff(random_walk)

# Plot manually for D since trend is not fitted
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].plot(random_walk, label='Original Data (Random Walk)', color='blue')
axes[0].set_title('D. Stochastic Trend (Before)')
axes[0].legend()

axes[1].plot(np.arange(1, 100), rw_detrended, label='Differenced Data', color='green')
axes[1].axhline(0, color='black', linestyle='--', linewidth=0.8)
axes[1].set_title('D. Stochastic Trend (After)')
axes[1].legend()
plt.tight_layout()
plt.savefig('assets/stochastic_trend.png')
plt.close()

print("Graphs generated successfully.")

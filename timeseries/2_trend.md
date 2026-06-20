# 2. The Trend ($T_t$)

## Detrending

### Step 1: The Visual Test (Plot & Inspect)
Generate a simple line plot of your raw data. Look closely at the overall long-term direction, ignoring the short-term seasonal wiggles. Your trend will almost always fall into one of these four visual categories:

#### A. Linear Trend
- **What it looks like**: The data climbs or falls steadily in a straight line over time.
- **The Math**: $T_t = \beta_0 + \beta_1 t$
- **Best Detrending Tool**: Linear Regression. Fit a straight line to the data and subtract it.

#### B. Non-Linear / Polynomial Trend
- **What it looks like**: The data curves. It might start slow and accelerate upward (exponential), or rise and then plateau (logarithmic).
- **The Math**: $T_t = \beta_0 + \beta_1 t + \beta_2 t^2 + \dots$
- **Best Detrending Tool**: Polynomial Regression. Fit a curve by choosing the appropriate degree (order) based on the number of turns in the graph.

#### C. Changing / Non-Parametric Trend
- **What it looks like**: The trend is smooth but erratic—it goes up for two years, flattens out, dips, and then goes up again. A single global equation cannot capture it.
- **Best Detrending Tool**: Moving Averages or STL / HP Filters. These tools calculate a rolling baseline that bends dynamically with the data.

#### D. Stochastic Trend (Random Walk)
- **What it looks like**: Highly erratic day-to-day or step-by-step drift with no stable long-term shape (very common in stock prices).
- **The Math**: $Y_t = Y_{t-1} + \epsilon_t$
- **Best Detrending Tool**: Differencing. Do not try to fit a trend line. Instead, subtract yesterday's value from today's value ($Y_t - Y_{t-1}$).

### Step 2: Statistical Verification (The KPSS Test)
If you aren't sure whether your visual guess is correct, you can back it up with a statistical test. The KPSS (Kwiatkowski-Phillips-Schmidt-Shin) test is specifically designed for this.

The KPSS test checks two different hypotheses:
1. Is the data stationary around a constant mean? (No trend exists).
2. Is the data stationary around a linear trend? (A predictable linear trend exists).

By running this test in Python (`statsmodels.tsa.stattools.kpss`), the output $p$-value will tell you definitively whether a deterministic trend exists or if you are dealing with a random stochastic drift that requires differencing.

### Step 3: Verify Your Success (The "After" Plot)
The ultimate way to know if you identified the trend accurately is to look at the residuals (the detrended data).

Once you subtract your calculated trend, plot the result. It is accurately detrended if it passes these two checks:
- **The Zero-Mean Check**: The graph must look completely horizontal, bouncing symmetrically above and below zero. If it still tilts or curves, your trend model was too simple (underfitted).
- **The Noise Check**: The remaining data should look like a combination of predictable seasonal waves and purely random noise.

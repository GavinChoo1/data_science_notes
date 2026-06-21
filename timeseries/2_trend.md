---
id: timeseries-trend
title: The Trend
desc: ''
updated: 1782008301000
created: 1782008301000
---

# 2. The Trend ($T_t$)

## Detrending

### Step 1: The Visual Test (Plot & Inspect)

Generate a simple line plot of your raw data. Look closely at the overall long-term direction, ignoring the short-term seasonal wiggles. Your trend will almost always fall into one of these four visual categories:

#### A. Linear Trend
> [!NOTE]
> **What it looks like**: The data climbs or falls steadily in a straight line over time.
> **The Math**: $T_t = \beta_0 + \beta_1 t$

**Best Detrending Tool**: Linear Regression. Fit a straight line to the data and subtract it.

![A. Linear Trend Before and After Detrending](assets/linear_trend.png)

#### B. Non-Linear / Polynomial Trend
> [!NOTE]
> **What it looks like**: The data curves. It might start slow and accelerate upward (exponential), or rise and then plateau (logarithmic).
> **The Math**: $T_t = \beta_0 + \beta_1 t + \beta_2 t^2 + \dots$

**Best Detrending Tool**: Polynomial Regression. Fit a curve by choosing the appropriate degree (order) based on the number of turns in the graph.

![B. Non-Linear Trend Before and After Detrending](assets/poly_trend.png)

#### C. Changing / Non-Parametric Trend
> [!NOTE]
> **What it looks like**: The trend is smooth but erratic—it goes up for two years, flattens out, dips, and then goes up again. A single global equation cannot capture it.

**Best Detrending Tool**: Moving Averages or STL / HP Filters. These tools calculate a rolling baseline that bends dynamically with the data.

![C. Changing Trend Before and After Detrending](assets/changing_trend.png)

#### D. Stochastic Trend (Random Walk)
> [!NOTE]
> **What it looks like**: Highly erratic day-to-day or step-by-step drift with no stable long-term shape (very common in stock prices).
> **The Math**: $Y_t = Y_{t-1} + \epsilon_t$

**Best Detrending Tool**: Differencing. Do not try to fit a trend line. Instead, subtract yesterday's value from today's value ($Y_t - Y_{t-1}$).

![D. Stochastic Trend Before and After Detrending](assets/stochastic_trend.png)

---

### Step 2: Statistical Verification (The KPSS Test)

If you aren't sure whether your visual guess is correct, you can back it up with a statistical test. The KPSS (Kwiatkowski-Phillips-Schmidt-Shin) test is specifically designed for this.

The KPSS test checks two different hypotheses:
1. Is the data stationary around a constant mean? (No trend exists).
2. Is the data stationary around a linear trend? (A predictable linear trend exists).

> [!TIP]
> By running this test in Python (`statsmodels.tsa.stattools.kpss`), the output $p$-value will tell you definitively whether a deterministic trend exists or if you are dealing with a random stochastic drift that requires differencing.

#### Deep Dive: KPSS Test

The KPSS test is a statistical test used to determine whether a time series is stationary or if it contains a trend. Unlike most other stationarity tests (like the ADF test), the KPSS test turns the logic upside down:

- **Null Hypothesis ($H_0$)**: The time series is stationary (either around a constant mean or around a deterministic trend).
- **Alternative Hypothesis ($H_1$)**: The time series is not stationary (it has a unit root / stochastic random trend).

> [!IMPORTANT]
> A low p-value (typically $< 0.05$) means you reject the null hypothesis, concluding that your data is not stationary and still has a random trend that needs to be fixed (usually by differencing).

##### Step-by-Step Breakdown of the KPSS Equation

The KPSS test works by breaking down your time series into three parts: a deterministic trend, a random walk, and stationary error.

**1. The Structural Model**
The test assumes the observed time series $Y_t$ can be written as:
$$Y_t = \xi t + r_t + \varepsilon_t$$
Where:
- $\xi t$ is a deterministic trend (a straight line over time $t$).
- $\varepsilon_t$ is a stationary error term (white noise).
- $r_t$ is a random walk component, defined as: $r_t = r_{t-1} + u_t$
*(Here, $u_t$ is pure random noise with a mean of 0 and a variance of $\sigma_u^2$).*

**Core logic:** If the variance of that random walk component ($\sigma_u^2$) is exactly zero, then $r_t$ becomes a constant baseline, meaning the random walk disappears. If the random walk disappears, the series is stationary! Therefore, the test fundamentally tests: $H_0: \sigma_u^2 = 0$.

**2. Calculate the Residuals ($e_t$)**
To isolate the random walk and noise, we first remove the deterministic parts by running a linear regression to get the estimated residuals:
$$e_t = Y_t - \hat{Y}_t$$

**3. Compute the Cumulative Sum of Residuals ($S_t$)**
Next, we track how the errors accumulate over time:
$$S_t = \sum_{i=1}^{t} e_i$$
If the data is stationary, the residuals will randomly bounce above and below zero, constantly canceling each other out, and $S_t$ will stay small. If there is a random drift, $S_t$ will grow larger.

**4. Calculate the Long-Run Variance ($s^2(l)$)**
We calculate a consistent estimator of the long-run variance of the residuals, which uses a look-back window (bandwidth $l$):
$$s^2(l) = \frac{1}{T} \sum_{t=1}^{T} e_t^2 + \frac{2}{T} \sum_{s=1}^{l} w(s, l) \sum_{t=s+1}^{T} e_t e_{t-s}$$
- $T$ is the total number of observations.
- $w(s, l)$ is a weighting function (usually a Newey-West Bartlett kernel).

**5. Calculate the KPSS Test Statistic ($LM$)**
Finally, we plug our cumulative sums ($S_t$) and long-run variance ($s^2(l)$) into the Lagrange Multiplier ($LM$) formula:
$$LM = \frac{\sum_{t=1}^{T} S_t^2}{T^2 \cdot s^2(l)}$$

> [!NOTE]
> **How to Interpret the Result**
> Compare the calculated $LM$ statistic to a table of critical values:
> - If $LM$ > critical value: Reject $H_0$. Data is not stationary (has a random trend).
> - If $LM$ < critical value: Fail to reject $H_0$. Data is stationary.

> [!NOTE]
> For more information on stationary error, read:
> [Deep Dive: Stationary Error](3_random_walk_vs_stationary.md)

---

### Step 3: Verify Your Success (The "After" Plot)

The ultimate way to know if you identified the trend accurately is to look at the residuals (the detrended data). Once you subtract your calculated trend, plot the result. It is accurately detrended if it passes these two checks:

1. **The Zero-Mean Check**: The graph must look completely horizontal, bouncing symmetrically above and below zero. If it still tilts or curves, your trend model was too simple (underfitted).
2. **The Noise Check**: The remaining data should look like a combination of predictable seasonal waves and purely random noise.

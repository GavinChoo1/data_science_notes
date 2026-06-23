---
id: timeseries-acf
title: Autocorrelation Function (ACF)
desc: "Deep dive into the Autocorrelation Function (ACF) plot, its math, and how to read correlograms"
updated: 1782008301000
created: 1782008301000
---

# Autocorrelation Function (ACF)

An Autocorrelation Function (ACF) plot, also known as a **correlogram**, is a visual tool used to measure how a data point in a time series relates to its own past values.

The "auto" in autocorrelation means _self_. Instead of measuring the relationship between two different variables (like studying study hours vs. exam scores), autocorrelation measures the relationship between a variable and a lagged version of itself (like today’s stock price vs. yesterday’s stock price).

---

## The Math: Understanding the Equation

To understand the ACF plot, we have to look at how we calculate the autocorrelation coefficient at a specific lag $k$ (written as $\rho_k$ or $r_k$).

The formula for the autocorrelation of a sample at lag $k$ is:

$$r_k = \frac{\sum_{t=k+1}^{n} (Y_t - \bar{Y})(Y_{t-k} - \bar{Y})}{\sum_{t=1}^{n} (Y_t - \bar{Y})^2}$$

Where:

- $Y_t$ is the value of the series at time $t$.
- $Y_{t-k}$ is the value of the series shifted back by $k$ time steps (the "lagged" value).
- $\bar{Y}$ is the overall mean (average) of the entire time series.
- $n$ is the total number of observations.

### Breaking Down the Components:

- **The Numerator (Autocovariance at Lag $k$)**: It calculates the covariance between the series and its lagged self using the standard cross-multiplication logic (how they move together relative to the mean).
- **The Denominator (Total Variance)**: It is the total sum of squared deviations from the mean (variance of the series). Dividing by the variance scales the result perfectly between $-1$ and $+1$, turning it into a standardized correlation coefficient.

---

## Concrete Example: Step-by-Step ACF Calculation

To understand how to calculate the Autocorrelation Function (ACF) step-by-step, we need to look at how a time series correlates with itself at different points in time.

When separating a random walk from a stationary error, the ACF is our definitive proof: a stationary error's ACF drops to zero immediately, while a random walk's ACF decays incredibly slowly.

Here is the step-by-step mathematical calculation for the ACF at Lag 1 ($k=1$), which measures how much today's values depend on yesterday's values.

### The Formula

The autocorrelation at lag $k$ (written as $\rho_k$ or "rho") is calculated by dividing the autocovariance ($c_k$) by the total variance ($c_0$):

$$\rho_k = \frac{c_k}{c_0}$$

Where the autocovariance at lag $k$ is:

$$c_k = \frac{1}{T} \sum_{t=k+1}^{T} (Y_t - \bar{Y})(Y_{t-k} - \bar{Y})$$

### Step-by-Step Calculation Example

Let's use a short time series of $T = 5$ observations:

$$Y = [2, 4, 5, 4, 5]$$

#### Step 1: Calculate the Mean ($\bar{Y}$)

First, find the simple average of the entire dataset.

$$\bar{Y} = \frac{2 + 4 + 5 + 4 + 5}{5} = \frac{20}{5} = 4$$

#### Step 2: Calculate the Variance / Lag 0 Covariance ($c_0$)

This acts as our denominator. It measures how much the data varies around its own mean. We subtract the mean from each point, square it, and sum them up:

$$c_0 = \frac{1}{5} \left[ (2-4)^2 + (4-4)^2 + (5-4)^2 + (4-4)^2 + (5-4)^2 \right]$$

$$c_0 = \frac{1}{5} \left[ (-2)^2 + (0)^2 + (1)^2 + (0)^2 + (1)^2 \right]$$

$$c_0 = \frac{1}{5} [4 + 0 + 1 + 0 + 1] = \frac{6}{5} = 1.2$$

#### Step 3: Align the Data for Lag 1 ($k=1$)

To find the covariance at Lag 1, we create a side-by-side comparison of the original data ($Y_t$) and the data shifted back by one time step ($Y_{t-1}$):

| Time ($t$) | Original ($Y_t$) | Lagged ($Y_{t-1}$) |
| :---: | :---: | :---: |
| 1 | 2 | *No past data* |
| 2 | 4 | 2 |
| 3 | 5 | 4 |
| 4 | 4 | 5 |
| 5 | 5 | 4 |

#### Visualizing Lag 1: The Scatter Plot (Lag Plot)

Before calculating the numbers, we can visualize this alignment. Autocorrelation is mathematically identical to a standard Pearson correlation, but calculated over a **lagged scatter plot** where we plot "yesterday's values" ($Y_{t-1}$) on the X-axis against "today's values" ($Y_t$) on the Y-axis:

![Lag 1 Scatter Plot showing Y_t vs Y_{t-1} for the sample data](assets/acf_lag1_scatter.png)

Looking at this plot, the points do not follow the diagonal line (some go up, some go down). This visual lack of a linear trend indicates that the correlation at Lag 1 will be close to $0$.

#### Step 4: Calculate the Lag 1 Autocovariance ($c_1$)

Now, we calculate the covariance using only the pairs that line up (from $t=2$ to $t=5$). For each pair, we subtract the mean ($\bar{Y} = 4$) from both values and multiply them together:

$$c_1 = \frac{1}{5} \sum_{t=2}^{5} (Y_t - 4)(Y_{t-1} - 4)$$

Let's calculate each of the 4 pairs:

- **Pair 1 ($t=2$)**: $(4 - 4) \times (2 - 4) = 0 \times (-2) = 0$
- **Pair 2 ($t=3$)**: $(5 - 4) \times (4 - 4) = 1 \times 0 = 0$
- **Pair 3 ($t=4$)**: $(4 - 4) \times (5 - 4) = 0 \times 1 = 0$
- **Pair 4 ($t=5$)**: $(5 - 4) \times (4 - 4) = 1 \times 0 = 0$

Summing them up:

$$c_1 = \frac{1}{5} [0 + 0 + 0 + 0] = 0$$

#### Step 5: Compute the Final Autocorrelation ($\rho_1$)

Divide the Lag 1 autocovariance by the total variance:

$$\rho_1 = \frac{c_1}{c_0} = \frac{0}{1.2} = 0$$

### How to Read This Result

An ACF value of $0$ at Lag 1 proves that there is absolutely zero linear relationship between what happened yesterday and what happened today.

If you plot the ACF across multiple lags (Lag 1, Lag 2, Lag 3, etc.), you get an ACF Plot:

- **Stationary Error**: The ACF value will be $1$ at Lag 0, and instantly drop close to $0$ for Lag 1 and beyond. It shows the data has no memory.
- **Random Walk**: Because a random walk carries its trend forward perpetually, its ACF calculation would yield values very close to $1.0$ for Lag 1, Lag 2, Lag 3, and drop off incredibly slowly over time.

---

## How to Read an ACF Plot: Three Example Scenarios

An ACF plot charts the lag number ($k = 1, 2, 3, \dots$) on the X-axis and the correlation coefficient ($r_k$) on the Y-axis. It also includes a shaded blue region representing the **95% confidence interval** (statistical significance boundary).

> [!NOTE]
> If a vertical bar pushes past this blue zone, the correlation at that lag is statistically significant (highly unlikely to be a random coincidence).

Here are the three most common patterns you will encounter:

### 1. Pure Random Noise (Stationary / White Noise)

If your data is truly random and stationary (like the residuals after you successfully clean a model), what happened yesterday has zero impact on today.

- **What the plot looks like**: Lag 0 will always be exactly $1.0$ (because a number is perfectly correlated with itself). Every single subsequent bar (Lag 1, Lag 2, etc.) will be tiny and sit comfortably inside the blue shaded margin of error.

### 2. Data with a Strong Trend (Non-Stationary)

If your data has a steady upward or downward trend, observations close to each other in time will have very similar values.

- **What the plot looks like**: You will see a distinct "tailing off" geometry. Lag 1 will be massive, Lag 2 slightly smaller, Lag 3 smaller still, forming a slow, gradual downward slope that takes a long time to cross back into the blue zone. This is a dead giveaway that the series is non-stationary and needs to be detrended.

### 3. Data with Seasonality

If your data has a repeating cycle—say, a weekly heartbeat in daily sales data—today's sales will be highly correlated with sales exactly 7 days ago, 14 days ago, and 21 days ago.

- **What the plot looks like**: The bars will form a wave-like pattern. You will see prominent, statistically significant spikes shooting out of the blue zone at regular intervals (e.g., exactly at Lag 7, Lag 14, Lag 21).

---

## The ACF Plot as a Diagnostic Superpower

While the textbook definition of the ACF plot is "measuring autocorrelation," its main practical superpower in the real world is acting as a diagnostic map to spot trends and seasonality before you build a model.

To put it all together, here is a quick reference table of exactly how the ACF plot talks to you:

| What you see on the ACF plot                               | What your data has      | What action you must take                           |
| :--------------------------------------------------------- | :---------------------- | :-------------------------------------------------- |
| **Bars slowly decay like a long, gradual ramp**            | A Trend                 | Detrend your data (e.g., difference it).            |
| **Bars spike rhythmically at regular lag intervals**       | Seasonality             | Deseasonalize your data (or use a seasonal model).  |
| **All bars are tiny and stay inside the blue shaded zone** | Pure Noise (Stationary) | Nothing! Your data is clean and ready for modeling. |

By checking the ACF plot at the beginning, middle, and end of your workflow, you ensure that you successfully strip away all the predictable patterns (trends and seasonality) until you are left with nothing but pure, uncorrelated random error.

> [!TIP]
> While the ACF plot measures total autocorrelation, the **Partial Autocorrelation Function (PACF)** is a complementary tool that strips away indirect correlation. To learn how it works and how to use it for model selection, check out the [Deep Dive: Partial Autocorrelation Function (PACF)](6_pacf.md).

---

## Visual Examples of ACF Plots

![ACF Examples in Three Scenarios](assets/acf_examples.png)

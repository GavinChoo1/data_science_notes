---
id: timeseries-pacf
title: Partial Autocorrelation Function (PACF)
desc: "Deep dive into the Partial Autocorrelation Function (PACF), its math, and how to use it to identify AR and MA models"
updated: 1782008301000
created: 1782008301000
---

# Partial Autocorrelation Function (PACF)

While the Autocorrelation Function (ACF) measures the total correlation between a data point $Y_t$ and its past value $Y_{t-k}$, it doesn't tell the whole story. Much of that correlation is often "inherited" through intermediate steps.

The **Partial Autocorrelation Function (PACF)** solves this by measuring the **direct correlation** between $Y_t$ and $Y_{t-k}$ after removing the linear effects of all intermediate lags ($Y_{t-1}, Y_{t-2}, \dots, Y_{t-k+1}$).

---

## The Concept: Removing the "Middlemen"

Imagine the temperature on three consecutive days: Monday ($Y_{t-2}$), Tuesday ($Y_{t-1}$), and Wednesday ($Y_t$).

- Monday's temperature affects Tuesday's temperature.
- Tuesday's temperature affects Wednesday's temperature.
- Because of this chain reaction, Monday's temperature is correlated with Wednesday's temperature.

If you run an **ACF** plot, it will show a strong correlation between Wednesday ($Y_t$) and Monday ($Y_{t-2}$). However, this is mostly an **indirect correlation** passed through the middleman, Tuesday ($Y_{t-1}$).

If you run a **PACF** plot, it strips away Tuesday's influence, measuring only the pure, direct relationship between Monday and Wednesday. If Monday has no unique information to offer Wednesday beyond what Tuesday already carries, the partial autocorrelation at lag 2 will be exactly **zero**.

---

## The Math: Two Ways to Define PACF

Mathematically, the partial autocorrelation coefficient at lag $k$ (written as $\phi_{kk}$ or $\alpha_k$) can be defined in two ways.

### Method 1: The Autoregressive Coefficient

The most common way to define the partial autocorrelation $\phi_{kk}$ at lag $k$ is as the last coefficient in a linear regression of $Y_t$ on its first $k$ lags:

$$Y_t = \phi_{k1} Y_{t-1} + \phi_{k2} Y_{t-2} + \dots + \phi_{kk} Y_{t-k} + \varepsilon_t$$

Where:

- $\phi_{ki}$ is the $i$-th coefficient in an autoregressive model of order $k$.
- $\phi_{kk}$ is the coefficient of the oldest lag ($Y_{t-k}$), which represents the partial autocorrelation at lag $k$.
- $\varepsilon_t$ is the residual error.

By including the intermediate lags ($Y_{t-1}, \dots, Y_{t-k+1}$) in the regression model, we control for their influence. The coefficient $\phi_{kk}$ measures the remaining correlation that is uniquely attributable to $Y_{t-k}$.

#### Visualizing Method 1: The 3D Regression Plane

The figure below illustrates this concept for an $AR(1)$ process. We fit a multiple linear regression $Y_t = \phi_{21} Y_{t-1} + \phi_{22} Y_{t-2} + \varepsilon_t$ and plot the resulting plane in the 3D space of ($Y_{t-2}$, $Y_{t-1}$, $Y_t$):

![3D regression plane showing PACF as multiple linear regression](assets/pacf_3d_regression.png)

Notice how the blue plane tilts steeply along the $Y_{t-1}$ axis (coefficient $\approx 0.72$) but is nearly **flat** along the $Y_{t-2}$ axis (coefficient $\approx 0.03$). The red lines are the residuals ($\varepsilon_t$). This flatness along $Y_{t-2}$ is precisely the PACF at Lag 2: once you account for yesterday ($Y_{t-1}$), two days ago ($Y_{t-2}$) adds virtually no unique predictive power.

### Method 2: Residual Correlation

Another way to calculate $\phi_{kk}$ is by finding the correlation between the residuals of two separate linear regressions:

1. Regress $Y_t$ on the intermediate lags to find what part of $Y_t$ cannot be explained by the intermediates:
   $$\hat{Y}_t = \beta_1 Y_{t-1} + \beta_2 Y_{t-2} + \dots + \beta_{k-1} Y_{t-k+1}$$
   $$u_t = Y_t - \hat{Y}_t$$

2. Regress $Y_{t-k}$ on the same intermediate lags to find what part of the oldest lag cannot be explained by the intermediates:
   $$\hat{Y}_{t-k} = \gamma_1 Y_{t-1} + \gamma_2 Y_{t-2} + \dots + \gamma_{k-1} Y_{t-k+1}$$
   $$v_{t-k} = Y_{t-k} - \hat{Y}_{t-k}$$

3. Calculate the partial autocorrelation as the simple Pearson correlation coefficient of these two residuals:
   $$\phi_{kk} = \text{Corr}(u_t, v_{t-k})$$

---

## Concrete Example: Step-by-Step PACF Calculation

To see how the PACF strips away intermediate relationships, let's perform a step-by-step calculation using the **Durbin-Levinson recursion**. This recursive algorithm is the standard method used by libraries like `statsmodels` in Python to calculate PACF values directly from the ACF values.

### The Durbin-Levinson Formulas

To calculate the partial autocorrelation $\phi_{kk}$ at lag $k$, we use the following recursive relations:

1. **At Lag 1 ($k=1$)**:
   $$\phi_{11} = r_1$$

2. **At Lag 2 ($k=2$)**:
   $$\phi_{22} = \frac{r_2 - \phi_{11} r_1}{1 - \phi_{11} r_1} = \frac{r_2 - r_1^2}{1 - r_1^2}$$
   _Intermediate coefficient needed for the next step:_
   $$\phi_{21} = \phi_{11} - \phi_{22}\phi_{11}$$

3. **At Lag 3 ($k=3$)**:
   $$\phi_{33} = \frac{r_3 - \phi_{21} r_2 - \phi_{22} r_1}{1 - \phi_{21} r_1 - \phi_{22} r_2}$$

---

### Step-by-Step Calculation Example

Let's use the exact same short time series of $T = 5$ observations from the [Autocorrelation Function (ACF) note](5_acf.md):

$$Y = [2, 4, 5, 4, 5]$$

From our ACF calculations in the previous note, we already know:

- The mean: $\bar{Y} = 4$
- The total variance (Lag 0 covariance): $c_0 = 1.2$
- The Lag 1 autocovariance: $c_1 = 0 \implies$ Lag 1 autocorrelation $r_1 = 0$

Let's compute the Lag 2 autocorrelation ($r_2$) and use the Durbin-Levinson recursion to find the PACF values at Lag 1 ($\phi_{11}$) and Lag 2 ($\phi_{22}$).

#### Step 1: Calculate the Lag 2 Autocorrelation ($r_2$)

First, we find the Lag 2 autocovariance ($c_2$) by aligning the data with a lag of 2:

| Time ($t$) | Original ($Y_t$) | Lagged ($Y_{t-2}$) |
| :--------: | :--------------: | :----------------: |
|     1      |        2         |   _No past data_   |
|     2      |        4         |   _No past data_   |
|     3      |        5         |         2          |
|     4      |        4         |         4          |
|     5      |        5         |         5          |

Now we calculate the covariance using only the 3 pairs that line up (from $t=3$ to $t=5$):

$$c_2 = \frac{1}{5} \sum_{t=3}^{5} (Y_t - 4)(Y_{t-2} - 4)$$

- **Pair 1 ($t=3$)**: $(Y_3 - 4) \times (Y_1 - 4) = (5 - 4) \times (2 - 4) = 1 \times (-2) = -2$
- **Pair 2 ($t=4$)**: $(Y_4 - 4) \times (Y_2 - 4) = (4 - 4) \times (4 - 4) = 0 \times 0 = 0$
- **Pair 3 ($t=5$)**: $(Y_5 - 4) \times (Y_3 - 4) = (5 - 4) \times (5 - 4) = 1 \times 1 = 1$

Summing them up:

$$c_2 = \frac{1}{5} [-2 + 0 + 1] = \frac{-1}{5} = -0.2$$

Next, divide by the total variance $c_0$ to get the Lag 2 autocorrelation $r_2$:

$$r_2 = \frac{c_2}{c_0} = \frac{-0.2}{1.2} = -\frac{1}{6} \approx -0.167$$

#### Step 2: Compute PACF at Lag 1 ($\phi_{11}$)

At Lag 1, the partial autocorrelation is identical to the standard autocorrelation:

$$\phi_{11} = r_1 = 0$$

#### Step 3: Compute PACF at Lag 2 ($\phi_{22}$)

Now we compute the partial autocorrelation at Lag 2. We use the formula to strip away any indirect correlation carried through Lag 1:

$$\phi_{22} = \frac{r_2 - r_1^2}{1 - r_1^2} = \frac{-0.167 - 0^2}{1 - 0^2} = -0.167$$

In this case, since the autocorrelation at Lag 1 was $r_1 = 0$, there was no "middleman" effect to strip away. As a result, the partial autocorrelation $\phi_{22}$ is exactly equal to the standard autocorrelation $r_2$.

---

### Graphical Representation of This Result

If we plot the **ACF** vs. the **PACF** for this sample dataset, we get:

```text
          ACF of Sample Data                       PACF of Sample Data
      1.0 | █                                  1.0 | █
      0.5 |                                    0.5 |
      0.0 +---+---+---                         0.0 +---+---+---
          |   |   |                                |   |   |
     -0.5 |       █                           -0.5 |       █
         Lag: 0   1   2                           Lag: 0   1   2
             (0) (-0.167)                             (0) (-0.167)
```

- **In the ACF plot**, we see a strong correlation of $1.0$ at Lag 0, zero correlation at Lag 1, and a negative correlation of $-0.167$ at Lag 2.
- **In the PACF plot**, because the Lag 1 correlation is $0$, there is no intermediate correlation pathway between $Y_t$ and $Y_{t-2}$. Thus, the PACF value at Lag 2 is exactly equal to the ACF value at Lag 2 ($-0.167$).

---

## How PACF is Used in the Real World

In time series modeling (specifically the **Box-Jenkins methodology** for ARIMA modeling), the combination of ACF and PACF plots is the primary tool used to determine the order of Autoregressive ($AR$) and Moving Average ($MA$) components.

### 1. Identifying Autoregressive $AR(p)$ Models

An Autoregressive process of order $p$, written as $AR(p)$, is modeled as:
$$Y_t = c + \phi_1 Y_{t-1} + \phi_2 Y_{t-2} + \dots + \phi_p Y_{t-p} + \varepsilon_t$$

- **ACF Behavior**: Tails off gradually (exponentially decaying or sinusoidal wave), because a shock at time $t$ propagates infinitely through the autoregressive chain.
- **PACF Behavior**: **Cuts off** abruptly after lag $p$. Since the true model only relies on lags up to $p$, any lag greater than $p$ has zero direct correlation with $Y_t$ once the intermediate lags are controlled.
- **Rule of Thumb**: If the PACF shows $p$ significant spikes before dropping inside the 95% confidence interval, you should fit an **$AR(p)$** model.

### 2. Identifying Moving Average $MA(q)$ Models

A Moving Average process of order $q$, written as $MA(q)$, is modeled as:
$$Y_t = c + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \theta_2 \varepsilon_{t-2} + \dots + \theta_q \varepsilon_{t-q}$$

- **ACF Behavior**: **Cuts off** abruptly after lag $q$. Since the series is only driven by the last $q$ shocks, observations separated by more than $q$ lags share zero common shocks.
- **PACF Behavior**: Tails off gradually (exponentially decaying or sinusoidal wave) instead of cutting off. This happens because the moving average shocks are back-calculated recursively, creating an infinite-memory autoregressive representation.
- **Rule of Thumb**: If the ACF cuts off after lag $q$ and the PACF decays slowly, you should fit an **$MA(q)$** model.

---

## Quick Diagnostic Reference Table

| Model            | ACF Plot                            | PACF Plot                           |
| :--------------- | :---------------------------------- | :---------------------------------- |
| **$AR(p)$**      | Decays / Tails off gradually        | **Cuts off abruptly after lag $p$** |
| **$MA(q)$**      | **Cuts off abruptly after lag $q$** | Decays / Tails off gradually        |
| **$ARMA(p, q)$** | Decays / Tails off gradually        | Decays / Tails off gradually        |

---

## Visual Comparison: AR(1) vs. MA(1)

Below is a visual example generated using simulated time series data. Notice how the behaviors of the ACF and PACF plots swap between the Autoregressive ($AR$) and Moving Average ($MA$) processes:

![ACF and PACF comparison for AR(1) and MA(1) processes](assets/pacf_examples.png)

---
id: timeseries-random-walk-vs-stationary
title: Random Walk vs. Stationary Error
desc: 'Deep dive into the differences between random walk and stationary error'
---

# Random Walk vs. Stationary Error

It is incredibly common to mix these two up because they are both built out of random noise, but they are fundamentally different in how they behave over time. The easiest way to understand the difference is to look at **memory**. 

- **Stationary Error ($\varepsilon_t$)**
  A stationary error term (often called white noise) represents pure, short-term randomness.
  - **The Math**: A sequence of independent random numbers drawn from a distribution with a mean of 0 and a constant variance ($\sigma^2$).
  - **Memory**: It has zero memory. Time step $t$ has absolutely no connection to time step $t-1$.
  - **Behavior**: It represents temporary shocks. The data immediately snaps back to its baseline.

- **Random Walk Component ($r_t$)**
  A random walk is built by accumulating (summing up) random shocks over time.
  - **The Math**: $r_t = r_{t-1} + u_t$
  - **Memory**: It has infinite memory. Because $r_{t-1}$ is embedded inside $r_t$, today's value is equal to the sum of every single random shock that has ever occurred.
  - **Behavior**: It represents permanent shocks. Shocks don't vanish; they alter your baseline permanently moving forward.

> [!TIP]
> **Visual Comparison: Shocks vs. Accumulation**
> Imagine you are flipping a coin: Heads = +1, Tails = -1.
> - **Stationary Error ($\varepsilon_t$)**: You look only at the result of the current flip. The result is always either +1 or -1. It never grows, never trends, and always bounces around 0.
> - **Random Walk ($r_t$)**: You keep a running total of your score. Your score can drift incredibly far away from 0 and stay there for a very long time.

![Stationary Error vs Random Walk](assets/rw_vs_stationary.png)

> [!WARNING]
> **Why This Matters for the KPSS Test**
> In the equation $Y_t = \xi t + r_t + \varepsilon_t$:
> If the variance of the shocks driving the random walk ($\sigma_u^2$) is greater than zero, the random walk grows, the series drifts randomly, and the data becomes non-stationary. If $\sigma_u^2 = 0$, the random walk turns off completely, leaving only the stationary error.

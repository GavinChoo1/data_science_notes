---
id: timeseries-fft
title: Fast Fourier Transform (FFT)
desc: "Deep dive into the Discrete Fourier Transform (DFT) and Fast Fourier Transform (FFT), with step-by-step manual calculations"
updated: 1782008301000
created: 1782008301000
---

# Fast Fourier Transform (FFT)

To understand the Fast Fourier Transform (FFT), we first need to look at what it actually calculates: the **Discrete Fourier Transform (DFT)**.

The DFT takes a time series and breaks it down into individual sine and cosine waves of different frequencies. The FFT is not a different mathematical transformation; it is simply a **highly optimized algorithm** designed to calculate the DFT much faster.

While a standard DFT takes $O(N^2)$ calculations, the FFT tricks the math into running in just $O(N \log N)$ steps, which is why modern digital audio, Wi-Fi, and time-series spectral analysis are possible.

---

## 1. The Mathematical Equation (DFT)

The formula to transform a sequence of $N$ time-domain samples, $x_n$, into the frequency domain, $X_k$, is:

$$X_k = \sum_{n=0}^{N-1} x_n \cdot e^{-j \frac{2\pi}{N} k n}$$

Where:

- $N$ is the total number of data points.
- $n$ is the current time index ($n = 0, 1, \dots, N-1$).
- $k$ is the current frequency index ($k = 0, 1, \dots, N-1$).
- $x_n$ is the value of your time-series data point at time $n$.
- $j$ is the imaginary unit ($\sqrt{-1}$).
- $X_k$ is a complex number ($a + bj$) representing both the **amplitude** and **phase** of frequency $k$.

### Euler's Formula Shortcut

To calculate this without dealing directly with exponents of $e$, we use Euler's Formula ($e^{-j\theta} = \cos(\theta) - j\sin(\theta)$) to split the equation into real and imaginary parts:

$$X_k = \sum_{n=0}^{N-1} x_n \left[ \cos\left(\frac{2\pi k n}{N}\right) - j \sin\left(\frac{2\pi k n}{N}\right) \right]$$

---

## 2. Step-by-Step Calculation (The FFT Strategy)

Most FFT algorithms (like the famous **Cooley-Tukey algorithm**) work by using a "divide-and-conquer" strategy. It breaks an $N$-point series into two halves: the even-indexed points and the odd-indexed points, calculates their pieces, and glues them back together.

Let's calculate the frequency components manually for a tiny, 4-point time series ($N = 4$):

$$x = [1, 2, 1, 0]$$

### Step 1: Set Up the Template for Each Frequency $k$

Because $N = 4$, our fraction inside the sine/cosine terms simplifies nicely:

$$\frac{2\pi k n}{N} = \frac{2\pi k n}{4} = \frac{\pi k n}{2}$$

Our equation for any given frequency $k$ becomes:

$$X_k = \sum_{n=0}^{3} x_n \left[ \cos\left(\frac{\pi k n}{2}\right) - j \sin\left(\frac{\pi k n}{2}\right) \right]$$

Here is the reference table of trigonometric values we will need:

|      Angle       | $\cos$ | $\sin$ |
| :--------------: | :----: | :----: |
|       $0$        |  $1$   |  $0$   |
| $\frac{\pi}{2}$  |  $0$   |  $1$   |
|      $\pi$       |  $-1$  |  $0$   |
| $\frac{3\pi}{2}$ |  $0$   |  $-1$  |
|      $2\pi$      |  $1$   |  $0$   |
|      $3\pi$      |  $-1$  |  $0$   |
| $\frac{9\pi}{2}$ |  $0$   |  $1$   |

### Step 2: Calculate $X_0$ (Frequency index $k = 0$)

This represents the baseline shift (the **DC offset**, or essentially the sum of your data). Plug in $k = 0$:

$$X_0 = \sum_{n=0}^{3} x_n [ \cos(0) - j\sin(0) ] = \sum_{n=0}^{3} x_n [ 1 - 0 ]$$

$$X_0 = x_0 + x_1 + x_2 + x_3$$

$$X_0 = 1 + 2 + 1 + 0 = \mathbf{4}$$

### Step 3: Calculate $X_1$ (Frequency index $k = 1$)

Plug in $k = 1$. Now the angles will change based on the time index $n$:

$$X_1 = x_0[\cos(0)-j\sin(0)] + x_1[\cos(\tfrac{\pi}{2})-j\sin(\tfrac{\pi}{2})] + x_2[\cos(\pi)-j\sin(\pi)] + x_3[\cos(\tfrac{3\pi}{2})-j\sin(\tfrac{3\pi}{2})]$$

Using the trig table:

| $n$ | $x_n$ | $\cos$ | $\sin$ | $x_n \cdot [\cos - j\sin]$ |
| :-: | :---: | :----: | :----: | :------------------------: |
|  0  |   1   |  $1$   |  $0$   |   $1 \cdot (1 - 0j) = 1$   |
|  1  |   2   |  $0$   |  $1$   |  $2 \cdot (0 - 1j) = -2j$  |
|  2  |   1   |  $-1$  |  $0$   |  $1 \cdot (-1 - 0j) = -1$  |
|  3  |   0   |  $0$   |  $-1$  |   $0 \cdot (0 + 1j) = 0$   |

Sum them up:

$$X_1 = 1 - 2j - 1 + 0 = \mathbf{-2j}$$

### Step 4: Calculate $X_2$ (Frequency index $k = 2$)

Plug in $k = 2$:

| $n$ | $x_n$ | Angle $\frac{\pi \cdot 2 \cdot n}{2}$ | $\cos$ | $\sin$ | $x_n \cdot [\cos - j\sin]$ |
| :-: | :---: | :-----------------------------------: | :----: | :----: | :------------------------: |
|  0  |   1   |                  $0$                  |  $1$   |  $0$   |   $1 \cdot (1 - 0j) = 1$   |
|  1  |   2   |                 $\pi$                 |  $-1$  |  $0$   |  $2 \cdot (-1 - 0j) = -2$  |
|  2  |   1   |                $2\pi$                 |  $1$   |  $0$   |   $1 \cdot (1 - 0j) = 1$   |
|  3  |   0   |                $3\pi$                 |  $-1$  |  $0$   |  $0 \cdot (-1 - 0j) = 0$   |

Sum them up:

$$X_2 = 1 - 2 + 1 + 0 = \mathbf{0}$$

### Step 5: Calculate $X_3$ (Frequency index $k = 3$)

Plug in $k = 3$:

| $n$ | $x_n$ | Angle $\frac{\pi \cdot 3 \cdot n}{2}$ | $\cos$ | $\sin$ | $x_n \cdot [\cos - j\sin]$ |
| :-: | :---: | :-----------------------------------: | :----: | :----: | :------------------------: |
|  0  |   1   |                  $0$                  |  $1$   |  $0$   |   $1 \cdot (1 - 0j) = 1$   |
|  1  |   2   |           $\frac{3\pi}{2}$            |  $0$   |  $-1$  |  $2 \cdot (0 + 1j) = 2j$   |
|  2  |   1   |                $3\pi$                 |  $-1$  |  $0$   |  $1 \cdot (-1 - 0j) = -1$  |
|  3  |   0   |           $\frac{9\pi}{2}$            |  $0$   |  $1$   |   $0 \cdot (0 - 1j) = 0$   |

Sum them up:

$$X_3 = 1 + 2j - 1 + 0 = \mathbf{2j}$$

---

## 3. The Final Spectrum Output

Our final frequency-domain array is:

$$X = [4, \ -2j, \ 0, \ 2j]$$

### How to Interpret This

Because these are complex numbers, scientists calculate the **Magnitude** (absolute strength) of each frequency using the Pythagorean theorem $|X_k| = \sqrt{\text{Re}^2 + \text{Im}^2}$:

| Frequency Index ($k$) | $X_k$ |             $             | X_k | = \sqrt{\text{Re}^2 + \text{Im}^2}$ |
| :-------------------: | :---: | :-----------------------: | --- | ----------------------------------- |
|   0 (DC Component)    |  $4$  |  $\sqrt{4^2 + 0^2} = 4$   |
|           1           | $-2j$ | $\sqrt{0^2 + (-2)^2} = 2$ |
|           2           |  $0$  |  $\sqrt{0^2 + 0^2} = 0$   |
|           3           | $2j$  |  $\sqrt{0^2 + 2^2} = 2$   |

> [!NOTE]
> Notice how Frequency 1 and Frequency 3 have the exact same magnitude ($2$)? That is due to a property called **symmetry**. In an FFT of real-world data, the second half of the output array is always a **mirror image** of the first half! This is why, in practice, you only need to look at the first $N/2$ frequency bins.

### Step-by-Step Visualization

The four panels below trace the entire FFT process from the input signal through Euler's twiddle factors to the final magnitude spectrum:

![FFT Step-by-Step Calculation for x = [1, 2, 1, 0]](assets/fft_step_by_step.png)

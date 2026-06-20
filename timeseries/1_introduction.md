# The 4 Components of a Time Series

## 1. The Trend ($T_t$)
The trend represents the long-term direction of the data. It tells you whether the values are generally increasing, decreasing, or staying stagnant over a long period.

**Example**: The steady increase in global internet usage over the last decade.

**Note**: The trend ignores short-term fluctuations and focuses entirely on the big picture.

## 2. Seasonality ($S_t$)
Seasonality refers to patterns that repeat at fixed, predictable intervals within a year, week, or even a day. These are usually tied to human habits, calendar events, or natural cycles.

**Example**: A massive spike in retail sales every December due to holiday shopping, or ice cream sales peaking every summer.

## 3. Cyclical Patterns ($C_t$)
Cyclical components are rises and falls that happen without a fixed period. Unlike seasonality, these fluctuations usually last longer than a year and their duration is unpredictable. They are often tied to economic or business cycles.

**Example**: Housing market booms and crashes that happen every 5 to 10 years.

## 4. Irregular / Residual Component ($I_t$)
Also known as "noise" or "white noise," this is the completely unpredictable, random variation left over after removing the trend, seasonality, and cycles. It is caused by unexpected, short-term events.

**Example**: A sudden drop in a store's sales because a massive snowstorm forced them to close for two days.

## How These Components Combine
To reconstruct or analyze the original data, statisticians combine these components using two main mathematical models:

### Additive Model
Use this model when the seasonal variations stay roughly the same size regardless of the trend's direction.

$$Y_t = T_t + S_t + C_t + I_t$$

### Multiplicative Model
Use this model when the seasonal variations change (increase or decrease) proportionally with the trend. As the trend goes up, the seasonal swings get wider.

$$Y_t = T_t \times S_t \times C_t \times I_t$$

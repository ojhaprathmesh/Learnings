# Time Series Analysis: From ARMA to ARCH/GARCH Models

## Overview
This project demonstrates a comprehensive time series analysis of three FTSE 250 stocks (DLR, KHC, CHTR), showcasing how prediction accuracy improves as we move from simple AR/MA models to more advanced ARCH and GARCH models for modeling financial volatility.

## Key Findings Summary

### 1. Why Raw Stock Prices Are Not Suitable for Prediction

**Problem with Raw Stock Prices:**
- **Non-stationarity**: Stock prices exhibit trends and do not have constant mean/variance over time
- **Unit root behavior**: Prices follow random walk patterns, making them unpredictable
- **Heteroscedasticity**: Variance changes over time, violating assumptions of linear models
- **Scale dependency**: Different stocks have vastly different price levels

**Why Log Returns Are Preferred:**
- **Stationarity**: Log returns typically have constant mean and variance
- **Scale independence**: Returns are normalized and comparable across different stocks
- **Financial interpretation**: Returns represent percentage changes, which are more meaningful for investment decisions
- **Better statistical properties**: More likely to follow normal distribution

From our analysis, the price vs returns plot clearly shows that while stock prices exhibit strong trends and non-stationary behavior, log returns fluctuate around zero with relatively constant variance, making them suitable for time series modeling.

### 2. ACF and PACF Analysis for ARMA Model Parameter Selection

**ACF (Autocorrelation Function) and PACF (Partial Autocorrelation Function) Interpretation:**

**DLR (Digital Realty Trust):**
- ACF shows gradual decay, suggesting AR component
- PACF cuts off after lag 1, indicating AR(1) process
- **Recommended ARMA model: ARMA(1,0) or AR(1)**
- Best fitted model: ARIMA(1,0) with AIC: -4898.93

**KHC (Kraft Heinz Company):**
- ACF shows oscillating pattern with gradual decay
- PACF shows significant spikes at multiple lags
- **Recommended ARMA model: ARMA(0,3) or MA(3)**
- Best fitted model: ARIMA(0,3) with AIC: -5245.83

**CHTR (Charter Communications):**
- ACF shows gradual decay with some oscillation
- PACF cuts off after lag 1 with some significance at lag 3
- **Recommended ARMA model: ARMA(1,3)**
- Best fitted model: ARIMA(1,3) with AIC: -4881.52

### 3. Model Performance Comparison: ARMA vs ARCH/GARCH

**ARMA Models (Linear Dependencies in Mean):**
- Good for capturing linear dependencies in the mean of returns
- Cannot model time-varying volatility
- Assume constant variance (homoscedasticity)
- Limited effectiveness for financial risk management

**ARCH/GARCH Models (Volatility Modeling):**
- Specifically designed to model time-varying volatility
- Capture volatility clustering (periods of high/low volatility)
- Better suited for financial risk management and option pricing
- Can model both mean and variance dynamics

**Performance Results:**
- **DLR**: ARIMA(1,0) AIC: -4898.93 vs GARCH(1,1) AIC: 4165.49
- **KHC**: ARIMA(0,3) AIC: -5245.83 vs GARCH(1,1) AIC: 3695.32
- **CHTR**: ARIMA(1,3) AIC: -4881.52 vs GARCH(1,1) AIC: 4250.76

*Note: ARIMA models have negative AIC values (better for mean modeling), while GARCH models have positive AIC values (focused on volatility modeling). These serve different purposes and are not directly comparable.*

### 4. Effectiveness of ARCH/GARCH for Volatility Clustering

**Evidence of Volatility Clustering:**
The volatility analysis plots clearly demonstrate:

1. **Volatility Clustering**: Periods of high volatility are followed by high volatility, and periods of low volatility are followed by low volatility
2. **Time-Varying Volatility**: The conditional volatility from GARCH models shows clear patterns of changing variance over time
3. **Persistence**: Volatility shocks have lasting effects, gradually decaying over time

**GARCH Model Advantages:**
- **Captures Stylized Facts**: Models the "volatility clustering" phenomenon observed in financial markets
- **Risk Management**: Provides better volatility forecasts for Value-at-Risk calculations
- **Option Pricing**: More accurate volatility estimates for derivatives pricing
- **Portfolio Optimization**: Better understanding of time-varying risk for asset allocation

**Conclusion:**
ARCH/GARCH models are significantly more effective than traditional ARMA models for modeling financial time series because they:
1. Explicitly model the time-varying nature of volatility
2. Capture the clustering of volatile periods
3. Provide better risk measures for financial decision-making
4. Account for the heteroscedastic nature of financial returns

While ARMA models are useful for modeling the mean behavior of returns, GARCH models are essential for understanding and predicting the risk characteristics of financial assets, making them indispensable tools in modern financial econometrics.

## Files Generated
- `time_series_analysis.py`: Main analysis script
- `plots/`: Directory containing all visualization outputs
  - `price_vs_returns.png`: Comparison of price levels vs log returns
  - `{TICKER}_acf_pacf.png`: ACF and PACF plots for each stock
  - `{TICKER}_volatility_analysis.png`: Volatility clustering analysis
- `requirements.txt`: Required Python packages
- `README.md`: This comprehensive analysis report

## How to Run
1. Install required packages: `pip install -r requirements.txt`
2. Run the analysis: `python time_series_analysis.py`
3. Check the `plots/` directory for generated visualizations
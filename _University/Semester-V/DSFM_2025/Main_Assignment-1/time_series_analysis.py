import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from arch import arch_model
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import yfinance as yf
warnings.filterwarnings('ignore')

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class TimeSeriesAnalysis:
    def __init__(self, tickers, start_date='2005-01-01', end_date='2014-12-31'):
        """
        Initialize the time series analysis with stock tickers
        
        Parameters:
        tickers (list): List of stock ticker symbols
        start_date (str): Start date for data collection
        end_date (str): End date for data collection
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.data = {}
        self.log_returns = {}
        self.results = {}
        
    def download_data(self):
        """Download stock data from Yahoo Finance"""
        print("Downloading stock data...")
        for ticker in self.tickers:
            try:
                stock_data = yf.download(ticker, start=self.start_date, end=self.end_date)
                self.data[ticker] = stock_data['Close']
                # Handle both single and multi-ticker downloads
                if ('Close', ticker) in stock_data.columns:
                    self.data[ticker] = stock_data[('Close', ticker)]
                else:
                    print(f"Available columns for {ticker}: {stock_data.columns.tolist()}")
                    raise KeyError("'Close' not found in data")
                
                print(f"✓ Downloaded data for {ticker}")
            except Exception as e:
                print(f"✗ Error downloading {ticker}: {e}")
        
    def calculate_log_returns(self):
        """Calculate log returns for all stocks"""
        print("\nCalculating log returns...")
        for ticker in self.tickers:
            if ticker in self.data:
                # Calculate log returns
                self.log_returns[ticker] = np.log(self.data[ticker] / self.data[ticker].shift(1)).dropna()
                print(f"✓ Calculated log returns for {ticker}")
    
    def plot_price_vs_returns(self):
        """Plot raw prices vs log returns to show stationarity"""
        fig, axes = plt.subplots(len(self.tickers), 2, figsize=(15, 4*len(self.tickers)))
        
        for i, ticker in enumerate(self.tickers):
            if ticker in self.data:
                # Raw prices
                axes[i, 0].plot(self.data[ticker], linewidth=1)
                axes[i, 0].set_title(f'{ticker} - Raw Stock Prices')
                axes[i, 0].set_ylabel('Price ($)')
                
                # Log returns
                axes[i, 1].plot(self.log_returns[ticker], linewidth=0.8, color='red')
                axes[i, 1].set_title(f'{ticker} - Log Returns')
                axes[i, 1].set_ylabel('Log Returns')
                axes[i, 1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig('plots/time_series/price_vs_returns.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def test_stationarity(self):
        """Perform Augmented Dickey-Fuller test for stationarity"""
        print("\n" + "="*60)
        print("STATIONARITY TESTS (Augmented Dickey-Fuller)")
        print("="*60)
        
        for ticker in self.tickers:
            if ticker in self.data:
                print(f"\n{ticker}:")
                
                # Test raw prices
                adf_price = adfuller(self.data[ticker].dropna())
                print(f"  Raw Prices - ADF Statistic: {adf_price[0]:.4f}")
                print(f"  Raw Prices - p-value: {adf_price[1]:.4f}")
                print(f"  Raw Prices - Stationary: {'Yes' if adf_price[1] < 0.05 else 'No'}")
                
                # Test log returns
                adf_returns = adfuller(self.log_returns[ticker])
                print(f"  Log Returns - ADF Statistic: {adf_returns[0]:.4f}")
                print(f"  Log Returns - p-value: {adf_returns[1]:.4f}")
                print(f"  Log Returns - Stationary: {'Yes' if adf_returns[1] < 0.05 else 'No'}")
    
    def plot_acf_pacf(self, ticker, lags=40):
        """Plot ACF and PACF for model identification"""
        if ticker not in self.log_returns:
            return
            
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))
        
        # ACF plot
        plot_acf(self.log_returns[ticker], lags=lags, ax=axes[0], alpha=0.05)
        axes[0].set_title(f'{ticker} - Autocorrelation Function (ACF)')
        
        # PACF plot
        plot_pacf(self.log_returns[ticker], lags=lags, ax=axes[1], alpha=0.05)
        axes[1].set_title(f'{ticker} - Partial Autocorrelation Function (PACF)')
        
        plt.tight_layout()
        plt.savefig(f'plots/time_series/{ticker}_acf_pacf.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def fit_arima_models(self, ticker, max_p=3, max_q=3):
        """Fit various ARIMA models and select best based on AIC"""
        if ticker not in self.log_returns:
            return
            
        print(f"\nFitting ARIMA models for {ticker}...")
        
        best_aic = np.inf
        best_model = None
        best_params = None
        model_results = []
        
        # Try different combinations of p and q
        for p in range(max_p + 1):
            for q in range(max_q + 1):
                try:
                    model = ARIMA(self.log_returns[ticker], order=(p, 0, q))
                    fitted_model = model.fit()
                    
                    aic = fitted_model.aic
                    model_results.append({
                        'p': p, 'q': q, 'AIC': aic,
                        'model_type': f'ARIMA({p},0,{q})'
                    })
                    
                    if aic < best_aic:
                        best_aic = aic
                        best_model = fitted_model
                        best_params = (p, q)
                        
                except:
                    continue
        
        # Store results
        self.results[ticker] = {
            'best_arima': best_model,
            'best_params': best_params,
            'model_comparison': pd.DataFrame(model_results)
        }
        
        print(f"Best ARIMA model for {ticker}: ARIMA{best_params} with AIC: {best_aic:.4f}")
        return best_model
    
    def fit_arch_garch_models(self, ticker):
        """Fit ARCH and GARCH models"""
        if ticker not in self.log_returns:
            return
            
        print(f"\nFitting ARCH/GARCH models for {ticker}...")
        
        returns = self.log_returns[ticker] * 100  # Scale for better convergence
        
        # Fit ARCH(1) model
        try:
            arch_model_fit = arch_model(returns, vol='ARCH', p=1)
            arch_result = arch_model_fit.fit(disp='off')
            self.results[ticker]['arch'] = arch_result
            print(f"✓ ARCH(1) model fitted for {ticker}")
        except Exception as e:
            print(f"✗ ARCH model failed for {ticker}: {e}")
        
        # Fit GARCH(1,1) model
        try:
            garch_model_fit = arch_model(returns, vol='GARCH', p=1, q=1)
            garch_result = garch_model_fit.fit(disp='off')
            self.results[ticker]['garch'] = garch_result
            print(f"✓ GARCH(1,1) model fitted for {ticker}")
        except Exception as e:
            print(f"✗ GARCH model failed for {ticker}: {e}")
    
    def compare_model_performance(self, ticker):
        """Compare performance of different models"""
        if ticker not in self.results:
            return
            
        print(f"\n" + "="*50)
        print(f"MODEL COMPARISON FOR {ticker}")
        print("="*50)
        
        returns = self.log_returns[ticker]
        
        # Split data for out-of-sample testing
        split_point = int(len(returns) * 0.8)
        test_data = returns[split_point:]
        
        performance_results = []
        
        # ARIMA model performance
        if 'best_arima' in self.results[ticker]:
            arima_model = self.results[ticker]['best_arima']
            arima_forecast = arima_model.forecast(steps=len(test_data))
            
            mse_arima = mean_squared_error(test_data, arima_forecast)
            mae_arima = mean_absolute_error(test_data, arima_forecast)
            
            performance_results.append({
                'Model': f"ARIMA{self.results[ticker]['best_params']}",
                'MSE': mse_arima,
                'MAE': mae_arima,
                'AIC': arima_model.aic
            })
        
        # ARCH/GARCH performance (using in-sample fit for demonstration)
        if 'arch' in self.results[ticker]:
            arch_model = self.results[ticker]['arch']
            performance_results.append({
                'Model': 'ARCH(1)',
                'MSE': 'N/A (Volatility Model)',
                'MAE': 'N/A (Volatility Model)',
                'AIC': arch_model.aic
            })
        
        if 'garch' in self.results[ticker]:
            garch_model = self.results[ticker]['garch']
            performance_results.append({
                'Model': 'GARCH(1,1)',
                'MSE': 'N/A (Volatility Model)',
                'MAE': 'N/A (Volatility Model)',
                'AIC': garch_model.aic
            })
        
        # Display results
        performance_df = pd.DataFrame(performance_results)
        print(performance_df.to_string(index=False))
        
        return performance_df
    
    def plot_volatility_clustering(self, ticker):
        """Plot volatility clustering and GARCH conditional volatility"""
        if ticker not in self.results or 'garch' not in self.results[ticker]:
            return
            
        returns = self.log_returns[ticker]
        garch_model = self.results[ticker]['garch']
        
        fig, axes = plt.subplots(2, 1, figsize=(15, 10))
        
        # Original returns
        axes[0].plot(returns.index, returns, linewidth=0.8, alpha=0.7)
        axes[0].set_title(f'{ticker} - Log Returns')
        axes[0].set_ylabel('Log Returns')
        axes[0].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        
        # GARCH conditional volatility
        conditional_vol = garch_model.conditional_volatility / 100  # Scale back
        axes[1].plot(returns.index, conditional_vol, linewidth=1, color='green')
        axes[1].set_title(f'{ticker} - GARCH(1,1) Conditional Volatility')
        axes[1].set_ylabel('Conditional Volatility')
        axes[1].set_xlabel('Date')
        
        plt.tight_layout()
        plt.savefig(f'plots/time_series/{ticker}_volatility_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        print("\n" + "="*80)
        print("COMPREHENSIVE TIME SERIES ANALYSIS SUMMARY")
        print("="*80)
        
        for ticker in self.tickers:
            if ticker in self.results:
                print(f"\n{ticker} Summary:")
                print("-" * 30)
                
                if 'best_arima' in self.results[ticker]:
                    arima_params = self.results[ticker]['best_params']
                    arima_aic = self.results[ticker]['best_arima'].aic
                    print(f"Best ARIMA Model: ARIMA{arima_params} (AIC: {arima_aic:.4f})")
                
                if 'arch' in self.results[ticker]:
                    arch_aic = self.results[ticker]['arch'].aic
                    print(f"ARCH(1) Model AIC: {arch_aic:.4f}")
                
                if 'garch' in self.results[ticker]:
                    garch_aic = self.results[ticker]['garch'].aic
                    print(f"GARCH(1,1) Model AIC: {garch_aic:.4f}")
    
    def run_complete_analysis(self):
        """Run the complete time series analysis pipeline"""
        # Create directory for plots
        import os
        os.makedirs('plots/time_series', exist_ok=True)
        
        # Step 1: Download data
        self.download_data()
        
        # Step 2: Calculate log returns
        self.calculate_log_returns()
        
        # Step 3: Plot prices vs returns
        self.plot_price_vs_returns()
        
        # Step 4: Test stationarity
        self.test_stationarity()
        
        # Step 5: ACF/PACF analysis for each stock
        for ticker in self.tickers:
            if ticker in self.log_returns:
                self.plot_acf_pacf(ticker)
        
        # Step 6: Fit ARIMA models
        for ticker in self.tickers:
            if ticker in self.log_returns:
                self.fit_arima_models(ticker)
        
        # Step 7: Fit ARCH/GARCH models
        for ticker in self.tickers:
            if ticker in self.log_returns:
                self.fit_arch_garch_models(ticker)
        
        # Step 8: Compare model performance
        for ticker in self.tickers:
            if ticker in self.results:
                self.compare_model_performance(ticker)
        
        # Step 9: Plot volatility clustering
        for ticker in self.tickers:
            if ticker in self.results:
                self.plot_volatility_clustering(ticker)
        
        # Step 10: Generate summary report
        self.generate_summary_report()

def main():
    """Main function to run the analysis"""
    tickers = ['DLR', 'KHC', 'CHTR']
    
    # Initialize object with desired tickers and date range
    analysis = TimeSeriesAnalysis(tickers, start_date='2020-01-01', end_date='2024-01-01')
    
    # Run complete analysis
    analysis.run_complete_analysis()
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("Check the 'plots/time_series' folder for visualizations")
    print("="*80)

if __name__ == "__main__":
    main()
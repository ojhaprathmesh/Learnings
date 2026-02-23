"""
FTSE250 Stock Data Analysis and Preprocessing
============================================

This script performs comprehensive data preparation, preprocessing, and visualization
for FTSE250 stock data analysis.
"""

from datetime import timedelta
import glob
import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
from sklearn.metrics import euclidean_distances
warnings.filterwarnings('ignore')

class FTSE250Analyzer:
    """
    A comprehensive class for FTSE250 stock data analysis and preprocessing.
    """
    
    def __init__(self, data_dir, start_date="2004-01-01", end_date="2014-01-01"):
        """
        Initialize the FTSE250 analyzer.
        
        Parameters:
        -----------
        data_dir : str
            Path to the data directory containing organized data
        start_date : str
            Start date for analysis (format: YYYY-MM-DD)
        end_date : str
            End date for analysis (format: YYYY-MM-DD)
        """
        self.data_dir = data_dir
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.ftse_live_data = None
        self.stock_data = {}
        self.master_df = None
        self.excluded_stocks = []
        
        # Create output directories
        self.create_output_directories()
        
    def create_output_directories(self):
        """Create necessary output directories."""
        os.makedirs("processed_data", exist_ok=True)
        os.makedirs("plots/ftse250_analysis", exist_ok=True)
        
    def load_ftse_constituent_data(self):
        """
        Load FTSE250 constituent data from CSV file with comprehensive logging.
        """
        print("=" * 60)
        print("LOADING FTSE250 CONSTITUENT DATA")
        print("=" * 60)
        
        ftse_file = os.path.join(self.data_dir, "FTSE Mid-Cap 250 (FTMC) Live.csv")
        
        try:
            self.ftse_live_data = pd.read_csv(ftse_file)
            
            # Success logging
            print(f"✓ Successfully loaded FTSE250 constituent data")
            print(f"  - File: {os.path.basename(ftse_file)}")
            print(f"  - Total records: {len(self.ftse_live_data)}")
            print(f"  - Columns: {list(self.ftse_live_data.columns)}")
            
            # Clean stock names for file matching
            self.ftse_live_data['Clean_Name'] = self.ftse_live_data['Name'].str.strip()
            
            # Display sample of loaded data
            print(f"\nSample of loaded constituent data:")
            print(f"{'Name':<30} {'Last':<10} {'Chg. %':<10}")
            print("-" * 50)
            for idx, row in self.ftse_live_data.head(5).iterrows():
                name = str(row['Name'])[:28] + ".." if len(str(row['Name'])) > 30 else str(row['Name'])
                last = str(row.get('Last', 'N/A'))[:8]
                raw_chg = str(row.get('Chg. %', 'N/A'))
                
                # Format change percentage with proper sign handling
                if raw_chg == 'N/A':
                    chg = 'N/A'
                else:
                    clean_chg = raw_chg.replace('+', '').replace('-', '').replace('%', '')
                    try:
                        chg_value = float(clean_chg)
                        if raw_chg.startswith('-') or chg_value < 0:
                            chg = f"-{abs(chg_value):.2f}%"
                        else:
                            chg = f"+{chg_value:.2f}%"
                    except ValueError:
                        chg = raw_chg
                
                chg = chg[:8]  # Truncate to fit column width
                print(f"{name:<30} {last:<10} {chg:<10}")
            
            if len(self.ftse_live_data) > 5:
                print(f"... and {len(self.ftse_live_data) - 5} more records")
            
            return True
            
        except FileNotFoundError:
            print(f"✗ ERROR: FTSE constituent file not found")
            print(f"  - Expected file: {ftse_file}")
            print(f"  - Please ensure the file exists in the correct location")
            return False
        except pd.errors.EmptyDataError:
            print(f"✗ ERROR: FTSE constituent file is empty")
            print(f"  - File: {ftse_file}")
            return False
        except pd.errors.ParserError as e:
            print(f"✗ ERROR: Failed to parse FTSE constituent file")
            print(f"  - File: {ftse_file}")
            print(f"  - Parser error: {e}")
            return False
        except Exception as e:
            print(f"✗ ERROR: Unexpected error loading FTSE constituent data")
            print(f"  - File: {ftse_file}")
            print(f"  - Error: {e}")
            return False
    
    def standardize_date_format(self, date_str):
        """
        Standardize various date formats to datetime objects.
        
        Parameters:
        -----------
        date_str : str
            Date string in various formats
            
        Returns:
        --------
        datetime
            Standardized datetime object
        """
        # Common date formats in financial data
        date_formats = [
            '%d-%m-%Y',    # 13-10-2022
            '%Y-%m-%d',    # 2022-10-13
            '%m/%d/%Y',    # 10/13/2022
            '%d/%m/%Y',    # 13/10/2022
            '%Y/%m/%d',    # 2022/10/13
        ]
        
        for fmt in date_formats:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except:
                continue
        
        # If none of the formats work, try pandas' automatic parsing
        try:
            return pd.to_datetime(date_str)
        except:
            return None
    
    def load_stock_historical_data(self):
        """
        Load and process historical stock data from individual CSV files with comprehensive logging.
        """
        print("\n" + "=" * 60)
        print("LOADING HISTORICAL STOCK DATA")
        print("=" * 60)
        
        stocks_dir = os.path.join(self.data_dir, "stocks")
        stock_files = glob.glob(os.path.join(stocks_dir, "*.csv"))
        
        print(f"Found {len(stock_files)} stock files in directory: {stocks_dir.replace(os.sep, '/')}")
        
        # Initialize tracking variables
        successful_loads = 0
        failed_loads = 0
        error_categories = {
            'file_not_found': 0,
            'no_date_column': 0,
            'no_price_column': 0,
            'date_parsing_error': 0,
            'price_parsing_error': 0,
            'empty_after_filter': 0,
            'general_error': 0
        }
        
        successful_stocks = []
        failed_stocks = []
        
        print(f"\nProcessing stock files...")
        print("-" * 60)
        
        for file_idx, file_path in enumerate(stock_files, 1):
            filename = os.path.basename(file_path)
            stock_name = None
            
            try:
                # Extract stock name from filename
                stock_name = filename.replace(" Historical Data.csv", "").replace("Historical Data.csv", "")
                
                # Handle special cases with numbers in parentheses
                if "(" in stock_name and ")" in stock_name:
                    stock_name = stock_name.split("(")[0].strip()
                
                # Load the CSV file
                try:
                    df = pd.read_csv(file_path)
                except FileNotFoundError:
                    error_categories['file_not_found'] += 1
                    failed_loads += 1
                    failed_stocks.append({
                        'name': stock_name,
                        'file': filename,
                        'error': 'File not found',
                        'category': 'file_not_found'
                    })
                    print(f"[{file_idx:3d}/{len(stock_files)}] ✗ {stock_name:<25} - File not found")
                    continue
                except pd.errors.EmptyDataError:
                    error_categories['general_error'] += 1
                    failed_loads += 1
                    failed_stocks.append({
                        'name': stock_name,
                        'file': filename,
                        'error': 'Empty file',
                        'category': 'general_error'
                    })
                    print(f"[{file_idx:3d}/{len(stock_files)}] ✗ {stock_name:<25} - Empty file")
                    continue
                
                # Standardize column names
                df.columns = df.columns.str.strip()
                
                # Handle different possible column names for date
                date_columns = ['Date', 'date', 'DATE']
                date_col = None
                for col in date_columns:
                    if col in df.columns:
                        date_col = col
                        break
                
                if date_col is None:
                    error_categories['no_date_column'] += 1
                    failed_loads += 1
                    failed_stocks.append({
                        'name': stock_name,
                        'file': filename,
                        'error': f'No date column found. Available columns: {list(df.columns)}',
                        'category': 'no_date_column'
                    })
                    print(f"[{file_idx:3d}/{len(stock_files)}] ✗ {stock_name:<25} - No date column")
                    continue
                
                # Convert date column
                try:
                    df['Date'] = df[date_col].apply(self.standardize_date_format)
                    df = df.dropna(subset=['Date'])
                    
                    if len(df) == 0:
                        error_categories['date_parsing_error'] += 1
                        failed_loads += 1
                        failed_stocks.append({
                            'name': stock_name,
                            'file': filename,
                            'error': 'All dates failed to parse',
                            'category': 'date_parsing_error'
                        })
                        print(f"[{file_idx:3d}/{len(stock_files)}] ✗ {stock_name:<25} - Date parsing failed")
                        continue
                        
                except Exception as e:
                    error_categories['date_parsing_error'] += 1
                    failed_loads += 1
                    failed_stocks.append({
                        'name': stock_name,
                        'file': filename,
                        'error': f'Date parsing error: {str(e)}',
                        'category': 'date_parsing_error'
                    })
                    print(f"[{file_idx:3d}/{len(stock_files)}] ✗ {stock_name:<25} - Date parsing error")
                    continue
                
                # Handle different possible column names for price
                price_columns = ['Price', 'Close', 'Adj Close', 'price', 'close']
                price_col = None
                for col in price_columns:
                    if col in df.columns:
                        price_col = col
                        break
                
                if price_col is None:
                    error_categories['no_price_column'] += 1
                    failed_loads += 1
                    failed_stocks.append({
                        'name': stock_name,
                        'file': filename,
                        'error': f'No price column found. Available columns: {list(df.columns)}',
                        'category': 'no_price_column'
                    })
                    print(f"[{file_idx:3d}/{len(stock_files)}] ✗ {stock_name:<25} - No price column")
                    continue
                
                # Clean price data (remove commas, convert to float)
                try:
                    if price_col != 'Price':
                        df['Price'] = df[price_col]
                    
                    # Clean price values
                    df['Price'] = df['Price'].astype(str).str.replace(',', '').str.replace('"', '')
                    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
                    
                    # Remove rows with invalid prices
                    original_len = len(df)
                    df = df.dropna(subset=['Price'])
                    
                    if len(df) == 0:
                        error_categories['price_parsing_error'] += 1
                        failed_loads += 1
                        failed_stocks.append({
                            'name': stock_name,
                            'file': filename,
                            'error': 'All prices failed to parse or are invalid',
                            'category': 'price_parsing_error'
                        })
                        print(f"[{file_idx:3d}/{len(stock_files)}] ✗ {stock_name:<25} - Price parsing failed")
                        continue
                        
                except Exception as e:
                    error_categories['price_parsing_error'] += 1
                    failed_loads += 1
                    failed_stocks.append({
                        'name': stock_name,
                        'file': filename,
                        'error': f'Price parsing error: {str(e)}',
                        'category': 'price_parsing_error'
                    })
                    print(f"[{file_idx:3d}/{len(stock_files)}] ✗ {stock_name:<25} - Price parsing error")
                    continue
                
                # Filter by date range
                df_filtered = df[(df['Date'] >= self.start_date) & (df['Date'] < self.end_date)]
                
                if len(df_filtered) == 0:
                    error_categories['empty_after_filter'] += 1
                    failed_loads += 1
                    failed_stocks.append({
                        'name': stock_name,
                        'file': filename,
                        'error': f'No data in date range {self.start_date} to {self.end_date}',
                        'category': 'empty_after_filter'
                    })
                    print(f"[{file_idx:3d}/{len(stock_files)}] ✗ {stock_name:<25} - No data in date range")
                    continue
                
                # Sort by date and set index
                df_filtered = df_filtered.sort_values('Date')
                df_filtered = df_filtered.set_index('Date')
                
                # Store the price series
                self.stock_data[stock_name] = df_filtered['Price']
                successful_loads += 1
                
                # Record successful load
                successful_stocks.append({
                    'name': stock_name,
                    'file': filename,
                    'records': len(df_filtered),
                    'date_range': f"{df_filtered.index.min().strftime('%Y-%m-%d')} to {df_filtered.index.max().strftime('%Y-%m-%d')}",
                    'original_records': original_len,
                    'filtered_records': len(df_filtered)
                })
                
                print(f"[{file_idx:3d}/{len(stock_files)}] ✓ {stock_name:<25} - {len(df_filtered):4d} records ({df_filtered.index.min().strftime('%Y-%m-%d')} to {df_filtered.index.max().strftime('%Y-%m-%d')})")
                
            except Exception as e:
                error_categories['general_error'] += 1
                failed_loads += 1
                failed_stocks.append({
                    'name': stock_name or 'Unknown',
                    'file': filename,
                    'error': f'Unexpected error: {str(e)}',
                    'category': 'general_error'
                })
                print(f"[{file_idx:3d}/{len(stock_files)}] ✗ {stock_name or 'Unknown':<25} - Unexpected error: {str(e)}")
                continue
        
        # Store results for summary
        self.load_summary = {
            'total_files': len(stock_files),
            'successful_loads': successful_loads,
            'failed_loads': failed_loads,
            'error_categories': error_categories,
            'successful_stocks': successful_stocks,
            'failed_stocks': failed_stocks
        }
        
        # Print detailed summary
        self.print_loading_summary()
        
        return successful_loads > 0
    
    def print_loading_summary(self):
        """
        Print comprehensive summary of data loading results.
        """
        print("\n" + "=" * 60)
        print("DATA LOADING SUMMARY")
        print("=" * 60)
        
        summary = self.load_summary
        
        # Overall statistics
        print(f"📊 OVERALL STATISTICS:")
        print(f"   Total files processed: {summary['total_files']}")
        print(f"   Successfully loaded:   {summary['successful_loads']} ({summary['successful_loads']/summary['total_files']*100:.1f}%)")
        print(f"   Failed to load:        {summary['failed_loads']} ({summary['failed_loads']/summary['total_files']*100:.1f}%)")
        
        # Failed loads details
        if summary['failed_loads'] > 0:
            print(f"\n❌ FAILED TO LOAD: {summary['failed_loads']} stocks")
            
            for stock in summary['failed_stocks']:
                print(f"   {stock['name']}")
        
        # Data quality metrics
        if summary['successful_loads'] > 0:
            total_records = sum(stock['records'] for stock in summary['successful_stocks'])
            avg_records = total_records / summary['successful_loads']
            
            print(f"\n📈 DATA QUALITY METRICS:")
            print(f"   Total records loaded:     {total_records:,}")
            print(f"   Avg records per stock:    {avg_records:.0f}")
            
            # Date range coverage
            all_start_dates = []
            all_end_dates = []
            for stock in summary['successful_stocks']:
                date_range = stock['date_range']
                start_date, end_date = date_range.split(' to ')
                all_start_dates.append(pd.to_datetime(start_date))
                all_end_dates.append(pd.to_datetime(end_date))
            
            earliest_start = min(all_start_dates)
            latest_end = max(all_end_dates)
            
            print(f"   Date coverage:            {earliest_start.strftime('%Y-%m-%d')} to {latest_end.strftime('%Y-%m-%d')}")
            print(f"   Analysis period:          {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}")
        
        print("=" * 60)
    
    def create_master_csv(self):
        """
        Create a consolidated CSV file with closing prices for all stocks.
        """
        print("Creating master CSV file...")
        
        if not self.stock_data:
            print("No stock data available to create master CSV")
            return False
        
        # Create a business day range for the entire period (excludes weekends)
        date_range = pd.bdate_range(start=self.start_date, end=self.end_date - timedelta(days=1))
        
        # Create master dataframe
        master_data = {}
        
        for stock_name, price_series in self.stock_data.items():
            # Reindex to business day range, this will introduce NaN for missing business days only
            full_series = price_series.reindex(date_range)
            master_data[stock_name] = full_series
        
        self.master_df = pd.DataFrame(master_data)
        
        # Add metadata columns
        self.master_df.index.name = 'Date'
        
        # Save to CSV
        output_file = "processed_data/ftse250_master_data.csv"
        self.master_df.to_csv(output_file)
        
        print(f"Master CSV created with {len(self.master_df.columns)} stocks and {len(self.master_df)} business days")
        
        return True
    
    def analyze_missing_data(self):
        """
        Analyze missing data patterns and identify stocks with >2 consecutive missing business days.
        """
        print("Analyzing missing data patterns...")
        
        if self.master_df is None:
            print("Master dataframe not available")
            return
        
        # Calculate missing data statistics
        missing_stats = {}
        stocks_to_exclude = []
        
        for stock in self.master_df.columns:
            series = self.master_df[stock]
            
            # Count total missing values
            total_missing = series.isna().sum()
            total_days = len(series)
            missing_percentage = (total_missing / total_days) * 100
            
            # Find consecutive missing periods (only for business days)
            is_missing = series.isna()
            consecutive_missing = []
            current_streak = 0
            max_streak = 0
            
            for missing in is_missing:
                if missing:
                    current_streak += 1
                    max_streak = max(max_streak, current_streak)
                else:
                    if current_streak > 0:
                        consecutive_missing.append(current_streak)
                    current_streak = 0
            
            # Add final streak if it ends with missing values
            if current_streak > 0:
                consecutive_missing.append(current_streak)
            
            missing_stats[stock] = {
                'total_missing': total_missing,
                'missing_percentage': missing_percentage,
                'max_consecutive_missing': max_streak,
                'consecutive_periods': consecutive_missing
            }
            
            # Check if stock should be excluded (>2 consecutive missing business days)
            # Use a more lenient threshold for business days
            if max_streak > 5:  # Allow up to 5 consecutive missing business days (1 week)
                stocks_to_exclude.append(stock)
        
        # Create missing data summary
        missing_df = pd.DataFrame(missing_stats).T
        missing_df.to_csv("processed_data/missing_data_analysis.csv")
        
        print(f"Missing data analysis completed")
        print(f"Stocks with >5 consecutive missing business days: {len(stocks_to_exclude)}")
        
        if stocks_to_exclude:
            print("Stocks to be excluded:")
            print(f"{'Name':<30} {'Consecutive Missing Business Days':<35}")
            print("-" * 65)
            for stock in stocks_to_exclude:
                max_missing = missing_stats[stock]['max_consecutive_missing']
                name = stock[:28] + ".." if len(stock) > 30 else stock
                print(f"{name:<30} {max_missing:<35}")
        
        self.excluded_stocks = stocks_to_exclude
        
        return missing_stats
    
    def remove_problematic_stocks(self):
        """
        Remove stocks with >2 consecutive missing days from the dataset.
        """
        if not self.excluded_stocks:
            print("No stocks to exclude")
            return
        
        print(f"Removing {len(self.excluded_stocks)} problematic stocks...")
        
        # Create cleaned dataset
        cleaned_df = self.master_df.drop(columns=self.excluded_stocks)
        
        # Update master dataframe
        self.master_df = cleaned_df
        
        print(f"Cleaned dataset created with {len(cleaned_df.columns)} stocks")
        
    
    def create_time_series_visualizations(self, output_dir="plots/ftse250_analysis"):
        """
        Generate 3x3 subplot grids displaying closing price time series.
        """
        print("Creating time series visualizations...")
        
        if self.master_df is None:
            print("Master dataframe not available")
            return
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        stocks = list(self.master_df.columns)
        n_stocks = len(stocks)
        
        # Calculate number of plots needed
        stocks_per_plot = 9
        n_plots = (n_stocks + stocks_per_plot - 1) // stocks_per_plot
        
        for plot_idx in range(n_plots):
            start_idx = plot_idx * stocks_per_plot
            end_idx = min(start_idx + stocks_per_plot, n_stocks)
            plot_stocks = stocks[start_idx:end_idx]
            
            # Create 3x3 subplot grid
            fig, axes = plt.subplots(3, 3, figsize=(20, 15))
            fig.suptitle(f'FTSE250 Stock Price Time Series - Set {plot_idx + 1}', fontsize=16, fontweight='bold')
            
            # Flatten axes for easier indexing
            axes_flat = axes.flatten()
            
            for i, stock in enumerate(plot_stocks):
                ax = axes_flat[i]
                
                # Plot the time series
                data = self.master_df[stock].dropna()
                ax.plot(data.index, data.values, linewidth=1.2, alpha=0.8)
                
                # Formatting
                ax.set_title(f'{stock}', fontsize=10, fontweight='bold')
                ax.set_xlabel('Date', fontsize=8)
                ax.set_ylabel('Price', fontsize=8)
                ax.grid(True, alpha=0.3)
                ax.tick_params(axis='x', rotation=45, labelsize=7)
                ax.tick_params(axis='y', labelsize=7)
                
                # Format y-axis to show prices nicely
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x:.0f}'))
            
            # Hide unused subplots
            for i in range(len(plot_stocks), len(axes_flat)):
                axes_flat[i].set_visible(False)
            
            plt.tight_layout()
            
            # Save the plot
            plot_filename = f"{output_dir}/closing_prices_set_{plot_idx + 1}.png"
            plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
            plt.close()
            
        print(f"Created {n_plots} visualization sets")
    
    def generate_summary_statistics(self):
        """
        Generate comprehensive summary statistics for the dataset.
        """
        print("Generating summary statistics...")
        
        if self.master_df is None:
            print("Master dataframe not available")
            return
        
        
        # Data completeness report
        completeness = {}
        for stock in self.master_df.columns:
            total_days = len(self.master_df)
            valid_days = self.master_df[stock].notna().sum()
            completeness[stock] = {
                'total_days': total_days,
                'valid_days': valid_days,
                'completeness_percentage': (valid_days / total_days) * 100
            }
        
        completeness_df = pd.DataFrame(completeness).T
        
        print("Summary statistics generated")
        
        return completeness_df
    
    def run_full_analysis(self):
        """
        Execute the complete analysis pipeline with enhanced logging.
        """
        print("\n" + "🚀 " + "="*58)
        print("FTSE250 STOCK DATA ANALYSIS PIPELINE")
        print("="*60)
        print(f"📅 Analysis Period: {self.start_date.date()} to {self.end_date.date()}")
        print(f"📂 Data Directory: {self.data_dir}")
        print("="*60)
        
        # Step 1: Load constituent data
        print("\n🔄 STEP 1: Loading FTSE250 Constituent Data...")
        if not self.load_ftse_constituent_data():
            print("❌ Failed to load FTSE constituent data")
            return False
        
        # Step 2: Load historical stock data
        print("\n🔄 STEP 2: Loading Historical Stock Data...")
        if not self.load_stock_historical_data():
            print("❌ Failed to load historical stock data")
            return False
        
        # Step 3: Create master CSV
        print("\n🔄 STEP 3: Creating Master CSV Dataset...")
        if not self.create_master_csv():
            print("❌ Failed to create master CSV")
            return False
        
        # Step 4: Create initial visualizations (before cleaning)
        print("\n🔄 STEP 4: Creating Initial Visualizations...")
        self.create_time_series_visualizations(output_dir="plots/ftse250_analysis/initial_plots")
        
        # Step 5: Analyze missing data
        print("\n🔄 STEP 5: Analyzing Missing Data Patterns...")
        missing_stats = self.analyze_missing_data()

        # Step 6: Remove problematic stocks
        print("\n🔄 STEP 6: Removing Problematic Stocks...")
        self.remove_problematic_stocks()
        
        # Step 7: Calculate and visualize log returns
        print("\n🔄 STEP 7: Calculating Log Returns...")
        self.calculate_log_returns()
        
        # Step 8: Remove outlier stocks based on log returns
        print("\n🔄 STEP 8: Removing Outlier Stocks...")
        self.remove_outlier_stocks()
        
        # Step 9: Perform correlation analysis
        print("\n🔄 STEP 9: Performing Correlation Analysis...")
        self.perform_correlation_analysis()
        
        # Step 10: Compute similarity matrix
        print("\n🔄 STEP 10: Computing Similarity Matrix...")
        self.compute_similarity_matrix()
        
        # Step 11: Perform 3D MDS analysis
        print("\n🔄 STEP 11: Performing 3D MDS Analysis...")
        self.perform_mds_analysis()
        
        # Step 12: Find optimal clusters using elbow method
        print("\n🔄 STEP 12: Finding Optimal Clusters with Elbow Method...")
        self.find_optimal_clusters_elbow_method()
        
        # Step 13: Perform k-means clustering visualization
        print("\n🔄 STEP 13: Performing K-means Clustering Visualization...")
        self.perform_kmeans_clustering_visualization()
        
        # Step 14: Analyze correlation states
        print("\n🔄 STEP 14: Analyzing Correlation States...")
        self.analyze_correlation_states()
        
        # Step 15: Create market state timeline visualization
        print("\n🔄 STEP 15: Creating Market State Timeline Visualization...")
        self.create_market_state_timeline()
        
        # Step 16: Generate summary statistics
        print("\n🔄 STEP 16: Generating Summary Statistics...")
        completeness_df = self.generate_summary_statistics()
        
        # Step 17: Create state transition matrix
        print("\n🔄 STEP 17: Creating State Transition Matrix...")
        self.create_state_transition_matrix()
        
        # Final summary
        print("\n" + "🎉 " + "="*58)
        print("ANALYSIS COMPLETE!")
        print("="*60)
        print(f"📊 Final dataset: {len(self.master_df.columns)} stocks, {len(self.master_df)} days")
        print(f"📅 Date range: {self.start_date.date()} to {self.end_date.date()}")
        print(f"❌ Excluded stocks: {len(self.excluded_stocks)}")
        
        print(f"\n📁 OUTPUT FILES CREATED:")
        print(f"   📄 processed_data/ftse250_master_data.csv")
        print(f"   📄 processed_data/missing_data_analysis.csv")

        print("="*60)
        
        return True

    def calculate_log_returns(self):
        """
        Calculate log returns using r(t) = ln(P(t)) - ln(P(t-1)) and create visualizations.
        """
        print("Calculating log returns...")
        
        if self.master_df is None:
            print("Master dataframe not available")
            return
        
        # Calculate log returns
        self.log_returns_df = np.log(self.master_df) - np.log(self.master_df.shift(1))
        self.log_returns_df = self.log_returns_df.dropna()
        
        print(f"Log returns calculated for {len(self.log_returns_df.columns)} stocks")
        
        # Create 3x3 grid visualizations for log returns
        self.create_log_returns_visualizations()
        

    def create_log_returns_visualizations(self, output_dir="plots/ftse250_analysis/log_returns"):
        """
        Create 3x3 subplot grids displaying log returns time series.
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        stocks = list(self.log_returns_df.columns)
        n_stocks = len(stocks)
        
        # Calculate number of plots needed
        stocks_per_plot = 9
        n_plots = (n_stocks + stocks_per_plot - 1) // stocks_per_plot
        
        for plot_idx in range(n_plots):
            start_idx = plot_idx * stocks_per_plot
            end_idx = min(start_idx + stocks_per_plot, n_stocks)
            
            current_stocks = stocks[start_idx:end_idx]
            
            # Create 3x3 subplot grid
            fig, axes = plt.subplots(3, 3, figsize=(15, 12))
            fig.suptitle(f'FTSE 250 Log Returns - Set {plot_idx + 1}', fontsize=16, fontweight='bold')
            
            # Flatten axes for easier indexing
            axes_flat = axes.flatten()
            
            for i, stock in enumerate(current_stocks):
                ax = axes_flat[i]
                
                # Plot log returns
                dates = self.log_returns_df.index
                returns = self.log_returns_df[stock]
                
                ax.plot(dates, returns, linewidth=0.8, alpha=0.8)
                ax.set_title(stock, fontsize=10, fontweight='bold')
                ax.grid(True, alpha=0.3)
                ax.tick_params(axis='x', rotation=45, labelsize=8)
                ax.tick_params(axis='y', labelsize=8)
                
                # Format y-axis to show percentage
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.2f}'))
            
            # Hide unused subplots
            for i in range(len(current_stocks), 9):
                axes_flat[i].set_visible(False)
            
            plt.tight_layout()
            
            # Save plot
            filename = f"log_returns_set_{plot_idx + 1}.png"
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()

    def remove_outlier_stocks(self):
        """
        Remove stocks with absolute log returns |r(t)| > 0.8 and document removal count.
        """
        print("Identifying and removing outlier stocks...")
        
        if self.log_returns_df is None:
            print("Log returns not calculated")
            return
        
        outlier_stocks = []
        outlier_details = {}
        
        for stock in self.log_returns_df.columns:
            returns = self.log_returns_df[stock]
            max_abs_return = returns.abs().max()
            
            if max_abs_return > 0.8:
                outlier_stocks.append(stock)
                outlier_details[stock] = {
                    'max_abs_return': max_abs_return,
                    'outlier_count': (returns.abs() > 0.8).sum()
                }
        
        print(f"Found {len(outlier_stocks)} stocks with |r(t)| > 0.8:")
        if outlier_stocks:
            print(f"{'Stock Name':<35} {'Max |r(t)|':<12} {'Outliers':<10}")
            print("-" * 57)
            for stock in outlier_stocks:
                details = outlier_details[stock]
                # Truncate long stock names
                display_name = stock[:33] + ".." if len(stock) > 35 else stock
                print(f"{display_name:<35} {details['max_abs_return']:<12.4f} {details['outlier_count']:<10}")
        
        # Remove outlier stocks from both dataframes
        if outlier_stocks:
            self.master_df = self.master_df.drop(columns=outlier_stocks)
            self.log_returns_df = self.log_returns_df.drop(columns=outlier_stocks)
            
            # Update excluded stocks list
            if not hasattr(self, 'excluded_stocks'):
                self.excluded_stocks = []
            self.excluded_stocks.extend(outlier_stocks)
            
            
            print(f"Removed {len(outlier_stocks)} outlier stocks")
            print(f"Remaining stocks: {len(self.master_df.columns)}")

    def perform_correlation_analysis(self):
        """
        Create full-period correlation matrix and rolling correlations (20-day epochs, 10-day shifts).
        """
        print("Performing correlation analysis...")
        
        if self.log_returns_df is None:
            print("Log returns not calculated")
            return
        
        # Full-period correlation matrix
        self.full_correlation_matrix = self.log_returns_df.corr()
        
        # Save full correlation matrix
        self.full_correlation_matrix.to_csv("processed_data/full_correlation_matrix.csv")
        
        # Visualize full correlation matrix
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(self.full_correlation_matrix, dtype=bool))
        sns.heatmap(self.full_correlation_matrix, mask=mask, annot=False, cmap='coolwarm', 
                   center=0, square=True, linewidths=0.5)
        plt.title('Full-Period Correlation Matrix', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig("plots/ftse250_analysis/full_correlation_matrix.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # Rolling correlations (20-day window, 10-day shift)
        print("Calculating rolling correlations...")
        window_size = 20
        shift_size = 10
        
        self.rolling_correlations = {}
        n_periods = (len(self.log_returns_df) - window_size) // shift_size + 1
        
        for i in range(n_periods):
            start_idx = i * shift_size
            end_idx = start_idx + window_size
            
            if end_idx <= len(self.log_returns_df):
                window_data = self.log_returns_df.iloc[start_idx:end_idx]
                corr_matrix = window_data.corr()
                self.rolling_correlations[f'period_{i+1}'] = corr_matrix
        
        print(f"Calculated {len(self.rolling_correlations)} rolling correlation matrices")
        
        # Visualize sample rolling correlations
        self.visualize_sample_rolling_correlations()

    def visualize_sample_rolling_correlations(self):
        """
        Visualize a sample of rolling correlation matrices.
        """
        # Select a few periods to visualize
        periods_to_show = min(6, len(self.rolling_correlations))
        period_keys = list(self.rolling_correlations.keys())[:periods_to_show]
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Sample Rolling Correlation Matrices (20-day windows)', fontsize=16, fontweight='bold')
        
        axes_flat = axes.flatten()
        
        for i, period_key in enumerate(period_keys):
            ax = axes_flat[i]
            corr_matrix = self.rolling_correlations[period_key]
            
            mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
            sns.heatmap(corr_matrix, mask=mask, annot=False, cmap='coolwarm', 
                       center=0, square=True, linewidths=0.5, ax=ax)
            ax.set_title(f'Period {i+1}', fontsize=12)
        
        # Hide unused subplots
        for i in range(periods_to_show, 6):
            axes_flat[i].set_visible(False)
        
        plt.tight_layout()
        plt.savefig("plots/ftse250_analysis/sample_rolling_correlations.png", dpi=300, bbox_inches='tight')
        plt.close()

    def compute_similarity_matrix(self):
        """
        Compute similarity matrix S(t1,t2) = <|C(t1) - C(t2)|> with normalization and symmetry validation.
        """
        print("Computing similarity matrix...")
        
        if not self.rolling_correlations:
            print("Rolling correlations not calculated")
            return
        
        n_periods = len(self.rolling_correlations)
        period_keys = list(self.rolling_correlations.keys())
        
        # Initialize similarity matrix
        self.similarity_matrix = np.zeros((n_periods, n_periods))
        
        # Compute pairwise similarities
        for i in range(n_periods):
            for j in range(n_periods):
                C_t1 = self.rolling_correlations[period_keys[i]]
                C_t2 = self.rolling_correlations[period_keys[j]]
                
                # Calculate absolute difference and take mean
                diff_matrix = np.abs(C_t1 - C_t2)
                similarity = np.nanmean(diff_matrix.values)
                self.similarity_matrix[i, j] = similarity
        
        # Normalize similarity matrix (0 = identical, 1 = maximally different)
        max_similarity = np.max(self.similarity_matrix)
        if max_similarity > 0:
            self.similarity_matrix = self.similarity_matrix / max_similarity
        
        # Validate symmetry
        symmetry_error = np.max(np.abs(self.similarity_matrix - self.similarity_matrix.T))
        print(f"Symmetry validation - Max error: {symmetry_error:.10f}")
        
        # Visualize similarity matrix with improved styling like reference image
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Create time period labels for visualization
        n_periods = len(self.similarity_matrix)
        start_year = 2005
        end_year = 2014
        year_labels = []
        for i in range(n_periods):
            year = start_year + (i * (end_year - start_year) / (n_periods - 1))
            year_labels.append(f'{int(year)}')
        
        # Create the heatmap with custom styling
        im = ax.imshow(self.similarity_matrix, cmap='turbo', aspect='auto', 
                      interpolation='nearest', vmin=0, vmax=1)
        
        # Set ticks and labels
        tick_positions = np.arange(0, n_periods, max(1, n_periods//10))
        ax.set_xticks(tick_positions)
        ax.set_yticks(tick_positions)
        ax.set_xticklabels([year_labels[i] for i in tick_positions], fontsize=10)
        ax.set_yticklabels([year_labels[i] for i in tick_positions], fontsize=10)
        
        # Add grid
        ax.grid(True, alpha=0.3, linewidth=0.5)
        
        # Labels and title
        ax.set_xlabel('Time Period', fontsize=12, fontweight='bold')
        ax.set_ylabel('Time Period', fontsize=12, fontweight='bold')
        ax.set_title('FTSE 250 Similarity Matrix S(t₁,t₂)', fontsize=14, fontweight='bold', pad=20)
        
        # Add colorbar with proper positioning
        cbar = plt.colorbar(im, ax=ax, shrink=0.8, aspect=30, pad=0.02)
        cbar.set_label('Dissimilarity', rotation=270, labelpad=20, fontsize=12, fontweight='bold')
        cbar.ax.tick_params(labelsize=10)
        
        # Set colorbar ticks
        cbar.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        
        plt.tight_layout()
        plt.savefig("plots/ftse250_analysis/similarity_matrix.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Similarity matrix computed: {self.similarity_matrix.shape}")

    def perform_mds_analysis(self):
        """
        Perform 3D MDS on similarity matrix with proper visualization, stress value, and variance explained.
        """
        print("Performing 3D MDS analysis...")
        
        if self.similarity_matrix is None:
            print("Similarity matrix not computed")
            return
        
        # Perform MDS
        mds = MDS(n_components=3, dissimilarity='precomputed', random_state=42)
        mds_coords = mds.fit_transform(self.similarity_matrix)
        
        # Calculate stress and variance explained
        stress = mds.stress_
        
        # Calculate variance explained using correlation between distance matrices
        original_distances = self.similarity_matrix
        mds_distances = euclidean_distances(mds_coords)
        
        # Correlation between original and MDS distances
        orig_flat = original_distances[np.triu_indices_from(original_distances, k=1)]
        mds_flat = mds_distances[np.triu_indices_from(mds_distances, k=1)]
        variance_explained = np.corrcoef(orig_flat, mds_flat)[0, 1] ** 2
        
        print(f"MDS Stress: {stress:.6f}")
        print(f"Variance Explained (R²): {variance_explained:.4f}")
        
        # Create 3D visualization
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')
        
        # Color points by time (gradient)
        n_points = len(mds_coords)
        colors = plt.cm.viridis(np.linspace(0, 1, n_points))
        
        scatter = ax.scatter(mds_coords[:, 0], mds_coords[:, 1], mds_coords[:, 2], 
                           c=colors, s=60, alpha=0.8)
        
        # Add labels for some points
        for i in range(0, n_points, max(1, n_points//10)):
            ax.text(mds_coords[i, 0], mds_coords[i, 1], mds_coords[i, 2], 
                   f'P{i+1}', fontsize=8)
        
        ax.set_xlabel('MDS Dimension 1')
        ax.set_ylabel('MDS Dimension 2')
        ax.set_zlabel('MDS Dimension 3')
        ax.set_title(f'3D MDS of Correlation Similarity\nStress: {stress:.6f}, R²: {variance_explained:.4f}', 
                    fontsize=14, fontweight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=20)
        cbar.set_label('Time Period', rotation=270, labelpad=15)
        
        plt.tight_layout()
        plt.savefig("plots/ftse250_analysis/3d_mds_plot.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print("3D MDS analysis completed and saved")

    def perform_kmeans_clustering_visualization(self):
        """
        Perform k-means clustering with optimal k value and create 3D visualization.
        """
        print("Performing k-means clustering with optimal k value...")
        
        if not hasattr(self, 'optimal_k'):
            print("Optimal k not found. Running elbow method first...")
            self.find_optimal_clusters_elbow_method()
        
        if not hasattr(self, 'log_returns_df') or self.log_returns_df is None:
            print("Log returns data not available for clustering")
            return
        
        # Prepare data for clustering - transpose to cluster time periods
        clustering_data = self.log_returns_df.T.values
        
        print(f"Performing k-means clustering with k={self.optimal_k}")
        print(f"Clustering data shape: {clustering_data.shape}")
        
        # Perform k-means clustering with optimal k
        kmeans = KMeans(n_clusters=self.optimal_k, random_state=42, n_init=10, max_iter=300)
        cluster_labels = kmeans.fit_predict(clustering_data)
        
        print(f"Clustering completed. Found {self.optimal_k} clusters")
        print(f"Cluster distribution: {np.bincount(cluster_labels)}")
        
        # Use MDS to project high-dimensional data to 3D for visualization
        print("Creating 3D projection for visualization...")
        
        distance_matrix = euclidean_distances(clustering_data)
        
        # Perform MDS for 3D visualization
        mds = MDS(n_components=3, dissimilarity='precomputed', random_state=42)
        coords_3d = mds.fit_transform(distance_matrix)
        
        # Create 3D scatter plot
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Define colors for clusters
        colors = ['green', 'blue', 'magenta', 'red', 'cyan', 'yellow', 'orange', 'purple', 'brown', 'pink']
        cluster_colors = [colors[i % len(colors)] for i in range(self.optimal_k)]
        
        # Plot each cluster with different colors
        for cluster_id in range(self.optimal_k):
            cluster_mask = cluster_labels == cluster_id
            cluster_points = coords_3d[cluster_mask]
            
            ax.scatter(cluster_points[:, 0], cluster_points[:, 1], cluster_points[:, 2],
                      c=cluster_colors[cluster_id], s=60, alpha=0.7, 
                      label=f'Cluster {cluster_id + 1}')
        
        # Add labels and formatting
        ax.set_xlabel('Coordinate 1', fontsize=12, fontweight='bold')
        ax.set_ylabel('Coordinate 2', fontsize=12, fontweight='bold')
        ax.set_zlabel('Coordinate 3', fontsize=12, fontweight='bold')
        ax.set_title(f'FTSE 250 (ε = 0.6)\nK-means Clustering Results (k = {self.optimal_k})', 
                    fontsize=14, fontweight='bold')
        
        # Add legend
        ax.legend(loc='upper left', bbox_to_anchor=(0.02, 0.98))
        
        # Set viewing angle for better visualization
        ax.view_init(elev=20, azim=45)
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig("plots/ftse250_analysis/kmeans_clustering_3d.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        
        return cluster_labels, coords_3d

    def find_optimal_clusters_elbow_method(self, n_trials=1000, max_k=10):
        """
        Find optimal number of clusters using elbow method with multiple trials for robustness.
        
        Parameters:
        -----------
        n_trials : int
            Number of different random initializations to test (default: 1000)
        max_k : int
            Maximum number of clusters to test (default: 10)
        """
        print(f"Finding optimal clusters using elbow method with {n_trials} trials...")
        
        if not hasattr(self, 'log_returns_df') or self.log_returns_df is None:
            print("Log returns data not available for clustering")
            return
        
        # Prepare data for clustering (transpose to cluster time periods)
        # Use log returns data - each row is a time period, each column is a stock
        clustering_data = self.log_returns_df.T.values  # Shape: (n_stocks, n_time_periods)
        
        print(f"Clustering data shape: {clustering_data.shape}")
        print(f"Testing k from 1 to {max_k} clusters with {n_trials} trials each")
        
        # Store results for each k
        k_range = range(1, max_k + 1)
        wcss_results = {}  # Will store all WCSS values for each k
        mean_wcss = []     # Mean WCSS for each k
        std_wcss = []      # Standard deviation of WCSS for each k
        
        # Test each number of clusters
        for k in k_range:
            print(f"  Testing k={k}...")
            wcss_trials = []
            
            # Run multiple trials for this k
            for trial in range(n_trials):
                if trial % 200 == 0 and trial > 0:
                    print(f"    Completed {trial}/{n_trials} trials for k={k}")
                
                if k == 1:
                    # For k=1, WCSS is just the total variance
                    centroid = np.mean(clustering_data, axis=0)
                    wcss = np.sum((clustering_data - centroid) ** 2)
                else:
                    # Run K-means clustering
                    kmeans = KMeans(n_clusters=k, random_state=trial, n_init=1, max_iter=300)
                    kmeans.fit(clustering_data)
                    wcss = kmeans.inertia_
                
                wcss_trials.append(wcss)
            
            # Store results for this k
            wcss_results[k] = wcss_trials
            mean_wcss.append(np.mean(wcss_trials))
            std_wcss.append(np.std(wcss_trials))
            
            print(f"    k={k}: Mean WCSS = {mean_wcss[-1]:.2f} ± {std_wcss[-1]:.2f}")
        
        # Find optimal k using elbow method
        optimal_k = self.find_elbow_point(k_range, mean_wcss)
        
        print(f"\n🎯 Optimal number of clusters: k = {optimal_k}")
        
        # Create comprehensive elbow plot
        self.create_elbow_plot(k_range, mean_wcss, wcss_results, optimal_k, n_trials)
        
        
        # Store optimal k for potential future use
        self.optimal_k = optimal_k
        
        return optimal_k, wcss_results

    def find_elbow_point(self, k_values, wcss_values):
        """
        Find the elbow point using the "knee" detection method.
        """
        # Convert to numpy arrays
        k_array = np.array(k_values)
        wcss_array = np.array(wcss_values)
        
        # Calculate the differences (first derivative)
        diff1 = np.diff(wcss_array)
        
        # Calculate the second differences (second derivative)
        diff2 = np.diff(diff1)
        
        # Find the point where the second derivative is maximum (most negative)
        # This indicates the sharpest bend in the curve
        elbow_idx = np.argmax(diff2) + 2  # +2 because we lost 2 points in double diff
        
        # Ensure we don't go out of bounds
        elbow_idx = min(elbow_idx, len(k_values) - 1)
        
        return k_values[elbow_idx]

    def create_elbow_plot(self, k_range, mean_wcss, wcss_results, optimal_k, n_trials):
        """
        Create elbow plot with main graph showing optimal k-line and mini graph showing all trial results.
        """
        print("Creating elbow plot visualization...")
        
        # Create figure with main plot and inset
        fig, ax1 = plt.subplots(1, 1, figsize=(12, 8))
        
        # Main graph: Plot only the optimal k-value line (blue, solid, thick)
        ax1.plot(k_range, mean_wcss, color='blue', linewidth=3, linestyle='-', 
                marker='o', markersize=8, label=f'Optimal k = {optimal_k}')
        
        # Highlight optimal k point
        ax1.axvline(x=optimal_k, color='red', linestyle='--', linewidth=2, 
                   label=f'Optimal k = {optimal_k}')
        
        # Main graph styling
        ax1.set_xlabel('Number of clusters k', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Intra cluster distance', fontsize=12, fontweight='bold')
        ax1.set_title(f'FTSE 250 (ε = 0.6)\nElbow Method - Optimal k = {optimal_k}', 
                     fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='upper right')
        
        # Set axis limits for main graph
        ax1.set_xlim(1, max(k_range))
        ax1.set_ylim(bottom=0)
        
        # Add annotation for optimal k
        ax1.annotate(f'Optimal k = {optimal_k}', 
                    xy=(optimal_k, mean_wcss[optimal_k-1]), 
                    xytext=(optimal_k+1.5, mean_wcss[optimal_k-1]*1.2),
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                    fontsize=11, fontweight='bold', color='red',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        # Create inset plot (mini graph showing all trials)
        from mpl_toolkits.axes_grid1.inset_locator import inset_axes
        axins = inset_axes(ax1, width="40%", height="40%", loc='upper right', 
                          bbox_to_anchor=(0.55, 0.55, 0.4, 0.4), bbox_transform=ax1.transAxes)
        
        # Mini graph: Show all trial lines with higher opacity and muted colors
        # Use muted color palette (grays and muted colors)
        muted_colors = ['#808080', '#A0A0A0', '#909090', '#B0B0B0', '#888888', 
                       '#999999', '#777777', '#AAAAAA', '#666666', '#BBBBBB']
        
        # Plot all individual trials in mini graph with higher opacity
        for trial_idx in range(n_trials):
            trial_wcss = [wcss_results[k][trial_idx] for k in k_range]
            color_idx = trial_idx % len(muted_colors)
            axins.plot(k_range, trial_wcss, color=muted_colors[color_idx], 
                      alpha=0.75, linewidth=0.8, linestyle='-')
        
        # Add the mean line (optimal line) to mini graph for reference
        axins.plot(k_range, mean_wcss, color='blue', linewidth=2, 
                  linestyle='-', marker='o', markersize=3, alpha=0.9)
        
        # Highlight optimal k in mini graph
        axins.axvline(x=optimal_k, color='red', linestyle='--', linewidth=1.5, alpha=0.8)
        
        # Mini graph styling
        axins.grid(True, alpha=0.3)
        axins.set_xlim(1, max(k_range))
        axins.set_ylim(bottom=0)
        axins.tick_params(labelsize=8)
        axins.set_xlabel('k', fontsize=9)
        axins.set_ylabel('WCSS', fontsize=9)
        axins.set_title(f'{n_trials} trials', fontsize=8, fontweight='bold')
        
        # Ensure responsive design
        plt.tight_layout()
        plt.savefig("plots/ftse250_analysis/elbow_method_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print("   📊 Saved: plots/ftse250_analysis/elbow_method_analysis.png")

    def analyze_correlation_states(self):
        """
        Analyze different market states based on correlation patterns and create visualizations.
        Identifies distinct correlation structures representing different market regimes.
        """
        print("Analyzing correlation structures of different market states...")
        
        if not self.rolling_correlations:
            print("Rolling correlations not calculated")
            return
        
        # Convert rolling correlations to feature vectors for clustering
        correlation_features = []
        period_keys = list(self.rolling_correlations.keys())
        
        for period_key in period_keys:
            corr_matrix = self.rolling_correlations[period_key]
            # Extract upper triangular part (excluding diagonal) as features
            upper_tri_indices = np.triu_indices_from(corr_matrix, k=1)
            features = corr_matrix.values[upper_tri_indices]
            correlation_features.append(features)
        
        correlation_features = np.array(correlation_features)
        
        # Use k-means to identify 4 distinct correlation states
        n_states = 4
        kmeans = KMeans(n_clusters=n_states, random_state=42, n_init=10)
        state_labels = kmeans.fit_predict(correlation_features)
        
        # Group periods by state
        states = {f'S{i+1}': [] for i in range(n_states)}
        for i, label in enumerate(state_labels):
            states[f'S{label+1}'].append(period_keys[i])
        
        # Calculate representative correlation matrix for each state (median)
        state_correlations = {}
        for state_name, periods in states.items():
            if len(periods) > 0:
                # Stack all correlation matrices for this state
                state_matrices = []
                for period in periods:
                    state_matrices.append(self.rolling_correlations[period].values)
                
                # Calculate median correlation matrix
                state_matrices = np.array(state_matrices)
                median_corr = np.median(state_matrices, axis=0)
                
                # Convert back to DataFrame with proper index/columns
                first_period_corr = self.rolling_correlations[periods[0]]
                state_correlations[state_name] = pd.DataFrame(
                    median_corr, 
                    index=first_period_corr.index, 
                    columns=first_period_corr.columns
                )
        
        # Create visualization of different correlation states
        self.visualize_correlation_states(state_correlations, states)
        
        # Save state information
        state_info = []
        for state_name, periods in states.items():
            state_info.append({
                'State': state_name,
                'Number_of_Periods': len(periods),
                'Periods': ', '.join(periods[:5]) + ('...' if len(periods) > 5 else ''),
                'Percentage': f"{len(periods)/len(period_keys)*100:.1f}%"
            })

        state_df = pd.DataFrame(state_info)
        
        print(f"Identified {n_states} distinct correlation states:")
        print(state_df.to_string(index=False))
        
        return state_correlations, states

    def visualize_correlation_states(self, state_correlations, states):
        """
        Create heatmap visualizations for different correlation states.
        """
        # Create 2x2 subplot layout similar to reference image
        fig, axes = plt.subplots(2, 2, figsize=(16, 14))
        fig.suptitle('Typical Correlation Structures of Different States', fontsize=16, fontweight='bold')
        
        axes_flat = axes.flatten()
        state_names = sorted(state_correlations.keys())
        
        # Color schemes for different states (similar to reference image)
        color_schemes = ['RdYlGn_r', 'RdYlBu_r', 'OrRd', 'Reds']
        
        for i, state_name in enumerate(state_names):
            if i < 4:  # Only plot first 4 states
                ax = axes_flat[i]
                corr_matrix = state_correlations[state_name]
                
                # Create heatmap with appropriate color scheme
                sns.heatmap(corr_matrix, 
                           annot=False, 
                           cmap=color_schemes[i], 
                           center=0 if 'RdYlGn' in color_schemes[i] or 'RdYlBu' in color_schemes[i] else None,
                           square=True, 
                           linewidths=0.1,
                           cbar_kws={'shrink': 0.8},
                           ax=ax,
                           vmin=-1, vmax=1)
                
                # Format the subplot
                ax.set_title(f'{state_name}', fontsize=14, fontweight='bold')
                ax.set_xlabel('')
                ax.set_ylabel('')
                
                # Rotate tick labels for better readability
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=8)
                ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8)
                
                # Add state information as text
                n_periods = len(states[state_name])
                total_periods = sum(len(periods) for periods in states.values())
                percentage = n_periods / total_periods * 100
                
                ax.text(0.02, 0.98, f'Periods: {n_periods}\n({percentage:.1f}%)', 
                       transform=ax.transAxes, fontsize=10, 
                       verticalalignment='top', 
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig("plots/ftse250_analysis/correlation_states_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Correlation states visualization saved to: plots/ftse250_analysis/correlation_states_analysis.png")

    def create_market_state_timeline(self):
        """
        Create timeline visualization showing market states (y-axis) vs time (x-axis).
        Similar to Q14 reference image.
        """
        print("Creating market state timeline visualization...")
        
        if not self.rolling_correlations:
            print("Rolling correlations not calculated")
            return None
        
        # First, we need to get the state assignments from correlation analysis
        # Convert rolling correlations to feature vectors for clustering
        correlation_features = []
        period_keys = list(self.rolling_correlations.keys())
        
        for period_key in period_keys:
            corr_matrix = self.rolling_correlations[period_key]
            # Extract upper triangular part (excluding diagonal) as features
            upper_tri_indices = np.triu_indices_from(corr_matrix, k=1)
            features = corr_matrix.values[upper_tri_indices]
            correlation_features.append(features)
        
        correlation_features = np.array(correlation_features)
        
        # Use k-means to identify 4 distinct correlation states
        n_states = 4
        kmeans = KMeans(n_clusters=n_states, random_state=42, n_init=10)
        state_labels = kmeans.fit_predict(correlation_features)
        
        # Create timeline data
        timeline_data = []
        window_size = 20
        shift_size = 10
        
        for i, (period_key, state_label) in enumerate(zip(period_keys, state_labels)):
            # Calculate the date for this period
            start_idx = i * shift_size
            period_date = self.log_returns_df.index[start_idx + window_size // 2]  # Middle of the window
            
            timeline_data.append({
                'Period': i + 1,
                'Date': period_date,
                'State': state_label + 1,  # Convert to 1-based indexing
                'State_Label': f'S{state_label + 1}'
            })
        
        timeline_df = pd.DataFrame(timeline_data)
        
        # Create the timeline visualization
        plt.figure(figsize=(16, 8))
        
        # Convert dates to years for x-axis
        years = [date.year + (date.dayofyear - 1) / 365.25 for date in timeline_df['Date']]
        states = timeline_df['State'].values
        
        # Create scatter plot with different colors for each state
        colors = ['blue', 'green', 'orange', 'red']
        state_colors = [colors[state - 1] for state in states]
        
        plt.scatter(years, states, c=state_colors, alpha=0.7, s=30)
        
        # Format the plot
        plt.xlabel('Time (Year)', fontsize=12, fontweight='bold')
        plt.ylabel('State', fontsize=12, fontweight='bold')
        plt.title('Market State Timeline - Correlation Frame', fontsize=14, fontweight='bold')
        
        # Set y-axis to show states 1-4
        plt.yticks([1, 2, 3, 4], ['S1', 'S2', 'S3', 'S4'])
        plt.ylim(0.5, 4.5)
        
        # Set x-axis range
        plt.xlim(min(years) - 0.5, max(years) + 0.5)
        
        # Add grid for better readability
        plt.grid(True, alpha=0.3)
        
        # Add legend
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                    markerfacecolor=colors[i], markersize=8, 
                                    label=f'S{i+1}') for i in range(4)]
        plt.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        plt.savefig("plots/ftse250_analysis/market_state_timeline.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Market state timeline saved to: plots/ftse250_analysis/market_state_timeline.png")
        return timeline_df

    def create_state_transition_matrix(self):
        """
        Create transition matrix showing transitions between consecutive market states.
        Similar to Q15 reference image.
        """
        print("Creating state transition matrix...")
        
        # First get the timeline data
        timeline_df = self.create_market_state_timeline()
        
        if timeline_df is None or len(timeline_df) < 2:
            print("Insufficient timeline data for transition analysis")
            return
        
        # Calculate transition counts
        n_states = 4
        transition_counts = np.zeros((n_states, n_states), dtype=int)
        
        states = timeline_df['State'].values
        for i in range(len(states) - 1):
            current_state = states[i] - 1  # Convert to 0-based indexing
            next_state = states[i + 1] - 1
            transition_counts[current_state, next_state] += 1
        
        # Calculate transition probabilities
        transition_probs = np.zeros((n_states, n_states))
        for i in range(n_states):
            row_sum = np.sum(transition_counts[i, :])
            if row_sum > 0:
                transition_probs[i, :] = transition_counts[i, :] / row_sum
        
        transition_df = pd.DataFrame(transition_counts, 
                                   index=[f'S{i+1}' for i in range(n_states)],
                                   columns=[f'S{i+1}' for i in range(n_states)])
        
        # Create the transition matrix visualization
        plt.figure(figsize=(10, 8))
        
        # Create heatmap with transition counts
        sns.heatmap(transition_counts, 
                   annot=True, 
                   fmt='d',
                   cmap='Blues',
                   xticklabels=[f'S{i+1}' for i in range(n_states)],
                   yticklabels=[f'S{i+1}' for i in range(n_states)],
                   cbar_kws={'label': 'Number of Transitions'})
        
        plt.title('State Transition Matrix - Consecutive Market States', fontsize=14, fontweight='bold')
        plt.xlabel('To State', fontsize=12, fontweight='bold')
        plt.ylabel('From State', fontsize=12, fontweight='bold')
        
        # Add text annotations for better readability
        for i in range(n_states):
            for j in range(n_states):
                count = transition_counts[i, j]
                if count > 0:
                    plt.text(j + 0.5, i + 0.5, str(count), 
                           ha='center', va='center', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig("plots/ftse250_analysis/state_transition_matrix.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print("State transition matrix saved to: plots/ftse250_analysis/state_transition_matrix.png")
        print(f"\nTransition Matrix (Counts):")
        print(transition_df.to_string())
        
        return transition_counts, transition_probs


def main():
    """
    Main execution function.
    """
    # Configuration
    data_directory = "data"
    start_date = "2003-10-01"
    end_date = "2013-10-01"
    
    # Initialize analyzer
    analyzer = FTSE250Analyzer(
        data_dir=data_directory,
        start_date=start_date,
        end_date=end_date
    )
    
    # Run full analysis
    success = analyzer.run_full_analysis()
    
    if success:
        print("\nAnalysis completed successfully!")
    else:
        print("\nAnalysis failed. Please check the error messages above.")


if __name__ == "__main__":
    main()
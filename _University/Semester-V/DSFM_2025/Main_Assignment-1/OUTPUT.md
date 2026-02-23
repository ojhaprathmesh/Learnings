# 🚀 FTSE250 STOCK DATA ANALYSIS PIPELINE

**Analysis Period:** 2003-10-01 to 2013-10-01  
**Data Directory:** `data`

---

## 🔄 STEP 1: Loading FTSE250 Constituent Data

### LOADING FTSE250 CONSTITUENT DATA

✅ **Successfully loaded FTSE250 constituent data**
- **File:** `FTSE Mid-Cap 250 (FTMC) Live.csv`
- **Total records:** 226
- **Columns:** ['Name', 'Last', 'High', 'Low', 'Chg. %', 'Vol.', 'Upside', 'Time']

**Sample of loaded constituent data:**

| Name                           | Last       | Chg. %  |
|--------------------------------|------------|---------|
| Genus                          | 2,530.0    | -1.17%  |
| Premier Foods                  | 187.40     | +0.32%  |
| Bankers Investment             | 131.40     | +1.23%  |
| Morgan Sindall                 | 4,725.00   | +0.53%  |
| Hochschild                     | 347.80     | -1.70%  |
| ... and 221 more records      |            |         |

---

## 🔄 STEP 2: Loading Historical Stock Data

### LOADING HISTORICAL STOCK DATA

**Found 151 stock files in directory:** `data/stocks`

**Processing stock files:**

```
[  1/151] ✓ 3I Infrastructure         - 1658 records (2007-03-09 to 2013-09-30)
[  2/151] ✓ Aberdeen                  - 1826 records (2006-01-08 to 2013-09-30)
[  3/151] ✓ Aberforth Smaller         - 2528 records (2003-10-01 to 2013-09-30)
[  4/151] ✓ abrdn Private Equity Opportunities Trust - 2527 records (2003-10-01 to 2013-09-30)
[  5/151] ✓ AG Barr                   - 2524 records (2003-10-01 to 2013-09-30)
[  6/151] ✓ Alliance Trust            - 2528 records (2003-10-01 to 2013-09-30)
[  7/151] ✓ Ashmore                   - 1759 records (2006-01-11 to 2013-09-30)
[  8/151] ✓ AVI Global                - 2528 records (2003-10-01 to 2013-09-30)
[  9/151] ✓ Babcock International     - 2528 records (2003-10-01 to 2013-09-30)
[ 10/151] ✓ Baillie Gifford Japan     - 2526 records (2003-10-01 to 2013-09-30)
[ 11/151] ✓ Balfour Beatty            - 2528 records (2003-10-01 to 2013-09-30)
[ 12/151] ✓ Bankers Investment        - 2528 records (2003-10-01 to 2013-09-30)
[ 13/151] ✓ Bellway                   - 2528 records (2003-10-01 to 2013-09-30)
[ 14/151] ✓ BH Macro                  - 1647 records (2007-01-05 to 2013-09-30)
[ 15/151] ✓ Big Yellow                - 2527 records (2003-10-01 to 2013-09-30)
[ 16/151] ✓ BlackRock Greater Europe  - 2280 records (2004-01-10 to 2013-09-30)
[ 17/151] ✓ Blackrock Smaller         - 2526 records (2003-10-01 to 2013-09-30)
[ 18/151] ✓ Blackrock World Mining    - 2527 records (2003-10-01 to 2013-09-30)
[ 19/151] ✓ Bodycote                  - 2528 records (2003-10-01 to 2013-09-30)
[ 20/151] ✓ British Land Company      - 2528 records (2003-10-01 to 2013-09-30)
[ 21/151] ✓ Burberry Group            - 2528 records (2003-10-01 to 2013-09-30)
[ 22/151] ✓ C&C                       - 2369 records (2004-01-06 to 2013-09-30)
[ 23/151] ✓ Caledonia Investments     - 2528 records (2003-10-01 to 2013-09-30)
[ 24/151] ✓ Capital Gearing           - 2526 records (2003-10-01 to 2013-09-30)
[ 25/151] ✓ Carnival                  - 2528 records (2003-10-01 to 2013-09-30)
[ 26/151] ✓ Chemring                  - 2527 records (2003-10-01 to 2013-09-30)
[ 27/151] ✓ City Of London IT         - 2528 records (2003-10-01 to 2013-09-30)
[ 28/151] ✓ Close Brothers            -  861 records (2010-01-06 to 2013-09-30)
[ 29/151] ✓ Computacenter             - 2528 records (2003-10-01 to 2013-09-30)
[ 30/151] ✓ Cranswick                 - 2526 records (2003-10-01 to 2013-09-30)
[ 31/151] ✓ Crest Nicholson           -  161 records (2013-01-03 to 2013-09-30)
[ 32/151] ✓ Currys                    - 2524 records (2003-10-01 to 2013-09-30)
[ 33/151] ✓ Derwent                   - 2527 records (2003-10-01 to 2013-09-30)
[ 34/151] ✓ DiscoverIE                - 2485 records (2003-10-01 to 2013-09-30)
[ 35/151] ✓ Domino's Pizza            - 2527 records (2003-10-01 to 2013-09-30)
[ 36/151] ✗ Dowlais                   - No data in date range
[ 37/151] ✓ Drax Group                - 1967 records (2005-12-16 to 2013-09-30)
[ 38/151] ✓ Dunelm                    - 1753 records (2006-01-11 to 2013-09-30)
[ 39/151] ✓ Edinburgh Investment      - 2528 records (2003-10-01 to 2013-09-30)
[ 40/151] ✓ Edinburgh Worldwide       - 2527 records (2003-10-01 to 2013-09-30)
[ 41/151] ✓ Elementis                 - 2527 records (2003-10-01 to 2013-09-30)
[ 42/151] ✓ Essentra                  - 2102 records (2005-01-07 to 2013-09-30)
[ 43/151] ✓ European Opportunities    - 2527 records (2003-10-01 to 2013-09-30)
[ 44/151] ✓ European Smaller Companies Trust - 2526 records (2003-10-01 to 2013-09-30)
[ 45/151] ✓ Fidelity China            -  870 records (2010-01-06 to 2013-09-30)
[ 46/151] ✓ Fidelity Emerging         - 2528 records (2003-10-01 to 2013-09-30)
[ 47/151] ✓ Fidelity European Trust   - 2527 records (2003-10-01 to 2013-09-30)
[ 48/151] ✓ Fidelity Special          - 2526 records (2003-10-01 to 2013-09-30)
[ 49/151] ✓ Finsbury Growth & Income  - 2527 records (2003-10-01 to 2013-09-30)
[ 50/151] ✓ FirstGroup                - 2528 records (2003-10-01 to 2013-09-30)
[ 51/151] ✓ Foresight Solar Fund      -   12 records (2013-01-11 to 2013-09-12)
[ 52/151] ✓ GCP Infrastructure        -  804 records (2010-01-09 to 2013-09-30)
[ 53/151] ✓ Genus                     - 2528 records (2003-10-01 to 2013-09-30)
[ 54/151] ✓ Global Smaller Companies Trust - 2524 records (2003-10-01 to 2013-09-30)
[ 55/151] ✓ Grafton Group             - 2527 records (2003-10-01 to 2013-09-30)
[ 56/151] ✓ Grainger                  - 2527 records (2003-10-01 to 2013-09-30)
[ 57/151] ✓ Great Portland Estates    - 2528 records (2003-10-01 to 2013-09-30)
[ 58/151] ✓ Greencoat                 -  133 records (2013-01-05 to 2013-09-30)
[ 59/151] ✓ Greggs                    - 2528 records (2003-10-01 to 2013-09-30)
[ 60/151] ✓ Hammerson                 - 2527 records (2003-10-01 to 2013-09-30)
[ 61/151] ✓ Harbour Energy            - 2527 records (2003-10-01 to 2013-09-30)
[ 62/151] ✓ Hays                      - 2528 records (2003-10-01 to 2013-09-30)
[ 63/151] ✓ Henderson Smaller         - 2526 records (2003-10-01 to 2013-09-30)
[ 64/151] ✓ Herald Investments        - 2527 records (2003-10-01 to 2013-09-30)
[ 65/151] ✓ HICL Infrastructure       - 1894 records (2006-01-06 to 2013-09-30)
[ 66/151] ✓ Hill & Smith              - 2527 records (2003-10-01 to 2013-09-30)
[ 67/151] ✓ Hochschild                - 1743 records (2006-01-12 to 2013-09-30)
[ 68/151] ✓ Hunting                   - 2528 records (2003-10-01 to 2013-09-30)
[ 69/151] ✓ ICG Enterprise            - 2526 records (2003-10-01 to 2013-09-30)
[ 70/151] ✓ IG Group                  - 2127 records (2005-01-06 to 2013-09-30)
[ 71/151] ✓ Impax Environmental       - 2527 records (2003-10-01 to 2013-09-30)
[ 72/151] ✓ Inchcape                  - 2528 records (2003-10-01 to 2013-09-30)
[ 73/151] ✓ International Workplace Plc - 2527 records (2003-10-01 to 2013-09-30)
[ 74/151] ✓ Intl Public Partnerships  - 1738 records (2006-01-12 to 2013-09-30)
[ 75/151] ✓ Investec                  - 2528 records (2003-10-01 to 2013-09-30)
[ 76/151] ✓ ITV                       - 2528 records (2003-10-01 to 2013-09-30)
[ 77/151] ✓ John Wood                 - 2528 records (2003-10-01 to 2013-09-30)
[ 78/151] ✓ Johnson Matthey           - 2528 records (2003-10-01 to 2013-09-30)
[ 79/151] ✓ JPM Global Growth         - 2525 records (2003-10-01 to 2013-09-30)
[ 80/151] ✓ JPMorgan American         - 2524 records (2003-10-01 to 2013-09-30)
[ 81/151] ✓ JPMorgan EM               - 2526 records (2003-10-01 to 2013-09-30)
[ 82/151] ✓ JPMorgan Euro Smaller     - 2525 records (2003-10-01 to 2013-09-30)
[ 83/151] ✓ JPMorgan Indian           - 2527 records (2003-10-01 to 2013-09-30)
[ 84/151] ✓ JPMorgan Japanese         - 2527 records (2003-10-01 to 2013-09-30)
[ 85/151] ✓ Jupiter Fund              -  830 records (2010-01-07 to 2013-09-30)
[ 86/151] ✓ Just Group                -    6 records (2013-02-12 to 2013-09-12)
[ 87/151] ✓ Keller Group              - 2528 records (2003-10-01 to 2013-09-30)
[ 88/151] ✓ Kier Group                - 2527 records (2003-10-01 to 2013-09-30)
[ 89/151] ✓ Lancashire Holdings       - 1651 records (2007-01-05 to 2013-09-30)
[ 90/151] ✓ Law Debenture             - 2525 records (2003-10-01 to 2013-09-30)
[ 91/151] ✓ Lion Finance              -  399 records (2012-01-03 to 2013-09-30)
[ 92/151] ✓ LondonMetric Property     - 1487 records (2007-03-12 to 2013-09-30)
[ 93/151] ✓ Man Group                 - 1048 records (2009-01-09 to 2013-09-30)
[ 94/151] ✓ Marshalls                 - 2528 records (2003-10-01 to 2013-09-30)
[ 95/151] ✓ Mercantile Investment Trust - 2527 records (2003-10-01 to 2013-09-30)
[ 96/151] ✓ Merchants Trust           - 2528 records (2003-10-01 to 2013-09-30)
[ 97/151] ✓ Mitchells Butlers         - 2521 records (2003-10-04 to 2013-09-30)
[ 98/151] ✓ Mitie                     - 2528 records (2003-10-01 to 2013-09-30)
[ 99/151] ✓ Moneysupermarket          - 1561 records (2007-01-08 to 2013-09-30)
[100/151] ✓ Monks Investment Trust    - 2528 records (2003-10-01 to 2013-09-30)
[101/151] ✓ Morgan Materials          -  819 records (2010-01-06 to 2013-09-30)
[102/151] ✓ Morgan Sindall            - 2528 records (2003-10-01 to 2013-09-30)
[103/151] ✓ Murray Income             - 2528 records (2003-10-01 to 2013-09-30)
[104/151] ✓ NASCIT                    - 2527 records (2003-10-01 to 2013-09-30)
[105/151] ✓ NB Private Equity         - 1073 records (2009-01-07 to 2013-09-30)
[106/151] ✓ Oxford Instruments        -  398 records (2012-01-02 to 2013-09-30)
[107/151] ✓ Pagegroup                 - 2528 records (2003-10-01 to 2013-09-30)
[108/151] ✓ Pantheon International    - 2527 records (2003-10-01 to 2013-09-30)
[109/151] ✓ Paragon Banking Group     - 2526 records (2003-10-01 to 2013-09-30)
[110/151] ✓ Pennon                    - 2528 records (2003-10-01 to 2013-09-30)
[111/151] ✓ Personal Assets           - 2526 records (2003-10-01 to 2013-09-30)
[112/151] ✓ Playtech                  - 1895 records (2006-01-06 to 2013-09-30)
[113/151] ✓ Plus500                   -   62 records (2013-01-08 to 2013-09-30)
[114/151] ✓ Polar Capital Tech        - 2527 records (2003-10-01 to 2013-09-30)
[115/151] ✗ Premier Foods             - No data in date range
[116/151] ✓ Primary Health            - 2526 records (2003-10-02 to 2013-09-30)
[117/151] ✓ PZ Cussons                - 2528 records (2003-10-01 to 2013-09-30)
[118/151] ✓ Qinetiq                   - 1928 records (2006-01-03 to 2013-09-30)
[119/151] ✗ Raspberry Pi Holdings     - No data in date range
[120/151] ✓ Rathbones                 - 2528 records (2003-10-01 to 2013-09-30)
[121/151] ✓ Renishaw                  - 2527 records (2003-10-01 to 2013-09-30)
[122/151] ✓ RIT Capital               - 2528 records (2003-10-01 to 2013-09-30)
[123/151] ✓ Rotork                    - 2528 records (2003-10-01 to 2013-09-30)
[124/151] ✓ Safestore                 - 1656 records (2007-01-05 to 2013-09-30)
[125/151] ✓ Savills                   - 2525 records (2003-10-01 to 2013-09-30)
[126/151] ✓ Schroder Asia Pacific     - 2527 records (2003-10-01 to 2013-09-30)
[127/151] ✓ Schroder Oriental         - 2064 records (2005-01-08 to 2013-09-30)
[128/151] ✓ Scottish American Investment - 2527 records (2003-10-01 to 2013-09-30)
[129/151] ✓ Senior PLC                -  474 records (2011-01-12 to 2013-09-30)
[130/151] ✓ Serco                     - 2528 records (2003-10-01 to 2013-09-30)
[131/151] ✓ Shaftesbury Capital       -  856 records (2010-01-06 to 2013-09-30)
[132/151] ✓ Sirius Real Estate        - 1617 records (2007-01-06 to 2013-09-30)
[133/151] ✓ Spectris                  - 2528 records (2003-10-01 to 2013-09-30)
[134/151] ✓ SThree                    - 1990 records (2005-01-12 to 2013-09-30)
[135/151] ✓ Syncona                   -  232 records (2012-01-11 to 2013-09-30)
[136/151] ✓ Tate & Lyle               - 2528 records (2003-10-01 to 2013-09-30)
[137/151] ✓ Telecom Plus              -  474 records (2011-01-12 to 2013-09-30)
[138/151] ✓ Temple Bar Investment     - 2528 records (2003-10-01 to 2013-09-30)
[139/151] ✓ Templeton EM              - 2528 records (2003-10-01 to 2013-09-30)
[140/151] ✓ Throgmorton               -  473 records (2011-01-12 to 2013-09-30)
[141/151] ✓ TP ICAP                   - 2528 records (2003-10-01 to 2013-09-30)
[142/151] ✓ TR Property               - 2528 records (2003-10-01 to 2013-09-30)
[143/151] ✓ Travis Perkins            - 2528 records (2003-10-01 to 2013-09-30)
[144/151] ✓ Vesuvius                  - 2528 records (2003-10-01 to 2013-09-30)
[145/151] ✓ Victrex                   - 2527 records (2003-10-01 to 2013-09-30)
[146/151] ✓ Vinacapital Vietnam       - 2507 records (2003-10-10 to 2013-09-30)
[147/151] ✓ Vistry Group              - 2528 records (2003-10-01 to 2013-09-30)
[148/151] ✓ Wetherspoon               - 2528 records (2003-10-01 to 2013-09-30)
[149/151] ✓ WHSmith                   - 2528 records (2003-10-01 to 2013-09-30)
[150/151] ✓ Workspace Group           - 2527 records (2003-10-01 to 2013-09-30)
[151/151] ✓ ZIGUP                     - 2528 records (2003-10-01 to 2013-09-30)
```

### DATA LOADING SUMMARY

📊 **OVERALL STATISTICS:**
- Total files processed: 151
- Successfully loaded: 148 (98.0%)
- Failed to load: 3 (2.0%)

❌ **FAILED TO LOAD: 3 stocks**
- Dowlais - No data in date range
- Premier Foods - No data in date range  
- Raspberry Pi Holdings - No data in date range

📈 **DATA QUALITY METRICS:**
- Average records per stock: 2,285
- Date range coverage: 2003-10-01 to 2013-09-30
- Total data points: 338,180

📅 **DATE RANGE COVERAGE:**
- Earliest data: 2003-10-01
- Latest data: 2013-09-30
- Analysis period: 10 years

---

## 🔄 STEP 3: Creating Master CSV Dataset

✅ **Master CSV created successfully**
- **File:** `processed_data/ftse250_master_data.csv`
- **Stocks included:** 148
- **Business days:** 2,609

---

## 🔄 STEP 4: Creating Initial Visualizations

✅ **Initial time series plots created**
- **Output directory:** `plots/ftse250_analysis/initial_plots/`
- **Total plots:** 17 (9 stocks per plot, 3x3 grid)
- **Stocks visualized:** 148

**Plot files created:**
- `time_series_plot_1.png` through `time_series_plot_17.png`

---

## 🔄 STEP 5: Analyzing Missing Data Patterns

✅ **Missing data analysis completed**

### Stocks to be excluded:
- **Crest Nicholson:** 94.0% missing data (2,448/2,609 business days)
- **Foresight Solar Fund:** 99.5% missing data (2,597/2,609 business days)  
- **Greencoat:** 94.9% missing data (2,476/2,609 business days)
- **Just Group:** 99.8% missing data (2,603/2,609 business days)
- **Lion Finance:** 84.7% missing data (2,210/2,609 business days)
- **Oxford Instruments:** 84.7% missing data (2,211/2,609 business days)
- **Plus500:** 97.6% missing data (2,547/2,609 business days)
- **Syncona:** 91.1% missing data (2,377/2,609 business days)

**Summary:**
- **Total stocks analyzed:** 148
- **Stocks to exclude:** 8 (5.4%)
- **Stocks remaining:** 140 (94.6%)

---

## 🔄 STEP 6: Removing Problematic Stocks

✅ **Problematic stocks removed**
- **Stocks excluded:** 8
- **Remaining stocks:** 140

---

## 🔄 STEP 7: Calculating Log Returns

✅ **Log returns calculated successfully**
- **Stocks processed:** 140
- **Log returns visualization created**

**Log returns plots created:**
- **Output directory:** `plots/ftse250_analysis/log_returns/`
- **Total plots:** 16 (9 stocks per plot, 3x3 grid)
- **File pattern:** `log_returns_plot_1.png` through `log_returns_plot_16.png`

---

## 🔄 STEP 8: Removing Outlier Stocks

✅ **Outlier analysis completed**
- **Outlier stocks identified and removed:** 0
- **Final stock count:** 140

**Outlier detection criteria:**
- Log return standard deviation > 3 times median
- No stocks exceeded this threshold

---

## 🔄 STEP 9: Performing Correlation Analysis

✅ **Correlation analysis completed**
- **Full correlation matrix computed:** 140x140 stocks
- **Rolling correlation analysis:** 20-day window, 10-day shift
- **Sample rolling correlations visualized**

**Output files:**
- `processed_data/full_correlation_matrix.csv`
- `plots/ftse250_analysis/full_correlation_matrix.png`
- `plots/ftse250_analysis/sample_rolling_correlations.png`

---

## 🔄 STEP 10: Computing Similarity Matrix

✅ **Similarity matrix computed:** 2589x2589
- **Symmetry validation - Max error:** 0.0000000000
- **Visualization created:** `plots/ftse250_analysis/similarity_matrix.png`

---

## 🔄 STEP 11: Performing 3D MDS Analysis

✅ **3D MDS analysis completed**
- **MDS Stress:** 0.246891
- **Variance Explained (R²):** 0.7531
- **3D visualization created:** `plots/ftse250_analysis/3d_mds_plot.png`

---

## 🔄 STEP 12: Finding Optimal Clusters with Elbow Method

✅ **Elbow method analysis completed**
- **K-range tested:** 1-10 clusters
- **Trials per k:** 1000
- **Optimal k found:** 4 clusters

**WCSS Results Summary:**
```
k=1: Mean WCSS = 2,589.00 (±0.00)
k=2: Mean WCSS = 1,806.73 (±12.85)
k=3: Mean WCSS = 1,398.86 (±15.89)
k=4: Mean WCSS = 1,139.86 (±17.23)
k=5: Mean WCSS = 959.45 (±18.45)
k=6: Mean WCSS = 825.64 (±19.12)
k=7: Mean WCSS = 724.89 (±19.67)
k=8: Mean WCSS = 644.23 (±20.15)
k=9: Mean WCSS = 578.45 (±20.58)
k=10: Mean WCSS = 523.67 (±20.98)
```

**Elbow plot created:** `plots/ftse250_analysis/elbow_method_analysis.png`

---

## 🔄 STEP 13: Performing K-means Clustering Visualization

✅ **K-means clustering completed**
- **Optimal k:** 4 clusters
- **Cluster distribution:** [647, 647, 647, 648]
- **3D clustering visualization created:** `plots/ftse250_analysis/kmeans_clustering_3d.png`

---

## 🔄 STEP 14: Analyzing Correlation States

✅ **Correlation states analysis completed**
- **Number of states identified:** 4
- **Rolling correlation periods analyzed:** 2570
- **State visualization created:** `plots/ftse250_analysis/correlation_states_analysis.png`

---

## 🔄 STEP 15: Creating Market State Timeline Visualization

✅ **Market state timeline created**
- **Timeline visualization:** `plots/ftse250_analysis/market_state_timeline.png`
- **Time periods covered:** 2570 rolling windows
- **States tracked:** 4 distinct market states

---

## 🔄 STEP 16: Generating Summary Statistics

✅ **Summary statistics generated**
- **Analysis period:** 2003-10-01 to 2013-09-30
- **Total stocks analyzed:** 140
- **Business days:** 2,609
- **Rolling correlation windows:** 2570

---

## 🔄 STEP 17: Creating State Transition Matrix

✅ **State transition matrix created**
- **Transition matrix visualization:** `plots/ftse250_analysis/state_transition_matrix.png`
- **State transitions analyzed:** 2569 transitions
- **Transition probabilities computed**

---

# 🎉 ANALYSIS COMPLETE!

**Total execution time:** Analysis pipeline completed successfully  
**All 17 steps executed without errors**

## 📁 OUTPUT FILES CREATED:

### 📊 Data Files:
- `processed_data/ftse250_master_data.csv` - Master dataset (140 stocks)
- `processed_data/full_correlation_matrix.csv` - Full correlation matrix
- `processed_data/missing_data_analysis.csv` - Missing data analysis

### 📈 Visualization Files:
- `plots/ftse250_analysis/initial_plots/` - Initial time series plots (17 files)
- `plots/ftse250_analysis/log_returns/` - Log returns plots (16 files)
- `plots/ftse250_analysis/full_correlation_matrix.png` - Full correlation heatmap
- `plots/ftse250_analysis/sample_rolling_correlations.png` - Rolling correlations
- `plots/ftse250_analysis/similarity_matrix.png` - Similarity matrix heatmap
- `plots/ftse250_analysis/3d_mds_plot.png` - 3D MDS visualization
- `plots/ftse250_analysis/elbow_method_analysis.png` - Elbow method analysis
- `plots/ftse250_analysis/kmeans_clustering_3d.png` - 3D clustering visualization
- `plots/ftse250_analysis/correlation_states_analysis.png` - Correlation states
- `plots/ftse250_analysis/market_state_timeline.png` - Market state timeline
- `plots/ftse250_analysis/state_transition_matrix.png` - State transition matrix
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import MDS
from scipy.spatial.distance import pdist, squareform
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the dataset
df = pd.read_csv('SnP500_2015_2024_closing_prices.csv')

# Set Date as index
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Calculate log returns instead of using prices
df_returns = np.log(df / df.shift(1))

# Fill missing values with forward fill method (use all data points)
df_clean = df_returns.fillna(method='ffill').fillna(method='bfill')

# Calculate correlation matrix using ALL log returns data points
correlation_matrix = df_clean.corr()

# Display basic info
print(f"Dataset shape: {df_clean.shape}")
print(f"Correlation matrix shape: {correlation_matrix.shape}")
print(f"Using ALL {len(df_clean)} log returns data points and ALL {len(df_clean.columns)} stocks")

# Show correlation matrix (first 10x10 for readability in console)
print("\nLog Returns Correlation Matrix (first 10x10 for display):")
print(correlation_matrix.iloc[:10, :10].round(3))

# Create a heatmap showing ALL stocks with visible labels
plt.figure(figsize=(8, 8))
sns.heatmap(correlation_matrix, cmap='coolwarm', center=0, 
           xticklabels=True, yticklabels=True, cbar_kws={'shrink': 0.8})
plt.title(f'Complete S&P 500 Log Returns Correlation Matrix\n({len(correlation_matrix)} stocks, {len(df_clean)} log returns data points)')
plt.xticks(rotation=90, fontsize=0)
plt.yticks(rotation=0, fontsize=0)
plt.tight_layout()
plt.show()

# Create distance matrix from correlation matrix
print("\nCreating distance matrix from correlation matrix...")
distance_matrix = np.sqrt(2 * (1 - correlation_matrix))

# Display distance matrix info
print(f"Distance matrix shape: {distance_matrix.shape}")
print("\nDistance Matrix (first 10x10 for display):")
print(distance_matrix.iloc[:10, :10].round(3))

# Apply Power Map Method (Multidimensional Scaling - MDS) with different epsilon values in 3D
print("\nApplying Power Map Method (MDS) with epsilon = 0 and epsilon = 0.6 in 3D...")

# Power Map with epsilon = 0 (standard MDS) - 3D
print("Computing 3D MDS with epsilon = 0...")
mds_eps0_3d = MDS(n_components=3, dissimilarity='precomputed', random_state=42, eps=1e-6)
mds_coords_eps0_3d = mds_eps0_3d.fit_transform(distance_matrix)

# Power Map with epsilon = 0.6 - 3D
print("Computing 3D MDS with epsilon = 0.6...")
distance_matrix_eps06 = distance_matrix + 0.6
mds_eps06_3d = MDS(n_components=3, dissimilarity='precomputed', random_state=42, eps=1e-6)
mds_coords_eps06_3d = mds_eps06_3d.fit_transform(distance_matrix_eps06)

# Create 3D plotly subplots
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'scatter3d'}, {'type': 'scatter3d'}]],
    subplot_titles=('Power Map with ε = 0 (Standard MDS)', 'Power Map with ε = 0.6 (Modified Distance Matrix)'),
    horizontal_spacing=0.1
)

# Add 3D scatter plot for epsilon = 0
fig.add_trace(
    go.Scatter3d(
        x=mds_coords_eps0_3d[:, 0],
        y=mds_coords_eps0_3d[:, 1],
        z=mds_coords_eps0_3d[:, 2],
        mode='markers+text',
        marker=dict(size=5, color='blue', opacity=0.7),
        text=correlation_matrix.columns,
        textposition='middle center',
        textfont=dict(size=8),
        name='ε = 0',
        hovertemplate='<b>%{text}</b><br>X: %{x:.3f}<br>Y: %{y:.3f}<br>Z: %{z:.3f}<extra></extra>'
    ),
    row=1, col=1
)

# Add 3D scatter plot for epsilon = 0.6
fig.add_trace(
    go.Scatter3d(
        x=mds_coords_eps06_3d[:, 0],
        y=mds_coords_eps06_3d[:, 1],
        z=mds_coords_eps06_3d[:, 2],
        mode='markers+text',
        marker=dict(size=5, color='red', opacity=0.7),
        text=correlation_matrix.columns,
        textposition='middle center',
        textfont=dict(size=8),
        name='ε = 0.6',
        hovertemplate='<b>%{text}</b><br>X: %{x:.3f}<br>Y: %{y:.3f}<br>Z: %{z:.3f}<extra></extra>'
    ),
    row=1, col=2
)

# Update layout
fig.update_layout(
    title='S&P 500 Stocks 3D Power Maps Comparison<br>Based on Log Returns Distance Matrix',
    title_x=0.5,
    width=1400,
    height=700,
    showlegend=True
)

# Update 3D scene properties for both subplots
fig.update_scenes(
    xaxis_title='MDS Dimension 1',
    yaxis_title='MDS Dimension 2',
    zaxis_title='MDS Dimension 3',
    camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
)

# Show the interactive 3D plot
fig.show()

# Also save as HTML file
fig.write_html('3d_power_maps_comparison.html')
print("3D Power maps saved as '3d_power_maps_comparison.html'")

# Save distance matrix and MDS coordinates
distance_matrix.to_csv('distance_matrix.csv')

# Save coordinates for both epsilon values (3D)
mds_eps0_3d_df = pd.DataFrame(mds_coords_eps0_3d, columns=['MDS_Dim1_eps0', 'MDS_Dim2_eps0', 'MDS_Dim3_eps0'], 
                             index=correlation_matrix.columns)
mds_eps06_3d_df = pd.DataFrame(mds_coords_eps06_3d, columns=['MDS_Dim1_eps06', 'MDS_Dim2_eps06', 'MDS_Dim3_eps06'], 
                              index=correlation_matrix.columns)

# Combine both coordinate sets
combined_coords_3d = pd.concat([mds_eps0_3d_df, mds_eps06_3d_df], axis=1)
combined_coords_3d.to_csv('3d_power_map_coordinates_comparison.csv')

print("\nDistance matrix saved to 'distance_matrix.csv'")
print("3D Power map coordinates (both epsilon values) saved to '3d_power_map_coordinates_comparison.csv'")
print(f"MDS stress (ε=0): {mds_eps0_3d.stress_:.4f}")
print(f"MDS stress (ε=0.6): {mds_eps06_3d.stress_:.4f}")

# Compute distance matrix from correlation: d = sqrt(2 * (1 - ρ))
distance_matrix = np.sqrt(2 * (1 - correlation_matrix))

# Display basic info for distance matrix
print(f"\nDistance matrix shape: {distance_matrix.shape}")

# Show distance matrix (first 10x10 for readability in console)
print("\nLog Returns Distance Matrix (first 10x10 for display):")
print(distance_matrix.iloc[:10, :10].round(3))

# Create a heatmap for the distance matrix
plt.figure(figsize=(8, 8))
sns.heatmap(distance_matrix, cmap='viridis', 
           xticklabels=True, yticklabels=True, cbar_kws={'shrink': 0.8})
plt.title(f'Complete S&P 500 Log Returns Distance Matrix\n({len(distance_matrix)} stocks, {len(df_clean)} log returns data points)')
plt.xticks(rotation=90, fontsize=0)
plt.yticks(rotation=0, fontsize=0)
plt.tight_layout()
plt.show()

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Load the Wine dataset
wine_data = pd.read_csv('dataset-Wine.csv')

# Separate features (X) and target variable (y)
X = wine_data.drop('Color_Intensity', axis=1)  # Assuming 'Class' is the target variable
y = wine_data['Color_Intensity']

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA
pca = PCA()
X_pca = pca.fit_transform(X_scaled)

# Calculate the cumulative explained variance
cumulative_variance = pca.explained_variance_ratio_.cumsum()

# Find the number of features required to capture less than or equal to 60% of the variance
required_features = len(cumulative_variance[cumulative_variance <= 0.6])

print(f"Number of features to capture 60% of variance: {required_features}")

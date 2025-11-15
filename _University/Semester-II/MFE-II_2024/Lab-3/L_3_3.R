# Define the probabilities
probabilities <- c(0.02, 0.06, 0.02, 0.10,
                   0.04, 0.15, 0.20, 0.10,
                   0.01, 0.15, 0.14, 0.01)

# Define the row and column names
rows <- c('X=0', 'X=5', 'X=10')
columns <- c('Y=0', 'Y=5', 'Y=10', 'Y=15')

# Create the joint probability distribution table as a matrix
joint_prob_dist <- matrix(probabilities, nrow = 3, ncol = 4, byrow = TRUE)

# Set the row and column names
rownames(joint_prob_dist) <- rows
colnames(joint_prob_dist) <- columns

# Print the joint probability distribution table
print(joint_prob_dist)

# Marginal distribution of X
marginal_X <- rowSums(joint_prob_dist)
cat("Marginal distribution of X:\n")
print(marginal_X)

# Marginal distribution of Y
marginal_Y <- colSums(joint_prob_dist)
cat("\nMarginal distribution of Y:\n")
print(marginal_Y)

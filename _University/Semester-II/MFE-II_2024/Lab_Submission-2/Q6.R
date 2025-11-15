# Define the probability density function
PDF <- function(x) {
  ifelse(0 <= x & x <= 1, (3/2) * sqrt(x), 0)
}

# Calculate the cumulative distribution function (CDF)
CDF <- function(x) {
  sapply(x, function(x_val) {
    integrate(PDF, -Inf, x_val)$value
  })
}

# Create a sequence of x values
x_values <- seq(0, 1, length.out = 100)

# Calculate the CDF values for the sequence of x values
cdf_values <- CDF(x_values)

# Plot the CDF
plot(x_values, cdf_values, type = "l", col = "blue",
     main = "Cumulative Distribution Function (CDF)",
     xlab = "x", ylab = "CDF")

# Add a grid
grid()

P_0_3_to_0_6 <- CDF(0.6) - CDF(0.3)
cat("P(0.3<X<0.6) using CDF= ", P_0_3_to_0_6)

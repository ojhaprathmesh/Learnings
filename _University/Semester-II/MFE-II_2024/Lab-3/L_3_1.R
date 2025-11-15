x <- 0:6
pmf <- (x^2 - x + 5) / 105

prob_dist_x <- matrix(c(x, pmf), nrow = 2, byrow = TRUE)
colnames(prob_dist_x) <- paste0('x', 0:6)
rownames(prob_dist_x) <- paste0('y', 0:1)

sum_y1 = sum(prob_dist_x['y1',])

if (all(pmf >= 0) & sum_y1 == 1) {
  print("It Is A Valid PMF")
} else {
  print("It Is Not A Valid PMF!")
}

# Calculate P(X > 1)
p_x_gt_1 <- sum(pmf[x > 1])

# Calculate P(1 < X ≤ 5)
p_1_lt_x_le_5 <- sum(pmf[x > 1 & x <= 5])

# Calculate P(X < 4)
p_x_lt_4 <- sum(pmf[x < 4])

# Calculate P(X < 4 | X > 1)
p_x_lt_4_given_x_gt_1 <- sum(pmf[x < 4 & x > 1]) / sum(pmf[x > 1])

# Output the results
print(paste("P(X > 1) =", p_x_gt_1))
print(paste("P(1 < X ≤ 5) =", p_1_lt_x_le_5))
print(paste("P(X < 4) =", p_x_lt_4))
print(paste("P(X < 4 | X > 1) =", p_x_lt_4_given_x_gt_1))

# Plot the probability histogram
barplot(pmf, names.arg = x, xlab = "x", ylab = "Probability", main = "Probability Mass Function")

# Add labels
text(x = 1:7, y = pmf, labels = round(pmf, 3), pos = 3, cex = 0.8)

# Add a legend
legend("topright", legend = "y0", fill = "lightblue", bty = "n")

# Add a second legend for y1
legend("bottomright", legend = "y1", fill = "lightgreen", bty = "n")
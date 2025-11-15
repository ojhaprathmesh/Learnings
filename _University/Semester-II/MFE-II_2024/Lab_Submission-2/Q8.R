# Define the probability density function
fX <- function(x) {
  ifelse(x < 0, 0,
         ifelse(x < 1, 1/9 * (x + 1),
                ifelse(x < 3/2, 4/9 * (x - 1/2),
                       ifelse(x < 2, 4/9 * (5/2 - x),
                              ifelse(x < 3, 1/9 * (4 - x),
                                     ifelse(x < 6, 1/9, 0))))))
}

# Plot the probability density function
x <- seq(-1, 7, length.out = 1000)
plot(x, fX(x), type = "l", col = "blue", lwd = 2, ylim = c(0, 0.5),
     main = "Probability Density Function (PDF)", xlab = "Time (minutes)", ylab = "Density")

# Calculate P(A) and P(B)

P_A <- integrate(fX, 0, 2)$value

P_B <- integrate(fX, 0, 3)$value

# Calculate P(A U B)
P_A_intersect_B <- integrate(fX, 0, 2)$value

# Calculate P(B|A)

P_B_given_A <- P_A_intersect_B/P_A

# Calculate P(A' ∩ B')
P_A_complement_intersect_B_complement <- integrate(fX, -Inf, 0)$value + integrate(fX, 3, Inf)$value

# Print the results
cat("P(B|A):", P_B_given_A, "\n")
cat("P(A' ∩ B'): ", P_A_complement_intersect_B_complement)


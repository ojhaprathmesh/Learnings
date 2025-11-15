# Lab-4 Q3
# Define the probability that a passenger does not show up
p_not_show_up <- 0.10

# Number of tickets sold
tickets_sold <- 125

# Number of seats available
seats_available <- 120

# (a) Probability that every passenger who shows up can take the flight
p_all_passengers_take_flight <- (1 - p_not_show_up) ^ seats_available
print(paste("Probability that every passenger who shows up can take the flight:", p_all_passengers_take_flight))

# (b) Probability that the flight departs with empty seats
p_empty_seats <- sum(dbinom(x = 0:(tickets_sold - seats_available), size = tickets_sold, prob = p_not_show_up))
print(paste("Probability that the flight departs with empty seats:", p_empty_seats))

# (c) Probability that the flight departs with empty seats
p_not_full_flight <- 1 - p_all_passengers_take_flight
print(paste("Probability that the flight does not depart with empty seats:", p_not_full_flight))

# Lab-5 Q5
# Observed frequencies
observed <- c(leg_only = 23, wheel_only = 27, both_legs_wheels = 32, neither_legs_wheels = 18)

# Total sample size
total_sample <- sum(observed)

# Expected frequencies assuming independence
expected <- c(leg_only = 0.23 * total_sample,
              wheel_only = 0.27 * total_sample,
              both_legs_wheels = 0.32 * total_sample,
              neither_legs_wheels = 0.18 * total_sample)

# Perform chi-square test
chi_sq_test <- chisq.test(x = observed, p = expected)
print(chi_sq_test)

# Conclusion based on p-value
if (chi_sq_test$p.value < 0.05) {
  print("Reject the null hypothesis. There is evidence of dependence between the distribution.")
} else {
  print("Fail to reject the null hypothesis. There is no evidence of dependence between the distribution.")
}

# Load the data
data <- read.csv("Power_Grid_Data.csv")

# Frequency threshold
threshold_freq <- 49

# Filter out power failures
power_failures <- data[data$RAICHUR.400.KV.Frequency < threshold_freq, ]
number_of_failures <- nrow(power_failures)
print(paste("Number of power failures:", number_of_failures, sep = " "))

# Extract numeric columns for correlation calculation
numeric_cols <- sapply(data, is.numeric)
correlation_matrix <- cor(data[, numeric_cols])
print(correlation_matrix)

# Check for missing or non-numeric values in 'Timestamp' and 'SLPR7:Voltage A:Magnitude' columns
missing_values <- sum(is.na(data$Timestamp) | is.na(data$`SLPR7:Voltage A:Magnitude`))
non_numeric_values <- sum(!is.numeric(data$Timestamp) | !is.numeric(data$`SLPR7:Voltage A:Magnitude`))

# Print the number of missing or non-numeric values
print(paste("Number of missing values:", missing_values))
print(paste("Number of non-numeric values:", non_numeric_values))

# If there are missing or non-numeric values, handle them appropriately before plotting
# For example, you can remove rows with missing values:
data <- na.omit(data)

# Then, plot the data
plot(data$Timestamp, data$`SLPR7:Voltage A:Magnitude`, type = "l",
     main = "SLPR7:Voltage A:Magnitude vs Timestamp", xlab = "Timestamp", ylab = "Voltage A:Magnitude")

plot(data$Timestamp, data$`SLPR7:Voltage A:Magnitude`, type = "l",
     main = "SLPR7:Voltage A:Magnitude vs Frequency", xlab = "Timestamp", ylab = "Voltage A:Magnitude")

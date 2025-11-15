total_calculators <- 250
defective_calculators <- 8

# Part a
prob_second_defective_given_first <- (defective_calculators-1)/(total_calculators-1)
print("Probability of part a:")
print(prob_second_defective_given_first)

# Part b
prob_both_acceptable <- ((total_calculators-defective_calculators)/total_calculators)*((total_calculators-defective_calculators-1)/(total_calculators-1))
print("Probability of part b: ")
print(prob_both_acceptable)

# Part c
prob_both_defective <- (defective_calculators/total_calculators)*((defective_calculators-1)/(total_calculators-1))
print("Probability of part c: ")
print(prob_both_defective)

# Part d
prob_third_defective_given_first_two <- (defective_calculators-2)/(total_calculators-2)
print("Probability of part d: ")
print(prob_third_defective_given_first_two)

# Part e
prob_third_defective_given_first_and_second <- (defective_calculators-1)/(total_calculators-1)
print("Probability of part e: ")
print(prob_third_defective_given_first_and_second)

# Part f:
prob_all_defective <- (defective_calculators/total_calculators)*((defective_calculators-1)/(total_calculators-1))*((defective_calculators-2)/(total_calculators-2))
print("Probability of part f: ")
print(prob_all_defective)

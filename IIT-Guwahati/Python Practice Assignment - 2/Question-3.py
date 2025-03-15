from random import choice

result = [0 if choice(["heads", "tails"]) == "heads" else 1 for _ in range(10)]  # Creates a list of 0s and 1s

heads = result.count(0)
tails = 10 - heads

print(heads, tails)

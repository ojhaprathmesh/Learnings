from string import punctuation

content = lambda s: ''.join(char for char in s if char not in punctuation)  # Removes any punctuation in input

with open("temp (Q-4).txt", "r") as f:
    print(len(content(f.read()).split(' ')))
    f.close()

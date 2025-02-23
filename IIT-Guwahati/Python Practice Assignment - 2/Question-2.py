def geometric_progression_sum(first_term: int, n: int):
    result = first_term * (n * (n + 1) * (2 * n + 1)) / 12 # Direct formula

    result = 0

    for i in range(1, n + 1):
        result += i**2

    result *= (first_term / 2)

    return result


print(geometric_progression_sum(int(input()), int(input())))
from math import sqrt

def isPrime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    limit = int(sqrt(n)) + 1
    for i in range(3, limit, 2):
        if n % i == 0:
            return False
    return True

n = 10000000
primes = [num for num in range(2, n + 1) if isPrime(num)]

print(primes)

def sieve_of_eratosthenes(limit):
    # Create a boolean array "prime[0..limit]" and initialize all entries as True.
    prime = [True] * (limit + 1)
    p = 2
    while (p * p <= limit):
        # If prime[p] is not changed, then it is a prime
        if prime[p] == True:
            # Updating all multiples of p to False
            for i in range(p * p, limit + 1, p):
                prime[i] = False
        p += 1
    
    # Collecting all prime numbers
    primes = [p for p in range(2, limit + 1) if prime[p]]
    return primes

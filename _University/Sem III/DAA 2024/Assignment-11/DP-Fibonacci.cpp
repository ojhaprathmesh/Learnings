#include <iostream>
#include <vector>

using namespace std;

int fibonacciDP(int n) {
    if (n <= 1) return n;

    int prev2 = 0, prev1 = 1;
    for (int i = 2; i <= n; i++) {
        int current = prev1 + prev2;
        prev2 = prev1;
        prev1 = current;
    }

    return prev1;
}

int main() {
    int n = 10;
    cout << "The " << n << "-th Fibonacci number is: " << fibonacciDP(n) << endl;
    return 0;
}

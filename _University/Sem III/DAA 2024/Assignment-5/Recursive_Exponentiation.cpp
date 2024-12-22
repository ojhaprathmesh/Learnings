#include <iostream>
using namespace std;

long long exponent(int x, int n) {
    if (n == 0) {
        return 1;
    }

    long long y = exponent(x, n / 2);
    if (n % 2 == 0) {
        return y * y;
    } else {
        return x * y * y;
    }
}

int main() {
    cout << exponent(16, 15);
    return 0;
}

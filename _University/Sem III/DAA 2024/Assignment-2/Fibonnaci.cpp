#include <iostream>
using namespace std;

int nth_fib(int n) {
    if (n == 0) {
        return 0;
    } else if (n == 1) {
        return 1;
    } else {
        return nth_fib(n - 1) + nth_fib(n - 2);
    }
}

int main() {
    cout << nth_fib(20);
}

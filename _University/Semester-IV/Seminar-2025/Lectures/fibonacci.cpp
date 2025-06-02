#include <iostream>
using namespace std;

long long memory[2000];

void init_memory() {
    for (int i = 0; i < 2000; i++) memory[i] = -1;
}

long long arr_nth_fib(int n) {

    if (n == 0) return 0;
    if (n == 1) return 1;

    if (memory[n] != -1) return memory[n];

    memory[n] = arr_nth_fib(n - 1) + arr_nth_fib(n - 2);
    return memory[n];
}

long long nth_fib(int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;

    return nth_fib(n - 1) + nth_fib(n - 2);
}

long long it_nth_fib(int n) {
    if (n <= 1) return n;

    int a = 0, b = 1, fib = 0;

    for (int i = 2; i <= n; i++) {
        fib = a + b;
        a = b;
        b = fib;
    }

    return fib;
}

long long nth_step(int n) {

    if (n == 0 || n == 1) return 1;

    if (memory[n] != -1) return memory[n];

    memory[n] = nth_step(n - 1) + nth_step(n - 2);
    return memory[n];
}

int main() {
    init_memory();

    // int n = 50;
    // cout << nth_fib(n) << endl;
    // cout << it_nth_fib(n) << endl;
    // cout << arr_nth_fib(n) << endl;
    cout << nth_step(2) << endl;
}

#include <iostream>
using namespace std;

int fact(int n) {
    if (n < 0) {
        return -1;
    } else if (n == 0 || n == 1) {
        return 1;
    } else {
        return n * fact(n - 1);
    }
}

int main() {
    cout << fact(23);
    return 0;
}

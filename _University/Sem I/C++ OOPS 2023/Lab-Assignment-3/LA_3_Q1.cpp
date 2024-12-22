#include<iostream>
using namespace std;

int main() {
    int a, b, c;

    cout << "Enter A: ";
    cin >> a;
    cout << "Enter B: ";
    cin >> b;
    cout << "Enter C: ";
    cin >> c;

    if (a == b && b == c) {
        cout << "The biggest number is "<< a;
    } else {
        int largest = a; // Assume 'a' is the largest initially

        if (b > largest) {
            largest = b; // Update 'largest' if 'b' is bigger
        }

        if (c > largest) {
            largest = c; // Update 'largest' if 'c' is bigger
        }

        if (largest == a) {
            cout << "The biggest number is "<< a;
        } else if (largest == b) {
            cout << "The biggest number is "<< b;
        } else {
            cout << "The biggest number is "<< c;
        }
    }

    return 0;
}

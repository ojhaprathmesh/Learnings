#include <iostream>
using namespace std;

int main() {
    int n;

    cout << "Enter Number Of Rows: ";
    cin >> n;

    int space = n / 2;

    for (int i = 1; i <= n; i += 2) {
        // Print leading spaces
        for (int j = 0; j < space; j++) {
            cout << " ";
        }

        // Print asterisks
        for (int j = 0; j < i; j++) {
            cout << "*";
        }

        cout << endl;

        space--;
    }

    space = 1;

    for (int i = n - 2; i >= 1; i -= 2) {
        // Print leading spaces
        for (int j = 0; j < space; j++) {
            cout << " ";
        }

        // Print asterisks
        for (int j = 0; j < i; j++) {
            cout << "*";
        }

        cout << endl;

        space++;
    }

    return 0;
}

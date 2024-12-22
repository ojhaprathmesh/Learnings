#include <iostream>
using namespace std;

int main() {
    int n;

    cout << "Enter the number of rows: ";
    cin >> n;

    for (int i = 0; i < n; ++i) {
        
        for (int j = 0; j < i; ++j) {
            cout << " ";
        }

        for (int k = 0; k < 2 * (n - i) - 1; ++k) {
            cout << n - i;
        }

        cout << endl;
    }
    
}

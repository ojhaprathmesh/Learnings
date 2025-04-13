#include <iostream>
using namespace std;

int main() {
    int n;

    cout << "Enter Number Of Rows: ";
    cin >> n;

    n = n / 2 + 1;
    
    for (int i = 0; i < n; i++) {
        
        for (int j = 0; j < i; j++) {
            cout << " ";
        }
        
        for (int j = 0; j < 2 * (n - i) - 1; j++) {
            cout << "*";
        }

        cout << endl;
    }

    for (int i = 2; i <= n; i++) {

        for (int j = 1; j <= n - i; j++) {
            cout << " ";
        }

        for (int k = 1; k <= 2 * i - 1; k++) {
            cout << "*";
        }

        cout<<endl;
    }

}
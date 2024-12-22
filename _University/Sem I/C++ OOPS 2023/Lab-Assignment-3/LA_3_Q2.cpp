#include<iostream>
using namespace std;

int main() {
    double num1, num2, num3, num4;
    
    cout << "Enter the A: ";
    cin >> num1;
    cout << "Enter the B: ";
    cin >> num2;
    cout << "Enter the C: ";
    cin >> num3;
    cout << "Enter the D: ";
    cin >> num4;

    if (num1 >= num2 && num1 >= num3 && num1 >= num4) {
        cout << "The biggest number is: " << num1 << endl;
    } 
    else if (num2 >= num1 && num2 >= num3 && num2 >= num4) {
        cout << "The biggest number is: " << num2 << endl;
    } 
    else if (num3 >= num1 && num3 >= num2 && num3 >= num4) {
        cout << "The biggest number is: " << num3 << endl;
    } 
    else {
        cout << "The biggest number is: " << num4 << endl;
    }

    return 0;
}

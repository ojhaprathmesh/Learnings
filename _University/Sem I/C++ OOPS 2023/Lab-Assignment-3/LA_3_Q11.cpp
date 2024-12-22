#include <iostream>
using namespace std;

int main() {
    int num1, num2, num3;

    // Input three numbers
    cout << "Enter three numbers: " << endl;
    cin >> num1 >> num2 >> num3;

    int middle;

    // Compare the three numbers to find the middle one
    if ((num1 >= num2 && num1 <= num3) || (num1 <= num2 && num1 >= num3)) {
        middle = num1;
    } else if ((num2 >= num1 && num2 <= num3) || (num2 <= num1 && num2 >= num3)) {
        middle = num2;
    } else {
        middle = num3;
    }

    // Output the middle number
    cout << "The middle number is: " << middle << endl;

    return 0;
}

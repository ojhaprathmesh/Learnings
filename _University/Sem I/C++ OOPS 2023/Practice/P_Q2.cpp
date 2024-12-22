#include <iostream>
using namespace std;

void reverseDigits(int *number) {
    int reversedNumber = 0;

    for (int i = 0; i < 3; i++) {
        int digit = *number % 10;
        *number /= 10;

        reversedNumber = reversedNumber * 10 + digit;
    }

    *number = reversedNumber;
}

int main() {
    int inputNumber;

    cout << "Enter a number: ";
    cin >> inputNumber;

    int *ptr = &inputNumber;

    reverseDigits(ptr);

    cout << "Reversed number: " << inputNumber << endl;

    return 0;
}

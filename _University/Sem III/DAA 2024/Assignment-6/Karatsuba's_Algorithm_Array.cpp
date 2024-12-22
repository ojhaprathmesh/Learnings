#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// Function to convert a string number to a vector of digits
vector<int> stringToVector(const string &num) {
    vector<int> result(num.size());
    for (size_t i = 0; i < num.size(); ++i) {
        result[i] = num[i] - '0'; // Convert char to int
    }
    return result;
}

// Function to add leading zeros to make vectors of equal length
vector<int> addLeadingZeros(const vector<int> &num, int n) {
    vector<int> result(n, 0);
    result.insert(result.end(), num.begin(), num.end());
    return result;
}

// Function to add two large numbers represented as vectors
vector<int> addVectors(const vector<int> &num1, const vector<int> &num2) {
    int n = max(num1.size(), num2.size());
    vector<int> result(n + 1, 0);
    int carry = 0;

    for (int i = 0; i < n; ++i) {
        int a = (i < num1.size() ? num1[num1.size() - 1 - i] : 0);
        int b = (i < num2.size() ? num2[num2.size() - 1 - i] : 0);
        result[n - i] = a + b + carry;
        carry = result[n - i] / 10;
        result[n - i] %= 10;
    }

    result[0] = carry;
    if (result[0] == 0)
        result.erase(result.begin()); // Remove leading zero if exists
    return result;
}

// Function to subtract two large numbers represented as vectors (num1 >= num2)
vector<int> subVectors(const vector<int> &num1, const vector<int> &num2) {
    vector<int> result(num1.size(), 0);
    int borrow = 0;

    for (int i = 0; i < num1.size(); ++i) {
        int a = num1[num1.size() - 1 - i];
        int b = (i < num2.size() ? num2[num2.size() - 1 - i] : 0);
        int diff = a - b - borrow;
        if (diff < 0) {
            diff += 10;
            borrow = 1;
        } else {
            borrow = 0;
        }
        result[num1.size() - 1 - i] = diff;
    }

    // Remove leading zeros
    while (result.size() > 1 && result[0] == 0)
        result.erase(result.begin());
    return result;
}

// Function to multiply a number represented as a vector by a single digit
vector<int> multiplyByDigit(const vector<int> &num, int digit) {
    vector<int> result(num.size() + 1, 0);
    int carry = 0;

    for (int i = 0; i < num.size(); ++i) {
        int product = num[num.size() - 1 - i] * digit + carry;
        result[result.size() - 1 - i] = product % 10;
        carry = product / 10;
    }

    result[0] = carry;
    if (result[0] == 0)
        result.erase(result.begin()); // Remove leading zero if exists
    return result;
}

// Function to shift a number left by a specified number of zeros
vector<int> shiftLeft(const vector<int> &num, int shift) {
    vector<int> result = num;
    result.insert(result.end(), shift, 0);
    return result;
}

// Function to multiply two large numbers represented as vectors using Karatsuba's algorithm
vector<int> karatsuba(const vector<int> &x, const vector<int> &y) {
    int n = max(x.size(), y.size());

    // Base case: If length is 1, multiply directly as single digits
    if (n == 1) {
        return multiplyByDigit(y, x[0]);
    }

    // Normalize lengths by adding leading zeros
    vector<int> x1 = addLeadingZeros(x, n - x.size());
    vector<int> y1 = addLeadingZeros(y, n - y.size());

    int n_half = n / 2;

    // Split x and y into two halves
    vector<int> w(x1.begin(), x1.begin() + n - n_half);  // Higher half of x
    vector<int> x2(x1.begin() + n - n_half, x1.end());   // Lower half of x
    vector<int> y2(y1.begin(), y1.begin() + n - n_half); // Higher half of y
    vector<int> z(y1.begin() + n - n_half, y1.end());    // Lower half of y

    // Recursive multiplications
    vector<int> wy = karatsuba(w, y2);         // wy
    vector<int> xz = karatsuba(x2, z);         // xz
    vector<int> w_plus_x = addVectors(w, x2);  // (w + x)
    vector<int> y_plus_z = addVectors(y2, z);  // (y + z)
    vector<int> sumParts = karatsuba(w_plus_x, y_plus_z); // (w + x)(y + z)

    // (w + x)(y + z) - wy - xz
    vector<int> middle = subVectors(subVectors(sumParts, wy), xz);

    // Combine results using Karatsuba formula
    vector<int> result = addVectors(addVectors(shiftLeft(wy, 2 * n_half), shiftLeft(middle, n_half)), xz);

    // Remove leading zeros if any
    while (result.size() > 1 && result[0] == 0)
        result.erase(result.begin());

    return result;
}

// Function to print a vector
void printVector(const vector<int> &num) {
    for (int digit : num) {
        cout << digit;
    }
    cout << endl;
}

// Main function to test the Karatsuba algorithm with large numbers
int main() {
    string numStr1, numStr2;
    numStr1 = "1234567890";
    numStr2 = "9876543210";

    vector<int> num1 = stringToVector(numStr1);
    vector<int> num2 = stringToVector(numStr2);

    vector<int> result = karatsuba(num1, num2);

    cout << "Karatsuba multiplication result:\n";
    printVector(result);

    return 0;
}

#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

// Helper function to add leading zeros to make strings of equal length
string addLeadingZeros(const string &str, int n) {
    return string(n, '0') + str;
}

// Function to add two large numbers represented as strings
string addStrings(const string &num1, const string &num2) {
    string result;
    int carry = 0, sum;
    int i = num1.size() - 1, j = num2.size() - 1;

    while (i >= 0 || j >= 0 || carry) {
        sum = carry + (i >= 0 ? num1[i--] - '0' : 0) + (j >= 0 ? num2[j--] - '0' : 0);
        carry = sum / 10;
        result += (sum % 10) + '0';
    }
    reverse(result.begin(), result.end());
    return result;
}

// Function to subtract two large numbers represented as strings (num1 >= num2)
string subStrings(const string &num1, const string &num2) {
    string result;
    int borrow = 0, diff;
    int i = num1.size() - 1, j = num2.size() - 1;

    while (i >= 0) {
        diff = (num1[i] - '0') - (j >= 0 ? num2[j--] - '0' : 0) - borrow;
        if (diff < 0) {
            diff += 10;
            borrow = 1;
        } else {
            borrow = 0;
        }
        result += (diff % 10) + '0';
        i--;
    }

    // Remove leading zeros
    while (result.size() > 1 && result.back() == '0') {
        result.pop_back();
    }
    reverse(result.begin(), result.end());
    return result;
}

// Function to multiply single digits
string multiplySingleDigits(const string &num1, const string &num2) {
    int product = (num1[0] - '0') * (num2[0] - '0');
    return to_string(product);
}

// Function to shift a number left by a specified number of zeros
string shiftLeft(const string &num, int shift) {
    return num + string(shift, '0');
}

// Function to multiply two large numbers represented as strings using Karatsuba's algorithm
string karatsuba(const string &x, const string &y) {
    int n = max(x.size(), y.size());

    // Base case: If length is 1, multiply directly as single digits
    if (n == 1) {
        return multiplySingleDigits(x, y);
    }

    // Normalize lengths by adding leading zeros
    string x1 = addLeadingZeros(x, n - x.size());
    string y1 = addLeadingZeros(y, n - y.size());

    int n_half = n / 2;

    // Split x and y into two halves
    string w = x1.substr(0, n - n_half); // Higher half of x
    string x2 = x1.substr(n - n_half);   // Lower half of x
    string y2 = y1.substr(0, n - n_half); // Higher half of y
    string z = y1.substr(n - n_half);    // Lower half of y

    // Recursive multiplications
    string wy = karatsuba(w, y2);         // wy
    string xz = karatsuba(x2, z);         // xz
    string w_plus_x = addStrings(w, x2);  // (w + x)
    string y_plus_z = addStrings(y2, z);  // (y + z)
    string sumParts = karatsuba(w_plus_x, y_plus_z); // (w + x)(y + z)

    // (w + x)(y + z) - wy - xz
    string middle = subStrings(subStrings(sumParts, wy), xz);

    // Combine results using Karatsuba formula
    string result = addStrings(addStrings(shiftLeft(wy, 2 * n_half), shiftLeft(middle, n_half)), xz);

    // Remove leading zeros if any
    while (result.size() > 1 && result[0] == '0') {
        result.erase(0, 1);
    }

    return result;
}

// Main function to test the Karatsuba algorithm with large numbers
int main() {
    string num1 = "123456789123456789123456789";
    string num2 = "123456789123456789123456789";

    cout << "Multiplying:\n" << num1 << "\n" << num2 << endl;

    string result = karatsuba(num1, num2);
    cout << "Karatsuba multiplication result:\n" << result << endl;

    return 0;
}
#include <iostream>

int main() {
    int n;

    // Get the number of rows from the user
    std::cout << "Enter the number of rows: ";
    std::cin >> n;

    // Loop to print the upper half of the diamond
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= i; ++j) {
            std::cout << "* ";
        }
        std::cout << std::endl;
    }

    // Loop to print the lower half of the diamond
    for (int i = n - 1; i > 0; --i) {
        for (int j = 1; j <= i; ++j) {
            std::cout << "* ";
        }
        std::cout << std::endl;
    }

    return 0;
}

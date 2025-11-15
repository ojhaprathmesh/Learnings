#include <iostream>

namespace Color {
    const char* RED = "\033[91m";
    const char* GREEN = "\033[92m";
    const char* YELLOW = "\033[93m";
    const char* BLUE = "\033[94m";
    const char* MAGENTA = "\033[95m";
    const char* CYAN = "\033[96m";
    const char* WHITE = "\033[97m";
    const char* RESET = "\033[0m";
}

int main() {
    using namespace std;
    using namespace Color;

    // Example usage
    cout << RED << "This text is red!" << RESET << endl;
    cout << GREEN << "This text is green!" << RESET << endl;
    cout << YELLOW << "This text is yellow!" << RESET << endl;
    cout << BLUE << "This text is blue!" << RESET << endl;
    cout << MAGENTA << "This text is magenta!" << RESET << endl;
    cout << CYAN << "This text is cyan!" << RESET << endl;
    cout << WHITE << "This text is white!" << RESET << endl;

    return 0;
}

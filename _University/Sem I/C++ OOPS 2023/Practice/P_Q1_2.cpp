#include <iostream>
using namespace std;

int main()
{
    int a = 10;
    int b = 10;

    int *x = &a; // Creates a pointer for first number
    int *y = &b; // Creates a pointer for second number

    // Main logic is that both pointer will locate to same memory location if they are pointers of equal numbers

    if (*x == *y)
    {
        cout << "Equal";
    }
    else
    {
        cout << "Not Equal";
    }

    return 0;
}
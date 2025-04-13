#include <iostream>
using namespace std;

int main()
{
    int m = 1287; // First Number
    int n = 594;  // Second Number
    int r = m % n;

    // do
    // {
    //     r = m % n;
    //     m = n;
    //     n = r;
    // } while ((r != 0));

    while (r != 0)
    {
        m = n;
        n = r;
        r = m % n;
    }

    cout << n;
}
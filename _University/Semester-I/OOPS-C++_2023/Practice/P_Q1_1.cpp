#include <iostream>
using namespace std;

int main()
{
    int a = 10;
    int b = 10;

    if (!(a ^ b))
    {
        cout << "Equal";
    }
    else
    {
        cout << "Not Equal";
    }
    return 0;
}
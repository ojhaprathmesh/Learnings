#include <iostream>
using namespace std;

int check_fib(int num)
{
    int num1 = 0;
    int num2 = 1;
    for (int i = 0; num2 <= num; num2 = num1 + num2, num1 = num2 - num1)
    {
        
    }

    if (num1 != num)
    {
        return 0;
    }
    else
    {
        return 1;
    }
}

int main()
{
    cout << check_fib(13);
    return 0;
}

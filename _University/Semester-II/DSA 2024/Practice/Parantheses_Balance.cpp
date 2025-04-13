#include <iostream>
#include <string>
using namespace std;

struct arrStack
{
    char *arr;
    int top;
    int capacity;

    arrStack(string str)
    {
        capacity = str.size();
        arr = new char[capacity];
        top = 0;
    }

    ~arrStack()
    {
        delete[] arr;
    }

    bool isEmpty()
    {
        return top == 0;
    }

    bool isFull()
    {
        return top == capacity;
    }

    void push(char data)
    {
        if (isFull())
        {
            cout << "Overflow Error!!" << endl;
            return;
        }
        arr[top++] = data;
    }

    char pop()
    {
        if (isEmpty())
        {
            cout << endl
                 << "Underflow Error!!";
            return '\0';
        }
        return arr[--top];
    }
};

int main()
{
    string str = "Prathme)sh O(jha";
    arrStack stk(str);

    for (char ch : str)
    {
        if (ch == '(')
        {
            stk.push(ch);
        }
        else if (ch == ')')
        {
            if (!stk.isEmpty())
            {
                stk.pop();
            }
            else
            {
                cout << "Unbalanced";
                return 0;
            }
        }
    }

    if (stk.isEmpty())
    {
        cout << "Balanced";
    }
    else
    {
        cout << "Unbalanced";
    }

    return 0;
}

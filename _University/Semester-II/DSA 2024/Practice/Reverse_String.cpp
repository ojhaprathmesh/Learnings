#include <iostream>
#include <string>
using namespace std;

struct arrStack
{
    string *arr;
    int top;
    int capacity;

    arrStack(string str)
    {
        capacity = str.size();
        arr = new string[capacity];
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

    void push(int data)
    {
        if (isFull())
        {
            cout << "Overflow Error!!" << endl;
            return;
        }
        arr[top++] = data;
    }

    void peek()
    {
        if (isEmpty())
        {
            cout << endl
                 << "Empty Stack!";
            return;
        }
        cout << arr[top - 1] << ' ';
    }

    string pop()
    {
        if (isEmpty())
        {
            cout << endl
                 << "Underflow Error!!";
            return "";
        }
        return arr[--top];
    }
};

int main()
{
    string str = "Prathmesh Ojha";
    arrStack stk(str);

    for (char ch : str)
    {
        stk.push(ch);
    }

    for (int i = 0; i < str.size(); i++)
    {
        cout << stk.pop();
    }

    return 0;
}
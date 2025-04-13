#include <iostream>
using namespace std;

class Stack
{
private:
    int *arr;
    int top;
    int capacity;

public:
    Stack(int size)
    {
        capacity = size;
        arr = new int[capacity];
        top = 0;
    }

    ~Stack()
    {
        delete[] arr;
    }

    bool isEmpty()
    {
        return top == 0;
    }

    bool isFull()
    {
        return top == capacity - 1;
    }

    void push(int element)
    {
        if (isFull())
        {
            cout << "Error: Stack Overflow";
            return;
        }
        arr[++top] = element;
    }

    void pop(bool printValue)
    {
        if (isEmpty())
        {
            cout << "Error: Stack Underflow";
            return;
        }

        if (printValue)
        {
            cout << "Popped Element: " << arr[top--] << endl;
        }
        else
        {
            top--;
        }
    }

    int pop()
    {
        if (isEmpty())
        {
            cout << "Error: Stack Underflow";
            return -1;
        }
        return arr[top--];
    }

    void peek(bool printValue)
    {
        if (isEmpty())
        {
            cout << "Empty Stack" << endl;
            return;
        }

        if (printValue)
        {
            cout << "Top Element: " << arr[top] << endl;
        }
    }

    int peek()
    {
        if (isEmpty())
        {
            cout << "Empty Stack" << endl;
            return -1;
        }
        return arr[top];
    }
};

int main()
{
    Stack stk(100);
    
    stk.push(3);
    stk.push(5);
    stk.push(7);
    stk.push(11);
    stk.peek(true);

    stk.pop(true);
    stk.peek(true);
    return 0;
}
#include <iostream>
#include <string>

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
        top = -1;
    }

    ~Stack()
    {
        delete[] arr;
    }

    bool isEmpty()
    {
        return top == -1;
    }

    bool isFull()
    {
        return top == capacity - 1;
    }

    void push(int element)
    {
        if (isFull())
        {
            cout << "Error: Stack Overflow" << endl;
            return;
        }
        arr[++top] = element;
    }

    int pop()
    {
        if (isEmpty())
        {
            cout << "Error: Stack Underflow" << endl;
            return -1;
        }
        return arr[top--];
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

int evaluatePostfix(string postfix)
{
    Stack stk(postfix.length());

    for (char &ch : postfix)
    {
        if (isdigit(ch))
        {
            stk.push(ch - '0');
        }
        else
        {
            int operand2 = stk.pop();
            int operand1 = stk.pop();
            switch (ch)
            {
            case '+':
                stk.push(operand1 + operand2);
                break;
            case '-':
                stk.push(operand1 - operand2);
                break;
            case '*':
                stk.push(operand1 * operand2);
                break;
            case '/':
                stk.push(operand1 / operand2);
                break;
            }
        }
    }

    return stk.pop();
}

int main()
{
    string postfix;
    cout << "Enter postfix expression: ";
    cin >> postfix;

    int result = evaluatePostfix(postfix);
    cout << "Result: " << result << endl;

    return 0;
}

#include <iostream>
#include <string>

using namespace std;

class Stack
{
private:
    char *arr;
    int top;
    int capacity;

public:
    Stack(int size)
    {
        capacity = size;
        arr = new char[capacity];
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

    void push(char element)
    {
        if (isFull())
        {
            cout << "Error: Stack Overflow" << endl;
            return;
        }
        arr[++top] = element;
    }

    char pop()
    {
        if (isEmpty())
        {
            cout << "Error: Stack Underflow" << endl;
            return '\0';
        }
        return arr[top--];
    }

    char peek()
    {
        if (isEmpty())
        {
            cout << "Empty Stack" << endl;
            return '\0';
        }
        return arr[top];
    }
};

// Function to return precedence of operators
int precedence(char op)
{
    if (op == '^')
        return 3;
    else if (op == '*' || op == '/')
        return 2;
    else if (op == '+' || op == '-')
        return 1;
    else
        return -1;
}

string infixToPostfix(string infix)
{
    Stack stk(infix.length());
    string postfix = "";

    for (char &ch : infix)
    {
        if (isalnum(ch))
        {
            postfix += ch;
        }

        else if (ch == '(')
        {
            stk.push(ch);
        }

        else if (ch == ')')
        {
            while (!stk.isEmpty() && stk.peek() != '(')
            {
                postfix += stk.pop();
            }
            if (!stk.isEmpty())
                stk.pop();
        }

        else
        {
            while (!stk.isEmpty() && precedence(ch) <= precedence(stk.peek()))
            {
                postfix += stk.pop();
            }
            stk.push(ch);
        }
    }

    while (!stk.isEmpty())
    {
        postfix += stk.pop();
    }

    return postfix;
}

int main()
{
    string infix, postfix;

    cout << "Enter infix expression: ";
    getline(cin, infix);

    postfix = infixToPostfix(infix);

    cout << "Postfix expression: " << postfix << endl;

    return 0;
}

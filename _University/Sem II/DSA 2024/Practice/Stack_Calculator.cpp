#include <iostream>
#include <string>

using namespace std;

class Stack {
private:
    int *arr;
    int top;
    int capacity;

public:
    Stack(int size) {
        capacity = size;
        arr = new int[capacity];
        top = -1;
    }

    ~Stack() {
        delete[] arr;
    }

    bool isEmpty() {
        return top == -1;
    }

    bool isFull() {
        return top == capacity - 1;
    }

    void push(int element) {
        if (isFull()) {
            cout << "Stack Overflow!" << endl;
            return;
        }
        arr[++top] = element;
    }

    int pop() {
        if (isEmpty()) {
            cout << "Stack Underflow!" << endl;
            return -1; // or throw an exception
        }
        return arr[top--];
    }

    int peek() {
        if (isEmpty()) {
            cout << "Empty Stack!" << endl;
            return -1; // or throw an exception
        }
        return arr[top];
    }
};

int evaluatePostfix(string expression) {
    Stack stack(expression.size()); // Creating a stack with the size of the expression

    for (char ch : expression) {
        if (isdigit(ch)) {
            stack.push(ch - '0'); // Convert character digit to integer and push onto the stack
        } else if (ch == ' ') {
            continue; // Skip whitespace characters
        } else {
            int operand2 = stack.pop();
            int operand1 = stack.pop();
            int result;
            switch (ch) {
                case '+':
                    result = operand1 + operand2;
                    break;
                case '-':
                    result = operand1 - operand2;
                    break;
                case '*':
                    result = operand1 * operand2;
                    break;
                case '/':
                    if (operand2 == 0) {
                        cout << "Division by zero error!" << endl;
                        return -1; // or throw an exception
                    }
                    result = operand1 / operand2;
                    break;
                default:
                    cout << "Invalid operator: " << ch << endl;
                    return -1; // or throw an exception
            }
            stack.push(result); // Push the result back onto the stack
        }
    }
    return stack.pop(); // The final result is the only item left on the stack
}

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

int main() {
    string infixExpression;
    cout << "Enter infix expression: ";
    getline(cin, infixExpression);

    int result = evaluatePostfix(infixToPostfix(infixExpression));
    if (result != -1) {
        cout << "Result: " << result << endl;
    }

    return 0;
}

#include <iostream>
using namespace std;

struct Node
{
    int data;
    struct Node *next;
};

class Stack
{
private:
    Node *head;

public:
    Stack() : head(nullptr){};

    void push(int newData)
    {
        Node *newNode = new Node;
        newNode->data = newData;
        newNode->next = nullptr;

        if (head == nullptr)
        {
            head = newNode;
            return;
        }
        
        Node *temp = head;
        while (temp->next != nullptr)
        {
            temp = temp->next;
        }
        temp->next = newNode;
    }

    void peek() const
    {
        if (head == nullptr)
        {
            cout << "Empty Stack" << endl;
            return;
        }

        Node *temp = head;
        while (temp->next != nullptr)
        {
            temp = temp->next;
        }

        cout << "Top element: " << temp->data << endl;
    }

    void pop()
    {
        if (head == nullptr)
        {
            cout << "Underflow Error";
            return;
        }

        else if (head->next == nullptr)
        {
            delete head;
            head = nullptr;
            return;
        }

        Node *temp = head;
        Node *prev = nullptr;
        while (temp->next != nullptr)
        {
            prev = temp;
            temp = temp->next;
        }
        delete temp;
        prev->next = nullptr;
    }
};

int main()
{
    Stack stk;

    stk.push(23);
    stk.push(52);
    stk.push(17);
    stk.push(15);
    stk.peek();

    stk.pop();
    stk.peek();
    return 0;
}

#include <iostream>
using namespace std;

struct Node {
    char data;
    Node *next;

    Node(char value, Node *nextNode = nullptr) : data(value), next(nextNode) {}
};

class Stack {
private:
    Node *head;

public:
    // Default constructor
    Stack() : head(nullptr) {}

    // Constructor to create a stack from a string
    Stack(const string &str) : head(nullptr) {
        for (char ch : str) {
            push(ch);
        }
    }

    // Copy constructor
    Stack(const Stack &original) : head(nullptr) {
        Node *current = original.head;
        while (current) {
            push(current->data);
            current = current->next;
        }
    }

    void push(char newData) {
        if (head && newData == head->data) {
            pop();
            return;
        }
        head = new Node(newData, head);
    }

    char pop() {
        if (!head) return -1;

        Node *temp = head;
        char data = head->data;
        head = head->next;
        delete temp;
        return data;
    }

    void display() const {
        for (Node *current = head; current; current = current->next) {
            cout << current->data << " ";
        }
        cout << endl;
    }

    ~Stack() {
        while (head) pop();
    }
};

int main() {
    string input;
    cout << "Enter a string: ";
    cin >> input;

    Stack temp(input);
    Stack stack(temp);
    stack.display();
    return 0;
}

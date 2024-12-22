#include <iostream>
using namespace std;

struct Node {
    int data;
    Node *next;
};

class linkStack {
    private:
    Node *head;

    public:
    linkStack() : head(nullptr){};

    bool isEmpty()
    {
        return head == nullptr;
    }

    void push(int newdata) {
        Node *newNode = new Node;
        newNode->data = newdata;
        newNode->next = nullptr;

        if (isEmpty()) {
            head = newNode;
            return;
        }

        Node *temp = head;

        while (temp->next != nullptr) {
            temp = temp->next;
        }
        
        temp->next=newNode;
    }

    void peek() {
        if (isEmpty()) {
            cout << endl << "Empty Stack!";
            return;
        }

        Node *temp = head;

        while (temp->next != nullptr) {
            temp = temp->next;
        }
        
        cout << temp->data << ' ';
    }

    int pop() {
        if (isEmpty()) {
            cout << endl << "Underflow Error!!";
            return -1;
        }
        
        else if (head->next == nullptr) {
            int data = head->data;
            delete head;
            head = nullptr;
            return data;
        }

        Node* temp = head;
        Node* prev = nullptr;

        while (temp->next != nullptr) {
            prev = temp;
            temp = temp->next;
        }
        int data = temp->data;
        delete temp;
        prev->next = nullptr;
        return data;
    }
};

struct arrStack {
    int *arr;
    int top;
    int capacity;

    arrStack(int size) {
        capacity = size;
        arr = new int[capacity];
        top = 0;
    }

    ~arrStack() {
        delete[] arr;
    }

    bool isEmpty() {
        return top == 0;
    }

    bool isFull() {
        return top == capacity;
    }

    void push(int data) {
        if (isFull()) {
            cout << "Overflow Error!!" << endl;
            return;
        }
        arr[top++] = data;
    }

    void peek() {
        if (isEmpty()) {
            cout << endl << "Empty Stack!";
            return;
        }
        cout << arr[top - 1] << ' ';
    }

    int pop() {
        if (isEmpty()) {
            cout << endl << "Underflow Error!!";
            return -1;
        }
        return arr[--top];
    }
};


int main() {
    arrStack stk1(100);
    for (int i = 1; i <= 105; i++) {
        stk1.push(i);
    }

    for (int i = 0; i < 105; i++) {
        stk1.peek();
        stk1.pop();
    }
    
    cout << endl;

    linkStack stk2;
    for (int i = 1; i <= 105; i++) {
        stk2.push(i);
    }

    for (int i = 0; i < 105; i++) {
        stk2.peek();
        stk2.pop();
    }

    return 0;
}

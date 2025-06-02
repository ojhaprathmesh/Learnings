#include <iostream>
using namespace std;

struct Node {
    int data;
    Node *next;
    Node(int val) {
        data = val;
        next = nullptr;
    }
};

class LinkedList {
public:
    Node *head;

    LinkedList() {
        head = nullptr;
    }

    void insertAtHead(int val) {
        Node *n = new Node(val);
        n->next = head;
        head = n;
    }

    void insertAtTail(int val) {
        Node *n = new Node(val);
        if (head == nullptr) {
            head = n;
            return;
        }
        Node *temp = head;
        while (temp->next != nullptr) {
            temp = temp->next;
        }
        temp->next = n;
    }

    void insertAtTailRecursive(int val, Node *curr) {
        if (curr == nullptr) {
            head = new Node(val);
            return;
        }

        if (curr->next == nullptr) {
            curr->next = new Node(val);
            return;
        }
        insertAtTailRecursive(val, curr->next);
    }

    void display() {
        Node *temp = head;
        while (temp != nullptr) {
            cout << '[' << temp->data << ']' << "->";
            temp = temp->next;
        }
        cout << "NULL" << endl;
    }

    // New efficient count function that traverses the list only when needed
    int count() {
        int count = 0;
        Node *temp = head;
        while (temp != nullptr) {
            count++;
            temp = temp->next;
        }
        return count;
    }

    void middleNode() {
        Node *slow = head;
        Node *fast = head;

        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;
            fast = fast->next->next;
        }

        cout << slow->data << endl;
    }

    void deleteAtIndex(int pos) {
        Node *temp = head;
        for (int i = 1; i < pos; i++) {
            temp = temp->next;
        }
        for (int i = pos; i < count() - 1; i++) {
            // Use the dynamic count function
            temp->data = temp->next->data;
            temp = temp->next;
        }
        temp->next = nullptr;
    }

    void reverse() {
        Node* prev = nullptr;
        Node* curr = head;
        Node* next;

        while (curr != nullptr) {
            next = curr->next;
            curr->next = prev;
            prev = curr;
            curr = next;
        }

        head = prev;
    }
};

int main() {
    LinkedList list;
    list.insertAtHead(1);
    list.insertAtHead(2);
    list.insertAtHead(3);
    list.insertAtTail(0);
    list.insertAtTail(-1);
    list.insertAtTail(-2);
    list.insertAtTailRecursive(-20, list.head);
    list.display();
    cout << "Node count: " << list.count() << endl;  // Display count only when needed
    list.deleteAtIndex(4);
    list.display();
    cout << "Node count: " << list.count() << endl;  // Display count again after deletion
    list.reverse();
    list.display();
}

#include <iostream>
using namespace std;

struct Node
{
    int data;
    struct Node *prev;
    struct Node *next;
};

class CircularDoublyLinkedList
{
private:
    Node *head;

public:
    CircularDoublyLinkedList() : head(nullptr) {}

    void insertAtBeginning(int newData)
    {
        Node *newNode = new Node;
        newNode->data = newData;
        newNode->prev = nullptr;
        newNode->next = nullptr;

        if (head == nullptr)
        {
            head = newNode;
            newNode->next = newNode;
            newNode->prev = newNode;
        }
        else
        {
            newNode->next = head;
            newNode->prev = head->prev;
            head->prev->next = newNode;
            head->prev = newNode;
            head = newNode;
        }
    }

    void display()
    {
        if (head == nullptr)
        {
            cout << "Empty List";
            return;
        }
        Node *temp = head;
        do
        {
            cout << temp->data << ' ';
            temp = temp->next;
        } while (temp != head);
        cout << endl;
    }

    void deleteAtBeginning()
    {
        if (head == nullptr)
        {
            cout << "Unable to delete: List is empty";
            return;
        }

        Node *temp = head;

        if (head->next == head)
        {
            delete head;
            head = nullptr;
        }
        else
        {
            head->prev->next = head->next;
            head->next->prev = head->prev;
            head = head->next;
            delete temp;
        }
    }
};

int main()
{
    CircularDoublyLinkedList myList;

    myList.insertAtBeginning(23);
    myList.insertAtBeginning(2);
    myList.insertAtBeginning(8);

    cout << "List after insertion: ";
    myList.display();

    myList.deleteAtBeginning();

    cout << "List after deletion: ";
    myList.display();

    myList.deleteAtBeginning();

    cout << "List after deletion: ";
    myList.display();

    return 0;
}

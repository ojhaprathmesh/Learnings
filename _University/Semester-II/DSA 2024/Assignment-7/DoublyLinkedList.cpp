#include <iostream>
using namespace std;

struct Node
{
    int data;
    struct Node *prev;
    struct Node *next;
};

class DoublyLinkedList
{
private:
    Node *head;

public:
    DoublyLinkedList() : head(nullptr) {}

    void insertAtBeginning(int newData)
    {
        Node *newNode = new Node;
        newNode->data = newData;
        newNode->prev = nullptr;
        newNode->next = nullptr;

        if (head == nullptr)
        {
            head = newNode;
        }
        else
        {
            newNode->next = head;
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
        while (temp != nullptr)
        {
            cout << temp->data << ' ';
            temp = temp->next;
        }
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
        head = head->next;
        if (head != nullptr)
        {
            head->prev = nullptr;
        }
        delete temp;
    }
};

int main()
{
    DoublyLinkedList myList;

    myList.insertAtBeginning(5);
    myList.insertAtBeginning(10);
    myList.insertAtBeginning(15);

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

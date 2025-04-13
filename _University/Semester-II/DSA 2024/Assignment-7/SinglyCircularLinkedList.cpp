#include <iostream>
using namespace std;

struct Node
{
    int data;
    struct Node *next;
};

class SinglyCircularLinkedList
{
private:
    Node *head;

public:
    SinglyCircularLinkedList() : head(nullptr){};

    void insertAtBeginning(int newData)
    {
        Node *newNode = new Node;
        newNode->data = newData;
        if (head == nullptr)
        {
            newNode->next = newNode;
            head = newNode;
        }
        else
        {
            Node *temp = head;
            while (temp->next != head)
            {
                temp = temp->next;
            }
            temp->next = newNode;
            newNode->next = head;
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
            cout << "Unable to delete : List is empty";
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
            // Traverse to the last node
            Node *last = head;
            while (last->next != head)
            {
                last = last->next;
            }
            last->next = head->next;
            head = head->next;
            delete temp;
        }
    }
};

int main()
{
    SinglyCircularLinkedList myList;

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
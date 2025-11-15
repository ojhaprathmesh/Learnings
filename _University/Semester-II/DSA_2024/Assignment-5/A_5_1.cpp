#include <iostream>
using namespace std;

struct Node
{
    int data;
    struct Node *next;
};

class SinglyLinkedList
{
private:
    Node *head;

public:
    SinglyLinkedList() : head(nullptr){};

    void insertAtBeginning(int newData)
    {
        Node *newNode = new Node;
        newNode->data = newData;
        newNode->next = head;
        head = newNode;
    }

    void insertAtEnd(int newData)
    {
        Node *newNode = new Node;
        newNode->data = newData;
        newNode->next = nullptr;

        if (head == nullptr)
        {
            head = newNode;
            return;
        }

        else
        {
            Node *temp = head;
            while (temp->next != nullptr)
            {
                temp = temp->next;
            }
            temp->next = newNode;
        }
    }

    void insertAfterIndex(int index, int newData)
    {
        if (index < 0)
        {
            cout << "Invalid index. Index must be non-negative." << endl;
            return;
        }

        Node *newNode = new Node;
        newNode->data = newData;
        newNode->next = nullptr;

        Node *current = head;
        int currentIndex = 0;

        while (current != nullptr && currentIndex < index - 1)
        {
            current = current->next;
            currentIndex++;
            cout << currentIndex;
        }

        if (current == nullptr)
        {
            cout << "Index out of range. Insertion failed." << endl;
            delete newNode;
            return;
        }

        newNode->next = current->next;
        current->next = newNode;
    }

    void insertInSortedOrder(int newData)
    {
        Node *newNode = new Node;
        newNode->data = newData;
        newNode->next = nullptr;

        if (head == nullptr || head->data >= newData)
        {
            newNode->next = head;
            head = newNode;
            return;
        }

        Node *temp = head;
        while (temp->next != nullptr && temp->next->data < newData)
        {
            temp = temp->next;
        }
        newNode->next = temp->next;
        temp->next = newNode;
    }

    void display() const
    {
        Node *temp = head;

        cout << "Linked List: ";

        while (temp != nullptr)
        {
            cout << temp->data << ' ';
            temp = temp->next;
        }
        cout << endl;
    }

    void deleteFirstNode()
    {
        if (head == nullptr)
        {
            cout << "Unable to delete : List is empty";
            return;
        }

        Node *temp = head;
        head = head->next;
        delete temp;
    }

    void deleteLastNode()
    {
        if (head == nullptr)
        {
            cout << "Unable to delete : List is empty";
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

    void deleteNodeWithValue(int value)
    {
        Node *temp = head;
        Node *prev = nullptr;

        if (temp != nullptr && temp->data == value)
        {
            head = temp->next;
            delete temp;
            return;
        }

        while (temp != nullptr && temp->data != value)
        {
            prev = temp;
            temp = temp->next;
        }

        if (temp == nullptr)
        {
            cout << "Value not found in the list." << endl;
            return;
        }

        prev->next = temp->next;
        delete temp;
    }

    void reverseList()
    {
        Node *prev = nullptr;
        Node *current = head;
        Node *next = nullptr;

        while (current != nullptr)
        {
            next = current->next;
            current->next = prev;
            prev = current;
            current = next;
        }
        head = prev;
    }

    void shrinkList()
    {
        Node *current = head;

        if (current == nullptr || current->next == nullptr)
        {
            cout << "List is too short to shrink." << endl;
            return;
        }

        while (current != nullptr && current->next != nullptr)
        {
            current->next = current->next->next;
            current = current->next;
        }
    }

    void growList()
    {
        Node *current = head;

        while (current != nullptr)
        {
            Node *newNode = new Node;
            newNode->data = current->data;
            newNode->next = current->next;
            current->next = newNode;
            current = newNode->next;
        }
    }
};

int main()
{
    SinglyLinkedList myList;

    // Insert nodes at the beginning
    myList.insertAtBeginning(3);
    myList.insertAtBeginning(5);
    myList.insertAtBeginning(7);
    myList.insertAtBeginning(11);
    myList.display();

    // Insert nodes at the end
    myList.insertAtEnd(13);
    myList.insertAtEnd(17);
    myList.display();

    // Insert nodes in sorted order
    myList.insertInSortedOrder(15);
    myList.insertInSortedOrder(9);
    myList.display();

    // Delete the first node
    myList.deleteFirstNode();
    myList.display();

    // Delete the last node
    myList.deleteLastNode();
    myList.display();

    // Delete a particular node with value 5
    myList.deleteNodeWithValue(5);
    myList.display();

    // Reverse the list
    myList.reverseList();
    myList.display();

    // Shrink the list
    myList.shrinkList();
    myList.display();

    // Grow the list
    myList.growList();
    myList.display();

    return 0;
}
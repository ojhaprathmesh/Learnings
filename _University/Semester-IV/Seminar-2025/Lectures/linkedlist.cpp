#include <iostream>
using namespace std;

struct Node
{
    int data;
    Node *next;
    Node(int val)
    {
        data = val;
        next = nullptr;
    }
};

class LinkedList
{
public:
    Node *head;
    int nodeCount = 0;

    LinkedList()
    {
        head = nullptr;
    }

    void insertAtHead(int val)
    {
        Node *n = new Node(val);
        n->next = head;
        head = n;
        nodeCount++;
    }

    void insertAtTail(int val)
    {
        Node *n = new Node(val);
        if (head == nullptr)
        {
            head = n;
            return;
        }
        Node *temp = head;
        while (temp->next != nullptr)
        {
            temp = temp->next;
        }
        temp->next = n;
        nodeCount++;
    }

    void insertAtTailRecursive(int val, Node *curr)
    {
        if (curr == nullptr)
        {
            head = new Node(val);
            nodeCount++;
            return;
        }

        if (curr->next == nullptr)
        {
            curr->next = new Node(val);
            nodeCount++;
            return;
        }
        insertAtTailRecursive(val, curr->next);
    }

    void display()
    {
        Node *temp = head;
        while (temp != nullptr)
        {
            cout << '[' << temp->data << ']' << "->";
            temp = temp->next;
        }
        cout << "NULL" << endl;
    }

    void count()
    {
        cout << nodeCount << endl;
    }

    void middleNode()
    {
        // Node *temp = head;
        // if (nodeCount == 0) {
        //     cout << "Empty list" << endl;
        //     return;
        // }

        // int mid = nodeCount / 2;

        // for (int i = 0; i < mid; i++) {
        //     temp = temp->next;
        // }

        // if (nodeCount % 2 == 0) {
        //     cout << temp->data << endl;
        // } else {
        //     cout << temp->data << endl;
        // }

        Node *slow = head;
        Node *fast = head;

        while (fast != nullptr && fast->next->next != nullptr)
        {
            slow = slow->next;
            fast = fast->next->next;
        }

        cout << slow->data << endl;
    }

    void deleteAtIndex(int pos)
    {
        Node *temp = head;
        for (int i = 1; i < pos; i++)
        {
            temp = temp->next;
        }
        for (int i = pos; i < nodeCount; i++)
        {
            temp->data = temp->next->data;
            temp = temp->next;
        }
        temp->next = nullptr;
        nodeCount--;
    }
};

int main()
{
    LinkedList list;
    list.insertAtHead(1);
    list.insertAtHead(2);
    list.insertAtHead(3);
    list.insertAtTail(0);
    list.insertAtTail(-1);
    list.insertAtTail(-2);
    list.insertAtTailRecursive(-20, list.head);
    list.display();
    list.count();
    // list.middleNode();
    list.deleteAtIndex(4);
    list.display();
}

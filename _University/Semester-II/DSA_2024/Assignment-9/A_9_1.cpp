#include <iostream>
using namespace std;

class BinaryTreeArray
{
private:
    int *tree;
    int capacity;
    int size;

public:
    BinaryTreeArray(int capacity) : capacity(capacity)
    {
        tree = new int[capacity];
        size = 0;
        for (int i = 0; i < capacity; ++i)
        {
            tree[i] = -1; // Initializing tree with -1 (indicating empty)
        }
    }

    ~BinaryTreeArray()
    {
        delete[] tree;
    }

    void insert(int value)
    {
        if (size == capacity)
        {
            cout << "Tree is full. Cannot insert more elements.\n";
            return;
        }
        tree[size++] = value;
    }

    void remove(int value)
    {
        for (int i = 0; i < capacity; ++i)
        {
            if (tree[i] == value)
            {
                tree[i] = -1; // Mark as empty
                return;
            }
        }
        cout << "Element not found in the tree.\n";
    }

    void inorderTraversal(int index)
    {
        if (index < size)
        {
            inorderTraversal(index * 2 + 1); // Left child
            if (tree[index] != -1)
            {
                cout << tree[index] << " ";
            }
            inorderTraversal(index * 2 + 2); // Right child
        }
    }

    void preorderTraversal(int index)
    {
        if (index < size)
        {
            if (tree[index] != -1)
            {
                cout << tree[index] << " ";
            }
            preorderTraversal(index * 2 + 1); // Left child
            preorderTraversal(index * 2 + 2); // Right child
        }
    }

    void postorderTraversal(int index)
    {
        if (index < size)
        {
            postorderTraversal(index * 2 + 1); // Left child
            postorderTraversal(index * 2 + 2); // Right child
            if (tree[index] != -1)
            {
                cout << tree[index] << " ";
            }
        }
    }
};

int main()
{
    BinaryTreeArray tree(10);

    tree.insert(1);
    tree.insert(2);
    tree.insert(3);
    tree.insert(4);
    tree.insert(5);

    cout << "Inorder Traversal: ";
    tree.inorderTraversal(0);
    cout << endl;

    cout << "Preorder Traversal: ";
    tree.preorderTraversal(0);
    cout << endl;

    cout << "Postorder Traversal: ";
    tree.postorderTraversal(0);
    cout << endl;

    return 0;
}

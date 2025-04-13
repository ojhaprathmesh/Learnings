#include <iostream>
using namespace std;

struct Node
{
    int data;
    Node *left;
    Node *right;

    Node(int value) : data(value), left(nullptr), right(nullptr) {}
};

class BinarySearchTree
{
private:
    Node *root;

    Node *insertRec(Node *root, int value)
    {
        if (root == nullptr)
        {
            return new Node(value);
        }
        if (value < root->data)
        {
            root->left = insertRec(root->left, value);
        }
        else if (value > root->data)
        {
            root->right = insertRec(root->right, value);
        }
        return root;
    }

    Node *minValueNode(Node *node)
    {
        Node *current = node;
        while (current && current->left != nullptr)
        {
            current = current->left;
        }
        return current;
    }

    Node *deleteRec(Node *root, int value)
    {
        if (root == nullptr)
        {
            return root;
        }
        if (value < root->data)
        {
            root->left = deleteRec(root->left, value);
        }
        else if (value > root->data)
        {
            root->right = deleteRec(root->right, value);
        }
        else
        {
            if (root->left == nullptr)
            {
                Node *temp = root->right;
                delete root;
                return temp;
            }
            else if (root->right == nullptr)
            {
                Node *temp = root->left;
                delete root;
                return temp;
            }
            Node *temp = minValueNode(root->right);
            root->data = temp->data;
            root->right = deleteRec(root->right, temp->data);
        }
        return root;
    }

    void inorderRec(Node *root)
    {
        if (root != nullptr)
        {
            inorderRec(root->left);
            cout << root->data << " ";
            inorderRec(root->right);
        }
    }

    void preorderRec(Node *root)
    {
        if (root != nullptr)
        {
            cout << root->data << " ";
            preorderRec(root->left);
            preorderRec(root->right);
        }
    }

    void postorderRec(Node *root)
    {
        if (root != nullptr)
        {
            postorderRec(root->left);
            postorderRec(root->right);
            cout << root->data << " ";
        }
    }

    int countLeafNodesRec(Node *root)
    {
        if (root == nullptr)
        {
            return 0;
        }
        if (root->left == nullptr && root->right == nullptr)
        {
            return 1;
        }
        return countLeafNodesRec(root->left) + countLeafNodesRec(root->right);
    }

    int countInternalNodesRec(Node *root)
    {
        if (root == nullptr || (root->left == nullptr && root->right == nullptr))
        {
            return 0;
        }
        return 1 + countInternalNodesRec(root->left) + countInternalNodesRec(root->right);
    }

    Node *findSiblingRec(Node *root, int value)
    {
        if (root == nullptr)
        {
            return nullptr;
        }
        if ((root->left && root->left->data == value) || (root->right && root->right->data == value))
        {
            return root;
        }
        Node *leftSibling = findSiblingRec(root->left, value);
        if (leftSibling != nullptr)
        {
            return leftSibling;
        }
        return findSiblingRec(root->right, value);
    }

    int countChildrenRec(Node *root, int value)
    {
        Node *node = search(root, value);
        if (node == nullptr)
        {
            return -1;
        }
        int count = 0;
        if (node->left != nullptr)
        {
            count++;
        }
        if (node->right != nullptr)
        {
            count++;
        }
        return count;
    }

    Node *search(Node *root, int value)
    {
        if (root == nullptr || root->data == value)
        {
            return root;
        }
        if (value < root->data)
        {
            return search(root->left, value);
        }
        return search(root->right, value);
    }

    Node *inorderSuccessor(Node *root, int value)
    {
        Node *current = search(root, value);
        if (current == nullptr)
        {
            return nullptr;
        }
        if (current->right != nullptr)
        {
            return minValueNode(current->right);
        }
        Node *successor = nullptr;
        while (root != nullptr)
        {
            if (current->data < root->data)
            {
                successor = root;
                root = root->left;
            }
            else if (current->data > root->data)
            {
                root = root->right;
            }
            else
            {
                break;
            }
        }
        return successor;
    }

    int heightRec(Node *root)
    {
        if (root == nullptr)
        {
            return 0;
        }
        int leftHeight = heightRec(root->left);
        int rightHeight = heightRec(root->right);
        return max(leftHeight, rightHeight) + 1;
    }

public:
    BinarySearchTree() : root(nullptr) {}

    void insert(int value)
    {
        root = insertRec(root, value);
    }

    void remove(int value)
    {
        root = deleteRec(root, value);
    }

    void inorderTraversal()
    {
        inorderRec(root);
        cout << endl;
    }

    void preorderTraversal()
    {
        preorderRec(root);
        cout << endl;
    }

    void postorderTraversal()
    {
        postorderRec(root);
        cout << endl;
    }

    bool search(int value)
    {
        Node *node = search(root, value);
        return node != nullptr;
    }

    int countLeafNodes()
    {
        return countLeafNodesRec(root);
    }

    int countInternalNodes()
    {
        return countInternalNodesRec(root);
    }

    Node *findSibling(int value)
    {
        return findSiblingRec(root, value);
    }

    int countChildren(int value)
    {
        return countChildrenRec(root, value);
    }

    Node *inorderSuccessor(int value)
    {
        return inorderSuccessor(root, value);
    }

    int height()
    {
        return heightRec(root);
    }
};

int main()
{
    BinarySearchTree bst;

    bst.insert(50);
    bst.insert(30);
    bst.insert(70);
    bst.insert(20);
    bst.insert(40);
    bst.insert(60);
    bst.insert(80);

    cout << "Inorder Traversal: ";
    bst.inorderTraversal();

    cout << "Preorder Traversal: ";
    bst.preorderTraversal();

    cout << "Postorder Traversal: ";
    bst.postorderTraversal();

    cout << "Search for 40: " << (bst.search(40) ? "Found" : "Not found") << endl;
    cout << "Search for 100: " << (bst.search(100) ? "Found" : "Not found") << endl;

    cout << "Number of leaf nodes: " << bst.countLeafNodes() << endl;
    cout << "Number of internal nodes: " << bst.countInternalNodes() << endl;

    Node *sibling = bst.findSibling(20);
    cout << "Sibling of 20: " << (sibling != nullptr ? to_string(sibling->data) : "Not found") << endl;

    cout << "Number of children of 30: " << bst.countChildren(30) << endl;
    cout << "Number of children of 70: " << bst.countChildren(70) << endl;

    Node *successor = bst.inorderSuccessor(30);
    cout << "Inorder successor of 30: " << (successor != nullptr ? to_string(successor->data) : "Not found") << endl;

    cout << "Height of the tree: " << bst.height() << endl;

    return 0;
}

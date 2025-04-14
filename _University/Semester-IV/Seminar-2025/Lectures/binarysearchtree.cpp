#include <iostream>
using namespace std;

struct TreeNode {
    int data;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int val) {
        data = val;
        left = nullptr;
        right = nullptr;
    }
};

class BinarySearchTree {
    public:
    TreeNode* root;
    
    BinarySearchTree() {
        root = nullptr;
    }
    
    TreeNode* insert(TreeNode* root, int val) {
        if (root == nullptr) {
            return new TreeNode(val);
        }
        if (val < root->data) {
            root->left = insert(root->left, val);
        } else if (val > root->data) {
            root->right = insert(root->right, val);
        }
        return root;
    }    

    void insert(int val) {
        root = insert(root, val);
    }

    TreeNode* search(TreeNode* root, int val) {
        if (root == nullptr || root->data == val) {
            return root;
        }
        if (val < root->data) {
            return search(root->left, val);
        }
        return search(root->right, val);
    }

    void postOrderDisplay(TreeNode* root) {
        if (root == nullptr) {
            return;
        }
        postOrderDisplay(root->left);
        postOrderDisplay(root->right);
        cout << root->data << " ";
    }

    void preOrderDisplay(TreeNode* root) {
        if (root == nullptr) {
            return;
        }
        cout << root->data << " ";
        preOrderDisplay(root->left);
        preOrderDisplay(root->right);
    }

    void inOrderDisplay(TreeNode* root) {
        if (root == nullptr) {
            return;
        }
        preOrderDisplay(root->left);
        cout << root->data << " ";
        preOrderDisplay(root->right);
    }

    int length(TreeNode* root) {
        int count = 0;
        if (root == nullptr) {
            return 0;
        } else {
            count++;
        }
        count += length(root->left);
        count += length(root->right);
        return count;
    }

    int count(TreeNode* root) {
        if (root == nullptr) {
            return 0;
        }

        return 1 + count(root->left) + count(root->right);
    }

    int height(TreeNode* root) {
        if (root == nullptr) {
            return 0;
        }
        return 1 + max(height(root->left), height(root->right));
    }
};

int main() {
    BinarySearchTree tree = BinarySearchTree();

    tree.insert(10);
    tree.insert(5);
    tree.insert(15);
    tree.insert(3);
    tree.insert(7);
    tree.insert(12);

    tree.postOrderDisplay(tree.root);
    cout << endl;
    tree.preOrderDisplay(tree.root);
    cout << endl;
    tree.inOrderDisplay(tree.root);
    cout << endl;
    cout << "Count: " << tree.count(tree.root) << endl;
    cout << "Length: " << tree.length(tree.root) << endl;
    cout << "Height: " << tree.height(tree.root) << endl;
    return 0;
}
#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

struct Node {
    string key;
    int value;
    Node* next;
    Node(string k, int v) : key(k), value(v), next(nullptr) {}
};

class HashMap {
private:
    vector<Node*> table;
    int capacity;
    int size;
    const double LOAD_FACTOR_THRESHOLD = 0.75;
    const int P = 37;  // Small prime number for hash calculation
    const int M = 1e9 + 9;  // Large prime number for modulus

    int customHashFunction(const string& key) {
        long long hashValue = 0;
        long long power = 1;  // Stores p^i
        
        for (char c : key) {
            hashValue = (hashValue + (c * power) % M) % M;
            power = (power * P) % M;  // Update p^i for next character
        }
        
        return hashValue % capacity;
    }

    void rehash() {
        int oldCapacity = capacity;
        capacity *= 2;
        vector<Node*> oldTable = table;
        table.assign(capacity, nullptr);
        size = 0;

        for (int i = 0; i < oldCapacity; i++) {
            Node* current = oldTable[i];
            while (current) {
                insert(current->key, current->value);
                Node* temp = current;
                current = current->next;
                delete temp;
            }
        }
    }

public:
    HashMap(int initialCapacity = 10) : capacity(initialCapacity), size(0) {
        table.assign(capacity, nullptr);
    }

    void insert(string key, int value) {
        if ((double)size / capacity >= LOAD_FACTOR_THRESHOLD) {
            rehash();
        }

        int index = customHashFunction(key);
        Node* current = table[index];

        while (current) {
            if (current->key == key) {
                current->value = value;
                return;
            }
            current = current->next;
        }

        Node* newNode = new Node(key, value);
        newNode->next = table[index];
        table[index] = newNode;
        size++;
    }

    int get(string key) {
        int index = customHashFunction(key);
        Node* current = table[index];

        while (current) {
            if (current->key == key) return current->value;
            current = current->next;
        }

        return -1;
    }

    void remove(string key) {
        int index = customHashFunction(key);
        Node* current = table[index];
        Node* prev = nullptr;

        while (current) {
            if (current->key == key) {
                if (prev) prev->next = current->next;
                else table[index] = current->next;
                delete current;
                size--;
                return;
            }
            prev = current;
            current = current->next;
        }
    }

    void display() {
        for (int i = 0; i < capacity; i++) {
            cout << "Bucket " << i << ": ";
            Node* current = table[i];
            while (current) {
                cout << "(" << current->key << ":" << current->value << ") -> ";
                current = current->next;
            }
            cout << "NULL" << endl;
        }
    }
};

int main() {
    HashMap map;
    map.insert("apple", 100);
    map.insert("banana", 200);
    map.insert("grape", 300);
    map.insert("cherry", 250);
    map.insert("mango", 150);
    map.insert("orange", 350);

    cout << "Value for key 'banana': " << map.get("banana") << endl;
    cout << "Value for key 'cherry': " << map.get("cherry") << endl;

    map.remove("banana");
    cout << "After deleting key 'banana':" << endl;
    map.display();

    return 0;
}

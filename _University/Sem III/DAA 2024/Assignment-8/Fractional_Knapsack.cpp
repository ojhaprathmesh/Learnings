#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct Item {
    int weight, value;
};

// Function to compare items by value/weight ratio
bool cmp(Item a, Item b) {
    return (double)a.value / a.weight > (double)b.value / b.weight;
}

double fractionalKnapsack(int W, vector<Item>& items) {
    sort(items.begin(), items.end(), cmp);

    int curWeight = 0;
    double finalValue = 0.0;

    for (auto& item : items) {
        if (curWeight + item.weight <= W) {
            curWeight += item.weight;
            finalValue += item.value;
        } else {
            finalValue += item.value * (double)(W - curWeight) / item.weight;
            break;
        }
    }

    return finalValue;
}

int main() {
    vector<Item> items = {{10, 60}, {20, 100}, {30, 120}};
    int W = 50;

    cout << "Maximum value in Knapsack = " << fractionalKnapsack(W, items);
}

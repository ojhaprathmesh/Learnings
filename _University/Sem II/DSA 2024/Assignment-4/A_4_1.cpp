#include <iostream>
using namespace std;

// Linear search algorithm
int linearSearch(int arr[], int size, int target) {
    for (int i = 0; i < size; ++i) {
        if (arr[i] == target) {
            return i; // Return the index of the target if found
        }
    }
    return -1; // Return -1 if the target is not found
}

int main() {
    int arr[] = {4, 2, 7, 1, 9, 5};
    int size = sizeof(arr) / sizeof(arr[0]); // Calculate the size of the array
    int target = 7;

    int index = linearSearch(arr, size, target);
    if (index != -1) {
        cout << "Element found at index " << index << ".\n";
    } else {
        cout << "Element not found in the array.\n";
    }

    return 0;
}

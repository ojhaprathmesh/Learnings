#include <iostream>
using namespace std;

// Iterative Binary search algorithm
int binarySearch(int arr[], int size, int target) {
    int left = 0;
    int right = size - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            return mid; // Return the index of the target if found
        } else if (arr[mid] < target) {
            left = mid + 1; // Search the right half of the array
        } else {
            right = mid - 1; // Search the left half of the array
        }
    }

    return -1; // Return -1 if the target is not found
}

int main() {
    int arr[] = {1, 3, 5, 7, 9, 11, 13, 15};
    int size = sizeof(arr) / sizeof(arr[0]); // Calculate the size of the array
    int target = 11;

    int index = binarySearch(arr, size, target);
    if (index != -1) {
        cout << "Element found at index " << index << ".\n";
    } else {
        cout << "Element not found in the array.\n";
    }

    return 0;
}

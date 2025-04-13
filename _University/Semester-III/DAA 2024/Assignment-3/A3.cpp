#include <iostream>
#include <vector>
using namespace std;

// Binary Search Function
int binarySearch(const vector<int>& arr, int target) {
    int low = 0;
    int high = arr.size() - 1;

    while (low <= high) {
        int mid = low + (high - low) / 2;

        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }

    return -1;  // Target not found
}

// Merge Function for Merge Sort
void merge(vector<int>& arr, int left, int mid, int right) {
    int size1 = mid - left + 1;
    int size2 = right - mid;

    vector<int> leftArr(size1), rightArr(size2);

    for (int i = 0; i < size1; ++i) {
        leftArr[i] = arr[left + i];
    }
    for (int j = 0; j < size2; ++j) {
        rightArr[j] = arr[mid + 1 + j];
    }

    int i = 0, j = 0, k = left;
    while (i < size1 && j < size2) {
        if (leftArr[i] <= rightArr[j]) {
            arr[k++] = leftArr[i++];
        } else {
            arr[k++] = rightArr[j++];
        }
    }

    while (i < size1) {
        arr[k++] = leftArr[i++];
    }

    while (j < size2) {
        arr[k++] = rightArr[j++];
    }
}

// Merge Sort Function
void mergeSort(vector<int>& arr, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

int main() {
    vector<int> arr = {12, 11, 13, 5, 6, 7};
    int target = 7;

    // Sort the array using merge sort
    mergeSort(arr, 0, arr.size() - 1);

    // Display the sorted array
    cout << "Sorted array: ";
    for (int num : arr) {
        cout << num << " ";
    }
    cout << endl;

    // Perform binary search on the sorted array
    int index = binarySearch(arr, target);

    if (index != -1) {
        cout << target << " found at index: " << index << endl;
    } else {
        cout << "Element not found in the array." << endl;
    }

    return 0;
}

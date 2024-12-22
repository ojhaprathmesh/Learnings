#include <iostream>
using namespace std;

// Function to swap two elements
void swap(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

// i. Bubble Sort
void bubbleSort(int arr[], int size) {
    for (int i = 0; i < size - 1; ++i) {
        for (int j = 0; j < size - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }
    }
}

// ii. Selection Sort
void selectionSort(int arr[], int size) {
    for (int i = 0; i < size - 1; ++i) {
        int minIndex = i;
        for (int j = i + 1; j < size; ++j) {
            if (arr[j] < arr[minIndex]) {
                minIndex = j;
            }
        }
        if (minIndex != i) {
            swap(arr[i], arr[minIndex]);
        }
    }
}

// iii. Insertion Sort
void insertionSort(int arr[], int size) {
    for (int i = 1; i < size; ++i) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

// iv. Merge Sort
void merge(int arr[], int left, int mid, int right) {
    int size1 = mid - left + 1;
    int size2 = right - mid;

    int leftArr[size1], rightArr[size2];

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

void mergeSort(int arr[], int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

// v. Quick Sort
int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; ++j) {
        if (arr[j] < pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

// Function to display an array
void displayArray(int arr[], int size) {
    for (int i = 0; i < size; ++i) {
        cout << arr[i] << " ";
    }
    cout << endl;
}   

int main() {
    int arr[] = {5, 3, 8, 1, 6, 2, 7, 4};
    int size = sizeof(arr) / sizeof(arr[0]);

    cout << "Original array: ";
    displayArray(arr, size);

    // // Bubble Sort
    // bubbleSort(arr, size);
    // cout << "Bubble sorted array: ";
    // displayArray(arr, size);

    // // Selection Sort
    // int arr2[] = {5, 3, 8, 1, 6, 2, 7, 4};
    // selectionSort(arr2, size);
    // cout << "Selection sorted array: ";
    // displayArray(arr2, size);

    // Insertion Sort
    int arr3[] = {5, 3, 8, 1, 6, 2, 7, 4};
    insertionSort(arr3, size);
    cout << "Insertion sorted array: ";
    displayArray(arr3, size);

    // // Merge Sort
    // int arr4[] = {5, 3, 8, 1, 6, 2, 7, 4};
    // mergeSort(arr4, 0, size - 1);
    // cout << "Merge sorted array: ";
    // displayArray(arr4, size);

    // Quick Sort
    int arr5[] = {5, 3, 8, 1, 6, 2, 7, 4};
    quickSort(arr5, 0, size - 1);
    cout << "Quick sorted array: ";
    displayArray(arr5, size);

    return 0;
}

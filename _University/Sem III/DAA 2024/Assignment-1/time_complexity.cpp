#include <iostream>
#include <vector>
#include <ctime>
using namespace std;

// Function to swap two elements
void swap(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

// i. Bubble Sort
int bubbleSort(vector<int>& arr) {
    int comparisons = 0;
    for (size_t i = 0; i < arr.size() - 1; ++i) {
        for (size_t j = 0; j < arr.size() - i - 1; ++j) {
            comparisons++;
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }
    }
    return comparisons;
}

// ii. Selection Sort
int selectionSort(vector<int>& arr) {
    int comparisons = 0;
    for (size_t i = 0; i < arr.size() - 1; ++i) {
        size_t minIndex = i;
        for (size_t j = i + 1; j < arr.size(); ++j) {
            comparisons++;
            if (arr[j] < arr[minIndex]) {
                minIndex = j;
            }
        }
        if (minIndex != i) {
            swap(arr[i], arr[minIndex]);
        }
    }
    return comparisons;
}

// iii. Insertion Sort
int insertionSort(vector<int>& arr) {
    int comparisons = 0;
    for (size_t i = 1; i < arr.size(); ++i) {
        int key = arr[i];
        size_t j = i - 1;
        while (j >= 0 && arr[j] > key) {
            comparisons++;
            arr[j + 1] = arr[j];
            j--;
        }
        comparisons++;
        arr[j + 1] = key;
    }
    return comparisons;
}

// iv. Merge Sort
int merge(vector<int>& arr, int left, int mid, int right) {
    int comparisons = 0;
    vector<int> leftArr(arr.begin() + left, arr.begin() + mid + 1);
    vector<int> rightArr(arr.begin() + mid + 1, arr.begin() + right + 1);

    size_t i = 0, j = 0, k = left;
    while (i < leftArr.size() && j < rightArr.size()) {
        comparisons++;
        if (leftArr[i] <= rightArr[j]) {
            arr[k++] = leftArr[i++];
        } else {
            arr[k++] = rightArr[j++];
        }
    }

    while (i < leftArr.size()) {
        arr[k++] = leftArr[i++];
    }
    while (j < rightArr.size()) {
        arr[k++] = rightArr[j++];
    }

    return comparisons;
}

int mergeSort(vector<int>& arr, int left, int right) {
    int comparisons = 0;
    if (left < right) {
        int mid = left + (right - left) / 2;
        comparisons += mergeSort(arr, left, mid);
        comparisons += mergeSort(arr, mid + 1, right);
        comparisons += merge(arr, left, mid, right);
    }
    return comparisons;
}

// v. Quick Sort
int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    int comparisons = 0;

    for (int j = low; j < high; ++j) {
        comparisons++;
        if (arr[j] < pivot) {
            swap(arr[++i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

int quickSort(vector<int>& arr, int low, int high) {
    int comparisons = 0;
    if (low < high) {
        int pi = partition(arr, low, high);
        comparisons += quickSort(arr, low, pi - 1);
        comparisons += quickSort(arr, pi + 1, high);
    }
    return comparisons;
}

// vi. Heap Sort
void heapify(vector<int>& arr, int size, int i, int& comparisons) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    comparisons++;
    if (left < size && arr[left] > arr[largest]) {
        largest = left;
    }

    comparisons++;
    if (right < size && arr[right] > arr[largest]) {
        largest = right;
    }

    if (largest != i) {
        swap(arr[i], arr[largest]);
        heapify(arr, size, largest, comparisons);
    }
}

int heapSort(vector<int>& arr) {
    int comparisons = 0;
    for (int i = arr.size() / 2 - 1; i >= 0; --i) {
        heapify(arr, arr.size(), i, comparisons);
    }

    for (int i = arr.size() - 1; i > 0; --i) {
        swap(arr[0], arr[i]);
        heapify(arr, i, 0, comparisons);
    }

    return comparisons;
}

// Function to generate a random array
void generateRandomArray(vector<int>& arr) {
    for (size_t i = 0; i < arr.size(); ++i) {
        arr[i] = rand() % 100; // Random numbers between 0 and 99
    }
}

// Function to display an array
void displayArray(const vector<int>& arr) {
    for (int num : arr) {
        cout << num << " ";
    }
    cout << endl;
}

int main() {
    srand(time(0)); // Seed the random number generator with current time
    const int size = 20;
    const int trials = 10;

    vector<int> originalArray(size);
    vector<int> bubbleArray(size), selectionArray(size), insertionArray(size), mergeArray(size), quickArray(size), heapArray(size);

    cout << "Trial\tBubbleSort\tSelectionSort\tInsertionSort\tMergeSort\tQuickSort\tHeapSort\n";

    for (int t = 0; t < trials; ++t) {
        generateRandomArray(originalArray);

        // Copy the original array to other arrays
        bubbleArray = originalArray;
        selectionArray = originalArray;
        insertionArray = originalArray;
        mergeArray = originalArray;
        quickArray = originalArray;
        heapArray = originalArray;

        // Sorting and counting comparisons
        cout << t + 1 << "\t";
        cout << bubbleSort(bubbleArray) << "\t\t";
        cout << selectionSort(selectionArray) << "\t\t";
        cout << insertionSort(insertionArray) << "\t\t";
        cout << mergeSort(mergeArray, 0, size - 1) << "\t\t";
        cout << quickSort(quickArray, 0, size - 1) << "\t\t";
        cout << heapSort(heapArray) << "\n";
    }

    return 0;
}

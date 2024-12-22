#include <iostream>
using namespace std;

void display(int array[], int size) {
    for (int i = 0; i < size; i++) {
        cout << array[i] << " ";
    }
    cout << endl;
}

int partition(int array[], int first, int last) {
    int pivot = array[last]; // Choosing the last element as the pivot
    int i = first - 1; // Index of smaller element

    for (int j = first; j < last; j++) {
        if (array[j] < pivot) {
            i++;
            swap(array[i], array[j]);
            cout << array[i] << array[j];
        }
    }
    swap(array[i + 1], array[last]);
    return i + 1;
}

void quick_sort(int array[], int first, int last) {
    if (first < last) {
        int index = partition(array, first, last);

        quick_sort(array, first, index - 1);
        quick_sort(array, index + 1, last);
    }
}

int main() {
    int arr[] = {7, 1, 3, 2, 5, 6, 2, 13, 43, 65, 84, 29, 62, 34, 23};
    int size = sizeof(arr) / sizeof(arr[0]);

    cout << "Original array: "; display(arr, size);

    quick_sort(arr, 0, size - 1);

    cout << "Sorted array: "; display(arr, size);

    return 0;
}

#include <iostream>
using namespace std;

int main() {
    // Define a 1D array
    const int size = 5;
    int array[size];

    // Insert data into the array
    cout << "Enter " << size << " integers:\n";
    for (int i = 0; i < size; ++i) {
        cin >> array[i];
    }

    // Traverse the array
    cout << "Array elements: ";
    for (int i = 0; i < size; ++i) {
        cout << array[i] << " ";
    }
    cout << "\n";

    // Access the array elements using pointers
    int* ptr = array;
    cout << "Array elements accessed using pointers: ";
    for (int i = 0; i < size; ++i) {
        cout << *(ptr + i) << " ";
    }
    cout << "\n";

    // Modify the content of i-th index of the array using the pointer
    int index;
    cout << "Enter the index to modify (0-" << size - 1 << "): ";
    cin >> index;
    if (index >= 0 && index < size) {
        cout << "Enter the new value: ";
        cin >> *(ptr + index);
        cout << "Array after modification: ";
        for (int i = 0; i < size; ++i) {
            cout << array[i] << " ";
        }
        cout << "\n";
    } else {
        cout << "Invalid index.\n";
    }

    // Verify that the elements of the array are stored in contiguous memory locations
    cout << "Memory addresses of array elements:\n";
    for (int i = 0; i < size; ++i) {
        cout << "Element " << i << ": " << &array[i] << "\n";
    }

    return 0;
}

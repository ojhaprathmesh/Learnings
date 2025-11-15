#include <iostream>
using namespace std;

void display(int array[], int size)
{
    for (int i = 0; i < size; i++)
    {
        cout << array[i] << ' ';
    }
    cout << endl;
}

void insertion_sort(int array[], int size) // Third Sort
{
    for (int i = 1; i < size; i++)
    {
        int value = array[i];
        int j = i;
        while (j > 0 && array[j - 1] > value)
        {
            array[j] = array[j - 1];
            j = j - 1;
        }
        array[j] = value;
    }
}

int main()
{
    int arr[] = {7, 1, 3, 2, 5, 6, 2, 13, 43, 65, 84, 29, 62, 34, 23};
    int size = sizeof(arr) / sizeof(arr[0]);

    cout << "Original array: ";
    display(arr, size);

    insertion_sort(arr, size);

    cout << "Sorted array: ";
    display(arr, size);

    return 0;
}

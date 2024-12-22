#include <iostream>
using namespace std;

void bubble_sort(int array[], int size) // First Sort
{
    for (int i = 0; i < size - 1; i++)
    {
        for (int j = 0; j < (size - 1) - i; j++)
        {
            if (array[j] > array[j + 1])
            {
                swap(array[j], array[j + 1]);
            }
        }
    }
}

void display(int array[], int size)
{
    for (int i = 0; i < size; i++)
    {
        cout << array[i] << ' ';
    }
    cout << endl;
}

int main()
{
    int arr[] = {7, 1, 3, 2, 5, 6, 2, 13, 43, 65, 84, 29, 62, 34, 23};
    int size = sizeof(arr) / sizeof(arr[0]);

    cout << "Original array: ";
    display(arr, size);

    bubble_sort(arr, size);

    cout << "Sorted array: ";
    display(arr, size);

    return 0;
}

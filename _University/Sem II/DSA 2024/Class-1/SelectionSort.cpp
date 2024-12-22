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

void selection_sort(int array[], int size) // Second Sort
{
    for (int i = 0; i < size - 1; i++) // 12 3 5 9 10
    {
        int min = i;
        for (int j = i + 1; j < size; j++)
        {
            if (array[j] < array[min])
            {
                min = j;
            }
        }
        if (min != i)
        {
            swap(array[i], array[min]);
        }
    }
}

int main()
{
    int arr[] = {7, 1, 3, 2, 5, 6, 2, 13, 43, 65, 84, 29, 62, 34, 23};
    int size = sizeof(arr) / sizeof(arr[0]);

    cout << "Original array: ";
    display(arr, size);

    selection_sort(arr, size);

    cout << "Sorted array: ";
    display(arr, size);

    return 0;
}

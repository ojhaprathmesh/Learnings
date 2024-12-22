#include <bits/stdc++.h>
using namespace std;

void display(int array[], int size)
{
    for (int i = 0; i < size; i++)
    {
        cout << array[i] << ' ';
    }
    cout << endl;
}

void merge(int array[], int left, int mid, int right)
{
    int sizeA = mid - left + 1;
    int sizeB = right - mid;

    int *leftArray = new int[sizeA];
    int *rightArray = new int[sizeB];

    copy(array + left, array + mid + 1, leftArray);
    copy(array + mid + 1, array + right + 1, rightArray);

    int i = 0, j = 0, k = left;

    // Merge the two subarrays into the original array
    while (i < sizeA && j < sizeB)
    {
        if (leftArray[i] <= rightArray[j])
        {
            array[k] = leftArray[i];
            i++;
        }
        else
        {
            array[k] = rightArray[j];
            j++;
        }
        k++;
    }

    // Copy remaining elements of leftArray, if any
    while (i < sizeA)
    {
        array[k] = leftArray[i];
        i++;
        k++;
    }

    // Copy remaining elements of rightArray, if any
    while (j < sizeB)
    {
        array[k] = rightArray[j];
        j++;
        k++;
    }

    // Free memory
    delete[] leftArray;
    delete[] rightArray;
}

void merge_sort(int array[], int left, int right)
{
    if (left < right)
    {
        int mid = left + (right - left) / 2;
        merge_sort(array, left, mid);
        merge_sort(array, mid + 1, right);
        merge(array, left, mid, right);
    }
}

int main()
{
    int arr[] = {7, 1, 3, 2, 5, 6, 2, 13, 43, 65, 84, 29, 62, 34, 23};
    int size = sizeof(arr) / sizeof(arr[0]);

    cout << "Original array: ";
    display(arr, size);

    merge_sort(arr, 0, size - 1);

    cout << "Sorted array: ";
    display(arr, size);

    return 0;
}

#include <iostream>
using namespace std;

int* arrayMinMax(const int given[], int size) {
    if (size <= 0)
        return nullptr;

    int min = given[0], max = given[0];

    for (int i = 1; i < size; ++i) {
        if (given[i] < min) min = given[i];
        if (given[i] > max) max = given[i];
    }

    return new int[2]{min, max}; // Return dynamically allocated array
}

int* arrayMinMaxRec(const int given[], int low, int high) {
    if (low == high) {
        return new int[2]{given[low], given[low]}; // Single element
    }

    if (high == low + 1) {
        return new int[2]{min(given[low], given[high]), max(given[low], given[high])}; // Two elements
    }

    int mid = (low + high) / 2;

    int* leftMinMax = arrayMinMaxRec(given, low, mid);
    int* rightMinMax = arrayMinMaxRec(given, mid + 1, high);

    int* result = new int[2];
    result[0] = min(leftMinMax[0], rightMinMax[0]); // Min
    result[1] = max(leftMinMax[1], rightMinMax[1]); // Max

    delete[] leftMinMax;
    delete[] rightMinMax;

    return result;
}

int main() {
    int input[] = {11, 92, 13, -4, 52};
    int size = sizeof(input) / sizeof(input[0]);

    int* minMax = arrayMinMaxRec(input, 0, size - 1);
    
    if (minMax) {
        cout << "Min: " << minMax[0] << endl;
        cout << "Max: " << minMax[1] << endl;
        delete[] minMax; // Free the allocated memory
    }

    return 0;
}

#include <iostream>
using namespace std;

// Function to define a 1D array with remaining space
void define1DArray(int* &array, int size) {
    array = new int[size];
}

// Function to insert an element into the 1D array
void insertElement(int* array, int& size, int element) {
    array[size] = element;
    size++;
}

// Function to delete an element from the 1D array
void deleteElement(int* array, int& size, int index) {
    if (index >= 0 && index < size) {
        for (int i = index; i < size - 1; i++) {
            array[i] = array[i + 1];
        }
        size--;
    }
}

// Function to define a 2D array and store data
void define2DArray(int** &array, int rows, int cols) {
    array = new int*[rows];
    for (int i = 0; i < rows; i++) {
        array[i] = new int[cols];
    }
}

// Function to traverse the 2D array and count non-zero elements
int countNonZeroElements(int** array, int rows, int cols) {
    int count = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (array[i][j] != 0) {
                count++;
            }
        }
    }
    return count;
}

// Function to validate storage order of the 2D array
bool validateStorageOrder(int** array, int rows, int cols) {
    bool rowMajor = true;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (array[i][j] != i * cols + j) {
                rowMajor = false;
                break;
            }
        }
    }
    return rowMajor;
}

// Function to add two matrices
void addMatrices(int** matrix1, int** matrix2, int** &result, int rows, int cols) {
    result = new int*[rows];
    for (int i = 0; i < rows; i++) {
        result[i] = new int[cols];
        for (int j = 0; j < cols; j++) {
            result[i][j] = matrix1[i][j] + matrix2[i][j];
        }
    }
}

// Function to multiply two matrices
void multiplyMatrices(int** matrix1, int** matrix2, int** &result, int rows1, int cols1, int cols2) {
    result = new int*[rows1];
    for (int i = 0; i < rows1; i++) {
        result[i] = new int[cols2];
        for (int j = 0; j < cols2; j++) {
            result[i][j] = 0;
            for (int k = 0; k < cols1; k++) {
                result[i][j] += matrix1[i][k] * matrix2[k][j];
            }
        }
    }
}

// Function to transpose a matrix
void transposeMatrix(int** matrix, int rows, int cols, int** &result) {
    result = new int*[cols];
    for (int i = 0; i < cols; i++) {
        result[i] = new int[rows];
        for (int j = 0; j < rows; j++) {
            result[i][j] = matrix[j][i];
        }
    }
}

// Function to check if a matrix is sparse and represent it efficiently
void checkAndRepresentSparseMatrix(int** matrix, int rows, int cols) {
    int countNonZero = countNonZeroElements(matrix, rows, cols);
    if (countNonZero <= (rows * cols) / 2) {
        cout << "The matrix is sparse.\n";
        cout << "Sparse matrix representation:\n";
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                cout << matrix[i][j] << " ";
            }
            cout << endl;
        }
    } else {
        cout << "The matrix is not sparse.\n";
    }
}

// Function to print a 2D matrix
void printMatrix(int** matrix, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            cout << matrix[i][j] << " ";
        }
        cout << endl;
    }
}

int main() {
    // Test the functions
    int* array;
    int arraySize = 0;

    define1DArray(array, 10);
    insertElement(array, arraySize, 5);
    insertElement(array, arraySize, 10);
    insertElement(array, arraySize, 15);
    deleteElement(array, arraySize, 1);

    int** matrix;
    define2DArray(matrix, 3, 3);
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            matrix[i][j] = i * 3 + j;
        }
    }

    cout << "Non-zero elements: " << countNonZeroElements(matrix, 3, 3) << endl;
    cout << "Storage order: " << (validateStorageOrder(matrix, 3, 3) ? "Row-major" : "Column-major") << endl;

    cout << "Matrix:\n";
    printMatrix(matrix, 3, 3);

    int** resultMatrix;
    addMatrices(matrix, matrix, resultMatrix, 3, 3);

    int** resultMatrix2;
    multiplyMatrices(matrix, matrix, resultMatrix2, 3, 3, 3);

    int** transposedMatrix;
    transposeMatrix(matrix, 3, 3, transposedMatrix);

    checkAndRepresentSparseMatrix(matrix, 3, 3);

    return 0;
}

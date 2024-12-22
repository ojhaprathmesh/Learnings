#include <iostream>
#include <vector>
using namespace std;

typedef vector<vector<int>> Matrix;

// Function to add two matrices
Matrix addMatrices(const Matrix &a, const Matrix &b) {
    int n = a.size();
    Matrix result(n, vector<int>(n));
    for (int i = 0; i < n; ++i) 
        for (int j = 0; j < n; ++j) 
            result[i][j] = a[i][j] + b[i][j];
    return result;
}

// Function to subtract two matrices
Matrix subMatrices(const Matrix &a, const Matrix &b) {
    int n = a.size();
    Matrix result(n, vector<int>(n));
    for (int i = 0; i < n; ++i) 
        for (int j = 0; j < n; ++j) 
            result[i][j] = a[i][j] - b[i][j];
    return result;
}

// Strassen's matrix multiplication
Matrix strassenMultiply(const Matrix &a, const Matrix &b) {
    int n = a.size();
    if (n == 1) {
        return {{a[0][0] * b[0][0]}};
    }

    int mid = n / 2;

    // Divide matrices into submatrices
    Matrix a11(mid, vector<int>(mid)), a12(mid, vector<int>(mid)),
           a21(mid, vector<int>(mid)), a22(mid, vector<int>(mid)),
           b11(mid, vector<int>(mid)), b12(mid, vector<int>(mid)),
           b21(mid, vector<int>(mid)), b22(mid, vector<int>(mid));

    for (int i = 0; i < mid; ++i) {
        for (int j = 0; j < mid; ++j) {
            a11[i][j] = a[i][j]; a12[i][j] = a[i][j + mid];
            a21[i][j] = a[i + mid][j]; a22[i][j] = a[i + mid][j + mid];
            b11[i][j] = b[i][j]; b12[i][j] = b[i][j + mid];
            b21[i][j] = b[i + mid][j]; b22[i][j] = b[i + mid][j + mid];
        }
    }

    // Calculate intermediate matrices
    Matrix m1 = strassenMultiply(addMatrices(a11, a22), addMatrices(b11, b22));
    Matrix m2 = strassenMultiply(addMatrices(a21, a22), b11);
    Matrix m3 = strassenMultiply(a11, subMatrices(b12, b22));
    Matrix m4 = strassenMultiply(a22, subMatrices(b21, b11));
    Matrix m5 = strassenMultiply(addMatrices(a11, a12), b22);
    Matrix m6 = strassenMultiply(subMatrices(a21, a11), addMatrices(b11, b12));
    Matrix m7 = strassenMultiply(subMatrices(a12, a22), addMatrices(b21, b22));

    // Combine results
    Matrix c11 = addMatrices(subMatrices(addMatrices(m1, m4), m5), m7);
    Matrix c12 = addMatrices(m3, m5);
    Matrix c21 = addMatrices(m2, m4);
    Matrix c22 = addMatrices(subMatrices(addMatrices(m1, m3), m2), m6);

    // Combine submatrices into the final result
    Matrix result(n, vector<int>(n));
    for (int i = 0; i < mid; ++i) {
        for (int j = 0; j < mid; ++j) {
            result[i][j] = c11[i][j]; 
            result[i][j + mid] = c12[i][j];
            result[i + mid][j] = c21[i][j];
            result[i + mid][j + mid] = c22[i][j];
        }
    }

    return result;
}

// Function to input a matrix
Matrix inputMatrix(int n) {
    Matrix matrix(n, vector<int>(n));
    cout << "Enter the elements of the matrix:" << endl;
    for (int i = 0; i < n; ++i) 
        for (int j = 0; j < n; ++j) 
            cin >> matrix[i][j];
    return matrix;
}

// Function to print a matrix
void printMatrix(const Matrix &matrix) {
    for (const auto& row : matrix) {
        for (int val : row) cout << val << " ";
        cout << endl;
    }
}

int main() {
    // Initialize matrices A and B as 2x2 matrices
    Matrix a = {{1, 2}, {3, 4}};  // Example matrix A
    Matrix b = {{5, 6}, {7, 8}};  // Example matrix B

    // Perform Strassen's multiplication
    Matrix result = strassenMultiply(a, b);

    // Display the result
    cout << "Strassen's algorithm result:" << endl;
    printMatrix(result);

    return 0;
}

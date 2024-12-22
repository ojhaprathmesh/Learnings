package com.company.practice;

import java.util.Scanner;

class Matrix {
    private final int[][] data;
    private final int size;

    public Matrix(int n) {
        this.size = n;
        this.data = new int[n][n];
    }

    public void read(Scanner scanner) {
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                System.out.printf("Enter element[%d][%d]: ", i, j);
                data[i][j] = scanner.nextInt();
            }
        }
        display();
    }

    public void transpose() {
        for (int i = 0; i < size; i++) {
            for (int j = i + 1; j < size; j++) {
                int temp = data[i][j];
                data[i][j] = data[j][i];
                data[j][i] = temp;
            }
        }
    }

    public void display() {
        System.out.println();
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                System.out.printf("%d ", data[i][j]);
            }
            System.out.println();
        }
    }
}

public class MatrixTranspose {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);

        System.out.print("Enter the length of square matrix: ");
        byte n = scan.nextByte();

        Matrix matrix = new Matrix(n);
        matrix.read(scan);
        matrix.transpose();
        matrix.display();

        scan.close();
    }
}

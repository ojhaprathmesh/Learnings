package com.company;

import java.util.Scanner;

public class _2D_Array_ {
    int[][] arr;

    public _2D_Array_(int rows, int cols) {
        arr = new int[rows][cols];
    }

    public static void main(String[] args) {
        _2D_Array_ arr1 = new _2D_Array_(4, 5);

        int[][] arr2 = new int[3][];
        arr2[0] = new int[2];
        arr2[1] = new int[5];
        arr2[2] = new int[7];

        Scanner scanner = new Scanner(System.in);

        for (int i = 0; i < arr2.length; i++) {
            for (int j = 0; j < arr2[i].length; j++) {
                System.out.printf("Enter array[%d][%d]:", i, j);
                arr2[i][j] = scanner.nextInt();
            }
        }
        scanner.close();

        for (int i = 0; i < arr2.length; i++) {
            for (int j = 0; j < arr2[i].length; j++) {
                System.out.printf("%d ", arr2[i][j]);
            }
            System.out.println();
        }
    }
}

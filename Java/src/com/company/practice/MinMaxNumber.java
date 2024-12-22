package com.company.practice;

public class MinMaxNumber {
    public static void main(String[] args) {
        int[] ar = {43, 12, 32, 11, 3, 2, -1, 49};
        int smallest = ar[0];
        int largest = ar[0];
        for (int i = 0; i < ar.length; i++) {
            if (ar[i] < smallest) {
                smallest = ar[i];
            }
            if (ar[i] > largest) {
                largest = ar[i];
            }
        }
        System.out.printf("Smallest: %d and Largest: %d", smallest, largest);
    }
}

package com.company.practice;

import java.util.Scanner;

public class SumOfMultiples {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a value of n: ");
        int n = scanner.nextInt();
        int sum = 0;
        for (int threes = n / 3, fives = n / 5; threes > 0 || fives > 0; threes--, fives--) {
            if (threes > 0) {
                sum += threes * 3;
            }
            if (fives > 0) {
                sum += fives * 5;
            }
        }

        System.out.printf("Sum of multiples of three and five up to %d = %d", n, sum);
    }
}

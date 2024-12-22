package com.company.practice;

import java.util.Scanner;

public class CheckIntegerPalindrome {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int number = scanner.nextInt();
        int noOfDigits = 1;

        while (number / Math.pow(10, noOfDigits) >= 1) {
            noOfDigits++;
        }

        System.out.println(noOfDigits);
        for (int i = noOfDigits + 1; i <= noOfDigits / 2; i++) {
            if (number % Math.pow(10, i) != number / Math.pow(10, noOfDigits - i));
        }
    }
}

package com.company.practice;

public class CalculateFactorial {
    public static void main(String[] args) {
        for (int i = 1; i <= 10; i++) {
            int result = 1, count = i;
            while (count != 1) {
                result *= count;
                count--;
            }
            System.out.printf("Factorial of %d = %d\n", i, result);
        }
    }
}

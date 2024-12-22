package com.company.practice;

import java.util.Scanner;

public class CalculateCGPA {

    public static float calculateCGPA(float num1, float num2, float num3) {
        return (num1 + num2 + num3) / 30;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter subject 1 marks: ");
        float a = scanner.nextFloat();
        System.out.print("Enter subject 2 marks: ");
        float b = scanner.nextFloat();
        System.out.print("Enter subject 3 marks: ");
        float c = scanner.nextFloat();

        System.out.printf("CGPA: %.2f%n", calculateCGPA(a, b, c));
    }
}

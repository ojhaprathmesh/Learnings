package com.company.practice;

import java.util.Scanner;

public class CalculatePercentage {

    public static float calculatePercentage(float num1, float num2, float num3, float num4, float num5) {
        return (num1 + num2 + num3 + num4 + num5) / 5;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter subject 1 marks: ");
        float a = scanner.nextFloat();
        System.out.print("Enter subject 2 marks: ");
        float b = scanner.nextFloat();
        System.out.print("Enter subject 3 marks: ");
        float c = scanner.nextFloat();
        System.out.print("Enter subject 4 marks: ");
        float d = scanner.nextFloat();
        System.out.print("Enter subject 5 marks: ");
        float e = scanner.nextFloat();

        System.out.println("Percentage: " + calculatePercentage(a, b, c, d, e));
    }
}

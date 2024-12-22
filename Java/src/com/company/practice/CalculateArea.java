package com.company.practice;

import java.util.Scanner;

public class CalculateArea {
    public static void main(String[] args) {
        do {
            System.out.println(" ==== Calculator Menu ====");
            System.out.println("1 -> Area of triangle");
            System.out.println("2 -> Area of circle");
            System.out.println("3 -> Area of rectangle");
            System.out.println("4 -> Exit");

            Scanner scanner = new Scanner(System.in);

            System.out.print("Enter your choice: ");
            int choice = scanner.nextInt();

            switch (choice) {
                case 1: {
                    double base, height;
                    System.out.print("Enter base of the triangle: ");
                    base = scanner.nextDouble();
                    System.out.print("Enter perpendicular height: ");
                    height = scanner.nextDouble();
                    double area = 0.5 * base * height;
                    System.out.printf("Area of triangle = %.5f unit²\n", area);
                    break;
                }
                case 2: {
                    double r;
                    System.out.print("Enter radius of the circle: ");
                    r = scanner.nextDouble();
                    double area = Math.PI * Math.pow(r, 2);
                    System.out.printf("Area of circle = %.5f unit²\n", area);
                    break;
                }
                case 3: {
                    double length, width;
                    System.out.print("Enter length: ");
                    length = scanner.nextDouble();
                    System.out.print("Enter width: ");
                    width = scanner.nextDouble();
                    double area = length * width;
                    System.out.printf("Area of rectangle = %.5f unit²\n", area);
                    break;
                }

                case 4: {
                    System.out.println("\nThank you for using the calculator");
                    System.exit(0);
                }

                default: {
                    System.out.println("\nWrong choice entered!!");
                    System.out.println("Terminating the program!!");
                    System.exit(-1);
                }
            }
        } while (true);
    }
}

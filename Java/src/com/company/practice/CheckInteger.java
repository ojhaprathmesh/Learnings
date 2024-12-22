package com.company.practice;

import java.util.Scanner;

public class CheckInteger {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a string: ");
        boolean check = scanner.hasNextInt();

        if (check) {
            System.out.println("It is an integer.");
        } else {
            System.out.println("It is not an integer.");
        }
    }
}

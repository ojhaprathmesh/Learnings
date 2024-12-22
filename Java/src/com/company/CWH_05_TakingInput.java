package com.company;

import com.company.practice.AddThreeNumbers;

import java.util.Scanner;

public class CWH_05_TakingInput {
    public static void main(String[] args) {
        System.out.println("Taking input from the user: ");
        Scanner scan = new Scanner(System.in);

        System.out.print("Number 1: ");
        int a = scan.nextInt();
        System.out.print("Number 2: ");
        int b = scan.nextInt();
        System.out.print("Number 3: ");
        int c = scan.nextInt();

        int sum = AddThreeNumbers.addThreeNumbers(a, b, c);
        System.out.println("Sum of " + a + " + " + b + " + " + c + " is " + sum);
    }
}

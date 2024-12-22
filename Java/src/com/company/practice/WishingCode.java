package com.company.practice;

import java.util.Scanner;

public class WishingCode {
    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter your name: ");
        String name = scanner.nextLine();

        System.out.print("Hello " + name + ", have a good day.");
    }
}

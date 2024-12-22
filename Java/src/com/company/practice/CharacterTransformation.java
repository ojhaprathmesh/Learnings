package com.company.practice;

import java.util.Scanner;

public class CharacterTransformation {
    void display(char[] array) {
        for (int i = 0; i < array.length; i++) {
            
        }
    }

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int n = scan.nextInt();
        char[] charArray = new char[n];

        for (int i = 0; i < n; i++) {
            charArray[i] = scan.nextLine().charAt(0);
        }

        display(charArray);
    }
}

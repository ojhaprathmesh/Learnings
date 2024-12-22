package com.company.practice;

import java.util.Scanner;

public class QuizPractice {
    public static void main(String[] args) {
        int arr[] = new int[4];
        arr[1] = 8;

        for (int i = 0; i < arr.length; i++) {
            System.out.println(arr[i]);
        }

        Scanner scanner = new Scanner("sample.txt");
        scanner.findAll("Hi");
    }
}

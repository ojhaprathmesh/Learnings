package com.company.practice;

import java.util.Scanner;

public class ConvertKilometerToMile {

    public static float convert(float n) {
        return n / 1.609344f;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the distance(in km): ");
        float distance = scanner.nextFloat();

        System.out.print(distance + " km = " + convert(distance) + " miles");
    }
}

package com.company.practice;

public class DetectSpaces {
    public static void detect(String string) {
        int twos = string.indexOf("  ");
        int threes = string.indexOf("   ");
        if (twos != -1 || threes != -1) {
            System.out.println("Contains required whitespaces!");
        } else {
            System.out.println("Doesn't contains required whitespaces!");
        }
    }

    public static void main(String[] arg) {
        detect("Prathmesh Ojha");
    }
}

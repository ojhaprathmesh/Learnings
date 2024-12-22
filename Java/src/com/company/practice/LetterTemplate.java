package com.company.practice;

import java.util.Scanner;

public class LetterTemplate {
    public static String fillLetter(String string) {
        String template = "Dear <|name|>, Thanks a lot!!";
        return template.replace("<|name|>", string);
    }

    public static void main(String[] arg) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter a name: ");
        String name = sc.nextLine();

        System.out.println(fillLetter(name));
    }
}

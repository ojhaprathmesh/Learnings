package com.company;

import com.company.practice.AddThreeNumbers;

// com.company.Main.java
public class Main {

    public static void main(String[] args) {
        // Define three numbers
        int number1 = 10;
        int number2 = 20;
        int number3 = 30;

        // Call the function from com.company.practice.AddThreeNumbers class and store the result
        int result = AddThreeNumbers.addThreeNumbers(number1, number2, number3);

        // Print the result
        System.out.println("The sum of " + number1 + ", " + number2 + ", and " + number3 + " is: " + result);
    }
}

package com.company.practice;

public class AddThreeNumbers {

    // Function to add three numbers
    public static int addThreeNumbers(int num1, int num2, int num3) {
        return num1 + num2 + num3;
    }

    public static void main(String[] args) {
        // Define three numbers
        int number1 = 10;
        int number2 = 20;
        int number3 = 30;

        // Call the function and store the result
        int result = addThreeNumbers(number1, number2, number3);

        // Print the result
        System.out.println("The sum of " + number1 + ", " + number2 + ", and " + number3 + " is: " + result);
    }
}

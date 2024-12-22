package com.company;

public class CWH_14_String_Methods {
    public static void main(String[] args) {
        // String string = new String("Prathmesh");
        String name = "Prathmesh Ojha";

        // Length Function
        System.out.println(name);
        int value = name.length();

        // Use of formatters
        System.out.printf("Size of %s is %d. \n", name, value);

        // Converts to Lowercase
        System.out.println(name.toLowerCase());
        System.out.println(name);

        // Converts to Uppercase
        System.out.println(name.toUpperCase());
        System.out.println(name);

        name = "    Prathmesh Ojha";
        System.out.println(name);

        // Trim Function
        name = name.trim();
        System.out.println(name);

        // Substring Function
        System.out.println(name.substring(10));

        System.out.println(name.substring(0, 9));

        // Replace Function
        String str = "Harry";
        System.out.print(str + " -> ");
        str = str.replace('r', 'p');
        System.out.println(str);

        str = str.replace("p", " ");
        System.out.println(str);

        str = str.replace("  y", "ier");
        System.out.println(str);

        // Checks starting of the string
        System.out.println(str.startsWith("Ha"));
        System.out.println(str.startsWith("ha"));

        // Checks ending of the string
        System.out.println(str.endsWith("er"));
        System.out.println(str.endsWith("eR"));

        // Returns character at given index position. Index starts at 0.
        System.out.println(name.charAt(11));

        // Returns index of the given character
        System.out.println(name.indexOf('a'));

        System.out.println(name.indexOf('a', 4));

        // Returns last index of the given character
        System.out.println(name.lastIndexOf('h'));

        System.out.println(name.lastIndexOf('h', 7));

        // Returns -1 if it doesn't find the character in the string
        System.out.println(name.indexOf('P', 3));

        // Returns true only if both case and string matches
        System.out.println(str.equals("Haier"));

        // Returns true if char matches. Doesn't check the case.
        System.out.println(str.equalsIgnoreCase("haier"));
    }
}

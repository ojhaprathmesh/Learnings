package com.company.practice;

public class SpaceToUnderscore {
    public static String replaceSpaceTo_ (String string) {
        return string.replace(' ','_');
    }
    public static void main(String[] arg) {
        String output = replaceSpaceTo_("Prathmesh Kumar Ojha 23 07 04");
        System.out.println(output);
    }
}

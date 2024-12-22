import java.util.Scanner;

public class Time {
    public static void main(String[] args) {
        int seconds, minutes, hours;

        Scanner scan = new Scanner(System.in);
        seconds = scan.nextInt();

        System.out.printf("%d seconds = ", seconds);

        minutes = seconds / 60;
        seconds = seconds % 60;

        hours = minutes / 60;
        minutes = minutes % 60;

        System.out.printf("%d hours, %d minutes and %d seconds", hours, minutes, seconds);
    }
}

import java.util.Scanner;

public class Convertor {
    public double celsiusToFahrenheit(double temperature) {
        return (temperature - 32) * 5 / 9;
    }

    public static void main(String[] args) {
        Convertor convertor = new Convertor();
        Scanner scan = new Scanner(System.in);
        System.out.print("Enter temperature(in °C): ");
        float input = scan.nextFloat();

        System.out.printf("%f°C = %.1f°F", input, convertor.celsiusToFahrenheit(input));
        System.out.println();
        System.out.printf("");
    }
}

import java.util.Scanner;

public class Interest {
    public static void main(String[] args) {
        int amount;
        float yearly_rate, income_tax;

        Scanner scan = new Scanner(System.in);
        System.out.print("Enter amount: ");
        amount = scan.nextInt();
        System.out.print("Enter yearly interest rate: ");
        yearly_rate = scan.nextFloat();
        System.out.print("Enter income tax: ");
        income_tax = scan.nextFloat();

        System.out.println("The amount of interest earned is " + (amount * yearly_rate / 100) * (1 - income_tax / 100));
    }
}

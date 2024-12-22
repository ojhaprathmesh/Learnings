import java.util.Scanner;

public class Print {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);

        System.out.print("What's our name: ");
        String name = scan.nextLine();
        System.out.print("Where do you live: ");
        String address = scan.nextLine();

        System.out.printf("\nSo your name is \nName: %s \nAddress: %s", name, address);
    }
}

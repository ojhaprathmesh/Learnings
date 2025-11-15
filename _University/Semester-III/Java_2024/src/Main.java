public class Main {
    int m = 100;
    static int n = 200;

    public static void main(String[] args) {
        Main M1 = new Main();
        Main M2 = new Main();
        Main M3 = new Main();
        M1.m = 1000;
        M1.n = 2000;

        System.out.println(M1.m + " " + M2.n + " " + M3.n + " " + M1.n);
    }
} 
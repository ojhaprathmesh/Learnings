public class Swap {
    public static void main(String[] args) {
        int a = 10, b = 20, c;
        System.out.printf("Before: a=%d, b=%d", a, b);
        c = a;
        a = b;
        b = c;
        System.out.printf("\nAfter:  a=%d, b=%d", a, b);
        a = 19;
        b = 23;
        System.out.printf("\nBefore: a=%d, b=%d", a, b);
        a = a + b;
        b = a - b;
        a = a - b;
        System.out.printf("\nAfter:  a=%d, b=%d", a, b);
    }
}

public class Demo {
    void Test(short a, int b) {
        System.out.println("fine");
    }

    void Test(long a, int b) {
        System.out.println("best");
    }

    public static void main(String args[]) {
        byte a = 10;
        short b = 15;
        Demo test = new Demo();
        test.Test(a, b);
    }
} 
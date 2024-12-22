public class Box {
    int length, breadth, height;

    Box() {
        length = 10;
        breadth = 10;
        height = 10;
    }

    Box(int l, int b, int h) {
        length = l;
        breadth = b;
        height = h;
    }

    void dimensions() {
        System.out.println(length);
        System.out.println(breadth);
        System.out.println(height);
    }

    public static void main(String[] args) {
        Box box1 = new Box();
        Box box2 = new Box(1, 2, 3);

        box1.dimensions();
        box2.dimensions();
    }
}
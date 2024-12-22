public class Area {
    public float calculate(float length, float breadth) {
        return length * breadth;
    }

    public float calculate(float side1, float side2, float side3) {
        float s = (side1 + side2 + side3) / 2;
        return (float) Math.sqrt(s * (s - side1) * (s - side2) * (s - side3));
    }

    public float calculate(float radius) {
        return (float) Math.PI * (float) Math.pow(radius, 2);
    }

    public static void main(String[] args) {
        Area area = new Area();
        System.out.println((area.calculate(3, 4, 5)));
    }
}

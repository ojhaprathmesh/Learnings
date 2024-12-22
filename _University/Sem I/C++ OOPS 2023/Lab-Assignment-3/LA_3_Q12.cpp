#include <iostream>
#include <cmath>
using namespace std;

int main() {
    int p, q, r, a, b, c;
    cin >> p >> q >> r >> a >> b >> c;

    // Calculate the distance from the center to the line
    float distance_center_to_line = abs(a * p + b * q + c) / sqrt(a * a + b * b);

    if (distance_center_to_line > r) {
        cout << "No Intersection" << endl;
    } else {
        // Calculate the chord length AB using the points of intersection
        float A = a * a + b * b;
        float B = 2 * a * c + 2 * b * q - 2 * a * p - 2 * b * q;
        float C = p * p + q * q - r * r;

        // Check the discriminant to determine if there are real solutions
        float discriminant = B * B - 4 * A * C;

        if (discriminant < 0) {
            cout << "No Intersection" << endl;
        } else {
            float x1 = (-B + sqrt(discriminant)) / (2 * A);
            float x2 = (-B - sqrt(discriminant)) / (2 * A);

            // Calculate the area of the triangle formed by A, B, and the center (p, q)
            float chord_length = abs(x1 - x2);
            float area = 0.5 * chord_length * distance_center_to_line;
            cout << area << endl;
        }
    }

    return 0;
}

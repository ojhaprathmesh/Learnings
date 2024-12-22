#include <iostream>

// Base class
class Shape {
public:
    void draw() {
        std::cout << "Drawing a shape." << std::endl;
    }
};

// Derived class 1
class Circle : public Shape {
public:
    void draw() {
        std::cout << "Drawing a circle." << std::endl;
    }
};

// Derived class 2
class Rectangle : public Shape {
public:
    void draw() {
        std::cout << "Drawing a rectangle." << std::endl;
    }
};

int main() {
    Circle myCircle;
    myCircle.draw();  // Draws a circle

    Rectangle myRectangle;
    myRectangle.draw();  // Draws a rectangle

    return 0;
}

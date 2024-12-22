#include <iostream>

// Base class
class Animal {
public:
    void eat() {
        std::cout << "Animal is eating." << std::endl;
    }
};

// Intermediate class 1
class FourLeggedAnimal : virtual public Animal {
public:
    void walk() {
        std::cout << "Four-legged animal is walking." << std::endl;
    }
};

// Intermediate class 2
class Bird : virtual public Animal {
public:
    void fly() {
        std::cout << "Bird is flying." << std::endl;
    }
};

// Derived class inheriting from both FourLeggedAnimal and Bird
class Griffin : public FourLeggedAnimal, public Bird {
public:
    void roar() {
        std::cout << "Griffin is roaring." << std::endl;
    }
};

int main() {
    Griffin myGriffin;
    myGriffin.eat();   // Inherited from Animal
    myGriffin.walk();  // Inherited from FourLeggedAnimal
    myGriffin.fly();   // Inherited from Bird
    myGriffin.roar();

    return 0;
}

#include <iostream>

// Base class
class Animal {
public:
    void eat() {
        std::cout << "Animal is eating." << std::endl;
    }
};

// Intermediate class
class Machine {
public:
    void work() {
        std::cout << "Machine is working." << std::endl;
    }
};

// Derived class inheriting from both Animal and Machine
class Robot : public Animal, public Machine {
public:
    void performTasks() {
        std::cout << "Robot is performing tasks." << std::endl;
    }
};

// Derived class inheriting from Robot
class RoboticAnimal : public Robot {
public:
    void makeSounds() {
        std::cout << "Robotic animal is making sounds." << std::endl;
    }
};

int main() {
    RoboticAnimal myRoboticAnimal;
    myRoboticAnimal.eat();         // Inherited from Animal
    myRoboticAnimal.work();        // Inherited from Machine
    myRoboticAnimal.performTasks(); // Inherited from Robot
    myRoboticAnimal.makeSounds();

    return 0;
}

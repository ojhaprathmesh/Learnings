#include<iostream>
using namespace std;

class Complex{
    int a, b;
    public:
        // Creating a constructor
        // Constructor is a special member function with the same name as of the class.
        // It is used to initialize the objects of its class.
        // It automatically invokes the whenever an object is created.
    
        Complex(void); // Contructor Declaration

        void printNumber()
        {
            cout << "Your number is " << a << " + " << b << "i" << endl;
        }
};

Complex :: Complex(void){
    a = 10;
    b = 0;
}

int main(){
    Complex c;
    c.printNumber();
    return 0;
}
#include<iostream>
using namespace std;

class A {
    public:
        void funA(){
            cout << "Class A";
        }
};

class B : virtual public A{
    public:
        void funB(){
            cout << "Class B";
        }
};

class C : virtual public A{
    public:
        void funC(){
            cout << "Class C";
        }
};

class D : public B, public C{
    public:    
        void funD(){
            cout << "Class D";
        }
};

int main() {
    A obja;
    B objb;
    C objc;
    D objd;

    obja.funA();
    objd.funA();

    return 0;
}
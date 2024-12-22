#include<iostream>
using namespace std;

class A {
    public:
        virtual void fun() = 0 ;
};

class B : public A {
    public:
        void fun() {
            cout << "Abstract Class";
        }
};

int main() {
    B objb;
    objb.fun();
    return 0;
}
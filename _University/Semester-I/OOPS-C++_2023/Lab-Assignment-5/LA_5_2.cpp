#include<iostream>
using namespace std;

class A
{
    public:
    A()
    {
        cout<<"A";
    }
};

class B: public A
{
    public:B(){
        cout<<"B";
    }
};

class C: public B
{
    public:
    C()
    {
        cout<<"C";
    }
};

int main()
{
    C objc;
    B objb;
    A obja;
}

#include<iostream>
using namespace std;

class A
{
    private:
        int a;
    public:
        A() {
            a = 10;
        }
        A(int x) {
            a = x;
        }
        A(A &obj) {
            a = obj.a;
            cout << a << endl;
        }
};

int main(){
    A obj1;
    A obj2(30);
    A obj3 = obj1;
    A obj4 = obj2;
    return 0;
}
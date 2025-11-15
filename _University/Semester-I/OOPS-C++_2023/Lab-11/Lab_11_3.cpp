#include<iostream>
using namespace std;

class calculator {
    public :
        void add(int a, int b) {
            cout << a + b;
        }

        void add(float a, float b) {
            cout << a + b;
        }

        void add(int a, int b, int c) {
            cout << a + b + c;
        }
};

int main(){
    calculator cal;
    cal.add(1, 2);
}
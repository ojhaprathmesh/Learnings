#include<iostream>
using namespace std;

int main(){
    int a = 10;
    int b = 20;

    cout<<"A = "<< a << endl;
    cout<<"B = "<< b << endl;

    a = a + b; // Here A Has Got Values Of Both
    b = a - b; // Here We Subtract Added Value To Swap A To B
    a = a - b; // Here We Subtract Subtracted Value To Swap B To A

    cout<<"A = "<< a << endl;
    cout<<"B = "<< b << endl;
}
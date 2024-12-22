#include<iostream>
using namespace std;

int main(){
    int a, b;
    cout<<"Enter A Integer Value: ";
    cin>>a;
    cout<<"Enter A Integer Value: ";
    cin>>b;
    cout<<"a = "<< a <<", b = "<< b << endl;
    
    int c;
    c = a;
    a = b;
    b = c;
    cout<<"a = "<< a <<", b = "<< b << endl;

    a = a + b;
    b = a - b;
    a = a - b;
    cout<<"a = "<< a <<", b = "<< b << endl;
}


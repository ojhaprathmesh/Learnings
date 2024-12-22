#include<iostream>
using namespace std;

int main(){
    int a;
    cout<<"Enter A Non-Singular Digit Number: ";
    cin>>a;
    cout<<a % 10 << endl;
    int b;
    b = a/10;
    a = a - (b*10);
    cout<<a;

}
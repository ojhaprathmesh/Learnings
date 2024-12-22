#include<iostream>
using namespace std;

int main(){
    int a, b;
    cout<<"Enter A Value: ";
    cin>>a;
    cout<<"Enter A Value: ";
    cin>>b;

    if (a>b){
        cout<<"a>b";
    }

    else if (a==b){
        cout<<"a=b";
    }

    else {
        cout<<"a<b";
    }
}
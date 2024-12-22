#include<iostream>
#include<bits/stdc++.h>
using namespace std;

int main(){
    float num;
    float req;
    cout<<"Enter A Number: ";
    cin>>num;

    req = cbrt(num);
    cout<<"The Cube Root Of "<<num<<" Is "<<req;
}
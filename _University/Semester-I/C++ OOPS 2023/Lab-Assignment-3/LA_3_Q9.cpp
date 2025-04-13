#include<iostream>
using namespace std;

int main(){
    int a, b, c, d, x;
    cout<<"Enter Four Distinct Numbers: " << endl;
    cin >> a >> b >> c >> d;
    cout<<"Enter A Similar Number: ";
    cin >> x;
    
    if (x==a) {
        cout<<"x is equal to a";
    }
    else if (x==b) {
        cout<<"x is equal to b";
    }
    else if (x==c) {
        cout<<"x is equal to c";
    }
    else {
        cout<<"x is equal to d";
    }
}
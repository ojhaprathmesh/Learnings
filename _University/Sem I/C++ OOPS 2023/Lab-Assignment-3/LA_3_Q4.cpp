#include<iostream>
using namespace std;

int main(){
    int a, b, c;
    cout << "Enter Side 1 Length: ";
    cin >> a;
    cout << "Enter Side 1 Length: ";
    cin >> b;
    cout << "Enter Side 1 Length: ";
    cin >> c;
    
    if (a*a + b*b == c*c){
        cout<<"Angle A is 90\370";
    }

    else {
        cout<<"Angle A is Not 90\370";
    }
}
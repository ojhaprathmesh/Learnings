#include<iostream>
using namespace std;

int main(){
    int a;
    cout<<"Enter Marks(In Integer): ";
    cin>>a;
    
    if (a>=90){
        cout<<"A Grade";
    }
    else if (a>=80){
        cout<<"B Grade";
    }
    else if (a>=70){
        cout<<"C Grade";
    }
    else if (a>=60){
        cout<<"D Grade";
    }
    else if (a<60){
        cout<<"E Grade";
    }
}
#include<iostream>
using namespace std;

int main(){
    cout<<"Enter A Year: ";
    int year;
    cin>>year;
    if (year%400==0 || year%4==0 && year%100!=0){
        cout<<"The Year " << year << " Is A Leap Year";
    }
    
    else {
        cout<<"The Year " << year << " Is Not A Leap Year";
    }
}
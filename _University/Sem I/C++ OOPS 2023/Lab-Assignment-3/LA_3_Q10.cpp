#include<iostream>
using namespace std;

int main(){
    int a, b, c, d, x;
    cout<<"Enter Four Numbers: " << endl;
    cin >> a >> b >> c >> d;
    cout<<"Enter A Similar Number: ";
    cin >> x;
    int count = 0;
    
    if (x==a) {
        count+=1;
    }
    if (x==b) {
        count+=1;
    }
    if (x==c) {
        count+=1;
    }
    if (x==d){
        count+=1;
    }

    cout<<count;
}
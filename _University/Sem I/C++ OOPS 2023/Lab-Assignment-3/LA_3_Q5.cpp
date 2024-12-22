#include<iostream>
using namespace std;

int main(){
    int a, b, c;
    cin >> a >> b >> c;

    if (b == 0){
        cout<<"This is a vertical line, with an undefined slope.";
    }

    else {
        double slope = -a/b;
        cout<<"This is a not vertical line, with an "<< slope <<" slope.";
    }
}
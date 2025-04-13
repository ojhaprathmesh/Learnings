#include <iostream>
using namespace std;

int main(){
    int n;
    long long fact = 1;
    cout<<"Enter A Number: ";
    cin >> n;

    for (int i = 1; i<=n; ++i){
        fact = fact*i;
    }
    cout<<fact;
}
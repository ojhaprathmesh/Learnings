#include <iostream>
using namespace std;

int main(){
    int n;
    cout<<"Enter A Number: ";
    cin >> n;
    int i = 0;
    int sum = 0;
    while (i<=n){
        sum = sum + i;
        i++;
    }
    // for (i=0; i<=n; i++){
    //     sum = sum + i;
    // }
    cout<<sum;
}
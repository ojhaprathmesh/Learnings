#include <iostream>
using namespace std;

int main(){
    for (int i = 101; i <= 200; i++){
        if (i%2==0){
            cout<<i<<endl;
        }
    }
    cout<<endl;
    int i = 101;
    while(i <= 200){
        if (i%2==0){
            cout<<i<<endl;
        }
        i++;
    }
}
#include <iostream>
using namespace std;

int main(){
    for (int i = 5; i>=1; i--){
        for (int j = i-5; j>0; j++){
            cout<<" ";
        }
        for (int k = i; k>=1; k--){
            cout<<"*";
        }
        cout<<endl;
    }   
}
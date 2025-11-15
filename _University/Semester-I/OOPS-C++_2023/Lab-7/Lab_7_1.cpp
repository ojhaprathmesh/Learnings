#include<iostream>
using namespace std;

int main(){
    char a[] = {'1', '2', '3', '4', '5'};
    int iterations = sizeof(a) / sizeof(a[0]) - 1;
    for (int i = iterations; i>=0; i--){
        cout<<a[i]<<' ';
    }
}
#include<iostream>

using namespace std;

int main(){
    int a = 10, b = 20;
    int sum = 0; // If We Dont Define A Value For Sum A Garbage Value Will Be Assigneds To It
    sum = a + b;
    int product = a * b;
    cout << "Sum = " << sum << endl;
    cout << "Product = " << product << endl;
    cout <<'\n'<<"This Is The End Of Program"; // endl can also be used for moving to next line
    return 0;
}
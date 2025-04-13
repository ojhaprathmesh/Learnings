#include <iostream>
using namespace std;

void A(){
    cout<<"I Am A"<<endl;
}

void B(){
    A();
    cout<<"I Am B"<<endl;
}

int main(){
    B();
    A();
    return 0;
}


#include<iostream>
using namespace std;

int main(){
    int a;
    cout<<"Enter A: ";
    cin>>a;
    int b;
    cout<<"Enter B: ";
    cin>>b;
    int c;
    cout<<"Enter C: ";
    cin>>c;

    if (a==b && b==c){
        cout<<"All Numbers Are Equal";
    }

    else if (a==b){
        if (b<c){
            cout<<"C is The Largest";
        }

        else{
            cout<<"Both A And B Are The Largest";
        }
    }    

    else if (b==c){
        if (c<a){
            cout<<"A Is The Largest";
        }

        else {
            cout<<"Both B And C Are The Largest";
        }
    }

    else if (c==a){
        if (a<b){
            cout<<"B Is The Largest";
        }

        else {
            cout<<"Both A And C Are The Largest";
        }
    }

    else {
        if (a>b && a>c){
            cout<<"A Is The Largest";
        }

        else if (b>c && b>a){
            cout<<"B Is The Largest";
        }

        else if (c>a && c>b) {
            cout<<"C Is The Largest";
        }
    }
}
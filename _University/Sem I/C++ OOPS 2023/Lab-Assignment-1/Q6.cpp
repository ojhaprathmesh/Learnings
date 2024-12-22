#include<string>
#include<iostream>
using namespace std;

int main(){
    string name;
    string address;
    long long contact;

    cout<<"Enter Your Name: ";
    getline(cin, name);

    cout<<"Enter Your Address: ";
    getline(cin, address);

    cout<<"Enter Your Phone Number: ";
    cin >>contact;

    cout<<"Name: "<<name<<endl;
    cout<<"Address: "<<address<<endl;
    cout<<"Phone Number: "<<contact;

}
#include<iostream>
using namespace std;

int main(){
    char ch;
    cout<<"Enter A Character: ";
    
    switch ((char)tolower(ch))
    {
    case 'a': cout<<"Given Character Is Vowel";
        break;
    
    case 'e': cout<<"Given Character Is Vowel";
        break;
    
    case 'i': cout<<"Given Character Is Vowel";
        break;
    
    case 'o': cout<<"Given Character Is Vowel";
        break;
    
    case 'u': cout<<"Given Character Is Vowel";
        break;
    
    default: cout<<"Given Character Is Consonant"; 
        break;
    }
}
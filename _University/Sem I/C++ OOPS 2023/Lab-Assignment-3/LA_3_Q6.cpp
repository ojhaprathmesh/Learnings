#include<iostream>
#include<cmath>
using namespace std;

int main(){
    int a, b, c;
    cin >> a >> b >> c;
    float d = (b*b - 4*a*c);
    if (d >= 0){
        float root1, root2;
        root1 = (-b + sqrt(d))/(2*a);
        root2 = (-b - sqrt(d))/(2*a);

        if (d > 0) {
            cout<<"First Root -> "<<root1<<endl<<"Second Root -> "<<root2;
        }
        else {
            cout<<"Root -> "<< root1 << endl;
        }
    }

    else {
        float img, real;
        img = sqrt(abs(d))/(2*a);
        real = -b/(2*a);
        cout << real << ' ' << img << ' ' << -img;
    } 
}

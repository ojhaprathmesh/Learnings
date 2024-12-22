#include<iostream>
using namespace std;

int main(){
    int a[3][2] = {0,1,2,3,4,5};

    for (int i=0; i<3; i++){
        for (int j=0; j<2; j++){
        cout << a[i][j] << " " << &a[i][j] << endl;
        }
    }

    cout << *(a[0] + 1) << " " << a[0] + 1 << endl;
    cout << *(a[1] + 2) << " " << a[1] + 2 << endl;
    cout << 1 + a;
    cout << a + 1 << endl;
    cout << a + 2 << endl;
    cout << &a[0][0] + 1 << endl;

}
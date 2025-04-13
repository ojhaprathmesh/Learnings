// #include<iostream>
// using namespace std;

// int main(){
//     char a[] = {'a','b','c','d','e'};
//     int size = sizeof(a) / sizeof(a[0]);
//     char b[size+1];
//     for (int i = (size-1); i>=0; i--){
//         b[size-1-i] = a[i];
//     }
//     b[size] = '\0';
//     cout<<b<<endl;
//     for (int i=0; i<size; i++){
//         cout<<b[i];
//     }
// }

// #include<iostream>
// using namespace std;
// int main(){
//     char a[]={'a','b','c','d','e'};
//     char b[5];
//     int i,j=0;
//     for(i=4;i>=0;i--)
//     {
//         b[4-i]= a[i];
//     }
//     cout<<b<<endl;
//     for(i=0;i<=4;i++)
//     {
//         cout<< b[i];
//     }
//     return 0;
// }

#include<iostream>
using namespace std;

int main(){
    int arr[] = {1, 2, 3, 4, 5};
    int len = sizeof(arr) / sizeof(arr[0]) - 1;

    for (int start = 0, end = len; start < end; start++, end--){
        int temp = arr[start];
        arr[start] = arr[end];
        arr[end] = temp; 
    }
    
    for (int i = 0; i<=len; i++){
        cout<<arr[i]<<' ';
    } 

    // for (int i = 1; i<=4; i++){
    //     for (int j = i; j<=4; j++){
    //         cout<<j;
    //     }
    //     cout<<endl;
    // }
}
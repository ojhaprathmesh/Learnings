#include <iostream>
using namespace std;

void towerOfHanoi(int n, char fromRod, char toRod, char auxRod) {
    // Base case: If there is only one disk to move
    if (n == 1) {
        cout << "Move disk 1 from rod " << fromRod << " to rod " << toRod << endl;
        return;
    }

    // Move top n-1 disks from fromRod to auxRod using toRod as auxiliary
    towerOfHanoi(n - 1, fromRod, auxRod, toRod);

    // Move the nth disk from fromRod to toRod
    cout << "Move disk " << n << " from rod " << fromRod << " to rod " << toRod << endl;

    // Move the n-1 disks from auxRod to toRod using fromRod as auxiliary
    towerOfHanoi(n - 1, auxRod, toRod, fromRod);
}

int main() {
    towerOfHanoi(3, 'A', 'B', 'C');
}

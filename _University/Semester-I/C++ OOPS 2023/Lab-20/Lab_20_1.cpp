#include <iostream>
using namespace std;

class A
{
private:
    int a = 10;

public:
    class B
    {
    private:
        int b = 20;

    public:
        void show()
        {
            cout << b << endl;
        }
    };

    void display()
    {
        cout << a;
    }
};

int main()
{
    A obj;
    obj.display();
    return 0;
}
#include<iostream>
using namespace std;

class car {
    private:
        string engine;
    
    public:
        string model = "XM102";
        int year;
        int weight = 200;
        float dimensions[3] = {6, 1.5, 2};
        
        void get_model() {
            cout << "Model : " << model << endl;
        }

        void set_model(string modelNo) {
            model = modelNo;
        }

        void get_dimensions() {
            cout << "Length : " << dimensions[0] << endl;
            cout << "Breadth : " << dimensions[1] << endl;
            cout << "Height : " << dimensions[2] << endl;
        }
};

int main() {
    car Ferrari;
    Ferrari.year = 2023;
    Ferrari.get_model();
    Ferrari.set_model("VW210");
    cout << "Year : " << Ferrari.year << endl;
    cout << "Weight : " << Ferrari.weight << endl;
    Ferrari.get_dimensions();
}
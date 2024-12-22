#include<iostream>
using namespace std;

class owner {
    public :
        string name;
        string nationality;
        int age;

        void set_name(string o_name) {
            name = o_name;
        }

        void set_age(int o_age) {
            age = o_age;
        }

        void set_aadhar(string o_nationality) {
            nationality = o_nationality;
        }
};

class car {
    private:
        string engine;
    
    public:
        owner c;
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

        void get_details() {
            cout << "Model : " << model << endl;
            cout << "Length : " << dimensions[0] << endl;
            cout << "Breadth : " << dimensions[1] << endl;
            cout << "Height : " << dimensions[2] << endl;
            cout << "Weight : " << weight << endl;
            cout << "Year : " << year << endl;
        }
};

class ship {
    private:
        string engine;
    
    public:
        owner s;
        string model = "XMS792";
        int year;
        int weight = 20000;
        float streamline = 0.98;
        
        void get_model() {
            cout << "Model : " << model << endl;
        }

        void set_model(string modelNo) {
            model = modelNo;
        }

        void get_stream_index() {
            cout << "Streamline Index : " << streamline << endl;
        }

        void get_details() {
            get_model();
            get_stream_index();
            cout << "Weight : " << weight << endl;
            cout << "Year : " << year << endl;
        }
};

int main() {
    car Ferrari;
    ship Titanic;

    Ferrari.year = 2023;
    Ferrari.set_model("VW210");
    // cout << "Year : " << Ferrari.year << endl;
    // cout << "Weight : " << Ferrari.weight << endl;
    Ferrari.get_details();

    Titanic.year = 2022;
    Titanic.set_model("VAW217");
    // cout << "Year : " << Titanic.year << endl;
    // cout << "Weight : " << Titanic.weight << endl;
    Titanic.s.set_name("Prathmesh");

    Titanic.get_details();
    
}
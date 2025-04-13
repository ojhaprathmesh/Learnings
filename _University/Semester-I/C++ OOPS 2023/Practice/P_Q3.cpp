#include<iostream>
using namespace std;

class Student{
    protected:
        int roll_no;
    public:
        void set_number(int a){
            roll_no = a;
        }
        void print_number(void){
            cout<<"Your roll no is "<< roll_no<<endl;
        }
};

class Test : virtual public Student{  // Declare Student as a virtual base class
    protected:
        float maths, physics;
    public:
        void set_marks(float m1, float m2){
            maths = m1;
            physics = m2;
        }

        void print_marks(void){
            cout << "Your result is here: "<<endl
                 << "Maths: "<< maths<<endl
                 << "Physics: "<< physics<<endl;
        }
};

class Sports: virtual public Student{  // Declare Student as a virtual base class
    protected:
        float score;
    public:
        void set_score(float sc){
            score = sc;
        }

        void print_score(void){
            cout<<"Your PT score is "<<score<<endl;
        }

};

class Result : public Test, public Sports{
    private:
        float total;
    public:
        void display(void){
            total = maths + physics + score;
            print_number();
            print_marks();
            print_score();
            cout<< "Your total score is: "<<total<<endl;
        }
};

int main() {
    Result obj;
    obj.set_number(123);
    obj.set_marks(90.5, 85.0);
    obj.set_score(75.5);
    obj.display();

    return 0;
}

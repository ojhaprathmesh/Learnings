#include <iostream>
#include <vector>
#include <string>

using namespace std;

class Student {
public:
    string name;
    string programEnrolled;
    string session;
    int rollNumber;
    int marksSub1;
    int marksSub2;
    int marksSub3;
    float aggregate;

    void inputStudent() {
        cout << "Enter student details:\n";
        cout << "Name: "; cin >> name;
        cout << "Program Enrolled: "; cin >> programEnrolled;
        cout << "Session: "; cin >> session;
        cout << "Roll Number: "; cin >> rollNumber;
        cout << "Marks in Subject 1: "; cin >> marksSub1;
        cout << "Marks in Subject 2: "; cin >> marksSub2;
        cout << "Marks in Subject 3: "; cin >> marksSub3;
        calculateAggregate();
    }

    void calculateAggregate() {
        aggregate = (marksSub1 + marksSub2 + marksSub3) / 3.0;
    }
};

Student findHighestScorer(const vector<Student>& students) {
    if (students.empty()) {
        cerr << "No students in database.\n";
        exit(1);
    }

    Student highestScorer = students[0];
    for (const auto& student : students) {
        if (student.aggregate > highestScorer.aggregate) {
            highestScorer = student;
        }
    }
    return highestScorer;
}

int main() {
    vector<Student> students;

    for (int i = 0; i < 5; ++i) {
        Student newStudent;
        newStudent.inputStudent();
        students.push_back(newStudent);
    }

    Student highestScorer = findHighestScorer(students);

    cout << "\nStudent with highest marks:\n";
    cout << "Name: " << highestScorer.name << endl;
    cout << "Program Enrolled: " << highestScorer.programEnrolled << endl;
    cout << "Session: " << highestScorer.session << endl;
    cout << "Roll Number: " << highestScorer.rollNumber << endl;
    cout << "Aggregate Marks: " << highestScorer.aggregate << endl;

    return 0;
}

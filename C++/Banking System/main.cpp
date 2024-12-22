#include<iostream>
#include<vector>
#include<string>
#include<sstream>
using namespace std;

struct User {
    string username, password, phone_no, address, aadhar_no;
    int age;
    float balance;
};

vector<User> users;

void displayMenu() {
    cout << "Welcome To Our Bank" << endl;
    cout << "1. Open an account" << endl;
    cout << "2. Show account info" << endl;
    cout << "3. Deposit" << endl;
    cout << "4. Withdraw" << endl;
    cout << "5. Fund Transfer" << endl;
    cout << "6. Exit" << endl;
}

int findUserByUsername(const string &username) {
    for (int i = 0; i < users.size(); i++) {
        if (users[i].username == username) {
            return i; // Return user index if found
        }
    }
    return -1; // User not found
}

bool validatePassword(int userIndex, const string &password) {
    return users[userIndex].password == password;
}

void openAccount() {
    User newUser;
    cout << "Enter your username: ";
    cin >> newUser.username;
    
    if (findUserByUsername(newUser.username) != -1) {
        cout << "Username already exists! Please try another one." << endl;
        return;
    }

    cout << "Create password: ";
    cin >> newUser.password;
    cout << "Enter your contact number: ";
    cin >> newUser.phone_no;
    cout << "Enter your age: ";
    cin >> newUser.age;
    cout << "Enter your address: ";
    cin >> newUser.address;
    cout << "Enter your Aadhar number: ";
    cin >> newUser.aadhar_no;
    cout << "Enter initial balance: Rs. ";
    cin >> newUser.balance;

    users.push_back(newUser);
    cout << "Account successfully created!" << endl;
}

void showAccountInfo() {
    string username;
    cout << "Enter your username: ";
    cin >> username;
    
    int userIndex = findUserByUsername(username);
    if (userIndex == -1) {
        cout << "User not found." << endl;
        return;
    }

    string password;
    int trial = 0;
    while (trial < 3) {
        cout << "Enter your password: ";
        cin >> password;
        if (validatePassword(userIndex, password)) {
            cout << "==== Account Details ====" << endl;
            cout << "Name: " << users[userIndex].username << endl;
            cout << "Phone Number: " << users[userIndex].phone_no << endl;
            cout << "Age: " << users[userIndex].age << endl;  // Display age as a number
            cout << "Address: " << users[userIndex].address << endl;
            cout << "Aadhar Number: " << users[userIndex].aadhar_no << endl;
            cout << "Balance: Rs. " << users[userIndex].balance << endl;
            return;
        } else {
            trial++;
            cout << "Invalid password! Attempts left: " << 3 - trial << endl;
        }
    }
    cout << "Too many incorrect password attempts. Access denied." << endl;
}

void deposit() {
    string username;
    cout << "Enter your username: ";
    cin >> username;

    int userIndex = findUserByUsername(username);
    if (userIndex == -1) {
        cout << "User not found." << endl;
        return;
    }

    string password;
    cout << "Enter your password: ";
    cin >> password;

    if (!validatePassword(userIndex, password)) {
        cout << "Invalid password!" << endl;
        return;
    }

    float depositAmount;
    cout << "Enter the deposit amount: Rs. ";
    cin >> depositAmount;
    users[userIndex].balance += depositAmount;
    cout << "Deposit successful! New balance: Rs. " << users[userIndex].balance << endl;
}

void withdraw() {
    string username;
    cout << "Enter your username: ";
    cin >> username;

    int userIndex = findUserByUsername(username);
    if (userIndex == -1) {
        cout << "User not found." << endl;
        return;
    }

    string password;
    cout << "Enter your password: ";
    cin >> password;

    if (!validatePassword(userIndex, password)) {
        cout << "Invalid password!" << endl;
        return;
    }

    float withdrawAmount;
    cout << "Enter the withdraw amount: Rs. ";
    cin >> withdrawAmount;
    if (users[userIndex].balance >= withdrawAmount) {
        users[userIndex].balance -= withdrawAmount;
        cout << "Withdraw successful! New balance: Rs. " << users[userIndex].balance << endl;
    } else {
        cout << "Insufficient funds! Transaction declined." << endl;
    }
}

void fundTransfer() {
    string username;
    cout << "Enter your username: ";
    cin >> username;

    int fromUserIndex = findUserByUsername(username);
    if (fromUserIndex == -1) {
        cout << "User not found." << endl;
        return;
    }

    string password;
    cout << "Enter your password: ";
    cin >> password;

    if (!validatePassword(fromUserIndex, password)) {
        cout << "Invalid password!" << endl;
        return;
    }

    string recipientUsername;
    cout << "Enter the recipient's username: ";
    cin >> recipientUsername;

    int toUserIndex = findUserByUsername(recipientUsername);
    if (toUserIndex == -1) {
        cout << "Recipient user not found." << endl;
        return;
    }

    float transferAmount;
    cout << "Enter the amount to transfer: Rs. ";
    cin >> transferAmount;

    if (users[fromUserIndex].balance >= transferAmount) {
        users[fromUserIndex].balance -= transferAmount;
        users[toUserIndex].balance += transferAmount;
        cout << "Transfer successful! Your new balance: Rs. " << users[fromUserIndex].balance << endl;
        cout << "Recipient's new balance: Rs. " << users[toUserIndex].balance << endl;
    } else {
        cout << "Insufficient funds for the transfer." << endl;
    }
}

int main() {
    while (true) {
        displayMenu();

        int choice;
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1: openAccount(); break;
            case 2: showAccountInfo(); break;
            case 3: deposit(); break;
            case 4: withdraw(); break;
            case 5: fundTransfer(); break;
            case 6:
                cout << "Thank you for using our banking system!" << endl;
                return 0;
            default:
                cout << "Invalid choice! Please try again." << endl;
        }
    }
}

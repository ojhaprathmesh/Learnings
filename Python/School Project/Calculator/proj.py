import sys
import mysql.connector as sql

conn = sql.connect(host='localhost', user='root', password='Pr@thmesh2307')
cur = conn.cursor()
cur.execute("create database if not exists dental_management_system;")
print("Database created succefully")
conn = sql.connect(host='localhost', user='root', password='Pr@thmesh2307', database='dental_management_system')
cur.execute(
    'create table patient_record( Patient_Name varchar(50), Age int(3),Doctor_Conculted varchar(50),Address varchar(150),Phone_Number bigint(15));')
cur.execute(
    'create table salary_record( Employee_Name varchar(50),Proffession varchar(20),Salary_Amount varchar(9),Address varchar(150),Phone_Number bigint(15));')
cur.execute('create table accounts( User_Name varchar(20) primary key, password varchar(30) unique);')
print('Tables created successfully')
conn.commit()
user = input("Enter New User Name : ")
user = user.upper()
passwrd = input("Enter New Password : ")
passwrd = passwrd.upper()
cur.execute("insert into accounts values('" + user + "','" + passwrd + "');")
print("ACCOUNT ADDED SUCCEFULLY")
conn.commit()
if conn.is_connected:
    print("                             Dental Management System              ")
    print("1. Login")
    print("2. Exit")
    print()
    option = int(input("Enter your choise : "))
    if option == 1:
        print()
        user = input('User Name : ')
        user = user.upper()
        cur.execute("select * from accounts where User_Name like '" + user + "';")
        datas = cur.fetchall()
        for i in datas:
            value_1 = i[0]
            value_2 = i[1]
        if user == value_1:
            password = input('Password : ')
            password = password.upper()
            if password == value_2:
                print()
                print('Login succefull')
                print()
                print("1. Add Patients records")
                print("2. Add Salary records")
                print("3. Veiw Patient Detail")
                print("4. Delete patient detail")
                print()
                choise = int(input('Enter a  option : '))
                if choise == 1:
                    print()
                    name = input('Name : ')
                    name = name.upper()
                    age = int(input('Age : '))
                    doc = input('Doctor Consulted : ')
                    doc = doc.upper()
                    add = input('Address : ')
                    add = add.upper()
                    phone_no = int(input('Phone Number : '))
                    cur.execute("insert into patient_record values('" + name + "'," + str(
                        age) + ",'" + doc + "','" + add + "'," + str(phone_no) + ");")
                    conn.commit()
                    print('Record added')
                if choise == 2:
                    print()
                    emp_name = input('Employee_Name : ')
                    emp_name = emp_name.upper()
                    proffesion = input('Proffession : ')
                    proffesion = proffesion.upper()
                    salary = int(input('Salary Amount : '))
                    add = input('Address : ')
                    add = add.upper()
                    phone_no = input('Phone_Number : ')
                    cur.execute("insert into salary_record values('" + emp_name + "','" + proffesion + "'," + str(
                        salary) + ",'" + add + "'," + str(phone_no) + ");")
                    conn.commit()
                    print('Record added')
                if choise == 3:
                    print()
                    name = input('Name of the patient : ')
                    name = name.upper()
                    cur.execute("select  * from patient_record where patient_name like '" + str(name) + "';")
                    data = cur.fetchall()
                    if data != 0:
                        for row in data:
                            print()
                            print("Patient Details : ")
                            print()
                            print('Name : ', row[0])
                            print('Age : ', row[1])
                            print('Doctor consulted : ', row[2])
                            print('Address : ', row[3])
                            print('Phone Number : ', row[4])
                            input()
                    else:
                        print()
                        print("Patient Record Doesnot Exist")
                        print()
                    if choise == 4:
                        name = input('Name of the patient : ')
                        name = name.upper()
                        cur.execute("delete from patient_record where Patient_Name like '" + name + "';")
                        print('Record Deleted Succefully')
            else:
                print('Invalid Password')
                print('Tryagain')
    elif option == 2:
        sys.exit()
conn.commit()
input()

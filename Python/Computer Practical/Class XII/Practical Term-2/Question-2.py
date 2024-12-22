import mysql.connector as mc

db = mc.connect(host="localhost", user="root", password="Pr@thmesh2307")
cursor = db.cursor()
try:
    cursor.execute("USE School;")
    cursor.execute("DROP TABLE Student;")
    cursor.execute("CREATE TABLE Student (`Admission Number` int NOT NULL PRIMARY KEY, Name varchar(25) NOT NULL,\
                   Class varchar(20), Stream varchar(20), `Total Marks` int, Grade varchar(5))")
    db.commit()

except Exception as E:
    print(E)


def fetchData():
    try:
        cursor.execute("SELECT * FROM `Student`")
        results = cursor.fetchall()
        for x in results:
            print(x)
    except Exception as e:
        print(e)


def addData():
    try:
        cursor.execute("INSERT INTO `Student` VALUES(4000,'Sachin','12','Non-Medical',370,'B+')")
        cursor.execute("INSERT INTO `Student` VALUES(6000,'Harshita','12','Medical',445,'A')")
        cursor.execute("INSERT INTO `Student` VALUES(5050,'Tanishka','12','Medical',425,'A')")
        cursor.execute("INSERT INTO `Student` VALUES(7000,'Nishant','12','Computer-Science',425,'A+')")
        db.commit()
        print("Records Added")

    except Exception as e:
        print(e)


def updateData():
    try:
        sqlCommand = "UPDATE `Student` SET `Admission Number`= 5000 WHERE Name='Tanishka'"
        cursor.execute(sqlCommand)
        print("Record Updated")
        db.commit()

    except Exception as e:
        print(e)


def delData():
    try:
        sqlCommand = "DELETE FROM `Student` WHERE Name='Tanishka'"
        cursor.execute(sqlCommand)
        print("Record Deleted")
        db.commit()

    except Exception as e:
        print(e)


print('Operations:-\n\tF - Fetch\n\tA - Add\n\tU - Update\n\tD - Delete\n\tX - Exit')
while True:
    choice = input("Enter The Operation:- ")

    if choice.lower() == 'a':
        addData()
    elif choice.lower() == 'f':
        fetchData()
    elif choice.lower() == 'u':
        updateData()
    elif choice.lower() == 'd':
        delData()
    elif choice.lower() == 'x':
        break
    else:
        choice = input("Please Enter Correct Operation:- ")


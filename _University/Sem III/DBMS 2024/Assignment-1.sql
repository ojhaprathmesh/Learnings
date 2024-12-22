CREATE DATABASE CompanyDB;
USE CompanyDB;

CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    HireDate DATE,
    Salary DECIMAL
);

ALTER TABLE Employees
ADD DepartmentID INT;

ALTER TABLE Employees
MODIFY Salary FLOAT;

INSERT INTO Employees (EmployeeID, FirstName, LastName, HireDate, Salary, DepartmentID)
VALUES
    (1, 'John', 'Doe', '2024-01-01', 60000, 1),
    (2, 'Jane', 'Smith', '2024-02-01', 55000, 2),
    (3, 'Alice', 'Johnson', '2024-03-01', 60000, 3),
    (4, 'Bob', 'Brown', '2024-04-01', 45000, 4),
    (5, 'Emily', 'Davis', '2024-05-01', 70000, 5);

ALTER TABLE Employees
DROP COLUMN HireDate;

CREATE TABLE Departments (
    DepartmentID INT PRIMARY KEY,
    DepartmentName VARCHAR(50)
);

INSERT INTO Departments (DepartmentID, DepartmentName)
VALUES
    (1, 'Human Resources'),
    (2, 'Finance'),
    (3, 'Engineering'),
    (4, 'Marketing'),
    (5, 'Sales');

-- Alter the Employees table to add a foreign key constraint

ALTER TABLE Employees
ADD CONSTRAINT fk_Department
FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID);

RENAME TABLE Departments TO Dept;

UPDATE Employees
SET Salary = 65000
WHERE EmployeeID = 1;

DELETE FROM Employees
WHERE EmployeeID = 1;

SELECT * FROM Employees;

SELECT FirstName, LastName, Salary
FROM Employees
WHERE Salary > 50000;

DELETE FROM Employees
WHERE Salary < 40000;
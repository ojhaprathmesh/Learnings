CREATE DATABASE EmployeeDepartmentDB;
USE EmployeeDepartmentDB;

-- Create Department table (should be created first)
CREATE TABLE Departments (
    dept_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL
);

-- Create Employee table
CREATE TABLE Employees (
    emp_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_name VARCHAR(100) NOT NULL,
    dept_id INT,
    hire_date DATE NOT NULL,
    salary INT NOT NULL,
    mgr_id INT,
    FOREIGN KEY (dept_id)
        REFERENCES Departments (dept_id)
);

-- Insert data into Departments table
INSERT INTO Departments (dept_name)
VALUES
("HR"),
("Finance"),
("IT"),
("Marketing");

-- Insert data into Employees table
INSERT INTO Employees (emp_name, dept_id, hire_date, salary, mgr_id)
VALUES
("Alice", 1, "2015-06-01", 70000, 4),
("Bob", 2, "2017-08-15", 55000, 4),
("Charlie", 3, "2014-09-23", 50000, 5),
("David", 1, "2013-03-12", 90000, NULL),
("Eve", 2, "2019-11-10", 60000, NULL),
("Frank", NULL, "2021-04-19", 65000, 4);

SELECT e.emp_name "Name", d.dept_name "Department" FROM Employees e
JOIN Departments d ON e.dept_id = d.dept_id;

SELECT d.dept_name "Department", e.emp_name "Employee"
FROM Departments d
JOIN Employees e ON d.dept_id = e.dept_id;

SELECT e.emp_name "Employee", d.dept_name "Department"
FROM Employees e
LEFT JOIN Departments d ON e.dept_id = d.dept_id;

-- FULL OUTER JOIN NOT SUPPORTED

SELECT 
    e.emp_name 'Employee', d.dept_name 'Department'
FROM
    Employees e
        INNER JOIN
    Departments d ON e.dept_id = d.dept_id
WHERE
    d.dept_name = 'IT'
        AND e.hire_date > '2015-01-01';

SELECT d.dept_name "Department"
FROM Departments d
LEFT JOIN Employees e ON d.dept_id = e.dept_id
WHERE e.dept_id IS NULL;

SELECT d.dept_name "Department", SUM(e.salary) "Total Salary"
FROM Employees e
INNER JOIN Departments d ON e.dept_id = d.dept_id
GROUP BY d.dept_name;

-- FULL OUTER JOIN NOT SUPPORTED

SELECT d.dept_name "Department", AVG(e.salary) "Average Salary"
FROM Departments d
LEFT JOIN Employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_name;

SELECT d.dept_name "Department", SUM(e.salary) "Total Salary"
FROM Employees e
RIGHT JOIN Departments d ON e.dept_id = d.dept_id
GROUP BY d.dept_name;

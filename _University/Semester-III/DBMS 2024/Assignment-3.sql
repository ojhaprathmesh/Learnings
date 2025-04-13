CREATE DATABASE EmployeeProjectDB;
USE EmployeeProjectDB;

-- Create Employee table
CREATE TABLE Employee (
    emp_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary DECIMAL(10, 2 ) NOT NULL
);

-- Create Project table
CREATE TABLE Project (
    project_id INT PRIMARY KEY AUTO_INCREMENT,
    project_name VARCHAR(100) NOT NULL,
    budget DECIMAL(15, 2 ) NOT NULL
);

-- Create EmployeeProject table (junction table)
CREATE TABLE EmployeeProject (
    emp_id INT,
    project_id INT,
    hours_worked DECIMAL(5, 2 ) NOT NULL,
    PRIMARY KEY (emp_id , project_id),
    FOREIGN KEY (emp_id)
        REFERENCES Employee (emp_id),
    FOREIGN KEY (project_id)
        REFERENCES Project (project_id)
);

-- Insert data into Employee table
INSERT INTO Employee (emp_name, department, salary)
VALUES 
('John Doe', 'IT', 60000),
('Jane Smith', 'HR', 55000),
('Alice Johnson', 'Finance', 70000),
('Bob Brown', 'IT', 62000),
('Charlie Davis', 'HR', 58000),
('Diana Adams', 'Marketing', 54000),
('Eve White', 'IT', 64000),
('Frank Green', 'Finance', 72000),
('Grace Black', 'Marketing', 53000),
('Henry Blue', 'Finance', 68000);

-- Insert data into Project table
INSERT INTO Project (project_name, budget)
VALUES 
('Project Alpha', 100000),
('Project Beta', 150000),
('Project Gamma', 200000),
('Project Delta', 120000),
('Project Epsilon', 90000);

-- Insert data into EmployeeProject table
INSERT INTO EmployeeProject (emp_id, project_id, hours_worked)
VALUES 
(1, 1, 120),
(2, 2, 80),
(3, 3, 100),
(4, 1, 110),
(5, 4, 90),
(6, 5, 60),
(7, 2, 130),
(8, 3, 95),
(9, 4, 85),
(10, 5, 70);

SELECT * FROM Employee
WHERE department = 'IT';

SELECT SUM(salary) AS 'Total Salary', department FROM Employee
GROUP BY department;

SELECT department FROM Employee
GROUP BY department
HAVING SUM(salary) > 150000;

SELECT emp_id, emp_name FROM Employee
ORDER BY salary DESC
LIMIT 5;

SELECT DISTINCT e.emp_name FROM Employee e
JOIN EmployeeProject ep ON e.emp_id = ep.emp_id
JOIN Project p ON ep.project_id = p.project_id
WHERE p.project_name IN ('Project Alpha', 'Project Beta');

SELECT * FROM Project
WHERE budget BETWEEN 100000 AND 150000;

SELECT * FROM Employee
WHERE 
	(department = 'IT' AND salary > 60000)
    OR
    (department = 'HR' AND salary > 55000);

SELECT * FROM Employee
WHERE department != 'Marketing';

SELECT * FROM Employee
WHERE emp_name LIKE 'J%';

SELECT * FROM Project
WHERE project_name LIKE '%Alpha%';

SELECT * FROM Employee
WHERE emp_name NOT LIKE '%a%';

SELECT * FROM Project
WHERE budget IS NULL;

SELECT DISTINCT e.emp_name, e.salary FROM Employee e
JOIN EmployeeProject ep ON e.emp_id = ep.emp_id
JOIN Project p ON ep.project_id = p.project_id
WHERE p.project_name LIKE '%Epsilon%'
ORDER BY e.salary DESC
LIMIT 3;

SELECT * FROM Employee
ORDER BY salary DESC;

SELECT MIN(salary) AS 'Minimum Salary' FROM Employee;

SELECT DISTINCT e.emp_name, e.salary FROM Employee e
JOIN EmployeeProject ep ON e.emp_id = ep.emp_id
JOIN Project p ON ep.project_id = p.project_id
WHERE p.project_name LIKE '%Project%'
ORDER BY salary;

SELECT DISTINCT e.emp_name, e.salary FROM Employee e
JOIN EmployeeProject ep ON e.emp_id = ep.emp_id
JOIN Project p ON ep.project_id = p.project_id
WHERE p.project_name NOT LIKE '%Beta%';

SELECT DISTINCT e.emp_name FROM Employee e
JOIN EmployeeProject ep ON e.emp_id = ep.emp_id
JOIN Project p ON ep.project_id = p.project_id
WHERE p.budget > 100000 AND p.project_name LIKE '%Project%';

SELECT DISTINCT e.emp_name FROM Employee e
JOIN EmployeeProject ep ON e.emp_id = ep.emp_id
JOIN Project p ON ep.project_id = p.project_id
WHERE p.project_name LIKE 'P%';

SELECT e.emp_name FROM Employee e
JOIN EmployeeProject ep ON e.emp_id = ep.emp_id
JOIN Project p ON ep.project_id = p.project_id
WHERE p.project_name LIKE '%Project%'
GROUP BY e.emp_id, e.emp_name
HAVING COUNT(DISTINCT p.project_id) > 1;

SELECT emp_id, emp_name 
FROM Employee 
WHERE emp_id > 5 AND EXISTS (
    SELECT * FROM Project 
    WHERE budget > 120000
);

SELECT DISTINCT e.emp_name, e.salary FROM Employee e
WHERE EXISTS ( 
	SELECT 1 FROM EmployeeProject ep
	WHERE e.emp_id = ep.emp_id
    AND EXISTS (
		SELECT 1 FROM Project p
		WHERE ep.project_id = p.project_id
        AND p.project_name LIKE '%Project%'))
ORDER BY salary;

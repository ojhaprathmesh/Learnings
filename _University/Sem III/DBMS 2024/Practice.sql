USE EmployeeProjectDB; -- Assignment-3

SELECT * FROM Employee;

SELECT project_name FROM Project;

SELECT COUNT(emp_id) 'Total Employees' FROM Employee;

SELECT emp_name EmployeeName, Salary  FROM Employee
WHERE emp_name = 'Alice Johnson';

SELECT DISTINCT Department FROM Employee;

SELECT * FROM Employee
WHERE department = 'IT';

SELECT AVG(salary) 'Average Salary' FROM Employee;

CREATE DATABASE NormalizationDatabase;
USE NormalizationDatabase;

-- Create Employees Table
CREATE TABLE Employees (
    EmployeeID VARCHAR(5) PRIMARY KEY,
    EmployeeName VARCHAR(50) NOT NULL
);

-- Create Courses Table
CREATE TABLE Courses (
    CourseID VARCHAR(5) PRIMARY KEY,
    CourseTitle VARCHAR(50) NOT NULL,
    TrainerName VARCHAR(50) NOT NULL
);

-- Create Training Table
CREATE TABLE Training (
    TrainingID VARCHAR(5) PRIMARY KEY,
    EmployeeID VARCHAR(5),
    TrainingDate DATE,
    CourseID VARCHAR(5),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);

-- Insert into Employees Table
INSERT INTO Employees (EmployeeID, EmployeeName)
VALUES
('E001', 'John'),
('E002', 'Jane'),
('E003', 'Mike'),
('E004', 'Alice'),
('E005', 'Bob');

-- Insert into Courses Table
INSERT INTO Courses (CourseID, CourseTitle, TrainerName)
VALUES
('C101', 'Safety', 'Mr. Adams'),
('C102', 'Management', 'Ms. Roberts'),
('C103', 'Leadership', 'Ms. Lee'),
('C104', 'Teamwork', 'Mr. Green'),
('C105', 'Time Management', 'Ms. White');

-- Insert into Training Table
INSERT INTO Training (TrainingID, EmployeeID, TrainingDate, CourseID)
VALUES
('T001', 'E001', '2024-09-05', 'C101'),
('T002', 'E002', '2024-09-06', 'C102'),
('T003', 'E001', '2024-09-07', 'C103'),
('T004', 'E003', '2024-09-08', 'C101'),
('T005', 'E004', '2024-09-09', 'C104'),
('T006', 'E005', '2024-09-10', 'C105'),
('T007', 'E001', '2024-09-11', 'C101');

-- 1. Retrieve all training entries where the TrainingDate is after 2024-09-06. 
SELECT * FROM Training WHERE TrainingDate > '2024-09-06';

-- 2. Get the first 3 training records.
SELECT * FROM Training LIMIT 3;

-- 3. Find all employees who have attended either Safety or Management training.
SELECT e.EmployeeName, c.CourseTitle 
FROM Employees e 
JOIN Training t ON e.EmployeeID = t.EmployeeID
JOIN Courses c ON t.CourseID = c.CourseID
WHERE c.CourseTitle = 'Safety' OR c.CourseTitle = 'Management';

-- 4. Count the total number of trainings attended by all employees.
SELECT COUNT(*) AS TotalTrainings FROM Training;

-- 5. List employees who attended courses with IDs C101, C103, or C105.
SELECT e.EmployeeName 
FROM Employees e
JOIN Training t ON e.EmployeeID = t.EmployeeID
WHERE t.CourseID IN ('C101', 'C103', 'C105');

-- 6. Retrieve all training sessions between 2024-09-07 and 2024-09-10.
SELECT * FROM Training WHERE TrainingDate BETWEEN '2024-09-07' AND '2024-09-10';

-- 7. Find employees who attended all courses conducted by Mr. Adams.
SELECT e.EmployeeName
FROM Employees e
WHERE NOT EXISTS (
  SELECT c.CourseID FROM Courses c 
  WHERE c.TrainerName = 'Mr. Adams'
  AND c.CourseID NOT IN (
    SELECT t.CourseID FROM Training t WHERE t.EmployeeID = e.EmployeeID
  )
);

-- 8. Retrieve courses where at least one employee attended.
SELECT CourseTitle 
FROM Courses 
WHERE CourseID = ANY (SELECT CourseID FROM Training);

-- 9. Find all employees who haven't attended any training.
SELECT e.EmployeeName
FROM Employees e
LEFT JOIN Training t ON e.EmployeeID = t.EmployeeID
WHERE t.TrainingID IS NULL;

-- 10. Get courses that are not titled Safety.
SELECT * FROM Courses WHERE CourseTitle NOT LIKE 'Safety';

-- 11. Get the count of training sessions each employee has attended.
SELECT e.EmployeeName, COUNT(t.TrainingID) AS TrainingCount
FROM Employees e
JOIN Training t ON e.EmployeeID = t.EmployeeID
GROUP BY e.EmployeeName;

-- 12. Find employees who have attended more than one training session.
SELECT e.EmployeeName, COUNT(t.TrainingID) AS TrainingCount
FROM Employees e
JOIN Training t ON e.EmployeeID = t.EmployeeID
GROUP BY e.EmployeeName
HAVING COUNT(t.TrainingID) > 1;

-- 13. Find courses where the title contains the word Management.
SELECT * FROM Courses WHERE CourseTitle LIKE '%Management%';

-- 14. Find the name of the trainer who conducted the most recent training.
SELECT TrainerName
FROM Courses
WHERE CourseID = (SELECT CourseID FROM Training ORDER BY TrainingDate DESC LIMIT 1);

-- 15. Get a list of all unique employees who have attended any training.
SELECT DISTINCT e.EmployeeName 
FROM Employees e
JOIN Training t ON e.EmployeeID = t.EmployeeID;

-- 16. List all training sessions in order of the training date.
SELECT * FROM Training ORDER BY TrainingDate;

-- 17. Get a list of all training sessions along with the employee name and course title.
SELECT t.TrainingID, e.EmployeeName, c.CourseTitle
FROM Training t
JOIN Employees e ON t.EmployeeID = e.EmployeeID
JOIN Courses c ON t.CourseID = c.CourseID;

-- 18. List all employees along with the course title they attended (if any).
SELECT e.EmployeeName, c.CourseTitle 
FROM Employees e
LEFT JOIN Training t ON e.EmployeeID = t.EmployeeID
LEFT JOIN Courses c ON t.CourseID = c.CourseID;

-- 19. Count the number of distinct courses attended by John.
SELECT 
    COUNT(DISTINCT t.CourseID) AS DistinctCourses
FROM
    Training t
        JOIN
    Employees e ON t.EmployeeID = e.EmployeeID
WHERE
    e.EmployeeName = 'John';

-- 20. List all employee names and trainer names (no duplicates).
SELECT EmployeeName FROM Employees
UNION
SELECT TrainerName FROM Courses;

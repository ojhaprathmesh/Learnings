USE adventureworks;

SELECT * FROM salesperson;
SELECT * FROM store;
SELECT * FROM salesorderdetail;
SELECT * FROM product;
SELECT * FROM customer;
SELECT * FROM transactionhistory;
SELECT * FROM emplodepartmentyee;
SELECT * FROM department;

-- For each manager list managerid, employeeid , title of the employee they manage
-- For each customer count the number of sales ordered they have made  

SELECT * FROM salesperson sp
NATURAL JOIN store s;

SELECT 
    *
FROM
    salesperson sp
        INNER JOIN
    store s ON s.SalesPersonID = sp.SalesPersonID
ORDER BY s.customerID;

SELECT 
    *
FROM
    salesperson sp
        LEFT JOIN
    store s ON s.SalesPersonID = sp.SalesPersonID
ORDER BY s.customerID;

SELECT 
    *
FROM
    salesperson sp
        RIGHT JOIN
    store s ON s.SalesPersonID = sp.SalesPersonID
ORDER BY s.customerID;
"""
USE school;
CREATE TABLE `books` (BookID varchar(5) PRIMARY KEY NOT NULL, BookName varchar(25) NOT NULL, AuthorName varchar(20), Publishers varchar(20), Price int, Type varchar(20), Qty int);
INSERT INTO books VALUES ('k0001', 'Let Us C', 'Sanjay Mukharjee', 'EPB', 450, 'Computer', 15);
INSERT INTO books VALUES ('p0001', 'Genuine', 'J.Mukhi', 'FIRST PUBL.', 755, 'Fiction', 24);
INSERT INTO books VALUES ('m0001', 'Mastering C++', 'Kankar', 'EPB', 165, 'Computer', 60);
INSERT INTO books VALUES ('n0002', 'VC++ Advance', 'P.Purohit', 'TDH', 250, 'Computer', 45);
INSERT INTO books VALUES ('k0002', 'Programming With Python', 'Sanjeev', 'FIRST PUBL.', 350, 'Fiction', 30);
SELECT * FROM books;
CREATE TABLE `issued` (BookID varchar(5), QtyIssued int);
INSERT INTO issued VALUES ('L02', 13);
INSERT INTO issued VALUES ('L04', 5);
INSERT INTO issued VALUES ('L05', 21);
SELECT * FROM issued;
SELECT * FROM books WHERE Publishers = 'FIRST PUBL.' AND AuthorName = 'P.Purohit';
SELECT * FROM books WHERE Publishers = 'FIRST PUBL.';
SELECT * FROM books;
UPDATE books SET PRICE=PRICE*95/100 WHERE Publishers = 'EPB';
SELECT * FROM books;
SELECT Type, SUM(Qty) AS TotalQty, SUM(Qty*Price) AS TotalPrice FROM books GROUP BY Type;
SET @MaxPrice = (SELECT MAX(Price) FROM books);
SELECT * FROM books WHERE Price= @MaxPrice;

"""

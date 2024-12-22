"""
USE school;
CREATE TABLE `store` (ItemNo int PRIMARY KEY NOT NULL, Item varchar(25) NOT NULL, Scode int, Qty int, Rate int, LastBuy date);
INSERT INTO store VALUES (2005, 'Sharpener Classic', 23, 60, 8, '2019-06-06');
INSERT INTO store VALUES (2003, 'Ball Pen 0.25', 22, 50, 25, '2020-02-01');
INSERT INTO store VALUES (2002, 'Gel Pen Premium', 21, 150, 12, '2000-02-24');
INSERT INTO store VALUES (2006, 'Gel Pen Classic', 21, 250, 20, '2019-03-11');
INSERT INTO store VALUES (2001, 'Eraser Small', 22, 220, 6, '2019-01-19');
INSERT INTO store VALUES (2004, 'Eraser Big', 22, 110, 8, '2019-12-2');
INSERT INTO store VALUES (2009, 'Ball Pen 0.5', 21, 180, 18, '2019-11-03');
SELECT * FROM store;
CREATE TABLE `suppliers` (Scode int, Sname varchar(25));
INSERT INTO suppliers VALUES (21, 'Premium Stationary');
INSERT INTO suppliers VALUES (23, 'Soft Plastics');
INSERT INTO suppliers VALUES (22, 'Tetra Supply');
SELECT * FROM suppliers;
SELECT * FROM store ORDER BY LastBuy;
SELECT * FROM store WHERE Rate > 15;
SELECT * FROM store WHERE Scode = 22 OR Qty >= 110;
SELECT Scode, MIN(Rate) FROM store GROUP BY Scode ORDER BY Scode;
SELECT COUNT(DISTINCT Scode) FROM store;
SELECT Rate*Qty FROM store WHERE ItemNo = 2004;
SELECT Item, Sname FROM store S, suppliers P
WHERE S.Scode = P.Scode AND ItemNo = 2006;
SELECT MAX(LastBuy) FROM Store;

"""

import mysql.connector as mc

db = mc.connect(host="localhost", user="root", password="Pr@thmesh2307")
cursor = db.cursor()
cursor.execute("USE School;")


def fetchData():
    try:
        cursor.execute("SELECT MAX(LastBuy) FROM store;")
        results = cursor.fetchall()
        for x in results:
            print(f'LastOrder Date:- {x[0]}')
    except Exception as e:
        print(e)


fetchData()

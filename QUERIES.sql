use group28_db;

#### QUERY 1 ####
SELECT C.branch_name, B.author, COUNT(DISTINCT O.reader_email) AS Amount_Of_Distinct_Readers
FROM Order_book AS O
LEFT JOIN Copies AS C 
	ON O.copy_id = C.copy_id
LEFT JOIN Book AS B 
	ON B.book_id = C.book_id
WHERE O.order_date >= DATE_ADD(NOW(), INTERVAL - 1 YEAR)
GROUP BY C.branch_name , B.author
ORDER BY 3 DESC;
  
  
#### QUERY 2 ####
SELECT O.reader_email, AVG(DATEDIFF(B2.date_of_borrowing, O.order_date)) AS AVG_days_order_to_borrow
FROM Order_book AS O
LEFT JOIN Borrow AS B1 
	ON O.request_id = B1.request_id
LEFT JOIN Borrow AS B2 
	ON B2.copy_id = O.copy_id
	AND B2.reader_email = O.reader_email
	AND B2.date_of_borrowing BETWEEN B1.returned_date AND DATE_ADD(B1.returned_date, INTERVAL 3 DAY)
WHERE B2.date_of_borrowing IS NOT NULL
GROUP BY O.reader_email;

#### QUERY 3 ####
SELECT C.branch_name, B.reader_email, AVG(DATEDIFF(B.extension_date, B.date_of_borrowing)) AS AVG_days_borrow_to_extention
FROM Borrow AS B
LEFT JOIN Copies AS C 
	ON B.copy_id = C.copy_id
WHERE B.extension_date IS NOT NULL
GROUP BY C.branch_name , B.reader_email # reader_emailnot required - just to make the table more readable
order by C.branch_name; # not required - just to make the table more readable 

#### QUERY 4####
SELECT C.branch_name, AVG(DATEDIFF(B2.date_of_borrowing, O.order_date)) AS AVG_days_order_to_borrow
FROM Order_book AS O
LEFT JOIN Copies as C
	ON C.copy_id = O.copy_id
LEFT JOIN Borrow AS B1 
	ON O.request_id = B1.request_id
LEFT JOIN Borrow AS B2 
	ON B2.copy_id = O.copy_id
	AND B2.reader_email = O.reader_email
	AND B2.date_of_borrowing BETWEEN B1.returned_date AND DATE_ADD(B1.returned_date, INTERVAL 3 DAY)
WHERE B2.date_of_borrowing IS NOT NULL
GROUP BY C.branch_name;


#### QUERY 5 ####
WITH calc_of_borrow AS(
SELECT reader_email, (count(request_id)/12) AS Monthly_Borrows_AVG, (count(extension_date)/12) AS Monthly_Extensions_AVG
FROM Borrow 
WHERE date_of_borrowing >= DATE_ADD(NOW(), INTERVAL - 1 YEAR)
GROUP BY reader_email
),
calc_of_orders AS (
SELECT reader_email, (count(*)/12) AS Monthly_Orders_AVG 
FROM Order_book 
WHERE order_date >= DATE_ADD(NOW(), INTERVAL - 1 YEAR)
GROUP BY reader_email
)
SELECT B.reader_email, B.Monthly_Borrows_AVG, B.Monthly_Extensions_AVG, 
	CASE WHEN O.Monthly_Orders_AVG IS NULL THEN 0 ELSE O.Monthly_Orders_AVG END AS Monthly_Orders_AVG 
FROM calc_of_borrow AS B
LEFT JOIN calc_of_orders AS O
ON B.reader_email = O.reader_email;




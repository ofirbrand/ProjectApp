use group28_db;

INSERT INTO Branch (branch_name, phone_number) VALUES
('City Center', 1123456),
('Ramat Aviv', 9983456);

INSERT INTO Branch_address (city, street, house_number, branch_name) VALUES
('Tel Aviv','Arlozerov', 120, 'City Center'),
('Tel Aviv', 'Einstein', 25, 'Ramat Aviv');

INSERT INTO Librarian (phone_number, librarian_email, full_name, librarian_password, begin_work_date, branch_name) VALUES
(878734, 'moshe@mail.com', 'moshe cohen','1111', '2019-06-26', 'City Center'),
(878734, 'david@mail.com', 'David Levy','1111', '2121-03-12', 'Ramat Aviv');

INSERT INTO Librarian_address (city, street, house_number, librarian_email) VALUES
('Tel Aviv', 'Arlozerov', 23,'moshe@mail.com'),
('Tel Aviv', 'Dizingof', 100,'david@mail.com');


INSERT into Reader(phone_number, reader_email, full_name, reader_password, date_of_birth) VALUES
(526738977, "ofir@gmail.com", 'Ofir Brand', 1111, '1995-08-22'),
(833274864, 'amit@gmail.com', 'Amit Meyron', 1111, '2000-04-17'),
(528390987, 'doron@gmail.com', "Doron Dahan", 1234, "1995-10-02"),
(632898880, 'nofar@gmail.com', "Nofar Wagner", 1234, "1996-09-24"),
(536789767, 'Tal@gmail.com', "Tal Eliram", 1234, "1996-06-27"),
(765890868, 'avi@gmail.com', "avi shalom", 1234, '1959-09-08'),
(999948373, 'soonil@gmai.com', "Soonil giaro", 1234, '1979-07-01'),
(333303827, 'roby@gmai.com', "roby gordon", 1234, '1979-07-18'),
(339873827, 'lior@gmai.com', "lior atedgi", 1234, '1979-01-28'),
(333301037, 'tomer@gmai.com', "tomer vernik", 1234, '1979-07-01'),
(333303827, 'devin@gmai.com', "devin booker", 1234, '1979-09-01');


INSERT INTO Reader_address (city, street, house_number, reader_email) VALUES
('Tel Aviv', 'King Georg', 62,'ofir@gmail.com'),
('Hod Hasharon', 'Ben Gurion', 100,'amit@gmail.com'),
('lod', 'Herzel', 100,'doron@gmail.com'),
('lod', 'Hapaamonin', 122,'nofar@gmail.com'),
('Tel Aviv', 'Ben Shitrit', 194,'Tal@gmail.com'),
('Gdera', 'Zakay', 43,'avi@gmail.com'),
('Kathmandu', 'Thamel', 45,'soonil@gmail.com'),
('Los Angeles', 'Star', 92,'roby@gmail.com'),
('Ashkelon', 'Hadror', 32,'lior@gmail.com'),
('Ramat Hasharon', 'Halotus', 04,'tomer@gmail.com'),
('Raanana', 'Klausner', 38,'devin@gmail.com');


-- BOOKS
INSERT INTO Book (book_name, author, publisher, publish_year) VALUES
('Harry Potter And The Philosophers Stone', 'J.K.Rowling', 'Bloomsbury', '1997-06-26'),
('Harry Potter And The Goblet Of Fire', 'J.K.Rowling', 'Bloomsbury', '2000-07-08'),
('Parnassus On Wheels', 'Christopher Morley', '	Doubleday', '1917-03-12'),
('Night', 'Elie Wiesel', 'Central Union of Polish Jews in Argentina', '1956-01-01'),
('Thinking, Fast And Slow', 'Daniel Kahneman', 'Farrar, Straus and Giroux', '2011-01-01'),
('My Michael', 'Amos Oz', 'Keter' , '1968-02-01'),
('Life Plays With Me', 'David Grossman', 'Hakibutz Hameuchad', '2019-03-12'),
('The Hunger Games', 'Suzanne Collins', 'Scholastic', '2008-03-12');

-- COPIES
INSERT INTO Copies (Book_id, branch_name, amount, copy_status) VALUES
(1, 'City Center', 2 , 'available'),
(2, 'City Center', 2 , 'available'),
(3, 'City Center', 2 , 'available'),
(4, 'City Center', 2, 'available'),
(5, 'City Center', 2 , 'available'),
(6, 'City Center', 2 , 'available'),
(7, 'City Center', 2 , 'available'),
(8, 'City Center', 2 , 'available'),
(1, 'Ramat Aviv', 2 , 'available'),
(2, 'Ramat Aviv', 2 , 'available'),
(3, 'Ramat Aviv', 2 , 'available'),
(4, 'Ramat Aviv', 2 , 'available'),
(5, 'Ramat Aviv', 2 , 'available'),
(6,'Ramat Aviv', 2 , 'available'),
(7, 'Ramat Aviv', 2 , 'available'),
(8, 'Ramat Aviv', 2 , 'available');

############# REGULAR BORROWS ###############
INSERT INTO Borrow (date_of_borrowing, status_of_request, copy_id, reader_email, returned_date) VALUES
("2021-03-01", 'returned', 1, "doron@gmail.com", "2021-03-08"),                 
("2022-04-02", 'returned', 1, "amit@gmail.com", "2022-04-10"),                 
("2020-05-03", 'returned', 1, "ofir@gmail.com", "2020-05-11"),                 
("2019-10-04", 'returned', 15, "tal@gmail.com", "2019-10-06"),                 
("2022-07-15", 'returned', 3, "nofar@gmail.com", "2022-07-21"),                 
("2022-01-06", 'returned', 5, "lior@gmail.com", "2022-01-18"),                 
("2022-08-07", 'returned', 7, "doron@gmail.com", "2022-08-15"),                 
("2022-05-08", 'returned', 9, "amit@gmail.com", "2022-05-11"),                 
("2020-09-09", 'returned', 2, "devin@gmail.com", "2020-09-20"),                 
("2018-01-10", 'returned', 19, "amit@gmail.com", "2018-01-22"),                 
("2021-01-11", 'returned', 2, "tal@gmail.com", "2022-01-25"),                
("2022-01-12", 'returned', 1, "ofir@gmail.com", "2022-01-19"),                 
("2020-01-13", 'returned', 3, "soonil@gmail.com", "2020-01-24"),                 
("2020-05-14", 'returned', 1, "amit@gmail.com", "2020-05-22"),                 
("2020-01-15", 'returned', 1, "doron@gmail.com", "2020-01-26"),                 
("2021-02-16", 'returned', 3, "nofar@gmail.com", "2021-02-28"),                 
("2021-04-17", 'returned', 4, "tomer@gmail.com", "2021-04-24"),                 
("2021-10-18", 'returned', 5, "roby@gmail.com", "2021-10-25"),                 
("2021-12-05", 'returned', 6, "avi@gmail.com", "2021-12-13"),                 
("2019-01-07", 'returned', 12, "tomer@gmail.com", "2019-01-16"),                 
("2019-03-01", 'returned', 16, "roby@gmail.com", "2019-03-09"),                
("2022-07-10", 'returned', 11, "devin@gmail.com", "2022-07-18"),                 
("2022-03-11", 'returned', 1, "nofar@gmail.com", "2022-03-20"),                 
("2022-09-03", 'returned', 2, "tal@gmail.com", "2022-09-11"),                 
("2022-07-23", 'returned', 5, "soonil@gmail.com", "2022-07-29"),                 
("2022-01-29", 'returned', 13, "lior@gmail.com", "2022-02-06"),                 
("2021-11-16", 'returned', 7, "avi@gmail.com", "2021-11-26"),                 
("2022-04-24", 'returned', 1, "lior@gmail.com", "2022-05-01");



############# EXTENSIONS ###############
INSERT INTO Borrow (date_of_borrowing, status_of_request, copy_id, reader_email, returned_date, extension_date) VALUES
("2022-10-01", 'returned', 2, "doron@gmail.com", "2022-10-19", "2022-10-13"),
("2022-10-02", 'returned', 17, "ofir@gmail.com", "2022-10-18", "2022-10-10"),
("2022-10-01", 'returned', 13, "nofar@gmail.com", "2022-10-20", "2022-10-11"),                 
("2022-10-03", 'returned', 4, "tomer@gmail.com", "2022-10-17", "2022-10-08"),                 
("2022-10-04", 'returned', 9, "roby@gmail.com", "2022-10-23", "2022-10-15"),
("2022-12-20", 'returned', 14, "roby@gmail.com", "2023-01-01", "2023-01-01"), ### happened from december 22 until january 23
("2022-12-02", 'returned', 3, "ofir@gmail.com", "2022-12-21", "2022-12-10");  ### happened in december 22



############# FRIRST SESSION OF BORROW - ORDER INSERTIONS: ###############
####### inserts of first borrow to make orders
INSERT INTO Borrow (date_of_borrowing, status_of_request, copy_id, reader_email, returned_date) VALUES
("2022-10-01", 'returned', 19, "doron@gmail.com", "2022-10-12"),
("2022-10-02", 'returned', 21, "ofir@gmail.com", "2022-10-14"),
("2022-10-01", 'returned', 22, "nofar@gmail.com", "2022-10-09"),                 
("2022-10-03", 'returned', 23, "tomer@gmail.com", "2022-10-15"),
("2022-11-09", 'returned', 19, "devin@gmail.com", "2022-11-16"), 
("2022-11-08", 'returned', 21, "roby@gmail.com", "2022-11-11"), 
("2022-11-02", 'returned', 22, "lior@gmail.com", "2022-11-13"),                
("2022-11-03", 'returned', 23, "doron@gmail.com", "2022-11-11");

##### insert of order
INSERT INTO Order_book (copy_id, request_id, reader_email, order_status, order_date, returned_date) VALUES
(19, 48, 'amit@gmail.com', 'orderable', '2022-10-7', '2022-10-12'),
(21, 49, 'avi@gmail.com', 'orderable', '2022-10-12', '2022-10-14'),
(22, 50, 'soonil@gmail.com', 'orderable', '2022-10-08', '2022-10-09'),
(23, 51, 'Tal@gmail.com', 'orderable', '2022-10-10', '2022-10-15'),
(19, 52, 'ofir@gmail.com', 'orderable', '2022-11-12', '2022-11-16'),
(21, 53, 'nofar@gmail.com', 'orderable', '2022-11-09', '2022-11-11'),
(22, 54, 'roby@gmail.com', 'orderable', '2022-11-10', '2022-11-13'),
(23, 55, 'amit@gmail.com', 'orderable', '2022-11-05', '2022-11-11'); 


####### inserts of seconed borrow to make orders
INSERT INTO Borrow (date_of_borrowing, status_of_request, copy_id, reader_email, returned_date) VALUES
("2022-10-13", 'returned', 19, "amit@gmail.com", "2022-10-19"),
("2022-10-16", 'returned', 21, "avi@gmail.com", "2022-10-22"),
("2022-10-09", 'returned', 22, "soonil@gmail.com", "2022-10-22"),                 
("2022-10-17", 'returned', 23, "Tal@gmail.com", "2022-10-26"),
("2022-11-18", 'returned', 19, "ofir@gmail.com", "2022-11-27"), 
("2022-11-12", 'returned', 21, "nofar@gmail.com", "2022-11-15"),
("2022-11-13", 'returned', 22, "roby@gmail.com", "2022-11-19"),                
("2022-11-17", 'returned', 23, "ofir@gmail.com", "2022-11-25");
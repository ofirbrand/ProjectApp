use group28_db;

drop table if exists Branch;
CREATE TABLE Branch
(
  branch_name VARCHAR(30) NOT NULL,
  phone_number VARCHAR(15) NOT NULL,
  PRIMARY KEY (branch_name)
);

drop table if exists Reader;
CREATE TABLE Reader
(
phone_number INT NOT NULL,
reader_email VARCHAR(50) NOT NULL,
full_name VARCHAR(50) NOT NULL,
reader_password VARCHAR(50) NOT NULL,
date_of_birth DATE NOT NULL,
PRIMARY KEY (reader_email)
);

drop table if exists Librarian;
CREATE TABLE Librarian
(
  phone_number INT NOT NULL,
  librarian_email VARCHAR(50) NOT NULL,
  full_name VARCHAR(50) NOT NULL,
  librarian_password VARCHAR(50) NOT NULL,
  begin_work_date DATE NOT NULL,
  branch_name VARCHAR(30) NOT NULL,
  PRIMARY KEY (librarian_email),
  FOREIGN KEY (branch_name) REFERENCES Branch(branch_name)
);


drop table if exists Reader_address;
CREATE TABLE Reader_address
(
  city VARCHAR(50) NOT NULL,
  street VARCHAR(50) NOT NULL,
  house_number INT NOT NULL,
  reader_email VARCHAR(50) NOT NULL,
  PRIMARY KEY (city, street, house_number, reader_email),
  FOREIGN KEY (reader_email) REFERENCES Reader(reader_email)
);

drop table if exists Librarian_address;
CREATE TABLE Librarian_address
(
  city VARCHAR(50) NOT NULL,
  street VARCHAR(50) NOT NULL,
  house_number INT NOT NULL,
  librarian_email VARCHAR(50) NOT NULL,
  PRIMARY KEY (city, street, house_number, librarian_email),
  FOREIGN KEY (librarian_email) REFERENCES Librarian(librarian_email)
);

drop table if exists Branch_address;
CREATE TABLE Branch_address
(
  city VARCHAR(50) NOT NULL,
  street VARCHAR(50) NOT NULL,
  house_number INT NOT NULL,
  branch_name VARCHAR(30) NOT NULL,
  PRIMARY KEY (city, street, house_number, branch_name),
  FOREIGN KEY (branch_name) REFERENCES Branch(branch_name)
);


drop table if exists Book;
CREATE TABLE Book
(
  book_id INT AUTO_INCREMENT,
  book_name VARCHAR(100) NOT NULL,
  author VARCHAR(100) NOT NULL,
  publisher VARCHAR(100) NOT NULL,
  publish_year YEAR NOT NULL,
  PRIMARY KEY (book_id)
);

drop table if exists Copies;
CREATE TABLE Copies
(
  copy_id INT AUTO_INCREMENT,
  book_id INT NOT NULL,
  branch_name VARCHAR(30) NOT NULL,
  amount INT NOT NULL,
  copy_status VARCHAR(15) NOT NULL,
  PRIMARY KEY (copy_id),
  FOREIGN KEY (branch_name) REFERENCES Branch(branch_name),
  FOREIGN KEY (book_id) REFERENCES Book(book_id)
);


drop table if exists Borrow;
CREATE TABLE Borrow
(
  request_id INT AUTO_INCREMENT,
  date_of_borrowing DATE,
  status_of_request VARCHAR(20) NOT NULL,
  copy_id INT NOT NULL,
  reader_email VARCHAR(50) NOT NULL,
  returned_date DATE,
  PRIMARY KEY (request_id),
  FOREIGN KEY (copy_id) REFERENCES Copies(copy_id),
  FOREIGN KEY (reader_email) REFERENCES Reader(reader_email)
);


drop table if exists Order_book;
CREATE TABLE Order_book
(
  copy_id INT NOT NULL,
  request_id INT NOT NULL,
  reader_email VARCHAR(50) NOT NULL,
  order_status VARCHAR(20) NOT NULL,
  returned_date date,
  PRIMARY KEY (reader_email, copy_id, request_id),
  FOREIGN KEY (reader_email) REFERENCES Reader(reader_email),
  FOREIGN KEY (copy_id) REFERENCES Copies(copy_id),
  FOREIGN KEY (request_id) REFERENCES Borrow(request_id)
);

-- INSERT INTO Branch (branch_name, phone_number) VALUES
-- ('City Center', 1123456),
-- ('Ramat Aviv', 9983456);

-- INSERT INTO Branch_address (city, street, house_number, branch_name) VALUES
-- ('Tel Aviv','Arlozerov', 120, 'City Center'),
-- ('Tel Aviv', 'Einstein', 25, 'Ramat Aviv');

-- INSERT INTO Librarian (phone_number, librarian_email, full_name, librarian_password, begin_work_date, branch_name) VALUES
-- (878734, 'moshe@mail.com', 'moshe cohen','1111', '2019-06-26', 'City Center'),
-- (878734, 'david@mail.com', 'David Levy','1111', '2121-03-12', 'Ramat Aviv');

-- INSERT INTO Librarian_address (city, street, house_number, librarian_email) VALUES
-- ('Tel Aviv', 'Arlozerov', 23,'moshe@mail.com'),
-- ('Tel Aviv', 'Dizingof', 100,'david@mail.com');


-- INSERT into Reader(phone_number, reader_email, full_name, reader_password, date_of_birth) VALUES
-- (526738977, "ofir@gmail.com", 'Ofir Brand', 1111, '1995-08-22'),
-- (833274864, 'amit@gmail.com', 'Amit Meyron', 1111, '2000-04-17'),
-- (528390987, 'doron@gmail.com', "Doron Dahan", 1234, "1995-10-02"),
-- (632898880, 'nofar@gmail.com', "Nofar Wagner", 1234, "1996-09-24"),
-- (536789767, 'Tal@gmail.com', "Tal Eliram", 1234, "1996-06-27"),
-- (765890868, 'avi@gmail.com', "avi shalom", 1234, '1959-09-08'),
-- (999948373, 'soonil@gmai.com', "Soonil giaro", 1234, '1979-07-01'),
-- (333303827, 'roby@gmai.com', "roby gordon", 1234, '1979-07-18'),
-- (339873827, 'lior@gmai.com', "lior atedgi", 1234, '1979-01-28'),
-- (333301037, 'tomer@gmai.com', "tomer vernik", 1234, '1979-07-01'),
-- (333303827, 'devin@gmai.com', "devin booker", 1234, '1979-09-01');

INSERT INTO Reader_address (city, street, house_number, reader_email) VALUES
('Tel Aviv', 'King Georg', 62,'ofir@gmail.com'),
('Hod Hasharon', 'Ben Gurion', 100,'amit@gmail.com');

-- BOOKS
-- INSERT INTO Book (book_name, author, publisher, publish_year) VALUES
-- ('Harry Potter And The Philosophers Stone', 'J.K.Rowling', 'Bloomsbury', year('1997-06-26')),
-- ('Harry Potter And The Goblet Of Fire', 'J.K.Rowling', 'Bloomsbury', year('2000-07-08')),
-- ('Parnassus On Wheels', 'Christopher Morley', '	Doubleday', year('1917-03-12')),
-- ('Night', 'Elie Wiesel', 'Central Union of Polish Jews in Argentina', year('1956-01-01')),
-- ('Thinking, Fast And Slow', 'Daniel Kahneman', 'Farrar, Straus and Giroux', year('2011-01-01')),
-- ('My Michael', 'Amos Oz', 'Keter' , year('1968-02-01')),
-- ('Life Plays With Me', 'David Grossman', 'Hakibutz Hameuchad', year('2019-03-12'));

-- COPIES
-- INSERT INTO Copies (Book_id, branch_name, amount, copy_status) VALUES
-- (1, 'City Center', 1 , 'available'),
-- (2, 'City Center', 3 , 'available'),
-- (3, 'City Center', 1 , 'available'),
-- (4, 'City Center', 3, 'available'),
-- (5, 'City Center', 2 , 'available'),
-- (6, 'City Center', 2 , 'available'),
-- (7, 'City Center', 1 , 'available'),
-- (8, 'City Center', 1 , 'available'),
-- (1, 'Ramat-Aviv', 1 , 'available'),
-- (2, 'Ramat-Aviv', 2 , 'available'),
-- (3, 'Ramat-Aviv', 2 , 'available'),
-- (4, 'Ramat-Aviv', 1 , 'available'),
-- (5, 'Ramat-Aviv', 3 , 'available'),
-- (6,'Ramat-Aviv', 1 , 'available'),
-- (7, 'Ramat-Aviv', 2 , 'available'),
-- (8, 'Ramat-Aviv', 1 , 'available');



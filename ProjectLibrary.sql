CREATE DATABASE IF NOT EXISTS `ProjectLibraries`;

USE ProjectLibraries;

CREATE TABLE Reader
(
phone_number INT NOT NULL,
reader_email VARCHAR(50) NOT NULL,
full_name VARCHAR(50) NOT NULL,
reader_password VARCHAR(50) NOT NULL,
date_of_birth DATE NOT NULL,
PRIMARY KEY (reader_email)
);

CREATE TABLE Branch
(
  branch_name VARCHAR(30) NOT NULL,
  phone_number VARCHAR(15) NOT NULL,
  PRIMARY KEY (branch_name)
);

insert into Branch(branch_name, phone_number) values
('Ramat Aviv', '097496104'),
('City Center', '097496667'),
('Kerem Hateimanim', '097696110')
;

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

-- drop table if exists Book;
CREATE TABLE Book
(
  book_id INT AUTO_INCREMENT,
  book_name VARCHAR(100) NOT NULL,
  author VARCHAR(100) NOT NULL,
  publisher VARCHAR(100) NOT NULL,
  publish_year DATE NOT NULL,
  PRIMARY KEY (book_id)
);

CREATE TABLE Reader_address
(
  city VARCHAR(50) NOT NULL,
  street VARCHAR(50) NOT NULL,
  house_number INT NOT NULL,
  reader_email VARCHAR(50) NOT NULL,
  PRIMARY KEY (city, street, house_number, reader_email),
  FOREIGN KEY (reader_email) REFERENCES Reader(reader_email)
);

CREATE TABLE Librarian_address
(
  city VARCHAR(50) NOT NULL,
  street VARCHAR(50) NOT NULL,
  house_number INT NOT NULL,
  librarian_email VARCHAR(50) NOT NULL,
  PRIMARY KEY (city, street, house_number, librarian_email),
  FOREIGN KEY (librarian_email) REFERENCES Librarian(librarian_email)
);

CREATE TABLE Branch_address
(
  city VARCHAR(50) NOT NULL,
  street VARCHAR(50) NOT NULL,
  house_number INT NOT NULL,
  branch_name VARCHAR(30) NOT NULL,
  PRIMARY KEY (city, street, house_number, branch_name),
  FOREIGN KEY (branch_name) REFERENCES Branch(branch_name)
);

-- drop table if exists Borrow;
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

-- drop table if exists Copies;
CREATE TABLE Copies
(
  copy_id INT AUTO_INCREMENT,
  book_id INT NOT NULL,
  branch_name VARCHAR(30) NOT NULL,
  amount INT NOT NULL,
  copy_status VARCHAR(15) NOT NULL,
  PRIMARY KEY (copy_id),
  FOREIGN KEY (branch_name) REFERENCES Branch(branch_name),
  FOREIGN KEY (book_id) REFERENCES book(book_id)
);

-- drop table if exists Order_book;
CREATE TABLE Order_book
(
  copy_id INT NOT NULL,
  request_id INT NOT NULL,
  reader_email VARCHAR(50) NOT NULL,
  order_status VARCHAR(20) NOT NULL,
  returned_date date,
  PRIMARY KEY (reader_email, copy_id, request_id),
  FOREIGN KEY (reader_email) REFERENCES Reader(reader_email),
  FOREIGN KEY (copy_id) REFERENCES copies(copy_id),
  FOREIGN KEY (request_id) REFERENCES Borrow(request_id)
);

-- INSERT INTO Book (book_name, author, publisher, publish_year) VALUES
-- ('Harry Potter And The Philosophers Stone', 'J.K.Rowling', 'Bloomsbury', '1997-06-26'),
-- ('Harry Potter And The Goblet Of Fire', 'J.K.Rowling', 'Bloomsbury', '2000-07-08'),
-- ('Parnassus On Wheels', 'Christopher Morley', '	Doubleday', '1917-03-12'),
-- ('Night', 'Elie Wiesel', 'Central Union of Polish Jews in Argentina', '1956-01-01'),
-- ('Thinking, Fast And Slow', 'Daniel Kahneman', 'Farrar, Straus and Giroux', '2011-01-01'),
-- ('Life Plays With Me', 'David Grossman', 'Hakibutz Hameuchad', '2019-03-12');

-- ADD ALSO INTO COPIES IF NOT ENTERING BOOKS THREW THE APP

-- INSERT INTO Branch (branch_name, phone_number) VALUES
-- ('City Centrt', 1123456),
-- ('Downtown', 9983456),
-- ('Uppuer City', 9876553),
-- ('Periphery', 4321567);

-- INSERT INTO Branch_address (city, street, house_number, branch_name) VALUES
-- ('Tel Aviv','Arlozerov', 120,'City Centrt'),
-- ('Tel Aviv', 'Begin',35 ,'Downtown'),
-- ('Tel Aviv', 'Einstein', 25,'Uppuer City'),
-- ('Tel Aviv', 'Yad Eliyahu', 8,'Periphery');

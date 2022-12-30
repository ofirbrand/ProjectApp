from datetime import datetime
from ProjectApp import cursor, connection
#No need for argument testing inside the classes - it will be testing during the form building/testing
#User arguments (common for Librarian's and Reader's) - email, name, phone_num, address
#No need for using @property and @setter
class User:
    counter = 0

    def __init__(self, email, name, phone_num, address, password):
        self.email = email
        self.name = name
        self.phone_num = phone_num
        self.address = address
        self.password = password
        User.counter += 1

    def __str__(self):
        str1 = f'Users name is: {self.name}'
        return str1

#inherit basic argument from User class
#Librarian's unique arguments = work_date_begin, branch
###create tests for email, work_date_begin(valid date argument)
class Librarian(User):
    counter = 0

    def __init__(self, email, name, phone_num, address, password, work_date_begin, branch_name):
        super().__init__(email, name, phone_num, address, password)
        self.work_date_begin = work_date_begin
        self.branch_name = branch_name
        Librarian.counter += 1

    def insert_new_book(self, book):
        #chack if the book is exists
        # if its exist, change book amount at copies
        # if book isn't exist create new Book instance and change book amount at copies
        if book.book_id in books:
            add_copy(book)
        else:
            book = Book(book)
        return book

    def borrow_handle(self, borrow):
        # check if the book available in the branch
        # fix the broken if statement
        if 1:
            borrow.request_status = "Accept"
        else:
            borrow.request_status = "Denied"


    def extension_handle(self, extension):
        pass

    def order_handle(self, order):
        pass

#inherit basic argument from User class
#Reader's arguments - email, name, d_birth, phone_num, address
#build valid date test for d_birth
class Reader(User):
    counter = 0

    def __init__(self, email, name, phone_num, address, password, d_birth):
        super().__init__(email, name, phone_num, address, password)
        self.d_birth = d_birth
        Reader.counter += 1

    def borrow_request(self, borrow):
        borrow.create_borrow(borrow)

    def search_book(self, book):
        pass

    def return_book(self, book):
        pass

    def my_books(self):
        pass

    def book_extension(self, book):
        pass

    def extension_request(self, book):
        pass

class Book:
    counter = 0

    def __init__(self, book_id, book_name, auther, year_published, publisher):
        self.book_id = book_id
        self.book_name = book_name
        self.auther = auther
        self.year_published = year_published
        self.publisher = publisher
        Book.counter += 1

class Copy(Book):
    def __init__(self, book_id, book_name, auther, year_published, publisher):
        super(Copy, self).__init__(book_id, book_name, auther, year_published, publisher)
        self.amount = 0

    def add_copy(self):
        self.amount += 1

class Branch:
    counter = 0

    def __init__(self, name, phone, address):
        self.name = name
        self.phone = phone
        self.address = address
        Branch.counter += 1


class Borrow:
    counter = 0

    def __init__(self, book, reader_email, librarian_email):
        self.book = book
        Borrow.counter += 1
        self.borrow_id = Borrow.counter
        self.date_of_borrowing = datetime.now().date()
        self.reader = reader_email
        self.librarian = librarian_email
        self.request_status = None

    def create_borrow(self, borrow):
        self.book = borrow.book
        Borrow.counter += 1
        self.borrow_id = Borrow.counter
        self.date_of_borrowing = borrow.datetime.now().date()
        self.reader = borrow.reader_email
        self.librarian = borrow.librarian_email
        self.request_status = "Request"


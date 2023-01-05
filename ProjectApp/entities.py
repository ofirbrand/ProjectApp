from datetime import datetime
from ProjectApp.routes import flash
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

#inherit basic argument from User class
#Librarian's unique arguments = work_date_begin, branch
###create tests for email, work_date_begin(valid date argument)
class Librarian(User):
    counter = 0

    def __init__(self, email, name, phone_num, address, password, work_date_begin, branch_name):
        super().__init__(email, name, phone_num, address, password)
        self.work_date_begin = work_date_begin
        self.branch_name = branch_name
        self.user_type = "Librarian"
        Librarian.counter += 1

    def add_new_book(self, book):
        cursor.execute("SELECT * FROM Book WHERE book_name like %s and author like %s;",
                       (book.book_name, book.author))
        is_book = cursor.fetchone()
        if is_book:  # if the book exists so there is at list 1 copy
            cursor.execute("SELECT * FROM Copies WHERE Book_id = %s and branch_name = %s;",
                           (book.book_id, self.branch_name))
            is_copy = cursor.fetchone()
            if is_copy:  # check if the copy that exists is in the same branch
                cursor.execute(""" SELECT C.copy_id, C.book_id, B.book_name, B.author, B.publisher, b.publish_year, 
                                            C.branch_name, C.amount
                                            FROM Copies AS C JOIN Book AS B ON C.book_id = B.book_id
                                            WHERE C.branch_name = %s AND C.book_id = %s""", (is_copy[2], is_copy[1]))
                copy_catch = cursor.fetchone()
                copy_temp = Copy(copy_id=copy_catch[0], book_id=copy_catch[1], book_name=copy_catch[2],
                                 author=copy_catch[3], publisher=copy_catch[4], year_published=copy_catch[5],
                                 branch=copy_catch[6], amount=copy_catch[7])
                copy_temp.add_copy()
                copy_temp.update_exist_copy()  # add 1 amount to all the copies with this book-id and branch-name
                return
            else:  # The book isn't exists in this branch. add new copy
                cursor.execute("INSERT INTO Copies(book_id, branch_name,amount, copy_status) VALUES(%s, %s, %s, %s)",
                               (book.book_id, self.branch_name, int(1), str('available')))
                connection.commit()
                return flash("A New Copy Has Been Added", 'success')
        else:  # the book isn't exists, add new book and new copy
            # add new book to the database
            cursor.execute("INSERT INTO Book(book_id, book_name, author, publisher, publish_year) "
                           "VALUES(%s, %s, %s, %s, %s)",
                           (book.book_id, book.book_name, book.author, book.publisher, book.year_published))
            connection.commit()
            # add new copy to the database
            cursor.execute("INSERT INTO Copies(book_id, branch_name, amount, copy_status) VALUES(%s, %s, %s, %s)",
                           (book.book_id, self.branch_name, int(1), str('available')))
            connection.commit()
            return flash(f"{book.book_name} Created As A New Book", 'success')

    def show_requests(self):
        cursor.execute("""SELECT Book.book_name, C.amount, C.copy_status, Bor.request_id, 
                          FROM Borrow AS Bor, Copies AS C, Book
                          WHERE Bor.book_id = C.book_id
                          AND Book.book_id = C.book_id
                          AND C.branch_name = %s""", self.branch_name)
        requests = cursor.fetchall()
        return requests

    def manage_request(self, request_id):
        cursor.execute("""SELECT C.amount, C.copy_status, C.copy_id, O.reader_email, O.date_of_order
                            FROM Borrow AS Bor, Copies AS C, Order_book AS O 
                            WHERE Bor.book_id = C.book_id
                            AND C.copy_id = O.copy_id
                            AND Bor.request_id = %s;""", request_id)
        temp_request = cursor.fetchone()
        if temp_request[0] > 0 and temp_request[1] == "available":
            cursor.execute("UPDATE Copies SET amount = amount - 1")
            connection.commit()
            cursor.execute("UPDATE Copies SET copy_status = 'orderable'")
            connection.commit()
            cursor.execute("SELECT order_status FROM Order_book "
                           "WHERE copy_id = %s AND O.reader_email = %s AND O.date_of_order = %s",
                           (temp_request[2], temp_request[3], temp_request[4]))
            is_exist_order = cursor.fetchone()
            if is_exist_order:
                cursor.execute("UPDATE Order_book SET order_status = 'orderable'")
                connection.commit()
                cursor.execute("UPDATE Borrow SET date_of_borrowing = %s WHERE request_id = %s",
                               (datetime.now().date(), request_id))
                connection.commit()
                return flash('Borrow Request Successfully Approved', 'success')
            else:
                return flash('Borrow Request Successfully Approved', 'success')
        else:
            return flash("Borrow Request Denied Because The Book Isn't Available In Stock", 'success')




            # update amount by minus 1, update copy_status to orderable, check if there's an order and if so update to orderable
            #update date of approve


# inherit basic argument from User class
# Reader's arguments - email, name, d_birth, phone_num, address
# build valid date test for d_birth
class Reader(User):
    counter = 0

    def __init__(self, email, name, phone_num, address, password, d_birth):
        super().__init__(email, name, phone_num, address, password)
        self.d_birth = d_birth
        self.user_type = "Reader"
        Reader.counter += 1

    def search_book(self, word):
        word = "%" + word + "%"
        cursor.execute("SELECT book_name FROM Book WHERE book_name LIKE %s", word)
        is_book_exist = cursor.fetchall()
        cursor.execute("SELECT author FROM Book WHERE author LIKE %s", word)
        is_author_exist = cursor.fetchall()
        if is_author_exist:
            authors = [''.join(i) for i in is_author_exist]
            books_list = []
            for author in authors:
                cursor.execute("""SELECT B.book_name, B.author, C.branch_name, MAX(C.amount),
                                SUM(CASE WHEN C.copy_status LIKE 'available' THEN 1 ELSE 0 END),
                                SUM(CASE WHEN C.copy_status LIKE 'orderable' THEN 1 ELSE 0 END)
                                FROM Copies AS C JOIN Book AS B ON C.book_id = B.book_id
                                WHERE B.author LIKE %s
                                GROUP BY 1 , 2 , 3""", author)
                # show orderable copies only when there are no available copies
                books_catch = cursor.fetchall()
                for b in books_catch:
                    lst = list(b)
                    books_list.append(lst)
            return books_list
            # for book in books_list:
            #     print(book)
        elif is_book_exist:
            books = [''.join(i) for i in is_book_exist]
            books_list = []
            for book in books:
                cursor.execute("""SELECT B.book_name, B.author, C.branch_name, MAX(C.amount),
                                SUM(CASE WHEN C.copy_status LIKE 'available' THEN 1 ELSE 0 END),
                                SUM(CASE WHEN C.copy_status LIKE 'orderable' THEN 1 ELSE 0 END)
                                FROM Copies AS C JOIN Book AS B ON C.book_id = B.book_id
                                WHERE B.book_name LIKE %s
                                GROUP BY 1 , 2 , 3""", book)
                books_catch = cursor.fetchall()
                for b in books_catch:
                    lst = list(b)
                    books_list.append(lst)
            return books_list
            # for book in books_list:
            #     print(book)
        else:
            return flash(f"No Book Or Author In The System Such As {word}", 'danger')

    def borrow_request(self, copy_id):
        cursor.execute("SELECT count(request_id) FROM Borrow WHERE reader_email = %s", self.email)
        amount_of_books = cursor.fetchone()
        if amount_of_books >= 3:
            return flash(f'{self.name}, We Are Sorry, But Reader Can Hold Only 3 Books Every Time')
        else:
            pass

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

    def __init__(self, book_id, book_name, author, year_published, publisher):
        self.book_id = book_id
        self.book_name = book_name
        self.author = author
        self.year_published = year_published
        self.publisher = publisher
        Book.counter += 1


class Copy(Book):
    def __init__(self, copy_id, book_id, book_name, author, year_published, publisher, branch, amount):
        super(Copy, self).__init__(book_id, book_name, author, year_published, publisher)
        self.copy_id = copy_id
        self.branch = branch
        self.status = 'available'
        self.amount = amount

    def add_copy(self):
        cursor.execute("INSERT INTO Copies(book_id, branch_name, copy_status, amount) VALUES(%s, %s, %s, %s)",
                       (self.book_id, self.branch, self.status, self.amount))
        connection.commit()
        # return flash('A New Copy Has Been Added', 'success')
        return flash("A New Copy Has Been Added", 'success')

    def update_exist_copy(self):
        cursor.execute("UPDATE Copies SET amount = %s WHERE book_id = %s AND branch_name = %s",
                       ((int(self.amount) + 1), self.book_id, self.branch))
        connection.commit()
        # return flash('This Book Is Already Exist. A New Copy Has Been Added', 'success')
        return flash("A New Copy Has Been Added And Copies Are Up To Date", 'success')

class Branch:
    counter = 0

    def __init__(self, name, phone, address):
        self.name = name
        self.phone = phone
        self.address = address
        Branch.counter += 1





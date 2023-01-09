from datetime import datetime
from ProjectApp.routes import flash
from ProjectApp import cursor, connection


class User:
    counter = 0

    def __init__(self, email, name, phone_num, address, password):
        self.email = email
        self.name = name
        self.phone_num = phone_num
        self.address = address
        self.password = password
        User.counter += 1


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
        cursor.execute("""SELECT C.copy_id, Book.book_name, C.amount, C.copy_status, Bor.request_id, Bor.reader_email 
                          FROM Borrow AS Bor, Copies AS C, Book
                          WHERE Bor.copy_id = C.copy_id
                          AND Book.book_id = C.book_id
                          AND C.branch_name = %s""", self.branch_name)
        requests_caught = cursor.fetchall()
        requests = []
        for request in requests_caught:
            lst = list(request)
            requests.append(lst)
        return requests

    def manage_request(self, request_id):
        cursor.execute("""SELECT C.amount, C.copy_status, C.copy_id, O.reader_email, O.date_of_order, BOR.reader_email
                            FROM Borrow AS Bor, Copies AS C, Order_book AS O 
                            WHERE Bor.book_id = C.book_id
                            AND C.copy_id = O.copy_id
                            AND Bor.request_id = %s;""", request_id)
        temp_request = cursor.fetchone()
        # check if the copy_status is available and amount in stock > 0
        if temp_request[0] > 0 and temp_request[1] == "available":
            # check if there is an order for this copy
            cursor.execute("SELECT * FROM Order_book WHERE copy_id = %s", temp_request[2])
            orders_catch = cursor.fetchall()
            if orders_catch:
                orders = list(map(list, orders_catch))
                for order in orders:
                    if order[0] != 'waiting':
                        # update: copy_amount, copy_status, borrow_status, borrow_date
                        cursor.execute("UPDATE Copies SET amount = amount - 1 WHERE Copy_id = %s", temp_request[2])
                        connection.commit()
                        cursor.execute("UPDATE Copies SET copy_status = 'available' WHERE Copy_id = %s",
                                       temp_request[2])
                        connection.commit()
                        cursor.execute("UPDATE Borrow SET status_of_request = 'approved' WHERE request_id = %s",
                                       request_id)
                        connection.commit()
                        return flash('Borrow Request Successfully Approved', 'success')
                    else:
                        if temp_request[5] == order[2]:
                            # update: copy_amount, copy_status, borrow_status, borrow_date, order_status
                            cursor.execute("UPDATE Copies SET amount = amount - 1 WHERE Copy_id = %s", temp_request[2])
                            connection.commit()
                            cursor.execute("UPDATE Copies SET copy_status = 'available' WHERE Copy_id = %s", temp_request[2])
                            connection.commit()
                            cursor.execute("UPDATE Borrow SET status_of_request = 'approved', date_of_borrowing = %s "
                                           "WHERE request_id = %s", request_id, datetime.now().date())
                            connection.commit()
                            cursor.execute("UPDATE Order_book SET order_status = 'orderable' "
                                           "WHERE copy_id = %s AND reader_email = %s AND date_of_order = %s",
                                           (order[3], order[2], order[1]))
                            connection.commit()
                            return flash('Borrow Request Successfully Approved', 'success')
                        else:
                            return flash("The Borrow request was rejected because the book is reserved", 'danger')
            else:
                # update: copy_amount, copy_status, borrow_status, borrow_date
                cursor.execute("UPDATE Copies SET amount = amount - 1 WHERE Copy_id = %s", temp_request[2])
                connection.commit()
                cursor.execute("UPDATE Copies SET copy_status = 'available' WHERE Copy_id = %s",
                               temp_request[2])
                connection.commit()
                cursor.execute("UPDATE Borrow SET status_of_request = 'approved' WHERE request_id = %s",
                               request_id)
                connection.commit()
                return flash('Borrow Request Successfully Approved', 'success')
        else:
            return flash("The Borrow request was rejected because the book isn't available", 'danger')
        #     cursor.execute("UPDATE Copies SET amount = amount - 1 WHERE Copy_id = %s", temp_request[2])
        #     connection.commit()
        #     cursor.execute("UPDATE Copies SET copy_status = WHERE Copy_id = %s", temp_request[2])
        #     connection.commit()
        #     # check if the copy was ordered
        #     # if the current copy was ordered t the last 3 days
        #     cursor.execute("SELECT order_status FROM Order_book "
        #                    "WHERE copy_id = %s AND O.reader_email = %s AND O.date_of_order = %s",
        #                    (temp_request[2], temp_request[3], temp_request[4]))
        #     is_exist_order = cursor.fetchone()
        #     if is_exist_order:
        #         cursor.execute("UPDATE Order_book SET order_status = 'orderable'")
        #         connection.commit()
        #         cursor.execute("UPDATE Borrow SET date_of_borrowing = %s WHERE request_id = %s",
        #                        (datetime.now().date(), request_id))
        #         connection.commit()
        #         return flash('Borrow Request Successfully Approved', 'success')
        #     else:
        #         return flash('Borrow Request Successfully Approved', 'success')
        # else:
        #     return flash("Borrow Request Denied Because The Book Isn't Available In Stock", 'success')


class Reader(User):
    counter = 0

    def __init__(self, email, name, phone_num, address, password, d_birth):
        super().__init__(email, name, phone_num, address, password)
        self.d_birth = d_birth
        self.user_type = "Reader"
        Reader.counter += 1

    def search_book(self, word):  # book[7] is the copy id with the smallest value from the same book.id in this branch
        word = "%" + word + "%"
        cursor.execute("SELECT book_name FROM Book WHERE book_name LIKE %s", word)
        is_book_exist = cursor.fetchall()
        cursor.execute("SELECT author FROM Book WHERE author LIKE %s", word)
        is_author_exist = cursor.fetchall()
        if is_author_exist:
            authors = [''.join(i) for i in is_author_exist]
            books_list = []
            for author in authors:
                cursor.execute("""SELECT B.book_name, B.author, C.branch_name, MAX(C.amount), BR.phone_number,
                                SUM(CASE WHEN C.copy_status LIKE 'available' THEN 1 ELSE 0 END),
                                SUM(CASE WHEN C.copy_status LIKE 'orderable' THEN 1 ELSE 0 END)
                                FROM Copies AS C, Book AS B, Branch as BR
                                WHERE C.book_id = B.book_id 
                                AND B.author LIKE %s 
                                AND BR.branch_name = C.branch_name 
                                GROUP BY 1 , 2 , 3""", author)
                # show orderable copies only when there are no available copies
                books_catch = cursor.fetchall()
                for b in books_catch:
                    lst = list(b)
                    books_list.append(lst)
            #new content to catch the copy_id
            for book in books_list:
                cursor.execute("""SELECT C.copy_id
                                    FROM Book AS B, Copies AS C
                                    WHERE B.book_id = C.book_id
                                    AND B.book_name = %s
                                    AND B.author = %s
                                    AND C.branch_name = %s""", (book[0], book[1], book[2]))
                copy_id = cursor.fetchone()
                book.append(copy_id[0])
            # end new content
            return books_list
        elif is_book_exist:
            books = [''.join(i) for i in is_book_exist]
            books_list = []
            for book in books:
                cursor.execute("""SELECT B.book_name, B.author, C.branch_name, MAX(C.amount), BR.phone_number, 
                                SUM(CASE WHEN C.copy_status LIKE 'available' THEN 1 ELSE 0 END),
                                SUM(CASE WHEN C.copy_status LIKE 'orderable' THEN 1 ELSE 0 END)
                                FROM Copies AS C, Book AS B, Branch as BR
                                WHERE C.book_id = B.book_id 
                                AND B.book_name LIKE %s 
                                AND BR.branch_name = C.branch_name
                                GROUP BY 1 , 2 , 3""", book)
                books_catch = cursor.fetchall()
                for b in books_catch:
                    lst = list(b)
                    books_list.append(lst)
            for book in books_list:
                cursor.execute("""SELECT C.copy_id
                                    FROM Book AS B, Copies AS C
                                    WHERE B.book_id = C.book_id
                                    AND B.book_name = %s
                                    AND B.author = %s
                                    AND C.branch_name = %s""", (book[0], book[1], book[2]))
                copy_id = cursor.fetchone()
                book.append(copy_id[0])
            return books_list
        else:
            return flash(f"No Book Or Author In The System Such As '{word[1:-1]}' ", 'danger')

    def borrow_request(self, copy_id):
        # check if the reader holds more than 3 books
        cursor.execute("SELECT count(request_id) "
                       "FROM Borrow "
                       "WHERE reader_email = %s"
                       "AND status_of_request = 'approved'", self.email)
        amount_of_books = cursor.fetchone()
        if amount_of_books[0] >= 3:
            return flash(f"{self.name}, We Are Sorry But Reader's Can Hold Only 3 Books Every Time", 'success')
        else:
            cursor.execute("SELECT C.copy_status FROM Copies WHERE copy_id = %s", copy_id)
            is_copy_available = cursor.fetchone()
            if is_copy_available[0] == 'available':
                # fix the insertion to Borrow table on column copy_id instead og book_id
                cursor.execute("INSERT INTO Borrow (status_of_request, copy_id, reader_email)"
                               "VALUES (%s, %s, %s)",
                               ('requested', copy_id, self.email))
                connection.commit()
                return flash(f"Your Borrow Request has been Received And Waiting To Be Approved", 'success')
            else:
                return flash("This Book Isn't Available So It Cannot Be Borrowed", 'danger')

    def return_book(self, book):
        pass

    def my_books(self):
        pass

    def book_extension(self, book):
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





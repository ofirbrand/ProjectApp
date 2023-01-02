from ProjectApp import connection, cursor
from ProjectApp.routes import session, request
from ProjectApp.entities import Librarian, Reader, Copy, Book
# city, street, house_number
# copy_id1 = 3
# cursor.execute("SELECT C.copy_id, C.book_id, B.book_name, B.author, B.publisher, b.publish_year, C.branch_name, C.amount"
#                "FROM Copies AS C JOIN Book AS B "
#                "ON C.book_id = B.book_id "
#                "WHERE C.copy_id = %s", copy_id1)
# copy1 = cursor.fetchone()
# copy = Copy(copy_id=copy1[0], book_id=copy1[1], book_name=copy1[2], auther=copy1[3],
#             publisher=copy1[4], year_published=copy1[5], branch=copy1[6], amount=copy1[7])
book_name = 'Life Plays With Me'
author = 'David Grossman'
publisher = 'Hakibutz Hameuchad'
year_published = '2019-03-12'
librarian_branch = 'City Center'
cursor.execute("SELECT * FROM Book WHERE book_name = %s and author = %s;", (book_name, author))
is_book = cursor.fetchone()
# print(is_book)
if is_book:  # if the book exists so there is at list 1 copy
    cursor.execute("SELECT * FROM Copies WHERE book_id = %s and branch_name = %s;", (is_book[0], librarian_branch))
    is_copy = cursor.fetchone()  # catch the copy
    cursor.execute(""" SELECT C.copy_id, C.book_id, B.book_name, B.author, B.publisher, b.publish_year, 
                    C.branch_name, C.amount
                    FROM Copies AS C JOIN Book AS B ON C.book_id = B.book_id
                    WHERE C.branch_name = %s AND C.book_id = %s""", (is_copy[2], is_copy[1]))
    copy_catch = cursor.fetchone()
    if copy_catch:  # check if the copy that exists is in the same branch
        copy_temp = Copy(copy_id=copy_catch[0], book_id=copy_catch[1], book_name=copy_catch[2],
                         auther=copy_catch[3], publisher=copy_catch[4], year_published=copy_catch[5],
                         branch=copy_catch[6], amount=copy_catch[7])
        copy_temp.add_copy()
        copy_temp.update_exist_copy()  # add 1 amount to all the copies with this book-id and branch-name
    else:  # The book isn't exists is in the same branch. add new copy
        book_catch = Book(book_id=is_book[0], book_name=is_book[1], auther=is_book[2],
                          year_published=is_book[3], publisher=is_book[4])
        cursor.execute("INSERT INTO Copies(book_id, branch_name,amount, copy_status) VALUES(%s, %s, %s, %s)",
                       (book_catch.book_id, librarian_branch, int(1), str('available')))
        connection.commit()
        print("A New Copy Has Been Added")
else:  # the book isn't exists, add new book and new copy
    # add new book to the database
    cursor.execute("INSERT INTO Book(book_name, author, publisher, publish_year) VALUES(%s, %s, %s, %s)",
                   (book_name, author, publisher, year_published))
    connection.commit()
    # add new copy to the database
    cursor.execute('SELECT * FROM Book WHERE book_name = %s AND author = %S', (book_name, author))
    temp_book = cursor.fetchone()
    cursor.execute("INSERT INTO Copies(book_id, branch_name, amount, copy_status) VALUES(%s, %s, %s, %s)",
                   (temp_book[0], librarian_branch, int(1), str('available')))
    connection.commit()
    print(f"{temp_book[1]} Created As A New Book In The System With 1 Copy")

# cursor.execute('SELECT * FROM Copies WHERE book_id = %s', book_id)
# temp_copy = cursor.fetchone()
# if temp_copy[2] == branch:
#     self.amount += 1
#     amount = 1
#     status = 'available'
#     cursor.execute("INSERT INTO Copies (book_id, amount, branch_name, copy_status) VALUES(%s, %s, %s, %s)",
#                    book_id, amount, branch, status)
#     cursor.execute("UPDATE Copies SET amount = %s WHERE copy_id = %s", (self.amount, temp_copy[0]))
# else:
#     pass

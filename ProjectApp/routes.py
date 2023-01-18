from flask import render_template, url_for, request, flash, redirect, session
from ProjectApp import app, connection, cursor, Session
from datetime import datetime, timedelta
import ProjectApp.entities as en

# login page view function
@app.route('/', methods=['POST', 'GET'])
@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    # user login by catching his details and direct him to right page for reader or librarian

    if request.method == 'POST':
        email = str(request.form['email'])
        password = str(request.form['password'])
        cursor.execute("SELECT * FROM Reader WHERE reader_email = %s", email)
        reader_temp = cursor.fetchone()
        cursor.execute("SELECT * FROM Librarian WHERE librarian_email = %s", email)
        librarian_temp = cursor.fetchone()
        if reader_temp:  # validate that user details are correct as reader
            if reader_temp[3] == password:
                cursor.execute("SELECT city, street, house_number FROM Reader_address WHERE reader_email = %s", email)
                address = cursor.fetchone()
                session["email"] = en.Reader(email=reader_temp[1], name=reader_temp[2], phone_num=reader_temp[0],
                                             address=address, password=reader_temp[3], d_birth=reader_temp[4])
                # create session with reader class
                return redirect('/reader2')
            else:
                flash('Password Incorrect', 'danger')
                return redirect('/')
        elif librarian_temp:
            if librarian_temp[3] == password:
                cursor.execute("SELECT city, street, house_number FROM Librarian_address WHERE librarian_email = %s",
                               email)
                address = cursor.fetchone()
                session["email"] = en.Librarian(email=librarian_temp[1], name=librarian_temp[2],
                                                phone_num=librarian_temp[0], address=address,
                                                password=librarian_temp[3], work_date_begin=librarian_temp[4],
                                                branch_name=librarian_temp[5])
                # create session with librarian class
                return redirect('/librarian2')
            else:
                flash('Password Incorrect', 'danger')
                return redirect('/')
        else:
            flash('The Email Address Is Not Saved In The System. Sign-Up Or Check For Email Typo', 'danger')
            return redirect('/')
    else:  # default get request
        return render_template('welcome.html')


@app.route('/logout')
def logout():  # log out by changing the session to null
    session["email"] = None
    return redirect('/')


@app.route('/registerLibrarian', methods=['GET', 'POST'])
def registerLibrarian():  # create new librarian user
    if request.method == 'POST':
        email = str(request.form['email'])
        cursor.execute(f"SELECT reader_email FROM Reader WHERE reader_email = %s", email)
        is_email_exist = cursor.fetchone()
        connection.commit()
        if is_email_exist:  # check if the email already exist - because it's a primary key
            flash(f"This Email Address Already Exists. Please Try New One", 'danger')
            return redirect('/registerLibrarian')
        else:  # check that all the fields are not empty
            name = str(request.form['name'])
            if not name:
                flash(f"You Must Enter Reader Name", 'danger')
                return redirect('/registerLibrarian')
            phone_num = request.form['phone']
            if not phone_num:
                flash(f"You Must Enter Phone Number", 'danger')
                return redirect('/registerLibrarian')
            city = str(request.form['city'])
            if not city:
                flash(f"You Must Enter City Name", 'danger')
                return redirect('/registerLibrarian')
            street = str(request.form['street'])
            if not street:
                flash(f"You Must Enter Street Name", 'danger')
                return redirect('/registerLibrarian')
            house_num = request.form['house']
            if not house_num:
                flash(f"You Must Enter House Number", 'danger')
                return redirect('/registerLibrarian')
            password = str(request.form['password'])
            if not password:
                flash(f"You Must Enter Password", 'danger')
                return redirect('/registerLibrarian')
            begin_work_date = request.form['begin_work_date']
            if not begin_work_date:
                flash(f"You Must Enter Begin Date Work", 'danger')
                return redirect('/registerLibrarian')
            branch_name = request.form['branch']
            if not branch_name:
                flash(f"You Must Enter Branch Name", 'danger')
                return redirect('/registerLibrarian')
            # creating python Librarian class
            cursor.execute("SELECT reader_email FROM Reader WHERE reader_email = %s", email)
            is_email_exist = cursor.fetchone()
            connection.commit()
            # insert data to Librarian table
            cursor.execute("INSERT INTO Librarian(phone_number, librarian_email, full_name, librarian_password, "
                           "begin_work_date, branch_name) VALUES(%s, %s, %s, %s, %s, %s)",
                           (phone_num, email, name, password, begin_work_date, branch_name))
            connection.commit()
            # insert data to Librarian_address table
            cursor.execute("INSERT INTO Librarian_address(city, street, house_number, librarian_email) "
                           "VALUES(%s, %s, %s, %s)",
                           (city, street, house_num, email))
            connection.commit()
            flash(f"Librarian User Created Successfully for {name}. You Are Now Able To Login", 'success')
            return redirect('/')
    else:  # default register librarian page
        title = "Librarian Register"
        cursor.execute("SELECT branch_name FROM Branch")
        branches_query = cursor.fetchall()
        branches_fixed = [''.join(i) for i in branches_query]
        return render_template('registerLibrarian.html', title=title, branches_fixed=branches_fixed)


@app.route('/registerReader', methods=['POST', 'GET'])
def registerReader():  # create new reader user
    if request.method == 'POST':
        email = str(request.form['email'])
        cursor.execute(f"SELECT reader_email FROM Reader WHERE reader_email = %s", email)
        is_email_exist = cursor.fetchone()
        connection.commit()
        if is_email_exist:  # check if the email already exist - because it's a primary key
            flash(f"This Email Address Already Exists. Please Try New One", 'danger')
            return redirect('/registerReader')
        else:  # tests that check that all the fields are not empty
            name = str(request.form['name'])
            if not name:
                flash(f"You Must Enter Reader Name", 'danger')
                return redirect('/registerReader')
            phone_num = request.form['phone']
            if not phone_num:
                flash(f"You Must Enter Phone Number", 'danger')
                return redirect('/registerReader')
            city = str(request.form['city'])
            if not city:
                flash(f"You Must Enter City Name", 'danger')
                return redirect('/registerReader')
            street = str(request.form['street'])
            if not street:
                flash(f"You Must Enter Street Name", 'danger')
                return redirect('/registerReader')
            house_num = request.form['house']
            if not house_num:
                flash(f"You Must Enter House Number", 'danger')
                return redirect('/registerReader')
            password = str(request.form['password'])
            if not password:
                flash(f"You Must Enter Password", 'danger')
                return redirect('/registerReader')
            date = request.form['date']
            if not date:
                flash(f"You Must Enter Date of Birth", 'danger')
                return redirect('/registerReader')
            cursor.execute("INSERT INTO Reader(phone_number, reader_email, full_name, reader_password, "
                           "date_of_birth) VALUES(%s, %s, %s, %s, %s)",
                           (phone_num, email, name, password, date))
            connection.commit()
            # insert data to Librarian_address table!
            cursor.execute("INSERT INTO Reader_address(city, street, house_number, reader_email) "
                           "VALUES(%s, %s, %s, %s)",
                           (city, street, house_num, email))
            connection.commit()
            flash(f"Reader User Created Successfully for {name}. You Are Now Able To Login", 'success')
            return redirect('/')
    else:
        title = "Reader Register"
        return render_template('registerReader.html', title=title)


@app.route('/reader2', methods=['GET', 'POST'])
def reader2():  # reader homepage - include search line to search books in the library
    session1 = session["email"]
    title = f"{session1.name}'s Home Page"
    if request.method == 'POST':  # catch searched word
        word = str(request.form['word'])
        test_word = "%" + word + "%"
        cursor.execute("SELECT book_name FROM Book WHERE book_name LIKE %s", test_word)
        is_book_exist = cursor.fetchall()
        cursor.execute("SELECT author FROM Book WHERE author LIKE %s", test_word)
        is_author_exist = cursor.fetchall()
        if is_author_exist or is_book_exist:  # if the word is part of book/author name show this book
            books = session1.search_book(word)  # OOP description is on 'entities.py'
            return render_template('requestbook.html', user=session1, title=title, books=books)
        else:
            flash(f"No Book Or Author In The System Such As '{word}' ", 'danger')
            return render_template('reader2.html', user=session1, title=title)
    else:
        return render_template('reader2.html', user=session1, title=title)


@app.route('/librarian2', methods=['GET', 'POST'])
def librarian2():  # librarian homepage
    session1 = session["email"]
    if session1.user_type == "Librarian":
        return render_template('librarian2.html', user=session1)
    else:
        return render_template('reader2.html', user=session1)


@app.route('/newbook', methods=['GET', 'POST'])
def newbook():
    title = "Add New Book"
    session1 = session["email"]
    if request.method == 'POST':
        book_name = str(request.form['book_name'])
        if not book_name:
            flash(f"You Must Enter Book Name", 'danger')
            return redirect('/newbook')
        author = str(request.form['author'])
        if not author:
            flash(f"You Must Enter Author Name", 'danger')
            return redirect('/newbook')
        publisher = str(request.form['publisher'])
        if not publisher:
            flash(f"You Must Enter Publisher Name", 'danger')
            return redirect('/newbook')
        publish_year = request.form['publish_year']
        if not publish_year:
            flash(f"You Must Enter Published Date", 'danger')
            return redirect('/newbook')
        cursor.execute('SELECT book_id FROM Book WHERE book_name like %s AND author like %s',
                       (book_name, author))
        is_book = cursor.fetchone()
        if is_book:  # if the book exist - update the copy amount
            book = en.Book(book_id=is_book[0], book_name=book_name, author=author, publisher=publisher,
                           year_published=publish_year)
            session1.add_new_book(book)  # OOP description is on 'entities.py'
            return render_template('newbook.html', user=session1, title=title)
        else:  # if the book isnt exist - create new instance of book
            cursor.execute("SELECT max(book_id) FROM Book")
            id_num = cursor.fetchone()
            book_id = int(''.join(map(str, id_num))) + 1  # add book_id because it usually happened with auto-increment
            book = en.Book(book_id=book_id, book_name=book_name, author=author, publisher=publisher,
                           year_published=publish_year)
            session1.add_new_book(book)  # OOP description is on 'entities.py'
            return render_template('newbook.html', user=session1, title=title)
    else:
        return render_template('newbook.html', user=session1, title=title)

@app.route('/mybooks', methods=['GET', 'POST'])
def mybooks():
    session1 = session["email"]
    title = f"{session1.name}'s Books"
    # catch the right variables and apply the function chosen by the reader
    if request.method == 'POST':
        if request.form['action'] == 'Return':
            request_id = request.form['request_id']
            copy_id = request.form['copy_id']  # OOP functions are written on 'entities.py'
            session1.return_book(request_id=request_id, copy_id=copy_id)
            return redirect('/mybooks')
        elif request.form['action'] == 'Extension':
            copy_id = request.form['copy_id']
            session1.extension(copy_id)  # OOP functions are written on 'entities.py'
            return redirect('/mybooks')
        elif request.form['action'] == 'Borrow':
            copy_id = request.form['copy_id']
            session1.borrow_request(copy_id)  # OOP functions are written on 'entities.py'
            return redirect('/mybooks')
        else:
            return redirect('/mybooks')
    else:
        # OOP description is on 'entities.py'
        # catch my books and my orders
        my_books = session1.my_books()
        orders = session1.my_orders()
        today = datetime.now().date()
        # show orders and books - if any of them exists
        if my_books:
            if orders:
                three_days = timedelta(days=3)
                return render_template('mybooks.html', user=session1, title=title, my_books=my_books,
                                       today=today, orders=orders, three_days=three_days)
            else:
                return render_template('mybooks.html', user=session1, title=title, my_books=my_books, today=today)
        else:
            if orders:
                three_days = timedelta(days=3)
                return render_template('mybooks.html', user=session1, title=title, today=today, orders=orders,
                                       three_days=three_days)
            else:
                return render_template('mybooks.html', user=session1, title=title)


@app.route('/managerequest', methods=['GET', 'POST'])
def managerequest():
    session1 = session["email"]
    if request.method == 'POST':
        request_id = request.form['request_id']
        session1.manage_request(request_id)
        flash(f"Request number {request_id} is closed!", 'success')
        requests = session1.show_requests()  # OOP description is on 'entities.py'
        if len(requests) > 0:
            return render_template('managerequest.html', user=session1, requests=requests)
        else:
            flash("There Are No More Open Requests In Your Branch", 'success')
            return render_template('managerequest.html', user=session1, requests=requests)
    else:
        requests = session1.show_requests()  # OOP description is on 'entities.py'
        if len(requests) > 0:  # check if there are any requests in the librarian's branch
            return render_template('managerequest.html', user=session1, requests=requests)
        else:
            flash("There Are No More Open Requests In Your Branch", 'success')
            return render_template('managerequest.html', user=session1, requests=requests)


@app.route('/requestbook', methods=['GET', 'POST'])
def requestbook():
    session1 = session["email"]
    if request.method == 'POST':
        # catch the right variables and apply the function chosen by the reader
        if request.form['action'] == 'Borrow':
            copy_id = request.form['copy_id']
            session1.borrow_request(copy_id)  # OOP description is on 'entities.py'
            return redirect('/reader2')
        elif request.form['action'] == 'Order':
            copy_id = request.form['copy_id']
            reader_email = request.form['reader_email']
            session1.order_book(copy_id=copy_id, reader_email=reader_email)  # OOP description is on 'entities.py''
            return redirect('/reader2')
        else:
            return redirect('/reader2')
    else:
        return render_template('requestbook.html', user=session1)


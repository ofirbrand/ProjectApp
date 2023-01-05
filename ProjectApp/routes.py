from flask import render_template, url_for, request, flash, redirect, session
from ProjectApp import app, connection, cursor, Session
import ProjectApp.entities as en


@app.route('/', methods=['POST', 'GET'])
@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    if request.method == 'POST':
        email = str(request.form['email'])
        password = str(request.form['password'])
        cursor.execute("SELECT * FROM Reader WHERE reader_email = %s", email)
        reader_temp = cursor.fetchone()
        cursor.execute("SELECT * FROM Librarian WHERE librarian_email = %s", email)
        librarian_temp = cursor.fetchone()
        if reader_temp:
            if reader_temp[3] == password:
                cursor.execute("SELECT city, street, house_number FROM Reader_Address WHERE reader_email = %s", email)
                address = cursor.fetchone()
                session["email"] = en.Reader(email=reader_temp[1], name=reader_temp[2], phone_num=reader_temp[0],
                                             address=address, password=reader_temp[3], d_birth=reader_temp[4])
                # session["email"] = request.form.get("email")  # change the session value to the correct class
                return redirect('/reader2')
            else:
                flash('Password Incorrect', 'danger')
        elif librarian_temp:
            if librarian_temp[3] == password:
                cursor.execute("SELECT city, street, house_number FROM Librarian_Address WHERE librarian_email = %s",
                               email)
                address = cursor.fetchone()
                session["email"] = en.Librarian(email=librarian_temp[1], name=librarian_temp[2],
                                                phone_num=librarian_temp[0], address=address,
                                                password=librarian_temp[3], work_date_begin=librarian_temp[4],
                                                branch_name=librarian_temp[5])
                # session["email"] = request.form.get("email")  # change the session value to the correct class
                return redirect('/librarian2')
            else:
                flash('Password Incorrect', 'danger')
        else:
            flash('The Email Address Is Not Saved In The System. Sign-Up Or Check For Email Typo', 'danger')
            return redirect('/')
    else:
        return render_template('welcome.html')


@app.route('/logout')
def logout():
    session["email"] = None
    return redirect('/')


@app.route('/registerLibrarian', methods=['GET', 'POST'])
def registerLibrarian():
    if request.method == 'POST':
        email = str(request.form['email'])
        name = str(request.form['name'])
        phone_num = str(request.form['phone'])
        city = str(request.form['city'])
        street = str(request.form['street'])
        house_num = int(request.form['house'])
        address = str(city + ", " + street + ", " + str(house_num))
        password = str(request.form['password'])
        begin_work_date = request.form['begin_work_date']
        branch_name = request.form['branch']
        # creating python Librarian class
        cursor.execute("SELECT reader_email FROM Reader WHERE reader_email = %s", email)
        is_email_exist = cursor.fetchone()
        connection.commit()
        if is_email_exist:
            flash("This Email Address Already Exists. Please Try New One", 'danger')
            return redirect('/registerLibrarian')
        else:
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
    else:
        title = "Librarian Register"
        cursor.execute("SELECT branch_name FROM Branch")
        branches_query = cursor.fetchall()
        branches_fixed = [''.join(i) for i in branches_query]
        return render_template('registerLibrarian.html', title=title, branches_fixed=branches_fixed)


@app.route('/registerReader', methods=['POST', 'GET'])
def registerReader():
    if request.method == 'POST':
        email = str(request.form['email'])
        cursor.execute(f"SELECT reader_email FROM Reader WHERE reader_email = %s", email)
        is_email_exist = cursor.fetchone()
        connection.commit()
        if is_email_exist:
            flash(f"This Email Address Already Exists. Please Try New One", 'error')
            return redirect('/registerReader')
        else:
            name = str(request.form['name'])
            phone_num = int(request.form['phone'])
            city = str(request.form['city'])
            street = str(request.form['street'])
            house_num = int(request.form['house'])
            password = str(request.form['password'])
            date = request.form['date']
            # creating python Librarian class
            # address = city + " " + str(street) + " " + str(house_num)
            # implement the Reader class  to the full_name content
            # user = en.Reader(email, name, phone_num, address, password, date)
            # insert data to Librarian table
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
        # add query that raise the Branches names to implement into the librarian register form
        return render_template('registerReader.html', title=title)


@app.route('/reader2', methods=['GET', 'POST'])
def reader2():
    session1 = session["email"]
    # cursor.execute('SELECT * from Reader WHERE reader_email = %s', session1.email)
    # user_reader = cursor.fetchone()
    # cursor.execute('SELECT * from Librarian WHERE Librarian_email = %s', session1.email)
    # user_librarian = cursor.fetchone()
    if session1.user_type == "Reader":
        user_dict = session1.__dict__.items()
        return render_template('reader2.html', user=session1, user_dict=user_dict)
    else:
        user_dict = session1.__dict__.items()
        return render_template('librarian2.html', user=session1, user_dict=user_dict)


@app.route('/librarian2', methods=['GET', 'POST'])
def librarian2():
    session1 = session["email"]
    # cursor.execute('SELECT * from Reader WHERE reader_email = %s', session1)
    # user_reader = cursor.fetchone()
    # cursor.execute('SELECT * from Librarian WHERE Librarian_email = %s', session1)
    # user_librarian = cursor.fetchone()
    if session1.user_type == "Librarian":
        user_dict = session1.__dict__.items()
        return render_template('librarian2.html', user=session1, user_dict=user_dict)
    else:
        user_dict = session1.__dict__.items()
        return render_template('reader2.html', user=session1, user_dict=user_dict)

@app.route('/newbook', methods=['GET', 'POST'])
def newbook():
    title = "Add New Book"
    session1 = session["email"]
    if request.method == 'POST':
        book_name = str(request.form['book_name'])
        author = str(request.form['author'])
        publisher = str(request.form['publisher'])
        publish_year = request.form['publish_year']
        cursor.execute('SELECT book_id FROM Book WHERE book_name like %s AND author like %s',
                       (book_name, author))
        is_book = cursor.fetchone()
        if is_book:
            book = en.Book(book_id=is_book[0], book_name=book_name, author=author, publisher=publisher,
                           year_published=publish_year)
            session1.add_new_book(book)
            return render_template('newbook.html', user=session1, title=title)
        else:
            cursor.execute("SELECT max(book_id) FROM Book")
            id_num = cursor.fetchone()
            book_id = int(''.join(map(str, id_num))) + 1
            book = en.Book(book_id=book_id, book_name=book_name, author=author, publisher=publisher,
                           year_published=publish_year)
            session1.add_new_book(book)
            return render_template('newbook.html', user=session1, title=title)
            # create an instance of book class
    else:
        return render_template('newbook.html', user=session1, title=title)

@app.route('/mybooks', methods=['GET', 'POST'])
def mybooks():
    session1 = session["email"]
    return render_template('mybooks.html', user=session1)

@app.route('/managerequest', methods=['GET', 'POST'])
def managerequest():
    session1 = session["email"]
    return render_template('managerequest.html', user=session1)

@app.route('/borroworder', methods=['GET', 'POST'])
def borroworder():
    session1 = session["email"]
    title = "Search Books"
    if request.method == 'POST':
        word = str(request.form['word'])
        books = session1.search_book(word)
        session['books'] = books
        session_books = session['books']
        return render_template('requestbook.html', user=session1, title=title, books=session_books)
    else:
        return render_template('borroworder.html', user=session1, title=title)

# @app.route('/requestbook', methods=['GET', 'POST'])
# def requestbook():
#     session1 = session["email"]
#     title = "Borrow/Order Book"
#     session_books = session['books']
#     if request.method == 'POST':
#
#         redirect()


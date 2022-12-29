from flask import render_template, url_for, request, flash, redirect, session
from ProjectApp import app, connection, cursor, Session
import ProjectApp.entities as en


@app.route('/', methods=['POST', 'GET'])
@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    if request.method == 'POST':
        email = str(request.form['email'])
        password = str(request.form['password'])
        cursor.execute("SELECT reader_email, reader_password FROM Reader WHERE reader_email = %s", email)
        reader_temp = cursor.fetchone()
        cursor.execute("SELECT librarian_email, librarian_password FROM Librarian WHERE librarian_email = %s", email)
        librarian_temp = cursor.fetchone()
        if reader_temp:
            if reader_temp[1] == password:
                session["email"] = request.form.get("email")
                return redirect('/reader')
            else:
                flash('Password Incorrect', 'error')
        elif librarian_temp:
            if librarian_temp[1] == password:
                session["email"] = request.form.get("email")
                return redirect('/reader')
            else:
                flash('Password Incorrect', 'error')
        else:
            flash('The Email Address Is Not Saved In The System. Sign-Up Or Check For A Typo')
            return redirect('/')
    else:
        return render_template('welcome.html')


@app.route('/registerLibrarian', methods=['GET', 'POST'])
def registerLibrarian():
    if request.method == 'POST':
        email = str(request.form['email'])
        name = str(request.form['name'])
        phone_num = str(request.form['phone'])
        city = str(request.form['city'])
        street = str(request.form['street'])
        house_num = int(request.form['house'])
        password = str(request.form['password'])
        begin_work_date = request.form['begin_work_date']
        branch_name = request.form['branch_name']
        cursor.execute("SELECT reader_email FROM Reader WHERE reader_email = %s", email)
        is_email_exist = cursor.fetchone()
        connection.commit()
        if is_email_exist:
            flash("This Email Address Already Exists. Please Try New One", 'error')
            return redirect('/registerLibrarian')
        else:
            # if there will be any necessary for librarian python class implementation
            # address = city + " " + str(street) + " " + str(house_num)
            # librarian = en.Librarian(email, name, phone_num, address, password, begin_work_date, branch_name)
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
        return render_template('registerLibrarian.html', title=title, branches=branches_fixed)


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
            # if there will be any necessary for reader python class implementation
            # address = city + " " + str(street) + " " + str(house_num)
            # reader = en.Reader(email, name, phone_num, address, password, date)
            # insert data to Librarian table!
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


# create librarian home page and delete the example in librarian register view function
# @app.route('/homepageLibrarian')
# def homepageLibrarian():  # create librarian home page
#     return render_template('homepageLibrarian.html')


# create reader home page and delete the example in reader register view function
# @app.route('/homepageReader', methods=['GET', 'POST'])
# def homepageReader():
#     return render_template('homepageReader.html')

@app.route('/reader', methods=['GET', 'POST'])
def reader():
    session1 = session["email"]
    cursor.execute('SELECT * from Reader WHERE reader_email = %s', session1)
    user_reader = cursor.fetchone()
    cursor.execute('SELECT * from Librarian WHERE Librarian_email = %s', session1)
    user_librarian = cursor.fetchone()
    if user_reader:
        reader_name = user_reader[2]
        return render_template('reader.html', reader_name=reader_name)
    else:
        librarian_name = user_librarian[2]
        return render_template('librarian.html', librarian_name=librarian_name)

@app.route('/librarian', methods=['GET', 'POST'])
def librarian():
    session1 = session["email"]
    cursor.execute('SELECT * from Reader WHERE reader_email = %s', session1)
    user_reader = cursor.fetchone()
    cursor.execute('SELECT * from Librarian WHERE Librarian_email = %s', session1)
    user_librarian = cursor.fetchone()
    if user_reader:
        reader_name = user_reader[2]
        return render_template('reader.html', reader_name=reader_name)
    else:
        librarian_name = user_librarian[2]
        return render_template('librarian.html', librarian_name=librarian_name)
from flask import render_template, url_for, request, flash, redirect, session
from ProjectApp import app
import ProjectApp.entities as en
from ProjectApp import connection, cursor, Session


@app.route('/', methods=['POST', 'GET'])
@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    return render_template('welcome.html')


@app.route('/registerLibrarian', methods=['GET', 'POST'])
def registerLibrarian():
    if request.method == 'POST':
        email = str(request.form['email'])
        # add test to check if the email address is unique
        name = str(request.form['name'])
        phone_num = str(request.form['phone'])
        city = str(request.form['city'])
        street = str(request.form['street'])
        house_num = int(request.form['house'])
        password = int(request.form['password'])
        begin_work_date = request.form['begin_work_date']
        branch_name = request.form['branch_name']
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
        return render_template('registerLibrarian.html', title=title)


@app.route('/registerReader', methods=['POST', 'GET'])
def registerReader():
    if request.method == 'POST':
        email = str(request.form['email'])
        name = str(request.form['name'])
        phone_num = int(request.form['phone'])
        city = str(request.form['city'])
        street = str(request.form['street'])
        house_num = int(request.form['house'])
        password = int(request.form['password'])
        date = request.form['date']
        # if there will be any necessary for reader python class implementation
        # address = city + " " + str(street) + " " + str(house_num)
        # reader = en.Reader(email, name, phone_num, address, password, date)
        # insert data to Librarian table
        cursor.execute("INSERT INTO Reader(phone_number, reader_email, full_name, reader_password, "
                       "date_of_birth) VALUES(%s, %s, %s, %s, %s)",
                       (phone_num, email, name, password, date))
        connection.commit()
        # insert data to Librarian_address table
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
@app.route('/homepageLibrarian')
def homepageLibrarian():  # create librarian home page
    return render_template('homepageLibrarian.html')


# create reader home page and delete the example in reader register view function
@app.route('/homepageReader', methods=['GET', 'POST'])
def homepageReader():
    return render_template('homepageReader.html')

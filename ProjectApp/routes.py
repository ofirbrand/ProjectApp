from flask import render_template, url_for, request
from ProjectApp import app
import ProjectApp.entities as en
# from ProjectApp import connection, cursor  # importing the functions that deals with SQL from __init__ page

@app.route('/', methods=['POST', 'GET'])
@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    return render_template('welcome.html')

@app.route('/register_librarian', methods=['GET', 'POST'])
def register_librarian():
    if request.method == 'POST':
        email = str(request.form['email'])
        name = str(request.form['name'])
        phone_num = int(request.form['phone'])
        address = str(request.form['address'])
        password = int(request.form['password'])
        begin_work_date = request.form['begin_work_date']
        branch_name = request.form['branch_name']
    return render_template('register_librarian.html')

@app.route('/registerReader', methods=['POST', 'GET'])
def registerReader():
    if request.method == 'POST':
        email = str(request.form['email'])
        name = str(request.form['name'])
        phone_num = int(request.form['phone'])
        address = str(request.form['address'])
        password = int(request.form['password'])
        date = request.form['date']
        reader = en.Reader(email, name, phone_num, address, password, date)
        items = reader.__dict__.items()
        return render_template('homepageReader.html', reader=reader, items=items)  # create homepageReader.html to show readers details
    else:
        return render_template('registerReader.html')

@app.route('/homepage_librarian')
def homepage_librarian():
    return render_template('homepage_librarian.html')

@app.route('/homepageReader', methods=['GET', 'POST'])
def homepageReader():
    return render_template('homepageReader.html')

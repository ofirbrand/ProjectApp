from flask import render_template, url_for, request
from ProjectApp import app
import ProjectApp.entities as en

@app.route('/', methods=['POST', 'GET'])
@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    return render_template('welcome.html')

@app.route('/register_librarian')
def register_librarian():
    return render_template('register_librarian.html')

@app.route('/registerReader', methods=['POST', 'GET'])
def registerReader():
    if request.method == 'POST':
        reader = en.Reader()
        reader.email = str(request.form['email'])
        reader.name = str(request.form['name'])
        reader.phone_num = int(request.form['phone'])
        reader.address = str(request.form['address'])
        reader.password = int(request.form['password'])
        return render_template('homepageReader.html', reader=reader)  # create homepageReader.html to show readers details
    else:
        return render_template('registerReader.html')

@app.route('/homepage_librarian')
def homepage_librarian():
    return render_template('homepage_librarian.html')

@app.route('/homepageReader')
def homepageReader():
    return render_template('homepageReader.html')

from flask import Flask
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
app.config['SECRET_KEY'] = '5479437c16e750c4c8e3a432fe891395'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Shlomo1995'
app.config['MYSQL_DATABASE_DB'] = 'ProjectLibraries'
mysql.init_app(app)
connection = mysql.connect()
cursor = connection.cursor()
from ProjectApp import routes



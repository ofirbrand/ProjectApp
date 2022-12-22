from flask import Flask
# from flaskext.mysql import MySQL


app = Flask(__name__)

from ProjectApp import routes



from flask import Flask, request
from flask_restful import Api
from .config import app_config

import pymysql as mysql

app = Flask(__name__)

# load from config.py in root folder
app.config.from_object(app_config["production"])


mysql = mysql.connect(host='localhost', user='root', password='', db='cti_lifegrow', cursorclass=mysql.cursors.DictCursor)

from myapp.entries.landmodel import LandEntry
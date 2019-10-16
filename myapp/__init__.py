from flask import Flask, request
from flask_restful import Api
from .config import app_config

from flask_mysqldb import MySQL

# def create_app():
    # Initialize flask app
# app_ = Flask(__name__, instance_relative_config=True)

    # return app_

app = Flask(__name__)
# app = create_app()
# load from config.py in root folder
# app.config.from_object(app_config["production"])

app.config['MYSQL_HOST'] = 'ctiafrica.io'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'silversands123!'
app.config['MYSQL_DB'] = 'cti_lifegrow'


mysql = MySQL(app)

from myapp.entries.landmodel import LandEntry
from flask import Flask
from flask_restful import Api
from .config import app_config

from flaskext.mysql import MySQL

def create_app():
    # Initialize flask app
    app_ = Flask(__name__, instance_relative_config=True)

    return app_


app = create_app()
# load from config.py in root folder
app.config.from_object(app_config["development"])

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'janet'
app.config['MYSQL_DATABASE_PASSWORD'] = 'swcti321./'
app.config['MYSQL_DATABASE_DB'] = 'cti_lifegrow'
app.config['MYSQL_DATABASE_HOST'] = 'http://ctiafrica.io/'
mysql.init_app(app)

from myapp.entries.landmodel import LandEntry
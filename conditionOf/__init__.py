import os
from flask import Flask
from flask_heroku import Heroku
import psycopg2

app = Flask(__name__)

heroku = Heroku(app)
def create_conn():
    conn = None
    if os.environ.has_key("DATABASE_URL"):
        username = os.environ["DATABASE_URL"].split(":")[1].replace("//","")
        password = os.environ["DATABASE_URL"].split(":")[2].split("@")[0]
        host = os.environ["DATABASE_URL"].split(":")[2].split("@")[1].split("/")[0]
        dbname = os.environ["DATABASE_URL"].split("/")[3]
        conn = psycopg2.connect(dbname=dbname, user=username, password=password, host=host) 
    else:
        import sqlite3
        conn = sqlite3.connect('/tmp/test.db')
    return conn

from util.gzipmiddleware import GzipMiddleware
app.wsgi_app = GzipMiddleware(app.wsgi_app, compresslevel=5)

import conditionOf.views

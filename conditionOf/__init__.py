import os
from flask import Flask
import psycopg2

app = Flask(__name__)
app.debug = True

from util.gzipmiddleware import GzipMiddleware
app.wsgi_app = GzipMiddleware(app.wsgi_app, compresslevel=5)

import conditionOf.views

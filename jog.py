#!/usr/bin/env pypy

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import g

import sqlite3
import os.path
import time
import uuid

# configuration
DATABASE = 'jog.db'
DEBUG = True
SECRET_KEY = uuid.uuid1()
USERNAME = 'admin'
PASSWORD = 'default'

# initiate flask
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object(__name__)
app.config.from_envvar('JOG_SETTINGS', silent=True)

# check for the database
if not os.path.isfile(app.config['DATABASE']):
    sys.exit('Database: %s not found' % app.config['DATABASE'])

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# create routes
@app.route("/")
def index():
    return render_template("index.html")

# run application
if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 80)
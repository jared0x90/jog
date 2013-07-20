#!/usr/bin/env pypy

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for

import sqlite3
import os.path
import time

# initiate db
dbname = 'jog.db'

if not os.path.isfile(dbname):
    sys.exit('Database: %s not found' % dbname)

jog_db_conn = sqlite3.connect(dbname)
jog_db_curs = jog_db_conn.cursor()


# initiate flask
app = Flask(__name__, static_folder='static', static_url_path='/static')

# create routes
@app.route("/")
def index():
    return render_template("index.html")

# run application
if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 80)
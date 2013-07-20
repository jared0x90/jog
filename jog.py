#!/usr/bin/env pypy

# flask imports
from flask import flash
from flask import Flask
from flask import g
from flask import Markup
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

# markdown imports
import markdown

# standard imports
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
app = Flask(
    __name__,
    static_folder='static',
    static_url_path='/static'
)
app.config.from_object(__name__)
app.config.from_envvar('JOG_SETTINGS', silent=True)

# check that the database exists
if not os.path.isfile(app.config['DATABASE']):
    sys.exit('Database: %s not found' % app.config['DATABASE'])

# database routines
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
    cur = g.db.execute('SELECT title, body, id, date_created FROM posts ORDER BY id desc')
    entries = [
        dict(
            title = row[0],
            body = Markup(markdown.markdown(row[1])),
            id = row[2],
            date_created = row[3]
        )
        for row in cur.fetchall()
    ]
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

# run application
if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 80)
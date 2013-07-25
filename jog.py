#!/usr/bin/env pypy

# flask imports
from flask import abort
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
PUBLIC_URL_BASE = 'http://www.jwd.me'
DATABASE = 'jog.db'
DEBUG = True
SECRET_KEY = str(uuid.uuid1())
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

@app.route('/post/<int:post_id>')
def show_post(post_id):
    cur = g.db.execute('SELECT title, body, id, date_created FROM posts WHERE id = ?', str(post_id))
    row = cur.fetchone()
    entry = dict(
        title = row[0],
        body = Markup(markdown.markdown(row[1])),
        id = row[2],
        date_created = row[3]
    )
    return render_template('post.html', entry=entry, puburl = PUBLIC_URL_BASE + '/post/' + str(entry['id']))

@app.route('/edit/<int:post_id>')
def edit_post(post_id):
    if not session.get('logged_in'):
        flash('You must login before editing a post.')
        return redirect(url_for('index'))
    cur = g.db.execute('SELECT title, body, id, date_created FROM posts WHERE id = ?', str(post_id))
    row = cur.fetchone()
    entry = dict(
        title = row[0],
        body = row[1],
        id = row[2],
        date_created = row[3]
    )
    return render_template('edit.html', entry=entry)

@app.route("/create")
def create_post():
    if not session.get('logged_in'):
        flash('You must login before posting.')
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/add', methods=['POST'])
def add_post():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute(
        'insert into posts (title, body, date_created) values (?, ?, ?)', [
            request.form['title'],
            request.form['body'],
            int(time.time())
        ]
    )
    g.db.commit()
    flash('New post was successfully created.')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

# run application
if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 80)
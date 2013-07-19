#!/usr/bin/env pypy

import sys
import sqlite3
import os.path
import time

dbname = 'jog.db'

if len(sys.argv) != 3:
    sys.exit('Usage: %s [file.post] "[Title]"' % sys.argv[0])

if not os.path.isfile(sys.argv[1]):
    sys.exit('Error: File %s not found' % sys.argv[1])

if len(sys.argv[2]) < 3:
    sys.exit('Error: Specify a longer title')

if not os.path.isfile(dbname):
    sys.exit('Database: %s not found' % dbname)

jog_db_conn = sqlite3.connect(dbname)
jog_db_curs = jog_db_conn.cursor()

with open (sys.argv[1], "r") as post:
    body = post.read()

print ("Inserting post \"%s\":\n%s" % (sys.argv[2], body))

try:
    post_data = (sys.argv[2], body, int(time.time()))
    jog_db_curs.execute("INSERT INTO posts(title, body, date_created) VALUES (?,?,?) ", post_data)
    jog_db_conn.commit()
    print('DB write successful')
except:
    print('Failure during DB write')
    raise
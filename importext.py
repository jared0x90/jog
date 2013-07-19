#!/usr/bin/env pypy

import sys
import sqlite3

if len(sys.argv) != 3:
    sys.exit('Usage: %s [file.post] "[Title]"' % sys.argv[0])

dbname = 'jog.db'

jog_db_conn = sqlite3.connect(dbname)
c = jog_db_conn.cursor()

with open (sys.argv[1], "r") as post:
    body = post.read()

print body
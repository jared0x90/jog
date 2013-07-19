/*

Jog Database Schema

==============================================================================

SQLite3 datatypes from:
http://www.sqlite.org/datatype3.html

NULL. The value is a NULL value.
INTEGER. The value is a signed integer, stored in 1, 2, 3, 4, 6, or 8 bytes depending on the magnitude of the value.
REAL. The value is a floating point value, stored as an 8-byte IEEE floating point number.
TEXT. The value is a text string, stored using the database encoding (UTF-8, UTF-16BE or UTF-16LE).
BLOB. The value is a blob of data, stored exactly as it was input.

==============================================================================

Sample schema from flask documentation availabel at:
http://flask.pocoo.org/docs/tutorial/schema/

drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

==============================================================================

Create your database by running the following command:

    sqlite3 jog.db < schema.sql

*/

drop table if exists posts;
create table posts (
    id integer primary key autoincrement,
    title text not null,
    body text not null,
    date_created integer not null
);
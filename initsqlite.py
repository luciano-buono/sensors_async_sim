import sqlite3

db_name =  "iot-sqlite.db"

# SQLite DB Table Schema
table_schema="""
drop table if exists temperature ;
create table temperature (
  value real,
  unit text,
  timestamp real primary key
);
drop table if exists pressure ;
create table pressure (
  value real,
  unit text,
  timestamp real primary key
);
drop table if exists frequency ;
create table frequency (
  value real,
  unit text,
  timestamp real primary key
);"""

#Connect or Create DB File
conn = sqlite3.connect(db_name)
curs = conn.cursor()

#Create Tables
sqlite3.complete_statement(table_schema)
curs.executescript(table_schema)

#Close DB
curs.close()
conn.close()

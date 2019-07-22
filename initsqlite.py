import sqlite3

db_name =  "iot-sqlite.db"

# SQLite DB Table Schema
table_schema="""
drop table if exists table_Terrazatemperatura ;
create table table_Terrazatemperatura (
  value real,
  unit text,
  timestamp real primary key
);
drop table if exists table_Patiotemperatura ;
create table table_Patiotemperatura (
  value real,
  unit text,
  timestamp real primary key
);
drop table if exists table_Jardintemperatura ;
create table table_Jardintemperatura (
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

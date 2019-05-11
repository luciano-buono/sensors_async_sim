import json
import sqlite3

db_name =  "iot-sqlite.db"

class DatabaseManager():
    def __init__(self):
        self.conn = sqlite3.connect(db_name)
        self.conn.commit()
        self.cur = self.conn.cursor()

    def add_del_update_db_record(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()

def write_to_db(dbObj, topic, jsonData):

    data = json.loads(jsonData)
#   query = ???
    print (query)
#   actually write to the db now

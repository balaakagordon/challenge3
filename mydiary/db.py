#!/usr/bin/python
import psycopg2
#from mydiary import app


class MyDiary_Database:
    def __init__(self):

        my_db = 'mydiary_db'
        try:
            self.conn = psycopg2.connect(dbname=my_db, user='mydiary_user', host='localhost', password='password', port='5432')
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("Unable to connect. Check dbname, user or password inputs.")
            print(e)

    def new_users_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (user_id SERIAL NOT NULL PRIMARY KEY, name VARCHAR(40) NOT NULL, email VARCHAR(60) NOT NULL, password VARCHAR(40) NOT NULL);""")
        self.conn.commit()

    def new_entries_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS entries (entry_id SERIAL NOT NULL PRIMARY KEY, user_id INTEGER NOT NULL, title VARCHAR(20) NOT NULL, data VARCHAR(500) NOT NULL, date_modified VARCHAR(10) NOT NULL);""")
        self.conn.commit()

    def drop_entries_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS entries;""")
        self.cursor.commit()

    def drop_users_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS users;""")
        self.cursor.commit() 
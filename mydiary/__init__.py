from flask import Flask, jsonify, request
#from mydiary import entries, users
#from models import MyDiary, Entries
from .db import MyDiary_Database


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

app_db = MyDiary_Database()
app_db.new_users_table
app_db.new_entries_table

from . import entries
from . import users

# def main():
#     insert_usr_str = """INSERT INTO users (user_id, name, email, password) VALUES(%s,%s,%s,%s);"""
#     insert_ent_str = """INSERT INTO entries (entry_id, user_id, title, data, date_created) VALUES(%s,%s,%s,%s,%s);"""
#     app_db.cursor.execute(insert_usr_str, (1,"Gordon Balaaka","gb@email.com","pass1"))
#     app_db.cursor.execute(insert_usr_str, (1,"Simon Peter","sp@email.com","pass2"))
#     app_db.cursor.execute(insert_usr_str, (1,"John Bosco","jb@email.com","pass3"))
#     app_db.cursor.execute(insert_ent_str, (1,1,"First Entry","This is the first test entry","08/02/18"))
#     app_db.cursor.execute(insert_ent_str, (1,2,"Second Entry","This is the second test entry","15/03/18"))
#     app_db.cursor.execute(insert_ent_str, (1,3,"Third Entry","This is the third test entry","16/05/18"))

#     get_ent_str = """SELECT * from entries;"""
#     get_usr_str = """SELECT * from users;"""
#     app_db.cursor.execute(get_ent_str)
#     my_entries = app_db.cursor.fetchall()
#     app_db.cursor.execute(get_usr_str)
#     my_users = app_db.cursor.fetchall()
#     # print(my_entries)
#     # print(my_users)


# if __name__
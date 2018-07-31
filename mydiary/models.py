"""
Holds the app's classes and methods
"""

# -*- coding: utf-8 -*-

"""importing packages"""
from mydiary import db
from mydiary import app_db, my_diary_object
#import jwt

import datetime
now = datetime.datetime.now()


""" the diary app is modelled as an object with it's own \
parameters and methods """
class MyDiary:
    def __init__(self):
        self.current_user = None    #current user's id
        self.user_entries = None
        self.user_index = 1

    def getUser(self, user_id):
        sql_fn = """SELECT * from users WHERE user_id = %s;"""
        app_db.cursor.execute(sql_fn, (user_id))
        rows = app_db.cursor.fetchall()
        if rows == []:
            message = "User not found"
            return message
        else:
            user = {
                "user_id" : rows[0],
                "name" : rows[1],
                "email" : rows[2],
                "password" : rows[3]
            }
            message = "User found"
            return message, user         #returns user as a dictionary

    def addUser(self, user_id_data, user_name, user_email, user_password):

        sql_check_fn = """SELECT * from entries WHERE email = %s AND name = %s;"""
        app_db.cursor.execute(sql_check_fn, (user_email, user_name))
        rows = app_db.cursor.fetchall()
        if rows[0] == []:
            sql_insert_fn = """INSERT INTO users (user_id, name, email, password) VALUES(%s,%s,%s,%s);"""
            app_db.cursor.execute(sql_insert_fn, (user_id_data,user_name,user_email,user_password))
            message = "Added successfully"
        else:
            message = "This user already exists!"
        return message
    

    def login(self, login_email, login_password):
        """ login method requires a username and password """
        sql_fn = """SELECT * from entries WHERE email = %s AND password = %s;"""
        app_db.cursor.execute(sql_fn, (login_email, login_password))
        rows = app_db.cursor.fetchall()
        if rows == []:
            message = "Sorry, incorrect credentials"
        else:
            self.current_user == rows[0]
            message = "You've been logged in successfully"
        return message

    def logout(self):
        """ logout method clears the currentUser and userEntries \
        variables """
        if self.current_user != None:
            self.current_user = None
            self.user_entries = None
            message = "Logout successful"
        else:
            message = "Nobody logged in!"
        return message

class Entries:
    """ Entry lists for each user are modelled as objects with \
    parameters and methods """

    def __init__(self):
        self.entry_index = 1
        self.entry_list = []
        self.all_entries = 0
        self.current_entries = 0
        self.deleted_entries = 0
        
        sql_fn = """SELECT * from entries;"""
        app_db.cursor.execute(sql_fn)
        rows = app_db.cursor.fetchall()
        self.current_entries = len(rows)
        self.all_entries = self.entry_index

    def addEntry(self, entry_id_data, user_id_data, title_data, entry_data, current_time):
        """ once a diary entry is created it sends itself to \
        Entries to be added to entrylist """
        entry_id = self.entry_index
        self.entry_index += 1

        sql_check_fn = """SELECT * from entries WHERE data = %s AND title = %s AND user_id = %s;"""
        app_db.cursor.execute(sql_check_fn, (entry_data, title_data, user_id_data))
        rows = app_db.cursor.fetchall()
        if rows == []:
            sql_insert_fn = """INSERT INTO entries (entry_id, user_id, title, data, date) VALUES(%s,%s,%s,%s,%s);"""
            app_db.cursor.execute(sql_insert_fn, (entry_id,user_id_data,title_data,entry_data,current_time))
            message = "Entry added successfully"
        else:
            message = "Entry already exists"
        return message
        

    def modifyEntry(self, title_data, entry_data, current_time, entry_id_data, user_id_data):
        """ this method edits diary entries """
        sql_check_fn = """SELECT * from entries WHERE user_id = %s AND entry_id = %s"""
        app_db.cursor.execute(sql_check_fn, (user_id_data, entry_id_data))
        rows = app_db.cursor.fetchall()
        if rows == []:
            message = "Entry not found"
        else:
            sql_update_fn = """UPDATE entries SET title = %s, data = %s, date = %s) WHERE user_id = %s AND entry_id = %s;"""
            app_db.cursor.execute(sql_update_fn, (title_data,entry_data,current_time,user_id_data,entry_id_data))
            message = "Entry edited"
        return message

    def deleteEntry(self, entry_id_data, user_id_data):
        """ this method deletes diary entries """
        sql_check_fn = """SELECT * from entries WHERE user_id = %s AND entry_id = %s;"""
        app_db.cursor.execute(sql_check_fn, (user_id_data, entry_id_data))
        rows = app_db.cursor.fetchall()
        if rows == []:         #should get one entry
            message = "Unable to delete. Entry does not exist" #abort(404)
        else:
            sql_delete_fn = """DELETE from entries where user_id = %s AND entry_id = %s;"""
            app_db.cursor.execute(sql_delete_fn, (user_id_data, entry_id_data))
            message = "Entry successfully deleted"
            self.deleted_entries += 1
        return message

    def getOneEntry(self, user_id, entry_id):
        sql_check_fn = """SELECT * from entries WHERE user_id = %s AND entry_id = %s;"""
        app_db.cursor.execute(sql_check_fn)
        row = app_db.cursor.fetchall()      #should fetch one entry
        if row == []:
            message = "Entry does not exist"
            return message
        else:
            entry = {
                'entry_id':row[0], 
                'user_id':row[1], 
                'title':row[2],
                'data':row[3],
                'date':row[4]
                }
            message = "Entry found"
            return message, entry

    def getAllEntries(self):
        sql_check_fn = """SELECT * from entries WHERE user_id = %s;"""
        app_db.cursor.execute(sql_check_fn)
        rows = app_db.cursor.fetchall()
        if rows == []:
            message = "No entries found"
            return message
        else:
            self.entry_list = []
            for row in rows:
                entry = {
                    'entry_id':row[0], 
                    'user_id':row[1], 
                    'title':row[2],
                    'data':row[3],
                    'date':row[4]
                    }
                self.entry_list.append(entry)
            return self.entry_list
from flask import Flask, jsonify, request
from mydiary import entries, users
from models import MyDiary, Entries
from db import MyDiary_Database


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

app_db = MyDiary_Database()

my_diary_object = MyDiary()
my_diary_object.user_entries = Entries()

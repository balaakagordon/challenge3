from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from .db import MyDiary_Database


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

app_db = MyDiary_Database()
# app_db.drop_users_table()
# app_db.drop_entries_table()
app_db.new_users_table()
app_db.new_entries_table()

from . import entries
from . import users

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import datetime

from .db import MyDiaryDatabase


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

app_db = MyDiaryDatabase()
# app_db.drop_users_table()
# app_db.drop_entries_table()
app_db.new_users_table()
app_db.new_entries_table()

now_time = "".join(str(datetime.datetime.now().day) +
                "/" + str(datetime.datetime.now().month) +
                "/" + str(datetime.datetime.now().year))


from . import entries
from . import users

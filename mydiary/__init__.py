from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import os
import datetime

from .db import MyDiaryDatabase


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

db_name = os.environ.get('db_name', None)
if db_name == "mydiarydb":
    app_db = MyDiaryDatabase(db_name)
else:
    db_name = "testdb"
    app_db = MyDiaryDatabase(db_name)
    app_db.drop_users_table()
    app_db.drop_entries_table()
    pass
app_db.new_users_table()
app_db.new_entries_table()


now_time = "".join(str(datetime.datetime.now().day) +
                "/" + str(datetime.datetime.now().month) +
                "/" + str(datetime.datetime.now().year))


from . import entries
from . import users

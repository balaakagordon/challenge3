# -*- coding: utf-8 -*-

from flask import Flask, jsonify, json, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import datetime

from .models import MyDiary, Entries
from mydiary import app, app_db


my_diary_object = MyDiary()
my_diary_object.user_entries = Entries()

now_time = "".join(str(datetime.datetime.now().day) +
                    "/" + str(datetime.datetime.now().month) +
                    "/" + str(datetime.datetime.now().year))


""" this route links to the login page """
@app.route('/auth/signup', methods=['GET', 'POST'])
def register():
    nums = "0123456789"
    invalid_str = ",.;:!][)(><+-=}{"
    if request.method == 'POST':
        if not request.json:
            return jsonify({"input error": "invalid data type"}), 400
        if 'email' not in request.json:
            return jsonify({"input error": "Please provide an email address"}), 400
        if 'name' not in request.json:
            return jsonify({"input error": "Please provide a name for the user"}), 400
        if 'password' not in request.json:
            return jsonify({"input error": "Please provide a user password"}), 400
        data = request.get_json()
        user_name=data["name"]
        name_error = False
        if len(user_name) <= 4:
            message = "Please enter a valid first and last name"
            name_error = True
        elif len(user_name.split()) < 2:
            message = "Please enter a valid first and last name"
            name_error = True
        for letter in user_name:
            if letter in invalid_str or letter in nums:
                message = "Invalid character. Please enter a valid first and last name"
                name_error = True
        if name_error == True:
            return jsonify({"input error": message}), 400
        user_email=request.json.get('email', "")
        email_error = False
        if "@" not in user_email:
            email_error = True
        elif user_email[0] in invalid_str:
            email_error = True
        if email_error == True:
            return jsonify({"input error": "Please enter a valid email address"}), 400
        user_password=request.json.get('password', "")
        if len(user_password) <= 5:
            return jsonify({"input error": "Password too short"}), 411
        add_user = my_diary_object.addUser(user_name, user_email, user_password)
        if add_user == "Added successfully":
            user = {
                'name':user_name,
                'email':user_email,
            }
            return jsonify({"user":user}), 201
        return jsonify({"message": add_user}), 409

""" links to the login page """
@app.route('/auth/login', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        if not request.json:
            return jsonify({"input error": "Wrong input data format"}), 401
        if 'email' not in request.json:
            return jsonify({"input error": "Cannot find email. Please provide valid login credentials"}), 400
        if 'password' not in request.json:
            return jsonify({"input error": "Cannot find password. Please provide valid login credentials"}), 400
        login_email=request.json.get('email', "")
        login_password=request.json.get('password', "")
        logged_in = my_diary_object.userLogin(login_email, login_password)
        if type(logged_in) == int:
            expires = datetime.timedelta(hours=1)
            access_token = create_access_token(identity=logged_in, expires_delta=expires)
            return json.dumps({"access_token": access_token}), 200
        return jsonify({'login' : logged_in}), 401

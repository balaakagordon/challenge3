# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
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
    #invalid_str = ",.;:!][(<)|>@£#%^&*-_=+}{?"
    invalid_str = ",.;:!][)(><+-=}{"
    if request.method == 'POST':
        if not request.json:
            return jsonify({"input error": "invalid data type"}), 401
        if not 'email' in request.json:
            return jsonify({"input error": "Please provide an email address"}), 401
        if not 'name' in request.json:
            return jsonify({"input error": "Please provide a name for the user"}), 401
        if not 'password' in request.json:
            return jsonify({"input error": "Please provide a user password"}), 401
        user_name=request.json.get('name', "")
        name_error = False
        if len(user_name) <= 4:
            message = "Please enter a valid first and last name"
            name_error = True
        elif len(user_name.split()) < 2:
            message = "Please enter a first and last name"
            name_error = True
        for letter in user_name:
            if letter in invalid_str or letter in nums:
                message = "Invalid character. Please enter a valid first and last name"
                name_error = True
        if name_error == True:
            return jsonify({"input error": message}), 401
        user_email=request.json.get('email', "")
        email_error = False
        if "@" not in user_email:
            email_error = True
        elif user_email[0] in invalid_str:
            email_error = True
        if email_error == True:
            return jsonify({"input error": "Please enter a valid email address"}), 401
        user_password=request.json.get('password', "")
        if len(user_password) <= 5:
            return jsonify({"input error": "Password too short"}), 401
        add_user = my_diary_object.addUser(user_name, user_email, user_password)
        if add_user == "Added successfully":
            user = {
                'name':user_name,
                'email':user_email,
            }
            return jsonify({"user":user}), 201
        return jsonify({"message": add_user}), 400

""" links to the login page """
@app.route('/auth/login', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        if not request.json:
            return jsonify({"input error": "please input json data"}), 401
        if not 'email' in request.json:
            return jsonify({"input error": "Please provide a login email"}), 401
        if not 'password' in request.json:
            return jsonify({"input error": "Please provide a login password"}), 401
        login_email=request.json.get('email', "")
        login_password=request.json.get('password', "")
        logged_in = my_diary_object.userLogin(login_email, login_password)
        if type(logged_in) == int:
            access_token = create_access_token(identity=logged_in)
            return jsonify(access_token=access_token), 200
        return jsonify({'login' : logged_in}), 400

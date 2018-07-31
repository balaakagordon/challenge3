from flask import Flask, jsonify, request
import datetime

from models import MyDiary, Entries
from mydiary import app, app_db


my_diary_object = MyDiary()
my_diary_object.user_entries = Entries()

now_time = "".join(str(datetime.datetime.now().day)\
            +"/"+str(datetime.datetime.now().month)\
            +"/"+str(datetime.datetime.now().year))


""" this route links to the login page """
@app.route('/auth/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if not request.json or not 'email' in request.json or not 'name' in request.json or not 'password' in request.json:
            message = "Please fill in all user data"
            return jsonify({"error":message})
        else:
            user_name=request.json.get('name', "")
            user_email=request.json.get('email', "")
            user_password=request.json.get('password', "")

            add_user = my_diary_object.addUser(user_name, user_email, user_password)
            if add_user == "Added successfully":
                user = {
                    'name':user_name,
                    'email':user_email,
                }
                return jsonify({'new_user' : user})
            else:
                return jsonify({"message":add_user})

""" links to the login page """
@app.route('/auth/login', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        if not request.json or not 'email' in request.json or not 'password' in request.json:
            jsonify({"error":"Please check your input data"})
        else:
            login_email=request.json.get('email', "")
            login_password=request.json.get('password', "")
            logged_in = my_diary_object.userLogin(login_email, login_password)
            if logged_in == "You've been logged in successfully":
                #token = jwt.encode({'user' : user_id , 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
                #return jsonify({'login' : 'sucessful', 'token' : token.decode('UTF-8') })
                return jsonify({'login' : 'sucessful'})
            else:
                return jsonify({'login' : logged_in})

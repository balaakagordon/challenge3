from flask import Flask, jsonify, request
import datetime
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from models import MyDiary, Entries
from mydiary import app, app_db


my_diary_object = MyDiary()
my_diary_object.user_entries = Entries()

now_time = "".join(str(datetime.datetime.now().day) + 
            "/" + str(datetime.datetime.now().month) + 
            "/" + str(datetime.datetime.now().year))

""" returns a single diary entry """
@app.route('/api/v1/entries/<int:diary_entry_id>', methods=['GET'])
@jwt_required
def get_entry(diary_entry_id):
    """ outputs one user entry specified by the id in the url """
    user_id = get_jwt_identity()
    get_entry = my_diary_object.user_entries.getOneEntry(
                    user_id,
                    diary_entry_id
                    )
    if get_entry == None:
        return jsonify({'error': 'Bad request, the specified entry does not exist.'}), 400
    return get_entry, 200

""" returns all diary entries """
@app.route('/api/v1/entries', methods=['GET'])
@jwt_required
def get_all_entries():
    """ outputs all entries for the logged in user """
    user_id_data = get_jwt_identity()
    get_entries = my_diary_object.user_entries.getAllEntries(user_id_data)
    return get_entries, 200

""" this route adds single diary entry """
@app.route('/api/v1/entries', methods=['POST'])
@jwt_required
def post_entry():
    """ this method creates a new entry """
    if not request.json:
        return jsonify({"input error": "please input json data"}), 401
    if 'entrydata' not in request.json:
        return jsonify({"message": "Diary entry field cannot be left blank"}), 401
    if 'entrytitle' not in request.json:
        return jsonify({"message": "Diary entry title cannot be left blank"}), 401
    entry_data=request.json.get('entrydata', "")
    title_data=request.json.get('entrytitle', "")
    user_id_data = get_jwt_identity()
    add_entry = my_diary_object.user_entries.addEntry(
                    user_id_data,
                    title_data,
                    entry_data,
                    now_time
                    )
    if add_entry == "Entry added successfully":
        new_entry = {
            'user_id' : user_id_data,
            'title' : title_data,
            'entrydata' : entry_data,
            'datecreated' : now_time
        }
    return jsonify({'message' : add_entry, 'entry added' : new_entry}), 201

""" this route updates a single diary entry """
@app.route('/api/v1/entries/<int:diary_entry_id>', \
            methods=['PUT'])
@jwt_required
def put_entry(diary_entry_id):
    """ this method updates an entry's data """
    if not request.json:
        return jsonify({"input error": "please input json data"}), 401
    if 'entrydata' not in request.json:
        return jsonify({"message": "Diary entry field cannot be left blank"}), 401
    if 'entrytitle' not in request.json:
        return jsonify({"message": "Diary entry title cannot be left blank"}), 401
    entry_data = request.json.get('entrydata', "")
    title_data = request.json.get('entrytitle', "")
    user_id_data = get_jwt_identity()
    entry_id_data = diary_entry_id
    edit_entry = my_diary_object.user_entries.modifyEntry(
                    title_data,
                    entry_data,
                    now_time,
                    entry_id_data,
                    user_id_data
                    )
    if edit_entry == "Entry edited":
        entry = {
            'entry_id': entry_id_data,
            'user_id': user_id_data,
            'title': title_data,
            'entrydata': entry_data,
            'datecreated': now_time
        }
        return jsonify({'entry':entry}), 201
    return jsonify({'error': edit_entry}), 400

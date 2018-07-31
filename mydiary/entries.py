from flask import Flask, jsonify, request
import datetime

from models import MyDiary, Entries
from mydiary import app, app_db


my_diary_object = MyDiary()
my_diary_object.user_entries = Entries()

now_time = "".join(str(datetime.datetime.now().day)\
            +"/"+str(datetime.datetime.now().month)\
            +"/"+str(datetime.datetime.now().year))

""" returns a single diary entry """
@app.route('/home/api/v1/entries/<int:diary_entry_id>', methods=['GET'])
#@login_required
def get_entry(diary_entry_id):
    """ outputs one user entry """
    #token = request.args.get('token')
    #data = jwt.decode(token, app.config['SECRET_KEY'])
    user_id = my_diary_object.current_user
    get_entry = my_diary_object.user_entries.getOneEntry(user_id, diary_entry_id)
    if get_entry == None:
        return jsonify({'error': 'Bad request, the specified entry does not exist.'})
    else:
        return get_entry

""" returns all diary entries """
@app.route('/home/api/v1/entries', methods=['GET'])
#@login_required
def get_all_entries():
    """ this method outputs all entries """
    #token = request.args.get('token')
    #data = jwt.decode(token, app.config['SECRET_KEY'])

    user_id_data = my_diary_object.current_user
    get_entries = my_diary_object.user_entries.getAllEntries(user_id_data)
    return get_entries

""" this route adds single diary entry """
@app.route('/home/api/v1/entries', methods=['POST'])
#@login_required
def post_entry():
    """ this method creates a new entry """
    #token = request.args.get('token')
    #data = jwt.decode(token, app.config['SECRET_KEY'])

    if not request.json or not 'entrydata' in request.json:
        return jsonify({"error": "Incorrect data format"})
    else:
        entry_data=request.json.get('entrydata', "")
        title_data=request.json.get('entrytitle', "")
        #entry_id_data = my_diary_object.user_entries.getNextEntryId + 1
        
        user_id_data = my_diary_object.current_user
        add_entry = my_diary_object.user_entries.addEntry(user_id_data, title_data, entry_data, now_time)
        if add_entry == "Entry added successfully":
            entry = {
                'user_id' : user_id_data,
                'title' : title_data,
                'entrydata' : entry_data,
                'datecreated' : now_time
            }
        return jsonify({'message' : add_entry, 'entry added' : entry})

""" this route updates a single diary entry """
@app.route('/home/api/v1/entries/<int:diary_entry_id>', \
                methods=['PUT'])
#@login_required
def put_entry(diary_entry_id):
    """ this method updates an entry's data """
    #token = request.args.get('token')
    #data = jwt.decode(token, app.config['SECRET_KEY'])

    if not request.json:
        return jsonify({"error": "Incorrect data format"})
    elif 'entrydata' in request.json and \
                type(request.json['entrydata']) is not unicode:
        return jsonify({"error": "Incorrect data format"})
    elif 'title' in request.json and type(request.json['title']) is not str:
        return jsonify({"error": "Incorrect data format"})
    entry_data = request.json.get('entrydata', "")
    title_data = request.json.get('entrytitle', "")
    entry_id_data = diary_entry_id
    user_id_data = my_diary_object.current_user
    edit_entry = my_diary_object.user_entries.modifyEntry(title_data, entry_data, now_time, entry_id_data, user_id_data)
    if edit_entry == "Entry edited":
        entry = {
            'entry_id': entry_id_data,
            'user_id': user_id_data,
            'title':title_data,
            'entrydata':entry_data,
            'datecreated':now_time
        }
        return jsonify({'entry':entry})
    else:
        return jsonify({'error': edit_entry})

""" this route deletes a diary entry """
@app.route('/home/api/v1/entries/<int:diary_entry_id>', methods=['DELETE'])
#@login_required
def delete_entry(diary_entry_id):
    """ this method deletes an entry """
    #token = request.args.get('token')
    #data = jwt.decode(token, app.config['SECRET_KEY'])

    entry_id_data = diary_entry_id
    user_id_data = my_diary_object.current_user
    entry_delete = my_diary_object.user_entries.deleteEntry(entry_id_data, user_id_data)
    return jsonify({'delete result':entry_delete})
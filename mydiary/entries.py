from mydiary import app, app_db, my_diary_object
from flask import Flask, jsonify



""" returns a single diary entry """
@app.route('/home/api/v1/entries/<int:diary_entry_id>', methods=['GET'])
#@login_required
def get_entry(diary_entry_id):
    """ outputs one user entry """
    #token = request.args.get('token')
    #data = jwt.decode(token, app.config['SECRET_KEY'])
    user_id = my_diary_object.current_user
    entry = my_diary_object.user_entries.getOneEntry(user_id, diary_entry_id)
    if entry == None:
        return jsonify({'error': 'Bad request, the specified entry does not exist.'})
    else:
        return jsonify({'entry':entry})
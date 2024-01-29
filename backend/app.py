from get_prediction import Predictions_Class
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import sqlite3
import sql_utils
import os


PLAYERS_DB = 'players.db'

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/upload', methods=['POST'])
def file_upload():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return jsonify({'message': f'File {filename} uploaded successfully'}), 200


@app.route('/get_table', methods=['GET'])
def get_teams():
    teams = sql_utils.get_table('teams.db', 'TEAMS')
    return jsonify(teams)


@app.route('/get_row/<db>', methods=['GET'])
def get_teams():
    teams = sql_utils.get_table('teams.db', 'TEAMS')
    return jsonify(teams)


@app.route('/get_batter', methods=['GET'])
def get_batter():
    id = request.args.get('id')
    response_data = sql_utils.get_sql_data(PLAYERS_DB, 'BATTERS', id)
    return jsonify(response_data)


@app.route('/get_pitcher', methods=['GET'])
def get_pitcher():
    id = request.args.get('id')
    response_data = sql.get_sql_data(PLAYERS_DB, 'PITCHERS', id)
    return jsonify(response_data)


@app.route('/make_prediction', methods=['GET'])
def make_prediction():
    my_obj = Predictions_Class()
    pitch_type = my_obj.get_type(request.args)
    pitch_speed = my_obj.get_speed(pitch_type)
    return jsonify(pitch_type, pitch_speed)


if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)

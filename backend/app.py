from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import sqlite3
import utils
import os


PLAYER_DB_FILENAME = 'players.db'

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


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/get_batter', methods=['GET'])
def get_batter():
    id = request.args.get('id')
    response_data = utils.get_sql_data(PLAYER_DB_FILENAME, 'BATTERS', id)
    return jsonify(response_data)


@app.route('/get_pitcher', methods=['GET'])
def get_pitcher():
    id = request.args.get('id')
    response_data = utils.get_sql_data(PLAYER_DB_FILENAME, 'PITCHERS', id)
    return jsonify(response_data)


if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
from get_prediction import Predictions_Class
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import sql_utils
import os

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
    

@app.route("/get_teams", methods=["GET"])
def get_teams():
    teams_dict = sql_utils.get_table("TEAMS")
    if teams_dict:
        return jsonify(teams_dict)
    else:
        return jsonify({"error": "Teams not found"}), 404


@app.route('/get_roster/<int:id>', methods=['GET'])
def get_roster(id):
    roster_dict = sql_utils.get_table("ROSTERS", where=("team_id", id))
    if roster_dict:
        return jsonify(roster_dict)
    else:
        return jsonify({"error": "Roster not found"}), 404


@app.route('/get_batter/<int:id>', methods=['GET'])
def get_batter(id):
    batter_dict = sql_utils.get_row("BATTERS", id)
    if batter_dict:
        return jsonify(batter_dict)
    else:
        return jsonify({"error": "Batter not found"}), 404


@app.route('/make_prediction', methods=['GET'])
def make_prediction():
    my_obj = Predictions_Class()
    pitch_type = my_obj.get_type(request.args)
    pitch_speed = my_obj.get_speed(pitch_type)
    return jsonify(pitch_type, pitch_speed)


if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)

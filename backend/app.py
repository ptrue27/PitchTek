from get_prediction import Predictions_Class
from PitchDataProcessor import PitchDataProcessor
from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename
from flask_cors import CORS
import sql_utils
import os
import statsapi
import plotly.express as px
import plotly.io as pio

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
    batters_dict = sql_utils.get_table("BATTERS", cols=["id", "name"], where=["team_id", id])
    pitchers_dict = sql_utils.get_table("PITCHERS", cols=["id", "name"], where=["team_id", id])
    roster_dict = {"batters": batters_dict, "pitchers": pitchers_dict}
    if batters_dict and pitchers_dict:
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


@app.route('/get_pitcher/<int:id>', methods=['GET'])
def get_pitcher(id):
    pitcher_dict = sql_utils.get_row("PITCHERS", id)
    if pitcher_dict:
        return jsonify(pitcher_dict)
    else:
        return jsonify({"error": "Pitcher not found"}), 404


@app.route('/make_prediction', methods=['GET'])
def make_prediction():
    my_obj = Predictions_Class()
    pitch_type = my_obj.get_type(request.args)
    pitch_speed = my_obj.get_speed(pitch_type)
    return jsonify(pitch_type, pitch_speed)


@app.route('/show-history')
def show_history():
    processor = PitchDataProcessor(
        input_file='C:/Users/davis/PitchTek-2/uploads/first_pitch.csv', output_dir='C:/Users/davis/PitchTek-2/tests')
    processor.process_data()

    # Assuming images are saved in 'static/images' directory under your Flask app
    image_files = os.listdir('C:/Users/davis/PitchTek-2/tests')
    image_urls = [
        f'C:/Users/davis/PitchTek-2/tests/{filename}' for filename in image_files if filename.endswith('.png')]

    # Return the image URLs in JSON format
    return jsonify(imageUrls=image_urls)


if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)

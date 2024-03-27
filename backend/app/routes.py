from app.get_prediction import Predictions_Class
from app import app, sql_utils, user_manager
import statsapi 
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os


@app.route('/sign_up', methods=['POST'])
def sign_up():
    data = request.get_json()
    result = user_manager.user_sign_up(data["username"], data["password"])
    if result == "success":
        return jsonify({'message': 'User signed up successfully'}), 201
    elif result == "exists":
        return jsonify({'message': 'Username is unavailable'}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    result = user_manager.user_login(data["username"], data["password"])
    if result:
        return jsonify({'message': 'User logged in successfully'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    user_manager.user_logout()
    return jsonify({'message': 'User logged out successfully'}), 200


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

@app.route("/api/mlb_player_stats", methods=['GET'])
def get_mlb_player_stats():
    # Assuming you're using the player's name to fetch stats
    player_name = request.args.get('player_name')
    # You might need to implement a way to resolve the player's name to an ID statsapi can use, as statsapi often requires player IDs for specific queries.

    # Fetch player stats using statsapi
    try:
        # Example: Fetching player info. You may need to adjust the query based on what info you need
        player_info = statsapi.lookup_player(player_name)
        if player_info:
            # Assuming the first result is the desired player
            player_id = player_info[0]['id']
            stats = statsapi.player_stat_data(player_id, type='career')  # Adjust season as needed
            return jsonify(stats)
        else:
            return jsonify({"error": "Player not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    pass
if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)

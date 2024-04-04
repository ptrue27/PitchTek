from app.get_prediction import Predictions_Class
from app import app, sql_utils, user_manager
#import statsapi 
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os


@app.route('/api/sign_up', methods=['POST'])
def sign_up():
    data = request.get_json()
    result = user_manager.user_sign_up(data["username"], data["password"])
    if result == "success":
        return jsonify({'message': 'User signed up successfully'}), 201
    elif result == "exists":
        return jsonify({'message': 'Username is unavailable'}), 400


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    result = user_manager.user_login(data["username"], data["password"])
    if result:
        return jsonify({'message': 'User logged in successfully'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    user_manager.user_logout()
    return jsonify({'message': 'User logged out successfully'}), 200


@app.route("/api/get_teams", methods=["GET"])
def get_teams():
    teams_dict = sql_utils.get_table("TEAMS")
    if teams_dict:
        return jsonify(teams_dict)
    else:
        return jsonify({"error": "Teams not found"}), 404


@app.route('/api/get_roster/<int:id>', methods=['GET'])
def get_roster(id):
    batters_dict = sql_utils.get_table("BATTERS", cols=["id", "name"], where=["team_id", id])
    pitchers_dict = sql_utils.get_table("PITCHERS", cols=["id", "name"], where=["team_id", id])
    roster_dict = {"batters": batters_dict, "pitchers": pitchers_dict}
    if batters_dict and pitchers_dict:
        return jsonify(roster_dict)
    else:
        return jsonify({"error": "Roster not found"}), 404


@app.route('/api/get_batter/<int:id>', methods=['GET'])
def get_batter(id):
    batter_dict = sql_utils.get_row("BATTERS", id)
    if batter_dict:
        return jsonify(batter_dict)
    else:
        return jsonify({"error": "Batter not found"}), 404


@app.route('/api/get_pitcher/<int:id>', methods=['GET'])
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


'''
UPLOAD_FOLDER = 'C:/Users/davis/PitchTek-2/backend/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 401
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        return jsonify({'message': 'File uploaded successfully'}), 200
@app.route("/api/mlb_player_stats", methods=['GET'])
def get_mlb_player_stats():
    player_name = request.args.get('player_name').lower().strip()
    try:
        player_info = statsapi.lookup_player(player_name)
        matched_player = None
        for player in player_info:
            # Compare lowercased and stripped names for a basic match
            if player_name == player['fullName'].lower().strip():
                matched_player = player
                break
        
        if matched_player:
            player_id = matched_player['id']
            stats = statsapi.player_stat_data(player_id, type='career')  # Adjust the type or season as needed
            return jsonify(stats)
        else:
            return jsonify({"error": "Player not found"}), 404
    except Exception as e:
        print("Failed to fetch player stats: %s", str(e))
        return jsonify({"error": str(e)}), 500
@app.route("/api/player_pitching_stats", methods=['GET'])
def get_player_pitching_stats():
    player_name = request.args.get('player_name')

    if not player_name:
        return jsonify({"error": "Please specify a player name"}), 400

    try:
        player_search = statsapi.lookup_player(player_name)
        if not player_search:
            return jsonify({"error": f"No players found with the name '{player_name}'."}), 404

        player_id = player_search[0]['id']
        player_data = statsapi.player_stat_data(player_id, group="pitching", type='career')

        if 'stats' in player_data and player_data['stats']:
            pitching_stats = player_data['stats'][0].get('stats', {})

            # List of desired stats keys
            desired_stats_keys = [
                'gamesPlayed', 'gamesStarted', 'groundOuts', 'airOuts', 'runs', 'doubles', 'triples',
                'homeRuns', 'strikeOuts', 'baseOnBalls', 'intentionalWalks', 'hits', 'hitByPitch',
                'avg', 'atBats', 'obp', 'slg', 'ops', 'caughtStealing', 'stolenBases',
                'stolenBasePercentage', 'groundIntoDoublePlay', 'numberOfPitches', 'era',
                'inningsPitched', 'wins', 'losses', 'saves', 'saveOpportunities', 'holds',
                'blownSaves', 'earnedRuns', 'whip', 'battersFaced', 'outs', 'gamesPitched',
                'completeGames', 'shutouts', 'strikes', 'strikePercentage', 'hitBatsmen', 'balks',
                'wildPitches', 'pickoffs', 'totalBases', 'groundOutsToAirouts', 'winPercentage',
                'pitchesPerInning', 'gamesFinished', 'strikeoutWalkRatio', 'strikeoutsPer9Inn',
                'walksPer9Inn', 'hitsPer9Inn', 'runsScoredPer9', 'homeRunsPer9', 'inheritedRunners',
                'inheritedRunnersScored', 'catchersInterference', 'sacBunts', 'sacFlies'
            ]

            # Constructing the structured_stats dictionary
            structured_stats = {stat: pitching_stats.get(stat, 'Stat not available') for stat in desired_stats_keys}

            return jsonify({
                "player_id": player_id,
                "name": player_search[0]['fullName'],
                "team": player_search[0].get('currentTeam', {}).get('name', 'N/A'),
                "stats": structured_stats
            })

        else:
            return jsonify({"error": "Pitching stats not found for this player"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route("/api/player_fielding_stats", methods=['GET'])
def get_player_fielding_stats():
    player_name = request.args.get('player_name')

    if not player_name:
        return jsonify({"error": "Please specify a player name"}), 400

    try:
        player_search = statsapi.lookup_player(player_name)
        if not player_search:
            return jsonify({"error": f"No players found with the name '{player_name}'."}), 404

        player_id = player_search[0]['id']
        player_data = statsapi.player_stat_data(player_id, group="fielding", type='career')

        if 'stats' in player_data and player_data['stats']:
            fielding_stats = player_data['stats'][0].get('stats', {})

            # Specified fielding stats keys
            desired_stats_keys = [
                'gamesPlayed', 'gamesStarted', 'assists', 'putOuts', 'errors', 'chances', 
                'fielding', 'rangeFactorPerGame', 'rangeFactorPer9Inn', 'innings', 'games', 
                'doublePlays', 'triplePlays', 'throwingErrors'
            ]

            # Position info might need special handling if it's nested
            position_info = fielding_stats.get('position', {})
            position = {
                'code': position_info.get('code', 'N/A'),
                'name': position_info.get('name', 'N/A'),
                'type': position_info.get('type', 'N/A'),
                'abbreviation': position_info.get('abbreviation', 'N/A')
            }

            # Constructing the structured_stats dictionary
            structured_stats = {stat: fielding_stats.get(stat, 'Stat not available') for stat in desired_stats_keys}
            structured_stats['position'] = position  # Add position info

            return jsonify({
                "player_id": player_id,
                "name": player_search[0]['fullName'],
                "team": player_search[0].get('currentTeam', {}).get('name', 'N/A'),
                "stats": structured_stats
            })

        else:
            return jsonify({"error": "Fielding stats not found for this player"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/player_batting_stats", methods=['GET'])
def get_player_batting_stats():
    player_name = request.args.get('player_name')

    if not player_name:
        return jsonify({"error": "Please specify a player name"}), 400

    try:
        player_search = statsapi.lookup_player(player_name)
        if not player_search:
            return jsonify({"error": f"No players found with the name '{player_name}'."}), 404

        player_id = player_search[0]['id']
        player_data = statsapi.player_stat_data(player_id, group="hitting", type='career')

        if 'stats' in player_data and player_data['stats']:
            batting_stats = player_data['stats'][0].get('stats', {})

            # Specified batting stats
            desired_stats_keys = [
                'gamesPlayed', 'groundOuts', 'airOuts', 'runs', 'doubles', 'triples',
                'homeRuns', 'strikeOuts', 'baseOnBalls', 'intentionalWalks', 'hits',
                'hitByPitch', 'avg', 'atBats', 'obp', 'slg', 'ops', 'caughtStealing',
                'stolenBases', 'stolenBasePercentage', 'groundIntoDoublePlay',
                'numberOfPitches', 'plateAppearances', 'totalBases', 'rbi', 'leftOnBase',
                'sacBunts', 'sacFlies', 'babip', 'groundOutsToAirouts', 'catchersInterference',
                'atBatsPerHomeRun'
            ]

            # Constructing the structured_stats dictionary
            structured_stats = {stat: batting_stats.get(stat, 'Stat not available') for stat in desired_stats_keys}

            return jsonify({
                "player_id": player_id,
                "name": player_search[0]['fullName'],
                "team": player_search[0].get('currentTeam', {}).get('name', 'N/A'),
                "stats": structured_stats
            })

        else:
            return jsonify({"error": "Batting stats not found for this player"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

'''

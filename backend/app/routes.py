from app.get_prediction import Predictions_Class
from app import app, user_manager, stats_api
#import statsapi 
from app.data_visualizer import DataVisualizer
import os
from flask import Flask, request, jsonify, send_file, send_from_directory
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend, which is non-interactive and does not require a GUI.
import matplotlib.pyplot as plt

import io
import base64
@app.route('/api/sign_up', methods=['POST'])
def sign_up():
    data = request.get_json()
    token = user_manager.user_sign_up(data["username"], data["password"])
    if token:
        seasons = ["2024 MLB", "2023 MLB", "2023 UNR", "2023 TMCC"]
        return jsonify({'message': 'User signed up successfully', 
                        'seasons': seasons, 'token': token}), 200
    else:
        return jsonify({'message': 'Username is unavailable'}), 400


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    token = user_manager.user_login(data["username"], data["password"])
    if token:
        seasons = ["2024 MLB", "2023 MLB", "2023 UNR", "2023 TMCC"]
        return jsonify({'message': 'User logged in successfully', 
                        'seasons': seasons, 'token': token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    user_manager.user_logout()
    return jsonify({'message': 'User logged out successfully'}), 200


@app.route("/api/get_teams", methods=["GET"])
def get_teams():
    teams_dict = stats_api.get_table("TEAMS")
    if teams_dict:
        return jsonify(teams_dict)
    else:
        return jsonify({"error": "Teams not found"}), 404


@app.route('/api/get_roster/<int:id>', methods=['GET'])
def get_roster(id):
    batters_dict = stats_api.get_table("BATTERS", cols=["id", "name"], where=["team_id", id])
    pitchers_dict = stats_api.get_table("PITCHERS", cols=["id", "name"], where=["team_id", id])
    roster_dict = {"batters": batters_dict, "pitchers": pitchers_dict}
    if batters_dict and pitchers_dict:
        return jsonify(roster_dict)
    else:
        return jsonify({"error": "Roster not found"}), 404


@app.route('/api/get_batter/<int:id>', methods=['GET'])
def get_batter(id):
    batter_dict = stats_api.get_row("BATTERS", id)
    if batter_dict:
        return jsonify(batter_dict)
    else:
        return jsonify({"error": "Batter not found"}), 404


@app.route('/api/get_pitcher/<int:id>', methods=['GET'])
def get_pitcher(id):
    pitcher_dict = stats_api.get_row("PITCHERS", id)
    if pitcher_dict:
        return jsonify(pitcher_dict)
    else:
        return jsonify({"error": "Pitcher not found"}), 404


@app.route('/make_prediction', methods=['GET'])
def make_prediction():
    #predicter = Predictions_Class()

    # Extract keys associated with 'param1'
    #param1_keys = [key for key in request.args.keys() if key.startswith('param1')]
    #param1_dict = {key.split('[', 1)[1][:-1]: request.args[key] for key in param1_keys}

    #pitch_type = predicter.get_type(param1_dict, request.args.get("param2"))
    #pitch_speed = predicter.get_speed(pitch_type)
    pitch_type = "Sinker (SI)"
    pitch_speed = 92.7
    return jsonify(pitch_type, pitch_speed)
df_global = pd.DataFrame()


@app.route('/get_latest_at_bat', methods=['GET'])
def get_latest_at_bat():
    player_name = request.args.get('player_name')
    if not player_name or df_global.empty:
        return jsonify({'error': 'No data or player name provided'}), 400

    # Filter the data for the selected player and get the latest entry
    player_data = df_global[df_global['player_from_des'] == player_name]
    latest_at_bat = player_data.iloc[-1]  # assuming the data is ordered chronologically

    # Prepare the data for visualization
    data = {
        'plate_x': latest_at_bat['plate_x'],
        'plate_z': latest_at_bat['plate_z'],
        'description': latest_at_bat['des']
    }
    return jsonify(data)
df_global = pd.DataFrame()
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    global df_global
    file = request.files['file']
    df_global = pd.read_csv(file)
    df_global['player_from_des'] = df_global['des'].apply(lambda x: ' '.join(x.split()[:2]))
    players = df_global['player_from_des'].unique().tolist()
    return jsonify(players)


os.makedirs('static', exist_ok=True)


@app.route('/fetch_latest_at_bat_plot', methods=['GET'])
def fetch_latest_at_bat_plot():
    player_name = request.args.get('player_name')
    if not player_name:
        return jsonify({'error': 'Player name parameter is missing'}), 400

    if df_global.empty or 'player_from_des' not in df_global.columns:
        return jsonify({'error': 'No data available or incorrect data format'}), 400

    mask = df_global['player_from_des'].str.contains(player_name, na=False)
    if not mask.any():
        return jsonify({'error': 'Player not found in data'}), 404

    start_index = mask[mask].index[0]
    end_index = mask[start_index:].idxmin() if False in mask[start_index:].values else None

    # Subset the data for the player
    player_data = df_global[start_index:end_index]
    player_data = player_data[player_data['des'] == player_data.loc[start_index, 'des']]

    if player_data.empty:
        return jsonify({'error': 'No data found for this player'}), 404

    latest_at_bat = player_data.iloc[-1]

    # Generate plot
    fig, ax = plt.subplots()
    ax.scatter(player_data['plate_x'], player_data['plate_z'], color='blue')

    # Adding a strike zone box
    strike_zone_bottom = 1.5
    strike_zone_top = 3.5
    plate_width = 1.42
    ax.add_patch(plt.Rectangle((-plate_width/2, strike_zone_bottom), plate_width, strike_zone_top - strike_zone_bottom, fill=False, color='red', lw=2))

    # Annotating points
    for i, point in enumerate(player_data.itertuples(), 1):
        ax.annotate(str(i), (point.plate_x, point.plate_z), textcoords="offset points", xytext=(0,10), ha='center')

    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 5)
    ax.set_title(f"Latest at-bat: {latest_at_bat['des']}")
    ax.set_xlabel('Plate X')
    ax.set_ylabel('Plate Z')

    # Save the plot to a file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    base_directory = os.path.dirname(os.path.dirname(os.path.dirname(current_directory)))
    filename = "latest_at_bat.png"
    file_path = os.path.join(base_directory, 'Pitchtek/frontend/src/assets/static/', filename)
    plt.savefig(file_path)
    plt.close(fig)

    return jsonify({'image_url': f'static/{filename}'})



@app.route('/get_latest_image', methods=['GET'])
def get_latest_image():
    return send_from_directory(app.static_folder, 'latest_at_bat_plot.png')
'''
# Directory where uploaded files are stored
UPLOAD_FOLDER = 'C:/Users/davis/PitchTek-2/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Variable to keep track of the latest uploaded file
latest_uploaded_file = None

@app.route('/api/upload', methods=['POST'])
def upload_file():
    global latest_uploaded_file
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)
    
    # Update the path of the latest uploaded file
    latest_uploaded_file = save_path
    print(latest_uploaded_file)
    return jsonify({'message': 'File uploaded successfully'}), 200


@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory('C:/Users/davis/PitchTek-2/frontend/src/assets/', filename)

@app.route('/api/generate-images', methods=['POST'])
def generate_images_route():
    print(" test: ", latest_uploaded_file)
    if latest_uploaded_file is None:
        return jsonify({'error': 'No file has been uploaded yet'}), 400

    # Initialize your DataVisualizer with the uploaded file
    visualizer = DataVisualizer(latest_uploaded_file)

    # Assuming your Flask app runs on localhost:5000, construct the URLs for the images
    image_urls = [
        'http://localhost:5000/images/heatMapOFCounts.png',
        'http://localhost:5000/images/count_vs_description_heatmap.png',
        'http://localhost:5000/images/pitchVeloLastGame.png'
    ]

    # Return these URLs in the response
    return jsonify({'message': 'Images generated successfully', 'images': image_urls})


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
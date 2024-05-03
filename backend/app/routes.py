from app.data_visualizer import DataVisualizer
from app import app, user_manager, stats_api, sql_utils

from datetime import datetime
from flask import request, jsonify, render_template, send_from_directory
from flask_jwt_extended import get_jwt_identity, jwt_required
import matplotlib
import os
import pandas as pd
import statsapi
from werkzeug.utils import secure_filename
from app.pitch_predictions import RF_prediction
from experiments.create_heatmap import make_heat_map

# Use the 'Agg' backend, which is non-interactive and does not require a GUI.
matplotlib.use('Agg')  
import matplotlib.pyplot as plt

# Configure directories using environment variables or default to a relative path
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './uploads')
app.config['STATIC_FOLDER'] = os.getenv('STATIC_FOLDER', './static')

df_global = pd.DataFrame()
#HOST = "localhost:5000" # development
HOST = "pitchtek.pro" # deployment


@app.route('/api/sign_up', methods=['POST'])
def sign_up():
    data = request.get_json()
    res = user_manager.user_sign_up(data["username"], data["password"])
    if res:
        return jsonify(res), 200
    return jsonify({'message': 'Username is unavailable'}), 400


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    res = user_manager.user_login(data["username"], data["password"])
    if res:
        return jsonify(res), 200
    return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    user_manager.user_logout()
    return jsonify({'message': 'User logged out successfully'}), 200

 
@app.route("/api/get_teams", methods=["GET"])
def get_teams():
    season_id = request.args.get("season_id")
    season_name = request.args.get("season_name")
    split_name = season_name.split()

    # Get MLB or custom teams
    if split_name[0] == "MLB":
        ids, names = stats_api.get_teams(int(split_name[1]))
    else:
        ids, names = sql_utils.get_cols("TEAMS", ["id", "name"],
                                        "season_id", season_id)
        
    return jsonify({"ids": ids, "names": names})


@app.route('/api/get_roster', methods=['GET'])
def get_roster():
    team_id = request.args.get("team_id")
    season_name = request.args.get("season_name")
    split_name = season_name.split()

    # Get MLB or custom roster
    if split_name[0] == "MLB":
        pitchers, batters = stats_api.get_roster(team_id, int(split_name[1]))
    else:
        ids, names = sql_utils.get_cols("PITCHERS", ["id", "name"],
                                        "team_id", team_id)
        pitchers = {"ids": ids, "names": names}
        ids, names = sql_utils.get_cols("BATTERS", ["id", "name"],
                                        "team_id", team_id)
        batters = {"ids": ids, "names": names}
    
    return jsonify({"pitchers": pitchers, "batters": batters})


@app.route('/api/get_batter', methods=['GET'])
def get_batter():
    id = request.args.get("id")
    season_name = request.args.get("season_name")
    split_name = season_name.split()

    # Get MLB batter
    if split_name[0] == "MLB":
        batter = stats_api.get_batter(id, int(split_name[1]))
        return jsonify(batter)

    return jsonify({"error": "Batter not found"}), 404


@app.route('/api/get_pitcher', methods=['GET'])
def get_pitcher():
    id = request.args.get("id")
    season_name = request.args.get("season_name")
    split_name = season_name.split()

    # Get MLB pitcher
    if split_name[0] == "MLB":
        pitcher = stats_api.get_pitcher(id, int(split_name[1]))
        return jsonify(pitcher)

    return jsonify({"error": "Pitcher not found"}), 404


@app.route('/api/get_versus', methods=['GET'])
def get_versus():
    pitcher_id = request.args.get("pitcher_id")
    batter_id = request.args.get("batter_id")
    season_name = request.args.get("season_name")
    split_name = season_name.split()

    # Get MLB pitcher
    if split_name[0] == "MLB":
        matchup = stats_api.get_versus(batter_id, pitcher_id)
        return jsonify(matchup)

    return jsonify({"error": "Versus statistics not found"}), 404


@app.route('/api/get_history', methods=['GET'])
def get_history():
    game_id = request.args.get("game_id")
    game_states = sql_utils.get_records("GAMESTATES", "game_id",  game_id)
    return jsonify({"game_states": game_states})


@app.route('/api/get_games', methods=['GET'])
def get_games():
    season_id = request.args.get("season_id")
    games = sql_utils.get_records("GAMES", "season_id", season_id, sort='DESC')
    ids, names = [], []
    for game in games:
        ids.append(game["id"])
        home, away = game["home_team_name"], game["away_team_name"]
        names.append(f"{game['start_time']} - {home} vs. {away}")
    return jsonify({"ids": ids, "names": names})


@app.route('/api/new_game', methods=['POST'])
def new_game():
    game = request.json
    current_time = datetime.now()
    game['start_time'] = current_time.strftime("%m/%d %I:%M")
    game_id = sql_utils.insert_record("GAMES", game, get_id=True)
    return jsonify({"id": game_id})

pitch_dict = {
    'CH' : "Changeup",
    'CU' : "Curveball",
    'FC' : "Cutter",
    'EP' : "Eephus",
    'FO' : "Forkball",
    'FF' : "Fastball",
    'KN' : "Knuckleball",
    'KC' : "Knuckle-Curve",
    'SC' : "Screwball",
    'SI' : "Sinker",
    'SL' : "Slider",
    'SV' : "Slurve",
    'FS' : "Splitter",
    'ST' : "Sweeper"
}

@app.route('/new_prediction', methods=['POST'])
def new_prediction():


    params = request.json  # Get all parameters passed
    print("Params received:", params)  # Log all params received

    # unpack game state variables
    release_speed = float(params["release_speed"])
    plate_x = float(params["plate_x"])
    plate_z = float(params["plate_z"])
    balls = int(params["balls"])
    strikes = int(params["strikes"])
    pitcher_id = int(params["pitcher_id"])

    # get pitch predictions
    pitch_type, location, error, average_release_speed\
        = RF_prediction(release_speed, plate_x, plate_z, balls, strikes, pitcher_id)

    # generate image and get image name
    file_name = make_heat_map(pitch_type, pitcher_id, location)

    prediction = {
        "img": file_name,
        "speed": round(average_release_speed,1),
        "location": location,
        "confidence": 1154.73,
        "type": pitch_dict[pitch_type],
    }

    # Store pitch data
    game_state = request.json
    game_state["prediction_img"] = prediction["img"]
    game_state["prediction_speed"] = prediction["speed"]
    game_state["prediction_location"] = prediction["location"]
    game_state["prediction_confidence"] = prediction["confidence"]
    game_state["prediction_type"] = prediction["type"]
    #sql_utils.insert_record("GAMESTATES", game_state)

    return jsonify(prediction)


@app.route('/api/new_season', methods=['POST'])
@jwt_required()
def new_season():
    season = request.json
    season["user_id"] = get_jwt_identity()

    # Handle season already exists
    if sql_utils.record_exists("SEASONS", season):
        return jsonify({"msg": "Season name already exists"}), 404
    
    # Add season to database
    season_id = sql_utils.insert_record("SEASONS", season, get_id=True)
    return jsonify({"id": season_id})


@app.route('/api/delete_season', methods=['POST'])
@jwt_required()
def delete_season():
    season = request.json
    season["user_id"] = get_jwt_identity()

    # Delete from database
    season_id = sql_utils.delete_record("SEASONS", season, get_id=True)
    return jsonify({"id": season_id})


@app.route('/api/new_team', methods=['POST'])
@jwt_required()
def new_team():
    team = request.json

    # Handle team already exists
    if sql_utils.record_exists("TEAMS", team):
        return jsonify({"msg": "Team name already exists"}), 404
    
    # Add team to database
    team_id = sql_utils.insert_record("TEAMS", team, get_id=True)
    return jsonify({"id": team_id})


@app.route('/api/delete_team', methods=['POST'])
@jwt_required()
def delete_team():
    team = request.json

    # Delete from database
    team_id = sql_utils.delete_record("TEAMS", team, get_id=True)
    return jsonify({"id": team_id})


@app.route('/api/download-template', methods=['GET'])
def download_template():
    try:
        # Define the directory where the file is stored
        directory_path = os.path.join(app.config['STATIC_FOLDER'], 'assets')
        
        # Define the filename
        filename = 'Pitch_Data_Template.csv'
        
        # Serve the file with the correct directory and filename
        print(directory_path,filename)
        return send_from_directory(directory_path, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": "File not found or server error", "message": str(e)}), 500


@app.route('/api/upload_csv', methods=['POST'])
def upload_csv():
    global df_global
    file = request.files['file']
    df_global = pd.read_csv(file)
    df_global['player_from_des'] = df_global['des'].apply(lambda x: ' '.join(x.split()[:2]))
    players = df_global['player_from_des'].unique().tolist()
    return jsonify(players)


@app.route('/api/fetch_latest_at_bat_plot', methods=['GET'])
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
    ax.set_title(f"{latest_at_bat['des']}")
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
    latest_uploaded_file = save_path
    return jsonify({'message': 'File uploaded successfully'}), 200


@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
@app.route('/api/generate-heatmap-counts', methods=['GET'])
def generate_heatmap_counts():
    visualizer = DataVisualizer(df_global)  # Assuming df_global is your DataFrame
    img_data = visualizer.generate_heatmap_of_counts()
    return send_file(img_data, mimetype='image/png', as_attachment=False)

@app.route('/api/generate-heatmap-description', methods=['GET'])
def generate_heatmap_description():
    visualizer = DataVisualizer(df_global)
    img_data = visualizer.generate_count_vs_description_heatmap()
    return send_file(img_data, mimetype='image/png', as_attachment=False)

@app.route('/api/generate-velocity-chart', methods=['GET'])
def generate_velocity_chart():
    visualizer = DataVisualizer(df_global)
    img_data = visualizer.generate_pitch_velocity_chart()
    return send_file(img_data, mimetype='image/png', as_attachment=False)


import base64

def encode_image(img_bytes):
    return base64.b64encode(img_bytes.getvalue()).decode('utf-8')

@app.route('/api/generate-images', methods=['POST'])
def generate_images_route():
    global latest_uploaded_file
    if latest_uploaded_file is None:
        return jsonify({'error': 'No file has been uploaded yet'}), 400

    try:
        visualizer = DataVisualizer(latest_uploaded_file)
        images = {
            'heatmap_counts': 'data:image/png;base64,' + encode_image(visualizer.generate_heatmap_of_counts()),
            'heatmap_description': 'data:image/png;base64,' + encode_image(visualizer.generate_count_vs_description_heatmap()),
            'velocity_chart': 'data:image/png;base64,' + encode_image(visualizer.generate_pitch_velocity_chart())
        }
        return jsonify(images)
    except Exception as e:
        return jsonify({'error': 'Failed to generate images', 'message': str(e)}), 500


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


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Check if the path corresponds to a static file
    static_path = os.path.join(app.static_folder, path)
    if os.path.isfile(static_path):
        return send_from_directory(app.static_folder, path)
    
    # Catch all
    return render_template('index.html')
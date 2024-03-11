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
import unittest


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(__name__)
        CORS(self.app, resources={r'/*': {'origins': '*'}})
        self.client = self.app.test_client()

    def test_mlb_player_stats_route(self):
        response = self.client.get(
            '/api/mlb_player_stats?player_name=Justin 4Verlander')
        self.assertEqual(response.status_code, 404)
        # Further assertions based on your response structure


if __name__ == '__main__':
    unittest.main()

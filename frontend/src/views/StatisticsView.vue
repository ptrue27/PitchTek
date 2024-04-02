<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" class="text-center">
        <div class="display-2 font-weight-bold mb-6">Baseball Statistics</div>
      </v-col>
    </v-row>
    
    <v-row>
      <v-col cols="12" md="6">
        <v-card class="pa-4 mx-auto elevation-6" outlined>
          <v-text-field v-model="pitcherId" label="Pitcher ID" outlined dense solo-inverted solo class="mb-2"></v-text-field>
          <v-btn color="green darken-1" dark @click="updatePitcherStats">Update</v-btn>
          <v-alert v-if="pitcherError" type="error" class="mt-2">{{ pitcherError }}</v-alert>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="pa-4 mx-auto elevation-6" outlined>
          <v-text-field v-model="batterId" label="Batter ID" outlined dense solo-inverted solo class="mb-2"></v-text-field>
          <v-btn color="green darken-1" dark @click="updateBatterStats">Update</v-btn>
          <v-alert v-if="batterError" type="error" class="mt-2">{{ batterError }}</v-alert>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <v-card class="mx-auto" flat>
          <v-img src="@/assets/pitcher.jpg" class="white--text align-end" height="200px" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)">
            <v-card-title>Pitcher Statistics</v-card-title>
          </v-img>
          <v-card-text>
            <v-simple-table fixed-header>
              <template v-slot:default>
                <thead>
                  <tr>
                    <th class="text-left">Stat</th>
                    <th class="text-left">Value</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(value, key) in pitcherStats.stats" :key="key">
                    <td>{{ key }}</td>
                    <td>{{ value }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="mx-auto" flat>
          <v-img src="@/assets/batter.jpg" class="white--text align-end" height="200px" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)">
            <v-card-title>Batter Statistics</v-card-title>
          </v-img>
          <v-card-text>
            <v-simple-table fixed-header>
              <template v-slot:default>
                <thead>
                  <tr>
                    <th class="text-left">Stat</th>
                    <th class="text-left">Value</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(value, key) in batterStats.stats" :key="key">
                    <td>{{ key }}</td>
                    <td>{{ value }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="selectedStat">
      <v-col>
        <v-card class="mx-auto" flat>
          <v-card-title class="headline">{{ selectedStat }}</v-card-title>
          <v-card-text>
            <canvas id="statChart"></canvas>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Chart from 'chart.js/auto';

import axios from 'axios';

export default {
  

  data() {
    
    return {
      pitcherId: '',
      batterId: '',
      pitcherStats: {
        'ERA': 0.0,
        'WHIP': 0,
        'Strikeouts': 0,
        'Walks': 0,
        'Innings Pitched': 0,
        'Wins': 0,
        'Losses': 0,
        'Strikeout-to-Walk Ratio': 0
      },
      batterStats: {
        'Batting Average': 0,
        'On-Base Percentage': 0,
        'Slugging Percentage': 0,
        'Home Runs': 0,
        'Runs Batted In': 0,
        'Hits': 0
      },
      selectedStat: null
    };
  },
  
   methods: {
    updatePitcherStats() {
      if (!this.pitcherId.trim()) {
        this.pitcherError = 'Please enter a Pitcher ID';
        return;
      }

      axios.get(`http://localhost:5000/api/player_pitching_stats`, { params: { player_name: this.pitcherId } })
        .then(response => {
          if (!response.data || Object.keys(response.data).length === 0) {
            this.pitcherError = 'Player does not exist or error';
          } else {
            this.pitcherStats = response.data;
            this.pitcherError = '';
          }
        })
        .catch(() => {
          this.pitcherError = 'Player does not exist or error';
        });
    },
    updateBatterStats() {
    if (!this.batterId.trim()) {
      this.batterError = 'Please enter a Batter ID';
      return;
    }

    axios.get(`http://localhost:5000/api/player_batting_stats`, { params: { player_name: this.batterId } })
      .then(response => {
        if (!response.data || Object.keys(response.data).length === 0) {
          this.batterError = 'Player does not exist';
        } else {
          this.batterStats = response.data;
          this.batterError = '';
        }
      })
      .catch(() => {
        this.batterError = 'Player does not exist or error';
      });
  },
    showGraph(stat) {
      this.selectedStat = stat;

      const data = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
          label: stat,
          data: [0, 10, 5, 2, 20, 30, 45],
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }]
      };

      if (this.chart) {
        this.chart.destroy();
      }

      this.chart = new Chart(
          document.getElementById('statChart'),
          {
            type: 'line',
            data: data,
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          }
      );
    }
  }
};
</script>

<style>
body {
  background-color: #004d40;
  /* Dark green background for the entire page */
}

.title {
  font-size: 2em;
  color: white;
  margin: 20px 0;
  font-weight: bold;
}
.player-id-input {
  max-width: 200px;
  margin-right: 10px;
  background-color: rgba(144, 238, 144, 0.3);
}
.image-container {
  border: 5px solid #96ce8a;
  /* Light green border for images */
  padding: 5px;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.player-image {
  max-width: 300px;
  height: 200px;
  object-fit: cover;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

th,
td {
  border: 1px solid #96ce8a;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #96ce8a;
  color: white;
}

h2 {
  margin-top: 20px;
  color: #2a6041;
}

tbody tr:hover {
  background-color: #c9e7c9;
  cursor: pointer;
}

#statChart {
  background-color: white;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-top: 20px;
}

.upload-button {
  background-color: #2b8c2a;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.upload-button:hover {
  background-color: #1b5e20;
  /* Even darker green on hover */
}
.player-id-input-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 10px; /* Adjust the margin to bring the text box closer to the picture */
}

.player-id-input .v-input__control .v-input__slot {
  border-radius: 25px; /* Rounded edges for the text box */
}

/* Ensure the text box aligns well with other components */
.player-id-input {
  width: 80%; /* Adjust the width as needed to align with other components */
  margin-top: -20px; /* Adjust the margin to move the text box closer to the picture */
  background-color: rgba(144, 238, 144, 0.3); /* Optional: Adjust the background color to enhance appearance */
}

/* Adjust the update button to align with the text box styling */
.update-button {
  margin-top: 10px;
  border-radius: 25px; /* Match the rounded edges of the text box */
}

/* Optional: Add additional styling to enhance the overall look */
.image-container {
  margin-bottom: 1px; /* Reduce the space between the image and the text box */
}

.update-button:hover {
  background-color: #1b5e20;
}

</style>
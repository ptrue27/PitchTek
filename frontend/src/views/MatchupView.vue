<template>
  <v-container fluid class="mb-5">
    <v-row justify="center">
      <v-col cols="12" class="text-center">
        <h2 class="display-1 font-weight-bold mb-3">Player Matchup</h2>
        <v-file-input label="Upload CSV" @change="handleFileUpload" outlined dense solo-inverted solo></v-file-input>
        <v-autocomplete
        v-if="players.length"
        v-model="selectedPlayer"
        :items="players"
        label="Select Player or Description"
        outlined
        dense
        solo-inverted
        solo
        class="mt-3"
      ></v-autocomplete>




        <v-btn color="blue darken-1" dark @click="generateStatsChart" :disabled="!selectedPlayer">Generate Stats</v-btn>
      </v-col>
    </v-row>
    <v-row v-if="chartInstance">
      <v-col>
        <canvas id="playerStatsChart"></canvas>
      </v-col>
    </v-row>
  </v-container>

 <v-container fluid>
  <v-row justify="center">
    <v-col cols="12">
      <v-simple-table dense>
  <template v-slot:default>
    <thead>
      <tr>
        <th class="text-left">Pitch Type</th>
        <th class="text-left">Event</th>
        <th class="text-left">Description</th>
        <th class="text-left">Plate X</th>
        <th class="text-left">Plate Z</th>
        <th class="text-left">Release Speed</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(pitch, index) in pitcherOutings" :key="index">
        <td>{{ pitch.pitchType }}</td>
        <td>{{ pitch.event }}</td>
        <td>{{ pitch.description }}</td>
        <td>{{ pitch.plateX }}</td>
        <td>{{ pitch.plateZ }}</td>
        <td>{{ pitch.releaseSpeed }}</td>
      </tr>
    </tbody>
  </template>
</v-simple-table>


    </v-col>
  </v-row>
</v-container>


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
          
          <v-alert v-if="pitcherError" type="error" class="mt-2">{{ pitcherError }}</v-alert>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="pa-4 mx-auto elevation-6" outlined>
          <v-text-field v-model="batterId" label="Batter ID" outlined dense solo-inverted solo class="mb-2"></v-text-field>
          
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

import Papa from 'papaparse';

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
      selectedStat: null,
      players: [],
      outingSummaries: [],
      chartData: null,
      chartInstance: null,
      nameIndexMap: new Map(), // To keep track of the indices
      selectedPlayer: '',
      pitcherOutings: [],
    };
  },


  
   methods: {
  updatePitcherStats() {
    this.pitcherError = ''; // Reset error message each time the method is called
    if (!this.pitcherId.trim()) {
      this.pitcherError = 'Please enter a Pitcher ID';
      return;
    }

    axios.get(`http://localhost:5000/api/player_pitching_stats`, { params: { player_name: this.pitcherId } })
      .then(response => {
        if (!response.data || Object.keys(response.data).length === 0) {
          this.pitcherError = 'No data found for this Pitcher ID';
        } else {
          this.pitcherStats = response.data;
        }
      })
      .catch(error => {
        this.pitcherError = 'Failed to fetch data: ' + error.message;
      });
  },
  updateBatterStats() {
    this.batterError = ''; // Reset error message each time the method is called
    if (!this.batterId.trim()) {
      this.batterError = 'Please enter a Batter ID';
      return;
    }

    axios.get(`http://localhost:5000/api/player_batting_stats`, { params: { player_name: this.batterId } })
      .then(response => {
        if (!response.data || Object.keys(response.data).length === 0) {
          this.batterError = 'No data found for this Batter ID';
        } else {
          this.batterStats = response.data;
        }
      })
      .catch(error => {
        this.batterError = 'Error fetching batter data: ' + error.message;
      });
  },
  handleFileUpload(event) {
  const file = event.target.files[0];
  const nameIndexMap = new Map(); // To remember the indices of each name

  Papa.parse(file, {
    header: true,
    dynamicTyping: true,
    complete: (results) => {
      this.csvData = results.data;
      const names = []; // For the dropdown list

      results.data.forEach((row, index) => {
        const playerName = row.player_name; // Adjust if your column name is different
        const desWords = row.des ? row.des.split(' ').slice(0, 2).join(' ') : '';

        // Check and add the player name from the 'player_name' column
        if (playerName && !nameIndexMap.has(playerName)) {
          names.push(playerName);
          nameIndexMap.set(playerName, index);
        }

        // Check and add the name from the 'des' column
        if (desWords && !nameIndexMap.has(desWords)) {
          names.push(desWords);
          nameIndexMap.set(desWords, index);
        }
      });

      this.players = names; // Now 'players' is just a list of names (strings)
      this.nameIndexMap = nameIndexMap; // Save the mapping separately
    },
  });
},
analyzePitcherData() {
  if (this.selectedPitcherIndex === null || !this.csvData) return;

  // Filter rows for the selected pitcher
  const pitcherData = this.csvData.filter((row, index) => index === this.selectedPitcherIndex);

  this.pitcherOutings = pitcherData.map(row => ({
    pitchType: row.pitch_type,
    event: row.event,
    description: row.description,
    plateX: row.plate_x,
    plateZ: row.plate_z,
    releaseSpeed: row.release_speed,
  }));
},
analyzeOutings() {
    if (!this.selectedPlayer || !this.csvData) return;

    // Filter rows for the selected player
    const playerRows = this.csvData.filter(row => row.player_name === this.selectedPlayer);

    // Initialize variables for outing analysis
    let outings = [];
    let currentOuting = [];
    let lastIndex = -1;

    // Group rows into outings
    playerRows.forEach((row, index) => {
      if (index - lastIndex > 1 && currentOuting.length > 0) {
        outings.push([...currentOuting]); // End of an outing
        currentOuting = [];
      }
      currentOuting.push(row); // Add row to current outing
      lastIndex = index;
    });
    if (currentOuting.length > 0) outings.push([...currentOuting]); // Add the last outing

    // Process each outing to summarize data
    this.outingSummaries = outings.map(outing => {
      const summary = {
        totalPitches: outing.length,
        pitches: outing.map(o => o.pitch_type), // Assuming 'pitch_type' is the column name
        speeds: outing.map(o => o.speed), // Assuming 'speed' is the column name
        plateZ: outing.map(o => o.plate_z), // Assuming 'plate_z' is the column name
        plateX: outing.map(o => o.plate_x), // Assuming 'plate_x' is the column name
      };
      return summary;
    });
  },
  generateStats() {
    if (!this.selectedPlayer || !this.csvData) return;

    // Filter rows for the selected player
    const playerRows = this.csvData.filter(row => row.player_name === this.selectedPlayer);

    // Group rows into outings and calculate stats for each outing
    let outings = [];
    let currentOuting = [];

    playerRows.forEach((row, index) => {
      if (index > 0 && row.player_name !== this.selectedPlayer) {
        outings.push(currentOuting);
        currentOuting = [];
      }
      currentOuting.push(row);
    });

    if (currentOuting.length) outings.push(currentOuting); // Add the last outing

    this.outingSummaries = outings.map(outing => ({
      totalPitches: outing.length,
      pitches: outing.map(o => o.pitch_type).join(', '),
      speeds: outing.map(o => o.pitch_speed).join(', '),
      plateZ: outing.map(o => o.plate_z).join(', '),
      plateX: outing.map(o => o.plate_x).join(', '),
    }));
  },


    generateStatsChart() {
      const selected = this.players.find(p => p.id === this.selectedPlayer);
      if (!selected) return;

      // Example chart generation logic, adjust as necessary
      const data = {
        labels: ['Stat 1', 'Stat 2', 'Stat 3'], // Placeholder labels
        datasets: [{
          label: selected.name,
          data: [10, 20, 30], // Placeholder data
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }]
      };

      if (this.chartInstance) {
        this.chartInstance.destroy();
      }

      this.chartInstance = new Chart(
        document.getElementById('playerStatsChart'),
        {
          type: 'bar', // Adjust chart type as needed
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
    },
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
    },
watch: {
  pitcherId(newVal, oldVal) {
    if (newVal.trim() !== oldVal.trim()) {
      this.updatePitcherStats();
    }
  },
  batterId(newVal, oldVal) {
    if (newVal.trim() !== oldVal.trim()) {
      this.updateBatterStats();
    }
  },
  selectedPlayer(newVal, oldVal) {
    if (newVal !== oldVal) {
      this.analyzeOutings();
    }
  },
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
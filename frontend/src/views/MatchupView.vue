  <template>
  <v-container fluid class="mb-5">
    <v-row justify="center">
      <v-col cols="12" class="text-center">
        <h2 class="display-1 font-weight-bold mb-3">Player Matchup</h2>
        <v-file-input 
          label="Upload CSV" 
          @change="handleFileUpload" 
          outlined 
          dense 
          solo-inverted 
          solo
        ></v-file-input>
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
        <v-btn color="primary" @click="fetchLatestAtBatPlot">Show Latest At-Bat Plot</v-btn>
        
        <v-col cols="12" sm="8" md="6">
        <v-img v-if="showImage"
              src="@/assets/static/latest_at_bat.png"
              alt="Latest At-Bat Plot">
        </v-img>
      </v-col>
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
            <v-img src="@/assets/silhouette.png" class="white--text align-end" height="200px" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)">
              <v-card-title>Pitcher Statistics</v-card-title>
            </v-img>
            <v-card-text>
              <v-simple-table fixed-header>
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th class="statistic-cell">Statistic</th>
                      <th class="value-cell">Value</th>
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
            <v-img src="@/assets/silhouette.png" class="white--text align-end" height="200px" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)">
              <v-card-title>Batter Statistics</v-card-title>
            </v-img>
            <v-card-text>
              <v-simple-table fixed-header>
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th class="statistic-cell">Statistic</th>
        <th class="value-cell">Value</th>
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
      showImage: false,
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
      generatedImageUrl: '@/PitchTek/frontend/src/assets/static/latest_at_bat.png',
      nameIndexMap: new Map(),
      selectedImageUrl: '@/PitchTek/frontend/src/assets/strikezone.jpg',
      pitcherOutings: [],
      placeholderImageUrl: '@/PitchTek/frontend/src/assets/strikezone.jpg',
      images: [
      '@/PitchTek/frontend/src/assets/default_heat_map.jpg',
      '@/PitchTek/frontend/src/assets/default_heat_map.jpg',
    ],
      selectedPlayer: null,
      playerIndices: [], // This will store the indices to display
      playerDescriptions: [],
    };
    },


    
    methods: {


      analyzeDescriptions() {
    if (!this.selectedPlayer || !this.csvData) return;

    // Filter rows for the selected player and collect descriptions
    const filteredDescriptions = this.csvData.filter(row => row.player_name === this.selectedPlayer)
                                             .map(row => ({ description: row.des }));

    // Store the descriptions in a data property
    this.playerDescriptions = filteredDescriptions;

  },
    updatePitcherStats() {
      this.pitcherError = ''; // Reset error message each time the method is called
      if (!this.pitcherId.trim()) {
        this.pitcherError = 'Please enter a Pitcher ID';
        return;
      }

      const host = "http://" + this.$store.state.host + "/api/player_pitching_stats";
      axios.get(host, { params: { player_name: this.pitcherId } })
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

    const host = "http://" + this.$store.state.host + "/api/player_batting_stats";
    axios.get(host, { params: { player_name: this.batterId } })

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
      let formData = new FormData();
      formData.append('file', file);

      const host = "http://" + this.$store.state.host + "/api/upload_csv";
      axios.post(host, formData)
        .then(response => {
          this.players = response.data;
        })
        .catch(error => console.error('Failed to upload file:', error));
    },
    fetchLatestAtBatPlot() {
      const timestamp = new Date().getTime();
      const host = "http://" + this.$store.state.host + "/api/fetch_latest_at_bat_plot";
      axios.get(host, { params: { player_name: this.selectedPlayer } })
        .then(response => {
          this.generatedImageUrl = `${response.data.image_url}?t=${timestamp}`;
          this.showImage = true;
        })
        .catch(error => {
          console.error("Error fetching latest at-bat plot:", error);
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
    updateChart(data) {
      const ctx = document.getElementById('playerStatsChart').getContext('2d');
      if (this.chartInstance) {
        this.chartInstance.destroy();
      }
      this.chartInstance = new Chart(ctx, {
        type: 'scatter',
        data: {
          datasets: [{
            label: data.description,
            data: [{ x: data.plate_x, y: data.plate_z }],
            backgroundColor: 'rgb(75, 192, 192)'
          }]
        },
        options: {
          scales: {
            x: {
              type: 'linear',
              position: 'bottom'
            }
          }
        }
      });
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
    selectedPlayer(newVal) {
      if (newVal && this.nameIndexMap.has(newVal)) {
        const playerData = this.nameIndexMap.get(newVal);
        this.selectedImageUrl = playerData.imageUrl || this.placeholderImageUrl;
      } else {
        this.selectedImageUrl = this.placeholderImageUrl; // Clear if no valid selection or before any selection
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
    border: 1px solid #135304;
    padding: 8px;
    text-align: left;
  }

  th {
    background-color: #145d03;
    color: white;
  }

  h2 {
    margin-top: 20px;
    color: #2a6041;
  }

  tbody tr:hover {
    background-color: #21cb21;
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

  .statistic-cell {
  font-weight: bold;
  color: #333; /* Dark color for statistic names */
}

.value-cell {
  background-color: #eee; /* Light grey background for values */
  color: #666; /* Dark grey color for text */
}

  /* Optional: Add additional styling to enhance the overall look */
  .image-container {
    margin-bottom: 1px; /* Reduce the space between the image and the text box */
  }

  .update-button:hover {
    background-color: #1b5e20;
  }

  </style>
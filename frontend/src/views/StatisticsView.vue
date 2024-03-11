<template>
    <v-row>
    <v-col class="text-center">
      <div class="title">Baseball Statistics</div>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="6">
      <div class="player-id-input-container">
        <v-text-field v-model="pitcherId" label="Pitcher ID" outlined dense class="player-id-input"></v-text-field>
        <v-btn @click="updatePitcherStats" class="update-button">Update</v-btn>
        <v-alert v-if="pitcherError" type="error" class="error-alert">{{ pitcherError }}</v-alert>
      </div>
    </v-col>
    <v-col cols="6">
      <div class="player-id-input-container">
        <v-text-field v-model="batterId" label="Batter ID" outlined dense class="player-id-input"></v-text-field>
        <v-btn @click="updateBatterStats" class="update-button">Update</v-btn>
        <v-alert v-if="batterError" type="error" class="error-alert">{{ batterError }}</v-alert>
      </div>
    </v-col>
  </v-row>
    <v-row>
        <v-col class="text-center">
            <div class="title">Baseball Statistics</div>
        </v-col>
    </v-row>
    <v-row>
        <v-col>
            <UploadButton class="upload-button" />
        </v-col>
    </v-row>
  <v-row>
    <v-col cols="6">
      <div class="image-container">
        <v-img src="@/assets/pitcher.jpg" alt="Pitcher" class="player-image"></v-img>
      </div>
      <h2>Pitcher Statistics</h2>
      <table>
        <thead>
        <tr>
          <th>Statistic</th>
          <th>Value</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(value, stat) in pitcherStats" :key="stat" @click="showGraph(stat)">
          <td>{{ stat }}</td>
          <td>{{ value }}</td>
        </tr>
        </tbody>
      </table>
    </v-col>
    <v-col cols="6">
      <div class="image-container">
        <v-img src="@/assets/batter.jpg" alt="Batter" class="player-image"></v-img>
      </div>
      <h2>Batter Statistics</h2>
      <table>
        <thead>
        <tr>
          <th>Statistic</th>
          <th>Value</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(value, stat) in batterStats" :key="stat" @click="showGraph(stat)">
          <td>{{ stat }}</td>
          <td>{{ value }}</td>
        </tr>
        </tbody>
      </table>
    </v-col>
  </v-row>
  <v-row v-if="selectedStat">
    <v-col>
      <div v-if="selectedStat">Graph for {{ selectedStat }}</div>
      <canvas id="statChart"></canvas>
    </v-col>
  </v-row>
</template>

<script>
import Chart from 'chart.js/auto';
import UploadButton from "@/components/UploadButton.vue";
import axios from 'axios';

export default {
  components: {
    UploadButton
  },
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

      axios.get(`http://localhost:5000/api/mlb_player_stats`, { params: { player_name: this.pitcherId } })
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

      axios.get(`http://localhost:5000/api/mlb_player_stats`, { params: { player_name: this.batterId } })
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
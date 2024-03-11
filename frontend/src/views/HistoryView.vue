<template>
  <div class="player-stats-container">
    <v-row>
      <v-col class="text-center">
        <div class="title">Player Statistics</div>
      </v-col>
    </v-row>

    <v-row align="center" justify="center">
      <v-col cols="8">
        <v-text-field v-model="playerName" label="Enter Player Name" outlined dense></v-text-field>
      </v-col>
      <v-col cols="4">
        <v-btn color="primary" @click="fetchPlayerStats">Fetch Stats</v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <table>
          <thead>
            <tr>
              <th>Statistic</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(value, stat) in playerStats" :key="stat">
              <td>{{ stat }}</td>
              <td>{{ value }}</td>
            </tr>
          </tbody>
        </table>
      </v-col>
    </v-row>

    <!-- HTML Graphs Section -->
    <v-row v-if="showGraphs">
      <v-col class="text-center">
        <div id="playerGraphs" ref="playerGraphs">Graphs will be loaded here...</div>
      </v-col>
    </v-row>
    <div class="player-stats-container"></div>
    <div ref="graphContainer"></div>

  </div>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      playerName: '',
      playerStats: {},
      showGraphs: false,
    };
  },
  mounted() {
     this.loadGraph();
  },
  methods: {
    
    fetchPlayerStats() {
      if (!this.playerName.trim()) {
        alert('Please enter a player name');
        return;
      }
 
      axios.get(`http://localhost:5000/api/mlb_player_stats`, { params: { player_name: this.playerName } })
        .then(response => {
          this.playerStats = response.data.stats;
          this.showGraphs = true;
          // After fetching the stats, load the corresponding Plotly graph
          this.loadGraph();
        })
        .catch(error => {
          console.error('Error fetching player stats:', error);
          alert('Failed to fetch player stats');
          this.showGraphs = false;
        });
    },
    loadGraph() {
  axios.get(`http://localhost:5000/show-history`)
    .then(response => {
      // Update imageUrls with the response data
      this.imageUrls = response.data.imageUrls;
      this.showImages = true; // Assuming you have a showImages data property to control the visibility of the image section
    })
    .catch(error => {
      console.error('Error loading images:', error);
      this.showImages = false;
    });
},

    
  }
};
</script>

<style scoped>
.player-stats-container {
  max-width: 800px;
  margin: auto;
}

.title {
  font-size: 2em;
  color: #004d40;
  margin: 20px 0;
  font-weight: bold;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
.plotly-graph-container {
  width: 100%; /* Adjust the width as needed */
  height: 500px; /* Adjust the height as needed */
  /* Additional styling as needed */
}

th, td {
  border: 1px solid #96ce8a;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #96ce8a;
  color: white;
}

/* Additional styles as needed */
</style>

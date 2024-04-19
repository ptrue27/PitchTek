<template>
  <v-container class="player-stats-container" fluid>
    <!-- Title Section -->
    <v-row>
      <v-col class="text-center">
        <h1 class="display-1">Player Statistics</h1>
      </v-col>
    </v-row>

    <!-- Upload and Generate Images Section -->
    <v-row align="center" justify="center" class="my-5">
      <v-col cols="12" md="8">
        <v-card class="pa-5" outlined tile>
          <v-card-title class="justify-center">
            <v-icon large color="success">mdi-cloud-upload</v-icon>
            <span class="headline ml-3">Upload Pitcher Data</span>
          </v-card-title>
          <v-card-text class="text-center mb-4">
            Select a file containing player statistics to upload and analyze.
          </v-card-text>
          <v-card-actions class="justify-center">
            <input type="file" @change="file => uploadFile(file.target.files[0])" />
            <v-btn color="success" @click="generateImages">Generate Images</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Images Display Section -->
    <v-row justify="center" class="my-5">
    <v-col v-for="image in images" :key="image" cols="12" sm="6" md="4">
      <v-img :src="image" :alt="'Generated Image ' + image" class="my-2" contain></v-img>
    </v-col>
  </v-row>

    <!-- Player Name Input and Fetch Stats Button -->
    <v-row align="center" justify="center">
      <v-col cols="12" md="8">
        <v-text-field v-model="playerName" label="Enter Player Name" outlined dense solo color="success"></v-text-field>
      </v-col>
      <v-col cols="12" md="4">
        <v-btn color="success" dark large @click="fetchPlayerStats" block>Fetch Stats</v-btn>
      </v-col>
    </v-row>

    <!-- Fielding Stats Table -->
    <v-card class="mt-5">
      <v-card-title class="green lighten-2 white--text">Fielding Stats</v-card-title>
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">Statistic</th>
              <th class="text-left">Value</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(value, stat) in fieldingStats" :key="`fielding-${stat}`">
              <td>{{ stat }}</td>
              <td>{{ value }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card>

    <!-- Pitching Stats Table -->
    <v-card class="mt-5">
      <v-card-title class="green lighten-2 white--text">Pitching Stats</v-card-title>
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">Statistic</th>
              <th class="text-left">Value</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(value, stat) in pitchingStats" :key="`pitching-${stat}`">
              <td>{{ stat }}</td>
              <td>{{ value }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card>

    <!-- Batting Stats Table -->
    <v-card class="mt-5">
      <v-card-title class="green lighten-2 white--text">Batting Stats</v-card-title>
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">Statistic</th>
              <th class="text-left">Value</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(value, stat) in battingStats" :key="`batting-${stat}`">
              <td>{{ stat }}</td>
              <td>{{ value }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  components: {
     
  },

  data() {
    return {
      playerName: '',
      fieldingStats: {},
      pitchingStats: {},
      battingStats: {},
      images : ["C:/Users/davis/PitchTek-2/frontend/public/images/count_vs_description_heatmap.png", "C:/Users/davis/PitchTek-2/frontend/public/images/heatMapOFCounts.png" , "C:/Users/davis/PitchTek-2/frontend/public/images/pitchVeloLastGame.png"]
    };
  },
  methods: {
    uploadFile(file) {
      const formData = new FormData();
      formData.append('file', file);

      axios.post('http://' + this.$store.state.host + '/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        console.log(response.data.message);
        // Additional actions based on successful upload, if needed
      })
      .catch(error => {
        console.error('Error during file upload:', error);
      });
    },
    generateImages() {
  axios.post('http://' + this.$store.state.host + '/api/generate-images')
    .then(response => {
      
      this.images = response.data.images;
    })
    .catch(error => {
      console.error('Error generating images:', error);
    });
},
    fetchPlayerStats() {
      if (!this.playerName.trim()) {
        alert('Please enter a player name');
        return;
      }

      this.fetchFieldingStats();
      this.fetchPitchingStats();
      this.fetchBattingStats();
    },
    fetchFieldingStats() {
      axios.get('http://' + this.$store.state.host + '/api/player_fielding_stats', { params: { player_name: this.playerName } })
        .then(response => {
          this.fieldingStats = response.data.stats || {};
        })
        .catch(error => {
          console.error('Error fetching fielding stats:', error);
          this.fieldingStats = { 'Data': 'Not Available' };
        });
    },
    fetchPitchingStats() {
      axios.get('http://' + this.$store.state.host + '/api/player_pitching_stats', { params: { player_name: this.playerName } })
        .then(response => {
          this.pitchingStats = response.data.stats || {};
        })
        .catch(error => {
          console.error('Error fetching pitching stats:', error);
          this.pitchingStats = { 'Data': 'Not Available' };
        });
    },
    fetchBattingStats() {
      axios.get('http://' + this.$store.state.host + '/api/player_batting_stats', { params: { player_name: this.playerName } })
        .then(response => {
          this.battingStats = response.data.stats || {};
        })
        .catch(error => {
          console.error('Error fetching batting stats:', error);
          this.battingStats = { 'Data': 'Not Available' };
        });
    },
   
  },
};
</script>

<style scoped>
.player-stats-container {
  max-width: 1200px;
  margin: auto;
  padding: 20px;
  background: rgba(240, 255, 244, 0.3); /* Subtle green background */
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.v-simple-table thead th {
  font-weight: bold;
  font-size: 1.1em;
}

.v-simple-table tbody tr:nth-child(odd) {
  background-color: rgba(144, 238, 144, 0.3); /* Light green for odd rows */
}

.v-simple-table tbody tr:hover {
  background-color: rgba(144, 238, 144, 0.5); /* Darker green on hover */
}

.v-btn {
  margin-top: 10px; /* Ensure button alignment */
}
</style>

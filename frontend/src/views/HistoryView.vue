<template>
  <div class="player-stats-container">
    <!-- Player Statistics Section -->
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

    <!-- Images Section -->
    <v-row>
      <v-col cols="12">
        <v-row>
          <!-- Dynamically create a column for each image -->
          <v-col cols="12" md="4" v-for="(imageUrl, index) in imageUrls" :key="index" class="mb-4">
            <div class="text-center">
              <div class="image-title">Stat {{ index + 1 }} </div>
              <img :src="imageUrl" class="player-image" :alt="'Image ' + index">
            </div>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios';
// Import images (consider moving them to the src/assets directory)
import image1 from 'C:/Users/davis/PitchTek-2/uploads/uploads_pitch_type_distribution.png';
import image2 from 'C:/Users/davis/PitchTek-2/uploads/uploads_pitch_type_distribution.png';
import image3 from 'C:/Users/davis/PitchTek-2/uploads/uploads_pitch_type_distribution.png';

export default {
  data() {
    return {
      playerName: '',
      playerStats: {},
      imageUrls: [image1, image2, image3],
    };
  },
  methods: {
    fetchPlayerStats() {
      if (!this.playerName.trim()) {
        alert('Please enter a player name');
        return;
      }

      // Replace the URL with your actual API endpoint
      axios.get(`http://localhost:5000/api/mlb_player_stats`, { params: { player_name: this.playerName } })
        .then(response => {
          this.playerStats = response.data.stats;
        })
        .catch(error => {
          console.error('Error fetching player stats:', error);
          alert('Failed to fetch player stats');
        });
    },
  },
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

th, td {
  border: 1px solid #96ce8a;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #96ce8a;
  color: white;
}

.player-image {
  max-width: 100%;
  margin-top: 20px;
  height: auto; /* Maintain aspect ratio */
}

.image-title {
  margin-bottom: 10px; /* Adjust space between title and image */
  font-size: 1.2em; /* Adjust title size */
  color: #333; /* Adjust title color */
}
</style>

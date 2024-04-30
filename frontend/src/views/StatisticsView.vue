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
            <input type="file" @change="uploadFile($event.target.files[0])" />

            <v-btn color="success" @click="generateImages">Generate Images</v-btn>
           
            <v-btn color="primary" @click="downloadTemplate">Download Template</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Images Display Section -->
    <v-row justify="center" class="my-5">
  <template v-if="Showimages">
    <v-col v-for="(image, index) in images" :key="index" cols="12" sm="6" md="4">
      <v-img :src="image" :alt="'Generated Image ' + index" class="my-2" contain></v-img>
    </v-col>
  </template>
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
        <th class="statistic-cell">Statistic</th>
        <th class="value-cell">Value</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(value, stat) in fieldingStats" :key="`fielding-${stat}`">
        <!-- Use v-bind:style to dynamically change styles -->
        <td class="statistic-cell">{{ stat }}</td>
        <td class="value-cell">{{ value }}</td>
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
              <th class="statistic-cell">Statistic</th>
        <th class="value-cell">Value</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(value, stat) in pitchingStats" :key="`pitching-${stat}`">
              <td class="statistic-cell">{{ stat }}</td>
              <td class="value-cell">{{ value }}</td>
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
              <th class="statistic-cell">Statistic</th>
        <th class="value-cell">Value</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(value, stat) in battingStats" :key="`batting-${stat}`">
              <td class="statistic-cell">{{ stat }}</td>
              <td class="value-cell">{{ value }}</td>
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
  data() {
    return {
      playerName: '',
      fieldingStats: {},
      pitchingStats: {},
      battingStats: {},
      Showimages: false,
      images: [
        '/images/count_vs_description_heatmap.png',
        '/images/heatMapOFCounts.png',
        '/images/pitchVeloLastGame.png'
      ]
    };
  },
  methods: {
    uploadFile(file) {
    // Create a new FileReader object
    const reader = new FileReader();

    // Define what happens when the file has been read
    reader.onload = (e) => {
        const content = e.target.result;
        // Split the content by newline to process each row
        const rows = content.split('\n').filter(line => line.trim() !== '');
        // Check the headers and remove any quotes
        const headers = rows[0].split(',').map(header => header.trim().replace(/['"]/g, ''));

        // Define required column names
        const requiredColumns = ['pitch_type', 'game_date', 'release_speed','plate_x','plate_z','events']; // Add your specific column names here
        // Determine which required columns are missing
        const missingColumns = requiredColumns.filter(col => !headers.includes(col));

        // Check if all required columns are present
        if (missingColumns.length > 0) {
            alert('Warning: The uploaded file is missing the following required column(s): ' + missingColumns.join(', '));
            return; // Stop further processing if the required columns are not found
        }

        // Check the row count (considering the first row as header)
        if (rows.length - 1 < 150) {
            alert('Warning: The uploaded file contains less than 150 rows. This might affect the analysis accuracy.');
        }

        
          // Proceed to upload the file to the server
          const formData = new FormData();
          formData.append('file', file);
          const host = "http://" + this.$store.state.host + "/api/upload";
          axios.post(host, formData, {
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
        
    };

    // Read the file as a text
    reader.readAsText(file);
},

  downloadTemplate() {
        window.location.href = "http://" + this.$store.state.host + "/api/download-template";
    },
    generateImages() {
  const host = `http://${this.$store.state.host}/api/generate-images`;
  axios.post(host)
    .then(response => {
      this.Showimages = true; // Make sure this only happens if successful
      this.images = [
        response.data.heatmap_counts,
        response.data.heatmap_description,
        response.data.velocity_chart
      ];
      console.log('Images generated:', this.images);
    })
    .catch(error => {
      console.error('Error generating images:', error);
      alert('Failed to generate images.'); // Provide feedback to the user
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
      const host = "http://" + this.$store.state.host + "/api/player_fielding_stats";
      axios.get(host, { params: { player_name: this.playerName } })

        .then(response => {
          this.fieldingStats = response.data.stats || {};
        })
        .catch(error => {
          console.error('Error fetching fielding stats:', error);
          this.fieldingStats = { 'Data': 'Not Available' };
        });
    },
    fetchPitchingStats() {
      const host = "http://" + this.$store.state.host + "/api/player_pitching_stats";
      axios.get(host, { params: { player_name: this.playerName } })

        .then(response => {
          this.pitchingStats = response.data.stats || {};
        })
        .catch(error => {
          console.error('Error fetching pitching stats:', error);
          this.pitchingStats = { 'Data': 'Not Available' };
        });
    },
    fetchBattingStats() {
      const host = "http://" + this.$store.state.host + "/api/player_batting_stats";
      axios.get(host, { params: { player_name: this.playerName } })

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

.statistic-cell {
  font-weight: bold;
  color: #f1f1f1; /* Dark color for statistic names */
  background-color: #004409; /* Light grey background for values */
}

.value-cell {
  background-color: #eee; /* Light grey background for values */
  color: #0c0505; /* Dark grey color for text */
}
.player-stats-container {
  max-width: 1200px;
  margin: auto;
  padding: 20px;
  background: rgba(240, 255, 244, 0.103); /* Subtle green background */
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.v-simple-table thead th {
  font-weight: bold;
  font-size: 1.1em;
}

.v-simple-table tbody tr:nth-child(odd) {
  background-color: rgba(24, 253, 24, 0.3); /* Light green for odd rows */
}

.v-simple-table tbody tr:hover {
  background-color: rgba(144, 238, 144, 0.5); /* Darker green on hover */
}

.v-btn {
  margin-top: 10px; /* Ensure button alignment */
}
</style>

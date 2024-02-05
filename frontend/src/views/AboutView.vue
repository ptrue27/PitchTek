<template>
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

export default {
  components: {
    UploadButton
  },
  data() {
    return {
      pitcherStats: {
        'ERA': 3.60,
        'WHIP': 1.15,
        'Strikeouts': 150,
        'Walks': 50,
        'Innings Pitched': 200,
        'Wins': 18,
        'Losses': 6,
        'Strikeout-to-Walk Ratio': 3.0
      },
      batterStats: {
        'Batting Average': '.320',
        'On-Base Percentage': '.380',
        'Slugging Percentage': '.550',
        'Home Runs': 30,
        'Runs Batted In': 100,
        'Hits': 180
      },
      selectedStat: null
    };
  },
  methods: {
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
}</style>
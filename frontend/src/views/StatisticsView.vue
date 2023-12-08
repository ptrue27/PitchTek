<template>
    <v-row>
        <v-col class="text-center">
            <div>Baseball Statistics</div>
        </v-col>
    </v-row>
    <v-row>
        <v-col>
            <UploadButton />
        </v-col>
        <v-col>
            <FlaskPing />
        </v-col>
    </v-row>
    <v-row>
        <v-col>
            <v-img img src="@/assets/pitcher.jpg" alt="Pitcher" class="player-image">
            </v-img>
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
    </v-row>
    <v-row>
        <v-col>
            <v-img img src="@/assets/batter.jpg" alt="Batter" class="player-image">
            </v-img>
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
            <!-- Placeholder for graph. Implement based on your chart library -->
            <div v-if="selectedStat">Graph for {{ selectedStat }}</div>
        </v-col>
    </v-row>
    <v-row v-if="selectedStat">
        <v-col>
            <canvas id="statChart"></canvas>
        </v-col>
    </v-row>
</template>

<script>
import Chart from 'chart.js/auto';
import UploadButton from "@/components/UploadButton.vue";
import FlaskPing from "@/components/FlaskPing.vue";

export default {
    components: {
        UploadButton,
        FlaskPing
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

            // Dummy data for the graph
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

            // Destroy the old chart if it exists
            if (this.chart) {
                this.chart.destroy();
            }

            // Create a new chart
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
.player-image {
    width: 100%;
    max-width: 300px;
    height: auto;
    margin-bottom: 20px;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th,
td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

th {
    background-color: #f4f4f4;
}

h2 {
    margin-top: 20px;
}

tbody tr {
    cursor: pointer;
}
</style>

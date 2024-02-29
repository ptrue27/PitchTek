<template>
    <div class="app-container">
        <header class="header">
            <h1>{{ pitcher.name }} - Performance Overview</h1>
        </header>

        <div class="player-image-container">
            <img :src="pitcher.image" alt="Pitcher Image" class="player-image" />
        </div>

        <section class="stats-section">
            <h2>Last 20 Games Performance</h2>
            <div class="stats-table">
                <table>
                    <thead>
                        <tr>
                            <th>Game</th>
                            <th>ERA</th>
                            <th>Strikeouts</th>
                            <th>Wins</th>
                            <th>Innings</th>
                            <th>Saves</th>
                            <th>K-Rate</th>
                            <th>Walks</th>
                            <th>Hits</th>
                            <th>HRs</th>
                            <th>ERs</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(performance, index) in filteredPerformance" :key="index">
                            <td>{{ index + 1 }}</td>
                            <td>{{ performance.era }}</td>
                            <td>{{ performance.strikeouts }}</td>
                            <td>{{ performance.wins }}</td>
                            <td>{{ performance.inningsPitched }}</td>
                            <td>{{ performance.saves }}</td>
                            <td>{{ performance.strikeoutRate }}</td>
                            <td>{{ performance.walks }}</td>
                            <td>{{ performance.hitsAllowed }}</td>
                            <td>{{ performance.homeRunsAllowed }}</td>
                            <td>{{ performance.earnedRuns }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <section class="charts-section">
            <div v-for="(data, stat, index) in chartData" :key="stat" class="chart-container">
                <h3>{{ stat.toUpperCase() }} Chart</h3>
                <div class="chart">
                    <canvas :ref="`chart-${index}`"></canvas>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
    data() {
        return {
            pitcher: {
                name: 'John Doe',
                image: 'pitcher.jpg',
                performance: [
                    // Dummy data for 20 games
                    ...Array.from({ length: 20 }, (_, i) => ({
                        game: i + 1,
                        era: Math.random() * 10,
                        strikeouts: Math.floor(Math.random() * 10),
                        wins: Math.floor(Math.random() * 5),
                        inningsPitched: Math.random() * 10,
                        saves: Math.floor(Math.random() * 5),
                        strikeoutRate: Math.random() * 100,
                        walks: Math.floor(Math.random() * 5),
                        hitsAllowed: Math.floor(Math.random() * 10),
                        homeRunsAllowed: Math.floor(Math.random() * 5),
                        earnedRuns: Math.floor(Math.random() * 10),
                    })),
                ],
            },
        };
    },
    computed: {
        filteredPerformance() {
            return this.pitcher.performance.slice(-20);
        },
        chartData() {
            const stats = ['era', 'strikeouts', 'wins', 'inningsPitched', 'saves', 'strikeoutRate', 'walks', 'hitsAllowed', 'homeRunsAllowed', 'earnedRuns'];
            let chartDataSets = {};

            stats.forEach(stat => {
                chartDataSets[stat] = {
                    labels: this.filteredPerformance.map((_, index) => `Game ${index + 1}`),
                    datasets: [{
                        label: stat.toUpperCase(),
                        data: this.filteredPerformance.map(performance => performance[stat]),
                        borderColor: this.getRandomColor(),
                        backgroundColor: 'rgba(0, 0, 0, 0)',
                    }]
                };
            });

            return chartDataSets;
        },
    },
    methods: {
        createChart(ref, data) {
            const ctx = this.$refs[ref].getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: data,
            });
        },
        getRandomColor() {
            const letters = '0123456789ABCDEF';
            let color = '#';
            for (let i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        },
    },
    mounted() {
        this.$nextTick(() => {
            Object.keys(this.chartData).forEach((stat, index) => {
                this.createChart(`chart-${index}`, this.chartData[stat]);
            });
        });
    },
};
</script>

<style scoped>
.app-container {
    background-color: #eef2f5;
    padding: 20px;
    font-family: 'Arial', sans-serif;
}

.header {
    text-align: center;
    margin-bottom: 30px;
}

.header h1 {
    color: #333;
    font-size: 2.5em;
}

.player-image-container {
    text-align: center;
    margin-bottom: 30px;
}

.player-image {
    max-width: 300px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.stats-section,
.charts-section {
    margin-bottom: 40px;
}

.stats-section h2,
.charts-section h3 {
    color: #333;
    margin-bottom: 15px;
    text-align: center;
}

.stats-table table {
    width: 100%;
    border-collapse: collapse;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.stats-table th,
.stats-table td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

.stats-table th {
    background-color: #4CAF50;
    color: white;
}

.stats-table tr:nth-child(even) {
    background-color: #f2f2f2;
}

.chart-container {
    margin-bottom: 30px;
}

.chart-container h3 {
    text-align: center;
    margin-bottom: 10px;
}

.chart {
    padding: 10px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}</style>

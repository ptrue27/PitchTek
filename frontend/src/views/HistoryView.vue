<template>
    <div class="app-container">
        <div class="pitcher-info-container">
            <div class="pitcher-info">
                <h1>{{ pitcher.name }}</h1>
                <img :src="pitcher.image" alt="Pitcher Image" />
            </div>
        </div>

        <div class="performance-table-container">
            <div class="performance-table-inner">
                <h2>Last 20 Games Performance</h2>
                <table class="performance-table">
                    <thead>
                        <tr>
                            <th>Game</th>
                            <th>ERA</th>
                            <th>Strikeouts</th>
                            <th>Wins</th>
                            <th>Innings Pitched</th>
                            <th>Saves</th>
                            <th>Strikeout Rate</th>
                            <th>Walks</th>
                            <th>Hits Allowed</th>
                            <th>Home Runs Allowed</th>
                            <th>Earned Runs</th>
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
        </div>

        <div v-for="(data, stat) in chartData" :key="stat" class="performance-chart-container">
            <div class="performance-chart-inner">
                <h2>{{ stat.toUpperCase() }} Performance Chart</h2>
                <div class="chart-wrapper">
                    <canvas :ref="`chart-${stat}`"></canvas>
                </div>
            </div>
        </div>
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
        createChart(stat, data) {
            const ctx = this.$refs[`chart-${stat}`].getContext('2d');
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
        Object.keys(this.chartData).forEach(stat => {
            this.createChart(stat, this.chartData[stat]);
        });
    },
};
</script>

<style scoped>
.app-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #f5f5f5;
    padding: 20px;
}

.pitcher-info-container,
.performance-table-container,
.performance-chart-container {
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
}

.pitcher-info {
    text-align: center;
    margin-bottom: 20px;
}

.performance-table-inner {
    text-align: center;
    margin-bottom: 20px;
}

.performance-chart-inner {
    text-align: center;
}

.performance-table {
    width: 100%;
    border-collapse: collapse;
}

th,
td {
    padding: 8px;
    border: 1px solid #ccc;
}

.chart-wrapper {
    max-width: 100%;
    height: auto;
}
</style>

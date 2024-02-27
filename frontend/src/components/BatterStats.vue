<template>
    <v-card style="width: 100%; margin: 10px 10px;">
        <!--Player select-->
        <v-row>
            <v-col>
                <v-select
                    :items="batterNames" 
                    v-model="batter.name"
                    @update:modelValue="handleBatterChange"
                    density="compact" 
                ></v-select>
            </v-col>
        </v-row>
        <v-row style="margin-top: -30px;">
            <!--Player image-->
            <v-col cols="3">
                <v-img
                    :src="batter.img"
                ></v-img>
            </v-col>

            <!--Player stats-->
            <v-col cols="9" class="pr-2">
                <div>
                    <table class="stats-table">
                        <thead>
                            <tr>
                            <th>HR</th>
                            <th>OB%</th>
                            <th>SLG%</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                            <td>{{ batter.hr }}</td>
                            <td>{{ batter.obp }}</td>
                            <td>{{ batter.slg }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </v-col>
        </v-row>
    </v-card>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';

export default {
    methods: {
        handleBatterChange() {
            const index = this.batterNames.indexOf(this.batter.name);
            const batterId = this.batterIds[index];
            const path = 'http://localhost:5000/get_batter/' + batterId;

            axios.get(path)
                .then((res) => {
                    const newBatter = res.data;
                    console.log("Changed Batter: " + newBatter);
                    this.$store.commit("setCurrentBatter", newBatter);
                })
                .catch((error) => {
                    console.error("Error changing batter: " + error);
                    this.$store.commit("setCurrentBatter", this.$store.state.default.batter);
                });
        },
    },
    computed: {
        ...mapState({
            batter: state => state.current.batter,
            batterIds: state => state.current.batterIds,
            batterNames: state => state.current.batterNames,
        }),
    },
}
</script>

<style>
.stats-table {
  border-collapse: collapse;
  width: 95%;
  font-size: 12px;
  margin-bottom: 8px;
}

.stats-table th, .stats-table td {
  border: 1px solid #ddd;
  text-align: left;
}

.stats-table th {
  background-color: #f2f2f2;
}
</style>
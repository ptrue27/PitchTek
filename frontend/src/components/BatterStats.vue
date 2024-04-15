<template>
    <v-card style="width: 100%; margin: 10px 10px; border: 2px solid #43A047;" 
        elevation="3" 
    >
        <!--Player select-->
        <v-row>
            <v-col>
                <v-select
                    :items="batterNames" 
                    v-model="batter.name"
                    @update:modelValue="handleBatterChange"
                    density="compact" 
                    color="green-darken-1"
                ></v-select>
            </v-col>
        </v-row>
        <v-row style="margin-top: -30px;">
            <!--Player image-->
            <v-col cols="3" style="margin-top: 0px;">
                <v-img v-if="batter.img"
                    :src="batter.img"
                ></v-img>
                <v-img v-else
                    src="@/assets/silhouette.png"
                ></v-img>
            </v-col>

            <!--Player stats-->
            <v-col cols="9" class="pr-2">
                <!--Counting stats table-->
                <v-row>
                    <v-col>
                        <div>
                            <table class="stats-table">
                                <thead>
                                    <tr>
                                    <th>Games</th>
                                    <th>PA</th>
                                    <th>Hits</th>
                                    <th>HR</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                    <td>{{ batter.games }}</td>
                                    <td>{{ batter.pa }}</td>
                                    <td>{{ batter.pa }}</td>
                                    <td>{{ batter.hr }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </v-col>
                </v-row>

                <!--Rate stats table-->
                <v-row style="margin-bottom: 5px;">
                    <v-col>
                        <div>
                            <table class="stats-table" color="green-darken-1">
                                <thead>
                                    <tr>
                                    <th>AVG</th>
                                    <th>OBP</th>
                                    <th>SLG</th>
                                    <th>OPS</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                    <td>{{ batter.avg }}</td>
                                    <td>{{ batter.obp }}</td>
                                    <td>{{ batter.slg }}</td>
                                    <td>{{ batter.ops }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </v-col>
                </v-row>
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
            const path = 'http://localhost:5000/api/get_batter/' + batterId;

            axios.get(path)
                .then((res) => {
                    const newBatter = res.data;
                    console.log("Changed Batter: " + newBatter);
                    if (this.pitcherId) {
                        const rand = Math.floor(Math.random() * 50);
                        this.$store.commit("setMatchup", rand);
                    }
                    else {
                        this.$store.commit("setMatchup", 0);
                    }
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
            pitcherId: state => state.current.pitcher.id,
        }),
    },
}
</script>

<style>
.stats-table {
  border-collapse: collapse;
  width: 95%;
  font-size: 14px;
}

.stats-table td {
  border: 1px solid #43A047;
  text-align: center;
}

.stats-table th {
  background-color: #f2f2f2;
  color: #43A047;
  border: 1px solid gray;
  text-align: center;
}
</style>
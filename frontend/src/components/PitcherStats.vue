<template>
    <v-card style="width: 100%; margin: 10px 10px; border: 2px solid #43A047;" 
        elevation="3"
    >
        <!--Player select-->
        <v-row>
            <v-col>
                <v-select
                    :items="pitcherNames" 
                    v-model="pitcher.name" 
                    @update:modelValue="handlePitcherChange"
                    density="compact" 
                    color="green-darken-1"
                ></v-select>
            </v-col>
        </v-row>
        <v-row style="margin-top: -30px;">
            <!--Player image-->
            <v-col cols="3" style="margin-top: 0px;">
                <v-img v-if="pitcher.img"
                    :src="pitcher.img"
                ></v-img>
                <v-img v-else
                    src="@/assets/silhouette.png"
                ></v-img>
            </v-col>

            <!--Counting stats-->
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
                                    <td>{{ pitcher.games }}</td>
                                    <td>{{ pitcher.batters }}</td>
                                    <td>{{ pitcher.hits }}</td>
                                    <td>{{ pitcher.hr }}</td>
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
                                    <th>ERA</th>
                                    <th>WHIP</th>
                                    <th>K/9</th>
                                    <th>BB/9</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                    <td>{{ pitcher.era }}</td>
                                    <td>{{ pitcher.whip }}</td>
                                    <td>{{ pitcher.kper9 }}</td>
                                    <td>{{ pitcher.bbper9 }}</td>
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
        handlePitcherChange() {
            const index = this.pitcherNames.indexOf(this.pitcher.name);
            const id = this.pitcherIds[index];
            const path = 'http://localhost:5000/api/get_pitcher/' + id;

            axios.get(path)
                .then((res) => {
                    const newPitcher = res.data;
                    if (this.batterId) {
                        const rand = Math.floor(Math.random() * 50);
                        this.$store.commit("setMatchup", rand);
                    }
                    else {
                        this.$store.commit("setMatchup", 0);
                    }
                    console.log("Changed pitcher: " + newPitcher.name + ", " + newPitcher.id);
                    this.$store.commit("setCurrentPitcher", newPitcher);
                })
                .catch((error) => {
                    console.error("Error changing pitcher: " + error);
                    this.$store.commit("setCurrentPitcher", this.$store.state.default.pitcher);
                });
        },
    },
    computed: {
        ...mapState({
            pitcher: state => state.current.pitcher,
            pitcherIds: state => state.current.pitcherIds,
            pitcherNames: state => state.current.pitcherNames,
            batterId: state => state.current.batter.id,
        }),
    },
};
</script>
<template>
    <v-card style="width: 100%; margin: 10px 10px;" 
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
            <v-col cols="3">
                <v-img v-if="pitcher.img"
                    :src="pitcher.img"
                ></v-img>
                <v-img v-else
                    src="@/assets/silhouette.png"
                ></v-img>
            </v-col>

            <!--Player stats-->
            <v-col cols="9" class="pr-2">
                <div>
                    <table class="stats-table">
                        <thead>
                            <tr>
                            <th>ERA</th>
                            <th>K/9</th>
                            <th>BB/9</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                            <td>{{ pitcher.era }}</td>
                            <td>{{ pitcher.kper9 }}</td>
                            <td>{{ pitcher.bbper9 }}</td>
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
        handlePitcherChange() {
            const index = this.pitcherNames.indexOf(this.pitcher.name);
            const id = this.pitcherIds[index];
            const path = 'http://localhost:5000/api/get_pitcher/' + id;

            axios.get(path)
                .then((res) => {
                    const newPitcher = res.data;
                    this.emitter.emit("ChangePitcher", newPitcher)
                    this.emitter.emit("ChangePitcher2", newPitcher)
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
        }),
    },
};
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
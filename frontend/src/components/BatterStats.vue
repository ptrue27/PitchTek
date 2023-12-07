<template>
    <v-card style="width: 100%; margin: 10px 10px;">
        <!--Player select-->
        <v-row>
            <v-col>
                <v-select
                    :items="names" v-model="data.name" 
                    @update:modelValue="handleBatterChange"
                    density="compact" 
                ></v-select>
            </v-col>
        </v-row>
        <v-row style="margin-top: -30px;">
            <!--Player image-->
            <v-col cols="3">
                <v-img
                    :src="data.img"
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
                            <td>{{ data.hr }}</td>
                            <td>{{ data.obp }}</td>
                            <td>{{ data.slg }}</td>
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

export default {
    data(){
        return{
            defaultData: {name: 'Select Player', img: "data:image/png;base64,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",
                   hr: '-', obp: '-', slg: '-'},
            data: {},
            names: ['Mike Trout', 'Shohei Ohtani'],
            ids: [1, 2]
        }
    },
    methods: {
        handleBatterChange() {
            const path = 'http://localhost:5000/get_batter';
            const ind = this.names.indexOf(this.data.name);
            const id = this.ids[ind];

            axios.get(path, { params: { id: id } })
                .then((res) => {
                    console.log(res.data)
                    this.data = res.data;
                })
                .catch((error) => {
                    console.error(error);
                    this.data = this.defaultData;
                });

            this.$store.commit('setBatter', {
                id: id,
                name: this.data.name,
                img: this.data.img
            });
        },
    },
    created() {
        this.data = this.defaultData;
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
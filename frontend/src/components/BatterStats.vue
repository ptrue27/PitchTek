<template>
    <v-card style="width: 100%; margin: 10px 10px;">
        <h3 class="ml-2">{{ player.name }}</h3>
        <v-row>
            <!--Player image-->
            <v-col cols="3">
                <v-img fluid
                    :src="player.img"
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
                            <td>{{ player.hr }}</td>
                            <td>{{ player.obp }}</td>
                            <td>{{ player.slg }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </v-col>
        </v-row>
    </v-card>
</template>

<script>
export default {
    data(){
        return{
            player: { name: 'Mike Trout', img: 'data:image/jpeg;base64,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', 
            hr: 35, obp: .402, slg: .517 },
        }
    },
}
</script>

<style>
.stats-table {
  border-collapse: collapse;
  width: 95%;
  font-size: 12px;
  margin-bottom: 5px;
}

.stats-table th, .stats-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.stats-table th {
  background-color: #f2f2f2;
}
</style>
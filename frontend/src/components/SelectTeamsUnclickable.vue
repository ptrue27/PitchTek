<template>
    <!--Team selection-->
    <v-row class="text-center" style="margin-bottom: -40px; margin-left: 3px; margin-top: 3px; margin-right: 3px;">
        <!--Input home team-->
        <v-col cols="6">
            <v-select readonly="true"
                :items="homeTeamNames"
                v-model="homeTeamName"
                variant="solo-filled"
                density="compact"
                color="green-darken-1"
                opacity=0
            ></v-select>
        </v-col>
                  
        <!--Input away team-->
        <v-col cols="6">
            <v-select readonly="true"
                :items="awayTeamNames" 
                v-model="awayTeamName"
                variant="solo-filled" 
                density="compact"
                color="green-darken-1"
                style="margin-bottom: -30px;"
            ></v-select>
        </v-col>
     </v-row>
              
    <!--Score input-->
    <v-row style="margin-bottom: -30px;">
        <!--Home Score-->
        <v-col cols="3" style="margin-top: 10px;" align="right">
            <p class="home-away" style="margin-right: 30px;">
                Home
            </p>
        </v-col>
        <v-col cols="2">
            <v-select readonly="true"
                :items="scores"
                v-model="homeScore"
                density="compact"
                variant="solo-filled"
                color="green-darken-1"
            ></v-select>
        </v-col>

        <v-col cols="2" class="score-spacer text-center">
            <p>-</p>
        </v-col>
        
        <!--Away Score-->
        <v-col cols="2">
            <v-select readonly="true"
                :items="scores"
                v-model="awayScore"
                density="compact"
                variant="solo-filled"
                color="green-darken-1"
            ></v-select>
        </v-col>
        <v-col cols="3" style="margin-top: 10px;" align="left">
            <p class="home-away" style="margin-left: 30px;">
                Away
            </p>
        </v-col>
    </v-row>
</template>

<script>


export default {
  props: {
    storeSnapshot: {
      type: Object,
      required: true
    }
  },

  computed: {
    homeTeamName: {
      get() {
        return this.storeSnapshot.home_name
      },
    },
    homeScore: {
      get() {
        return this.storeSnapshot.home_score
      },
    },
    awayTeamName: {
      get() {
        return this.storeSnapshot.away_name
      },
    },
    awayScore: {
      get() {
        return this.storeSnapshot.away_score
      },
    },
  },
};
</script>

<style>
    .score-spacer {
        margin-top: -3px;
        font-size: 30px;
    }
    .home-away {
        font-weight: bold;
        font-size: 16px;
        margin-top: -5px;
    }

</style>
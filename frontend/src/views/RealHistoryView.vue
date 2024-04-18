<template>
  <div id="app">
    <h1>Previous Predictions</h1>
    <form @submit.prevent="">

    </form>
    <div>
      <ItemComponent
        v-for="(team, index) in teams"
        :key="index"
        :HomeTeamName="team.HomeTeamName"
        :HomeScore="team.HomeScore"
        :AwayTeamName="team.AwayTeamName"
        :AwayScore="team.AwayScore"
        :Inning="team.Inning"
        :pitch-type="team.pitchType"
        :pitcher-id="team.pitcherId"
        :base-colors="team.baseColors"
      />
    </div>
  </div>
</template>

<script>
import ItemComponent from '@/components/PreviousPrediction2.vue';

export default {
  components: {
    ItemComponent
  },
  data() {
    return {
      teams: [],
      newTeam: {
        //teamName: '',
        //score: ''
      }
    }
  },
  mounted() {
      this.emitter.on("UpdateHistory", (pitcher_obj) => {

        console.log("Here100", pitcher_obj)

        this.addTeam(pitcher_obj);

      });
  },
  methods: {
    addTeam(pitcher_obj) {
      this.teams.push({
        HomeTeamName: pitcher_obj.HomeTeamName,
        HomeScore: pitcher_obj.HomeScore,
        AwayTeamName: pitcher_obj.AwayTeamName,
        AwayScore: pitcher_obj.AwayScore,
        Inning: pitcher_obj.Inning,
        pitchType: pitcher_obj.pitchType,
        pitcherId: pitcher_obj.pitcherId,
        baseColors: pitcher_obj.baseColors
      });


    }
  }
}
</script>

<style>
#app {
  text-align: center;
}

input, button {
  margin: 5px;
}
</style>

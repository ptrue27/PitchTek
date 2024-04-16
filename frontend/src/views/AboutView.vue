<template>
  <div id="app">
    <h1>Team Scores List</h1>
    <form @submit.prevent="addTeam">
      <input type="text" v-model="newTeam.teamName" placeholder="Enter team name" required>
      <input type="text" v-model="newTeam.score" placeholder="Enter score" required>
      <button type="submit">Add Team</button>
    </form>
    <div>
      <ItemComponent
        v-for="(team, index) in teams"
        :key="index"
        :teamName="team.teamName"
        :score="team.score"
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
        teamName: '',
        score: ''
      }
    }
  },
  mounted() {
      this.emitter.on("NewUpdateHistory", (pitcher_obj) => {

        console.log("Here100", pitcher_obj)

        this.addTeam(pitcher_obj);

      });
  },
  methods: {
    addTeam(pitcher_obj) {
      this.teams.push({
        teamName: pitcher_obj.pitchType[0],
        score: pitcher_obj.pitcherId
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

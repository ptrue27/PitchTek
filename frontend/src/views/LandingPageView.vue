<template>
  <div class="dashboard-container">
    <!--Title-->
    <v-row>
        <v-col class="text-center d-flex justify-center">
            <v-card class="landing-v-card" elevation="3">
                <h1 style="font-size: 45px; margin-top: 2px;">PitchTek.</h1>
                <h3 style="margin-bottom: 8px;">Bringing machine learning to the diamond.</h3>
            </v-card> 
        </v-col>
    </v-row>

    <!--User form-->
    <v-row style="margin-top: 20px;">
      <v-col cols="4">
        <v-img src="@/assets/pitcher_silhouette.png" height="275px"/>
      </v-col>
      <v-col cols="4" class="d-flex justify-center">
        <LoginUser />
      </v-col>
        <v-col cols="4">
          <v-img src="@/assets/batter_silhouette.png" height="325px"/>
        </v-col>
    </v-row>

  </div>
</template>

<script>
import LoginUser from "@/components/LoginUser.vue"

export default {
  components: {
    LoginUser,
  },
}
</script>

<style>
.landing-v-card {
  border: 2px solid gray;
  margin-top: 150px; 
  width: 400px;
}
</style>
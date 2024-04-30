<template>
    <v-app-bar>
      <router-link to="/" class="text-decoration-none d-flex align-center" 
        style="width: 170px;"
      >
        <!--Logo Icon and Title-->
        <v-img
          src="@/assets/baseball-icon.png"
          alt="PitchTek logo"
          max-height="50"
          max-width="50"
          class="ml-5"
          contain
        ></v-img>

        <v-app-bar-title class="ml-3 text-decoration-none" style="color: black;">
          PitchTek
        </v-app-bar-title>
      </router-link>

      <v-spacer></v-spacer>

      <!--About button-->
      <v-btn
        to="/about"
        prepend-icon="mdi-information"
        variant="tonal" class="mr-5"
      >
        About
      </v-btn>

      <!--Dashboard button-->
      <v-btn
        v-if="$store.state.isLoggedIn"
        to="/dashboard"
        prepend-icon="mdi-view-dashboard"
        variant="tonal" class="mr-5"
      >
        Dashboard
      </v-btn>

      <!--Matchup button-->
      <v-btn
        v-if="$store.state.isLoggedIn"
        to="/matchup"
        prepend-icon="mdi-account-multiple"
        variant="tonal" class="mr-5"
      >
        Matchup
      </v-btn>

      <!--Statistics button-->
      <v-btn
        v-if="$store.state.isLoggedIn"
        to="/statistics"
        prepend-icon="mdi-magnify"
        variant="tonal" class="mr-5"
      >
        Statistics
      </v-btn>

      <!--Account button-->
      <v-btn
        v-if="$store.state.isLoggedIn"
        to="/account"
        prepend-icon="mdi-account-circle"
        variant="tonal" class="mr-5"
      >
        Account
      </v-btn>

      <!--Logout button-->
      <v-btn
        v-if="$store.state.isLoggedIn"
        @click="logoutUser"
        prepend-icon="mdi-logout"
        variant="tonal" class="mr-2"
      >
        Logout
      </v-btn>

    </v-app-bar>
</template>

<script>
import axios from 'axios';
  
export default {
  methods: {
    async logoutUser() {
      try {
        // Make POST request
        const path = 'http://' + this.$store.state.host + '/api/logout';
        const response = await axios.post(path);
        
        // Check if logout was successful
        if (response.status == 200) {
          sessionStorage.removeItem('token');
          this.$store.commit("logout")
          this.$router.push({ name: 'LandingPage' });
          console.log("Logged out")
        } 
      } 
      
      // Handle error
      catch (error) {
        console.error('Error logging out user:', error);
      }
    }
  }
};
</script>
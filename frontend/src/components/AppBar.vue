<template>
    <v-app-bar>
      <!--Logo Icon and Title-->
      <v-img
        src="@/assets/baseball-icon.png"
        alt="PitchTek logo"
        max-height="50"
        max-width="50"
        class="ml-5"
        contain
      ></v-img>

      <v-app-bar-title>PitchTek</v-app-bar-title>

      <!--About button-->
      <v-btn
        to="/about"
        prepend-icon="mdi-view-dashboard"
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

      <!--Statistics button-->
      <v-btn
        v-if="$store.state.isLoggedIn"
        to="/statistics"
        prepend-icon="mdi-magnify"
        variant="tonal" class="mr-5"
      >
        Statistics
      </v-btn>

      <!--History button-->
      <v-btn
        v-if="$store.state.isLoggedIn"
        to="/history"
        prepend-icon="mdi-history"
        variant="tonal" class="mr-5"
      >
        History
      </v-btn>

      <!--Real History button-->
      <v-btn
        v-if="$store.state.isLoggedIn"
        to="/realhistory"
        prepend-icon="mdi-history"
        variant="tonal" class="mr-5"
      >
        Real History
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
        const path = 'http://localhost:5000/logout'
        const response = await axios.post(path);
        console.log(response.data);
        
        // Check if logout was successful
        if (response.status == 200) {
          this.$store.commit("logout")
          this.$router.push({ name: 'LandingPage' });
        } 
      } 
      
      // Handle error
      catch (error) {
        console.error('Error logging in user:', error);
      }
    }
  }
};
</script>
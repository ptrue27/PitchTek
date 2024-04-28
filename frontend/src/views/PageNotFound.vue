<template>
  <v-container fluid class="dashboard-container">
    <v-row justify="center" style="margin-top: 250px;"> 
        <v-col cols="4">
          <v-img src="@/assets/whiff.png" height="275px"/>
        </v-col>
        <v-col cols="4" class="text-center"> 
            <div class="center-card"> 
              <v-card class="login-card card-border" elevation="3">
                <h1 style="margin-top: 5px;">Strikeout!</h1>
                <h3>Error 404: Page Not Found</h3>
                <router-link to="/">
                  <p style="margin-top: 30px; margin-bottom: 9px;">
                    Return to Login
                  </p>
                </router-link>
              </v-card>
            </div> 
        </v-col>
        <v-col cols="4"></v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.center-card {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
</style>

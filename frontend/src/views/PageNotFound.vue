<template>
  <v-container fluid class="dashboard-container">
    <v-row justify="center" style="margin-top: 250px;"> 
        <v-col cols="12" md="6" class="text-center"> 
            <div class="center-card"> 
              <v-card class="login-card">
                <h1>Strikeout!</h1>
                <h3>Error 404: Page not found</h3>

                <router-link to="/">
                  <p style="margin-top: 30px;">Return to login page</p>
                </router-link>
              </v-card>
            </div> 
        </v-col>
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

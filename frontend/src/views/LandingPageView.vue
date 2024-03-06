<template>
  <v-container fluid>
    <!--Title-->
    <v-row>
        <v-col class="text-center">
            <div style="margin-top: 150px;">
                <h1>PitchTek</h1>
                <h3>Bringing machine learning to the diamond.</h3>
            </div> 
        </v-col>
    </v-row>

    <!--User form-->
    <v-row 
      style="margin-top: 20px;"
    >
      <v-col 
        cols="12"
        class="d-flex justify-center"
      >
        <LoginUser />
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
import LoginUser from "@/components/LoginUser.vue"

export default {
  components: {
    LoginUser,
  },
}
</script>
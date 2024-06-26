<template>
    <v-card class="login-card card-border" elevation="3">
        <!--Title-->
        <v-card-title class="border-bottom text-center">
          {{ mode }}
        </v-card-title>

        <!--Username input-->
        <v-row style="padding-left: 20px; padding-right: 20px; margin-top: 10px">
          <v-col>
            <v-text-field 
              type="text" 
              v-model="username" 
              placeholder="Email" 
              class="my-text-input"
              :rules="usernameRules"
              ref="usernameInput"
              variant="outlined"
            />
          </v-col>
        </v-row>

        <!--Password Input-->
        <v-row style="padding-left: 20px; padding-right: 20px; margin-top: 10px">
          <v-col>
            <v-text-field 
              type="password" 
              v-model="password" 
              placeholder="Password"
              class="my-text-input"
              :rules="passwordRules"
              ref="passwordInput"
              variant="outlined"
            />
          </v-col>
        </v-row>

        <!--Error message-->
        <v-row>
          <v-col class="text-center error-message">
            <p>{{ errorMessage }}</p>
          </v-col>
        </v-row>

        <!--Submit Button-->
        <v-row>
          <v-col class="text-center">
            <v-btn @click="loginUser" color="green-darken-1">Submit</v-btn>
          </v-col>
        </v-row>

        <!--Switch forms-->
        <v-row style="margin-bottom: 5px;">
          <v-col class="text-center">
            <button @click="switchMode" style="text-decoration: underline;">
              {{ unsetMode }}
            </button>
          </v-col>
        </v-row>

    </v-card>
  </template>
  
<script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        mode: "Login",
        unsetMode: "Sign Up",
        username: '',
        password: '',
        errorMessage: '',
        usernameRules: [
          v => !!v || 'Email is required',
          v => /.+@.+\..+/.test(v) || 'Email must be valid',
          v => (v && v.length <= 64) || 'Email must be less than 64 characters'
        ],
        passwordRules: [
          v => !!v || 'Password is required',
          v => (v && v.length >= 8 && v.length <= 64) || 'Password must be between 8 and 64 characters',
          v => /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()])/.test(v) || 'Password must contain at least 1 lowercase letter, 1 uppercase letter, 1 number, and 1 special character',
        ],
      };
    },
    methods: {
      switchMode() {
        this.errorMessage = '';
        let temp = this.mode;
        this.mode = this.unsetMode;
        this.unsetMode = temp;
      },
      async loginUser() {
        try {
          // Validate the input fields
          const valid_username = await this.$refs.usernameInput.validate() == "";
          const valid_password = await this.$refs.passwordInput.validate() == "";
          if (!(valid_username && valid_password)) {
            return;
          }

          // Make POST request
          let endpoint = "sign_up";
          if (this.mode == "Login") {
            endpoint = "login"
          }
          const path = 'http://' + this.$store.state.host + '/api/' + endpoint;
          const response = await axios.post(path, {
            username: this.username,
            password: this.password
          });
          
          // Check if request was successful
          if (response.status == 200 || response.status == 201) {
            this.errorMessage = '';
            console.log("RESPONSE" + response.data)
            this.$store.commit("login", response.data);
            this.$router.push({ name: 'Dashboard' });
          } 
        } 
        
        // Handle error
        catch (error) {
          this.errorMessage = error.response.data.message;
          console.error('Error logging in user:', this.errorMessage);
          if (this.$store.state.isLoggedIn) {
            this.$store.commit("logout");
          }
        }
      }
    }
  };
</script>
  
<style>
  .error-message {
    color: rgb(182, 45, 45);
  }
  .login-card {
    width: 300px;
  }
  .my-text-input {
    margin-left: 3px;
    margin-right: 3px;
  }
</style>
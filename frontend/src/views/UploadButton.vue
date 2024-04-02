<template>
    <v-container>
      <v-row>
        <v-col>
          <v-file-input 
            v-model="selectedFile" 
            label="Choose File" 
            @change="onFileChange" 
            filled 
            prepend-icon="mdi-paperclip"
          ></v-file-input>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-btn 
            color="success" 
            class="ma-2" 
            dark 
            @click="uploadFile" 
            :loading="loading" 
            :disabled="!selectedFile || loading"
            rounded
          >
            Upload
            <v-icon right dark>
              mdi-upload
            </v-icon>
          </v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <p v-if="message">{{ message }}</p>
        </v-col>
      </v-row>
    </v-container>
  </template>
  <script>
  //import axios from 'axios';
  
  export default {
    data() {
      return {
        selectedFile: null,
        message: '',
        loading: false
      };
    },
    methods: {
      onFileChange(event) {
        this.selectedFile = event.target.files[0];
      },
      uploadFile() {
        this.loading = true;
        const formData = new FormData();
        formData.append('file', this.selectedFile);
        
        
        setTimeout(() => {
          this.message = 'File uploaded successfully'; // Example success message
          this.loading = false;
        }, 1500);
      }
    }
  };
  </script>
  
  <style>
.v-btn {
  border-radius: 10px; 
}
</style>

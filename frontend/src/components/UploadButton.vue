<template>
  <v-container>
    <v-row>
      <v-col>
        <v-file-input
          v-model="selectedFile"
          label="Choose File"
          @change="onFileSelected"
          filled
          prepend-icon="mdi-paperclip"
          :show-size="true"
          clearable
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
          :disabled="!selectedFile"
          rounded
        >
          Uplo2ad
          <v-icon right dark>
            mdi-uploa2d
          </v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <p v-if="fileName">Selected file: {{ fileName }}</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
      fileName: '',
    };
  },
  methods: {
    onFileSelected() {
      if (this.selectedFile) {
        this.fileName = this.selectedFile.name; // Display the name of the file
      }
    },
    uploadFile() {
      const formData = new FormData();
       formData.append('file', this.selectedFile);

      axios
        .post('http://localhost:5000/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then((response) => {
          alert(response.data); // Alert the server response
        })
        .catch((error) => {
          console.error('Error uploading file:', error);
        });
    },
  },
};
</script>

<style>
.v-btn {
  border-radius: 10px;
}
</style>

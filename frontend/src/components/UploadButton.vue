<template>
    <div>
        <input type="file" @change="onFileChange">
        <button @click="uploadFile">Upload</button>
        <p v-if="message">{{ message }}</p>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            selectedFile: null,
            message: ''
        };
    },
    methods: {
        onFileChange(event) {
            this.selectedFile = event.target.files[0];
        },
        uploadFile() {
            const formData = new FormData();
            formData.append('file', this.selectedFile);

            axios.post('http://localhost:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
                .then(response => {
                    this.message = response.data.message;
                })
                .catch(error => {
                    console.error('Error:', error);
                    this.message = 'Upload failed';
                });
        }
    }
};
</script>
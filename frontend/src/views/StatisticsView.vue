<template>
    <div>
        <div v-for="fileName in fileNames" :key="fileName">
            <div v-html="loadedHTML[fileName]"></div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            fileNames: ['zone.html', 'strikes.html',' sv_id.html'], // List your HTML filenames here
            loadedHTML: {}
        };
    },
    mounted() {
        this.loadGraphs();
    },
    methods: {
        loadGraphs() {
            this.fileNames.forEach(fileName => {
                const filePath = `C:/Users/davis/PitchTek-2/dataVisual/${fileName}`; // Adjust the path to where your HTML files are served
                axios.get(filePath).then(response => {
                    this.$set(this.loadedHTML, fileName, response.data);
                }).catch(error => {
                    console.error(`Failed to load ${fileName}:`, error);
                });
            });
        }
    }
};
</script>

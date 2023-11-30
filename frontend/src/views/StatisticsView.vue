<template>
    <v-row>
        <v-col class="text-center">   
            <div>Statistics</div>
        </v-col>
    </v-row>
    <v-row>
        <v-col><UploadButton /></v-col>
        <v-col><FlaskPing /></v-col>
          </v-row>
</template>

<script>
import UploadButton from "@/components/UploadButton.vue"
import FlaskPing from "@/components/FlaskPing.vue"

export default {
    components: {
    UploadButton,
    FlaskPing
  }
}
</script>
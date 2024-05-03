<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          label="Release Speed (mph)"
          type="number"
          v-model="pitchData.release_speed"
          :rules="[rules.required, rules.releaseSpeedRange]"
          required
        ></v-text-field>
        <v-text-field
          label="Plate X Position"
          type="number"
          v-model="pitchData.plate_x"
          :rules="[rules.required, rules.plateXRange]"
          required
        ></v-text-field>
        <v-text-field
          label="Plate Z Position"
          type="number"
          v-model="pitchData.plate_z"
          :rules="[rules.required, rules.plateZRange]"
          required
        ></v-text-field>
        <v-text-field
          label="Number of Balls"
          type="number"
          v-model="pitchData.balls"
          :rules="[rules.required, rules.ballsRange]"
          required
        ></v-text-field>
        <v-text-field
          label="Number of Strikes"
          type="number"
          v-model="pitchData.strikes"
          :rules="[rules.required, rules.strikesRange]"
          required
        ></v-text-field>
        <v-btn :disabled="!isValid" color="blue darken-1" dark @click="predictPitch">
          Predict Pitch
        </v-btn>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Prediction Results</v-card-title>
          <v-card-text>
            <div><strong>Pitch Type:</strong> {{ prediction.type }}</div>
            <div><strong>Location (X, Z):</strong> {{ prediction.location }}</div>
            <div><strong>Confidence:</strong> {{ prediction.confidence }}%</div>
            <div><strong>Error Margin (X, Z):</strong> {{ prediction.error }}</div>
            <v-img :src="imageSource" max-height="300" max-width="500"></v-img>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      pitchData: {
        release_speed: null,
        plate_x: null,
        plate_z: null,
        balls: null,
        strikes: null,
      },
      prediction: {
        type: '',
        location: '',
        error: '',
        confidence: '',
        image: ''
      },
      imageSource: '',
      rules: {
        required: value => !!value || 'Required.',
        releaseSpeedRange: value => (value >= 40 && value <= 105) || 'Release speed must be between 40 and 105 mph.',
        plateXRange: value => (value >= -2 && value <= 2) || 'Plate X position must be between -2 and 2 feet.',
        plateZRange: value => (value >= 1 && value <= 6) || 'Plate Z position must be between 1 and 6 feet.',
        ballsRange: value => (value >= 0 && value <= 3) || 'Number of balls must be between 0 and 3.',
        strikesRange: value => (value >= 0 && value <= 2) || 'Number of strikes must be between 0 and 2.',
      }
    };
  },
  computed: {
    isValid() {
      return (
        this.pitchData.release_speed !== null &&
        this.pitchData.plate_x !== null &&
        this.pitchData.plate_z !== null &&
        this.pitchData.balls !== null &&
        this.pitchData.strikes !== null
      );
    }
  },
  methods: {
    predictPitch() {
      axios.post('http://localhost:5000/new_prediction', this.pitchData)
        .then(response => {
          this.prediction = response.data;
          this.imageSource = `data:image/png;base64,${response.data.image}?${new Date().getTime()}`;
          this.imageSource = `data:image/png;base64,${response.data.image}`; 
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }
  }
};
</script>

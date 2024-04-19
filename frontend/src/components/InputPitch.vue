<template>
    <v-dialog width="500" v-model="dialog">
        <template v-slot:activator="{ props: activatorProps }">
            <v-btn
                v-bind="activatorProps"
                prepend-icon="mdi-baseball"
                text="Record Pitch"
                color="green-darken-1"
                variant="outlined"
                class="record-btn"
            ></v-btn>
        </template>

            <v-card class="text-center">
                <v-card-title class="border-bottom">Record Pitch</v-card-title>
                <v-row style="margin-top: 3px;">
                    <!--Input Pitch Location-->
                    <v-col style="margin-left: 5px;">
                        <v-row>
                            <v-col class="justify-center text-center">
                                <InputPitchLocation style="margin-left: 20px;" />
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col>
                                <p class="location-text">
                                    Location
                                </p>
                            </v-col>
                        </v-row>
                    </v-col>

                    <v-col>
                        <!--Select Pitch Type-->
                        <v-row>
                            <v-col 
                                cols="4" class="no-wrap" 
                                style="margin-left: -30px; margin-right: -40px;"
                            >
                                <p style=" margin-top: 40px;" class="location-text">
                                    Type
                                </p>
                            </v-col>
                            <v-col cols="8">
                                <v-select
                                    :items="types" 
                                    v-model="type"
                                    @update:modelValue="handlePitchTypeChange"
                                    variant="solo-filled"
                                    density="compact" 
                                    style="width: 185px; margin-top: 30px;"
                                ></v-select>
                            </v-col>
                        </v-row>

                        <!--Input Pitch Speed-->
                        <v-row>
                            <v-col cols="4" class="no-wrap" 
                                style="margin-left: -30px; margin-right: -40px;"
                            >
                                <p style="margin-top: 3px;" class="location-text">Speed</p>
                            </v-col>
                            <v-col cols="8">
                                <v-text-field
                                    v-model="speed"
                                    variant="filled"
                                    type="number"
                                    step="0.1"
                                    dense
                                    outlined
                                    style="width: 100px; margin-top: -15px;"
                                ></v-text-field>
                            </v-col>
                        </v-row>


                        <!--Predict button-->
                        <v-row>
                            <v-col class="d-flex justify-center" style="margin-top: -10px; margin-left: -50px;">
                                <v-btn
                                    prepend-icon="mdi-arrow-right-bold-box"
                                    class="mx-auto"
                                    @click="handlePredictButtonClick"
                                    color="green-darken-1"
                                >Save Pitch</v-btn>  
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>

                
                <!--Close button-->
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        text="Close"
                        @click="dialog = false"
                        color="green-darken-1"
                    ></v-btn>
                </v-card-actions>
            </v-card>
    </v-dialog> 
</template>

<script>
    import axios from 'axios';
    import InputPitchLocation from "@/components/InputPitchLocation.vue";

    export default {
        components: {
            InputPitchLocation
        },
        data() {
            return {
                dialog: false,
                type: "Select Pitch",
                types: ["Changeup (CH)",
                        "Curveball (CU)",
                        "Cutter (FC)",
                        "Eephus (EP)",
                        "Forkball (FO)",
                        "Four-Seam Fastball (FF)",
                        "Knuckleball (KN)",
                        "Knuckle-curve (KC)",
                        "Screwball (SC)",
                        "Sinker (SI)",
                        "Slider (SL)",
                        "Slurve (SV)",
                        "Splitter (FS)",
                        "Sweeper (ST)"],
                speed: 0.0,
                curr_pitcher_id: "NA",
            };
        },
        methods: {
            handlePredictButtonClick() {
                console.log('Predict Button clicked!');

                const path = 'http://' + this.$store.state.host + '/make_prediction';
                const params = this.gameState;
                axios.get(path, { params })
                .then((res) => {
                    const predictions = res.data.predictions;
                    console.log("Pitch Predictions Recieved: " + predictions);
                    this.$store.commit("predict", predictions);
                })
                .catch((error) => {
                    console.error(error);
                });
                this.dialog = false;
            },
            handlePitchTypeChange() {
                console.log('Changed Pitch Type');
            },
        },
        computed: {
            gameState() {
                return {
                    inning: this.$store.state.inning,
                };
            }
        },

    };
</script>

<style>
  .location-text {
    font-weight: bold;
    margin-left: -48px;
    margin-top: -18px;
  }
  .border-bottom {
    border-bottom: 1px solid gray;
    background-color: #F2F2F2;
  }
</style>
<template>
    <v-dialog width="500">
        <template v-slot:activator="{ props: activatorProps }">
            <v-btn
                v-bind="activatorProps"
                color="green-darken-1"
                prepend-icon="mdi-baseball"
                text="Record Pitch"
                variant="outlined"
            ></v-btn>
        </template>

        <template v-slot:default="{ isActive }">
            <v-card class="text-center" title="Record Pitch">
                <v-row style="margin-top: 3px;">
                    <!--Input Pitch Location-->
                    <v-col>
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
                            <v-col class="d-flex justify-center">
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
                        @click="isActive.value = false"
                    ></v-btn>
                </v-card-actions>
            </v-card>
        </template>
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
                grid: [
                [false, false, false],
                [false, false, false],
                [false, false, false]
                ],
                type: "Select Pitch",
                types: ["4-Seam Fastball", "2-Seam Fastball", "Curveball", 
                        "Slider", "Change Up", "Cutter"],
                speed: 0.0,
            };
        },
        methods: {
            handlePredictButtonClick() {
                console.log('Predict Button clicked!');

                const path = 'http://localhost:5000/make_prediction';

                axios.get(path, { params: this.gameState})
                .then((res) => {
                    console.log("Pitch Prediction Recieved: " + res.data)
                    this.emitter.emit("ChangePitch", res.data)
                })
                .catch((error) => {
                    console.error(error);
                });
            },
            handlePitchTypeChange() {
                console.log('Changed Pitch Type');
            },
        },
    };
</script>

<style>
  .location-text {
    font-weight: bold;
    margin-left: -48px;
    margin-top: -18px;
  }
</style>
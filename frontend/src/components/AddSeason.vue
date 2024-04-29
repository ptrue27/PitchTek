<template>
    <v-dialog width="500" v-model="dialog">
        <template v-slot:activator="{ props: activatorProps }">
            <!-- Small Circular Addition Button -->
            <v-chip 
                v-bind="activatorProps"
                class="small-addition-button"
                color="green-darken-1"
                size="x-small"
                :pill="true"
            >
                <v-icon>mdi-plus</v-icon>
            </v-chip>
        </template>

        <v-card class="text-center">
            <v-card-title class="border-bottom">Add Season</v-card-title>

            <!--Input Season Name-->
            <v-row style="margin-top: 35px;">
                <v-col cols="2" class="d-flex justify-end">
                    <p style="margin-top: 3px;" class="location-text">
                        Name:
                    </p>
                </v-col>
                <v-col cols="7">
                    <v-row>
                        <v-col>
                            <v-text-field
                                v-model="seasonName"
                                variant="filled"
                                dense
                                outlined
                                style="width: 275px; margin-top: -15px;"
                                :rules="validationRules"
                                placeholder="Enter season name"
                                ref="seasonInput"
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    
                    <!--Error message-->
                    <v-row style="margin-top: 0px;">
                        <v-col class="text-center error-message">
                            <p>{{ errorMessage }}</p>
                        </v-col>
                    </v-row>
                </v-col>

            <!--Save button-->
                <v-col cols="3" style="padding-right: 30px; margin-top: -2px;">
                    <v-btn
                        prepend-icon="mdi-arrow-right-bold-box"
                        class="mx-auto"
                        @click="handleAdd"
                        color="green-darken-1"
                        :disabled="isButtonDisabled"
                    >Save</v-btn>  
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

    export default {
        data() {
            return {
                dialog: false,
                seasonName: "",
                errorMessage: "",
                validationRules: [
                    v => v.trim() !== "" || "Name cannot be empty",
                    v => !v.startsWith(" ") || "Name cannot start with a space",
                    v => /^[a-zA-Z0-9 ]+$/.test(v) || "Invalid characters",
                    v => v.length <= 32 || "Name must be 32 characters or fewer",
                ],
            };
        },
        methods: {
            async handleAdd() {
                // Check for valid input
                const valid_input = await this.$refs.seasonInput.validate() == "";
                if (!valid_input) {
                    return;
                }
                
                const path = "http://" + this.$store.state.host + "/api/new_season";
                const token = localStorage.getItem("token");
                const body = {
                    name: this.seasonName,
                };

                axios.post(path, body, { headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    } 
                })
                    .then((res) => {
                        const seasonId = res.data.id;
                        console.log("Added season: " + seasonId);
                        const newSeason = {
                            id: seasonId,
                            name: this.seasonName,
                        };
                        this.$store.commit("addSeason", newSeason);
                        this.errorMessage = "";
                        this.seasonName = "";
                        this.dialog = false;
                    })
                    .catch((error) => {
                        this.errorMessage = error.response.data.msg;
                        console.error('Error adding season:', this.errorMessage);
                    });

            },
        },
        computed: {
            isButtonDisabled() {
                return this.seasonName == "";
            },
        },

    };
</script>

<style>
    .small-addition-button {
        border: 1px solid #43A047;
    }
</style>
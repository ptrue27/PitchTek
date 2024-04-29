<template>
    <v-dialog width="500" v-model="dialog">
        <template v-slot:activator="{ props: activatorProps }">
            <!-- Small Circular Addition Button -->
            <v-chip 
                v-bind="activatorProps"
                class="small-deletion-button"
                color="red-darken-1"
                size="x-small"
                :pill="true"
                style="margin-left: 3px;"
            >
                <v-icon>mdi-minus</v-icon>
            </v-chip>
        </template>

        <v-card class="text-center">
            <v-card-title class="border-bottom">Delete Season</v-card-title>

            <!--Delete Season Warning-->
            <v-row style="margin-top: 15px;">
                <v-col cols="7" class="text-center">
                    <v-row>
                        <v-col style="font-size: 18px;">
                            <p>Warning! This season will be permanantly deleted:</p>
                        </v-col>
                    </v-row>
                    <v-row style="margin-top: 0px; font-size: 18px;">
                        <v-col>
                            <strong>{{ this.$store.state.account.seasonName }}</strong>
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
                <v-col cols="5" style="padding-right: 30px; margin-top: 27px;">
                    <v-btn
                        prepend-icon="mdi-trash-can"
                        class="mx-auto"
                        @click="handleDelete"
                        color="red-darken-1"
                        :disabled="isButtonDisabled"
                    >Delete</v-btn>  
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
                errorMessage: "",
            };
        },
        methods: {
            async handleDelete() {
                const path = "http://" + this.$store.state.host + "/api/delete_season";
                const token = localStorage.getItem("token");
                const body = {
                    name: this.$store.state.account.seasonName,
                };

                axios.post(path, body, { headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    } 
                })
                    .then((res) => {
                        const seasonId = res.data.id;
                        console.log("Deleted season: " + seasonId);
                        const oldSeason = {
                            id: seasonId,
                            name: this.$store.state.account.seasonName,
                        };
                        this.$store.commit("deleteSeason", oldSeason);
                        this.errorMessage = "";
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
                return !this.$store.state.account.seasonId;
            },
        },
    };
</script>

<style>
    .small-deletion-button {
        border: 1px solid #E53935;
    }
</style>
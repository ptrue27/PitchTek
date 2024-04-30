<template>
    <v-dialog width="400" v-model="dialog">
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
            <v-card-title class="border-bottom">Delete Team</v-card-title>

            <!--Delete Team Warning-->
            <v-row style="margin-top: 5px;">
                <v-col class="text-center">
                    <!--Warning-->
                    <v-row>
                        <v-col class="d-flex justify-center">
                            <v-card style="width: 70%; font-size: 14px;"
                                class="small-deletion-button" color="red-lighten-5"
                            >
                                <p><strong>Warning!</strong><br>
                                The following team will be permanently deleted.</p>
                            </v-card>
                        </v-col>
                    </v-row>
                    <v-row style="margin-top: 10px; font-size: 18px; text-decoration: underline;">
                        <v-col cols="6" class="d-flex justify-end" 
                            style="padding-right: 20px; margin-top: 5px"
                        >
                            <strong>{{ this.$store.state.account.teamName }}</strong>
                        </v-col>

                        <!--Delete button-->
                        <v-col cols="6" style="padding-right: 35px; margin-top: 0px;">
                            <v-btn
                                prepend-icon="mdi-trash-can"
                                class="mx-auto"
                                @click="handleDelete"
                                color="red-darken-1"
                                :disabled="isButtonDisabled"
                            >Delete</v-btn>  
                        </v-col>
                    </v-row>
                    
                    <!--Error message-->
                    <v-row style="margin-top: 0px;">
                        <v-col class="text-center error-message">
                            <p>{{ errorMessage }}</p>
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

    export default {
        data() {
            return {
                dialog: false,
                errorMessage: "",
            };
        },
        methods: {
            async handleDelete() {
                const path = "http://" + this.$store.state.host + "/api/delete_team";
                const token = localStorage.getItem("token");
                const body = {
                    name: this.$store.state.account.teamName,
                    season_id: this.$store.state.account.seasonId,
                };

                axios.post(path, body, { headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    } 
                })
                    .then((res) => {
                        const teamId = res.data.id;
                        console.log("Deleted team: " + teamId);
                        const oldTeam = {
                            id: teamId,
                            name: this.$store.state.account.teamName,
                        };
                        this.$store.commit("deleteTeam", oldTeam);
                        this.errorMessage = "";
                        this.dialog = false;
                    })
                    .catch((error) => {
                        this.errorMessage = error.response.data.msg;
                        console.error('Error deleting team:', this.errorMessage);
                    });
            },
        },
        computed: {
            isButtonDisabled() {
                return !this.$store.state.account.teamId;
            },
        },
    };
</script>
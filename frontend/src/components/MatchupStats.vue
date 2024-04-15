<template>
    <v-card
        style="width: 100%; margin: 10px 10px; border: 2px solid #43A047;"
        elevation="3"
    >
        <v-row class="border-bottom" style="margin-top: 0px; font-weight: bold">
            <v-col class="text-center">
                <div>{{ pitcherName }} vs. {{ batterName }}</div>
            </v-col>
        </v-row>

        <!--Matchup table-->
        <v-row style="margin-top: 18px;">
            <v-col style="margin-left: 30px; margin-right: -15px;">
                <table class="stats-table">
                        <thead>
                            <tr>
                            <th>PA</th>
                            <th>K</th>
                            <th>BB</th>
                            <th>Hits</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                            <td>{{ matchup.pa }}</td>
                            <td>{{ matchup.k }}</td>
                            <td>{{ matchup.bb }}</td>
                            <td>{{ matchup.hits }}</td>
                            </tr>
                        </tbody>
                </table>
            </v-col>
        </v-row>

        <!--Hits table-->
        <v-row style="margin-bottom: 5px;">
            <v-col style="margin-left: 30px; margin-right: -15px;">
                <table class="stats-table">
                        <thead>
                            <tr>
                            <th>1B</th>
                            <th>2B</th>
                            <th>3B</th>
                            <th>HR</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                            <td>{{ matchup.singles }}</td>
                            <td>{{ matchup.doubles }}</td>
                            <td>{{ matchup.triples }}</td>
                            <td>{{ matchup.hr }}</td>
                            </tr>
                        </tbody>
                </table>
            </v-col>
        </v-row>
    </v-card>
</template>

<script>
import { mapState } from 'vuex';

export default {
    computed: {
        ...mapState({
            pitcher: state => state.current.pitcher,
            batter: state => state.current.batter,
            matchup: state => state.matchup,
        }),
        pitcherName() {
            if (this.pitcher.name == "Select Pitcher") {
                return "--------";
            }
            else {
                return this.pitcher.name;
            }
        },
        batterName() {
            if (this.batter.name == "Select Batter") {
                return "--------";
            }
            else {
                return this.batter.name;
            }
        },
    }
};
</script>
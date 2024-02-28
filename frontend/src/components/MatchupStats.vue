<template>
    <v-card
        style="width: 100%; margin: 10px 10px;"
        height="150"
    >
        <v-row>
            <v-col class="text-center">
                <div>{{ pitcherName }} vs. {{ batterName }}</div>
            </v-col>
        </v-row>

        <v-row style="margin-top: -10px;">
            <v-col>
                <div style="margin-left: 15px;">
                    <table class="stats-table">
                        <thead>
                            <tr>
                            <th>PA</th>
                            <th>K</th>
                            <th>BB</th>
                            <th>H</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                            <td>41</td>
                            <td>8</td>
                            <td>3</td>
                            <td>16</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
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
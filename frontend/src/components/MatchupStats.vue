<template>
    <v-card
        style="width: 100%; margin: 10px 10px;"
        height="150"
    >
        <v-row>
            <v-col class="text-center">
                <div>{{ pitcher.name }} vs. {{ batter.name }}</div>
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
export default {
    data() {

    },
    computed: {
        pitcher() {
            return this.$store.state.pitcher
        },
        batter() {
            return this.$store.state.batter
        },
    }
};
</script>
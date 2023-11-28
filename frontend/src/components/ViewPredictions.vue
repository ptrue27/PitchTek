<template>
  <v-container fluid>
    <v-card>
      <!-- Displaying Paginated Data -->
      <v-list>
        <v-list-item-group>
          <v-list-item v-for="item in currentData" :key="item.id">
            <!-- Content for each row -->
            <v-list-item-content>
                <v-row>
                    <v-col cols="5">
                        <v-img fluid
                            src="@/assets/strikezone.jpg"
                        ></v-img>
                    </v-col>
                    <!--Innings and count-->
                    <v-col cols="7">
                        <!--Title-->
                        <v-row>
                            <v-col class="my-title">Confidence: {{item.confidence}}%</v-col>
                        </v-row>
                        <!--Pitch info-->
                        <v-row>
                            <v-col>Pitch type:</v-col>
                            <v-col>{{item.type}}</v-col>
                        </v-row>
                        <v-row>
                            <v-col>Speed:</v-col>
                            <v-col>{{item.speed}} mph</v-col>
                        </v-row>
                        <v-row>
                            <v-col>Location:</v-col>
                            <v-col>({{item.locationX}}, {{item.locationY}})</v-col>
                        </v-row>
                    </v-col>    
                </v-row>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>

      <!-- Pagination Controls -->
      <v-card-actions class="text-center">
        <v-container class="pb-0">
            <v-btn 
                @click="prevPage" 
                :disabled="currentPage === 0"
            >
                <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
            <span>{{ currentPage + 1 }}</span>
            <v-btn @click="nextPage" :disabled="currentPage === pages.length - 1">
                <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
        </v-container>
      </v-card-actions>

    </v-card>
  </v-container>
</template>

<style>
.my-title {
    white-space: nowrap;
    text-align: center;
}
.prediction-number {
    white-space: nowrap;
    text-align: center;
    font-size: 10px;
    padding-left: 2px;
}
</style>

<script>
export default {
  data() {
    return {
      data: [
        {id: 1, confidence: '43.23', type: 'Fastball', speed: 98.21, locationX: 55, locationY: 79},
        {id: 2, confidence: '25.90', type: 'Curveball', speed: 86.64, locationX: 12, locationY: 24},
        { id: 3, confidence: '7.04', type: 'Slider', speed: 82.27, locationX: 78, locationY: 38},
      ],
      itemsPerPage: 1,
      currentPage: 0,
      pages: [],
    };
  },
  created() {
    this.pages = Array.from({ length: Math.ceil(this.data.length / this.itemsPerPage) }, (_, index) => {
      const startIndex = index * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.data.slice(startIndex, endIndex);
    });
  },
  computed: {
    currentData() {
      return this.pages[this.currentPage] || [];
    },
  },
  methods: {
    prevPage() {
      this.currentPage = Math.max(this.currentPage - 1, 0);
    },
    nextPage() {
      this.currentPage = Math.min(this.currentPage + 1, this.data.length - 1);
    },
  },
};
</script>
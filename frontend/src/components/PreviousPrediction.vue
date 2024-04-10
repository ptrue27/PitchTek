<template>
  <div class="custom-component">
    <div class="text-table">
      <table>
        <tr>
          <th>Attribute</th>
          <th>Value</th>
        </tr>
        <tr v-for="(item, index) in tableData" :key="index">
          <td>{{ item.attribute }}</td>
          <td>{{ item.value }}</td>
        </tr>
      </table>
    </div>
    <div class="image-container">
      <img :src=imageURL alt="Image" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      image_path: "default_heat_map.jpg",
      /*curr_pitcher_name: "",
      curr_pitcher_id: "NA",
      currentimage : 0,
      data: [
        {id: 1, confidence: 'NA', type: 'NA', speed: 'NA', locationX: 'NA', locationY: 'NA'},
        {id: 2, confidence: 'NA', type: '', speed: 'NA', locationX: 'NA', locationY: 'NA'},
        {id: 3, confidence: '7.04', type: 'Slider', speed: 82.27, locationX: 78, locationY: 38},
      ],
      itemsPerPage: 1,
      currentPage: 0,
      pages: [],*/
    };
  },
    computed: {
    imageURL(){
      return require("@/assets/heat_maps/" + this.image_path)
    },
  },
};
</script>

<style>
.custom-component {
  display: flex;
}

.image-container {
  flex: 1;
}

.text-table {
  flex: 2;
}

table {
  width: 100%;
}

th, td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
}
</style>

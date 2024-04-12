<template>
  <div class="strikezone-container">
    <div v-for="(row, rowIndex) in grid" :key="rowIndex" class="strikezone-row">
      <div
        v-for="(cell, colIndex) in row"
        :key="colIndex"
        class="strikezone-cell"
        :class="{ 'active': cell }"
        @click="toggleCell(rowIndex, colIndex)"
      ></div>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        grid: [
          [false, false, false],
          [false, false, false],
          [false, false, false]
        ]
      };
    },
    methods: {
      toggleCell(rowIndex, colIndex) {
        for (let row = 0; row < this.grid.length; row++) {
          for (let col = 0; col < this.grid[row].length; col++) {
            this.grid[row][col] = false;
          }
        }
        this.grid[rowIndex][colIndex] = true;
      }
    }
  };
</script>

<style scoped>
  .strikezone-container {
    display: flex;
    flex-direction: column;
  }

  .strikezone-row {
    display: flex;
  }

  .strikezone-cell {
    width: 50px;
    height: 75px;
    background-color: #EEEEEE;
    border: 1px solid black;
  }

  .strikezone-cell.active {
    background-color: #43A047;
  }
</style>
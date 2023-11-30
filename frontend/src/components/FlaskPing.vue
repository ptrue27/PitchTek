<template>
    <div>
        <v-btn @click="getMessage"></v-btn>
        <p>{{ msg }}</p>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      msg: 'Hi',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/ping';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {

          console.error(error);
        });
    },
  },
};
</script>
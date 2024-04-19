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
      msg: 'ping',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://' + this.$store.state.host + '/ping';
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
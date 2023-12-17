import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import router from './router'
import store from './store'

// Import 'mitt' to communicate between components
import mitt from 'mitt';
const emitter = mitt();

loadFonts()

const app= createApp(App)
                                  .use(vuetify)
                                  .use(router)
                                  .use(store)
                                  //.mount('#app')

app.config.globalProperties.emitter = emitter;
app.mount('#app');
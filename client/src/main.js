import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./assets/main.css";
import vClickOutside from "click-outside-vue3"

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App);

app.use(vClickOutside)
app.use(ElementPlus)

app.use(router);

app.mount("#app");

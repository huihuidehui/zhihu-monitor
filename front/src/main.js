import Vue from 'vue'
import App from './App.vue'
import router from "./router";
import store from "./store";
import VCharts from 'v-charts'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import "./assets/css/base.css";
// import { VeLine } from 'v-charts-v2/lib/index.esm'
// import VeLine from 'v-charts-v2/lib/line'

// Vue.component(VeLine.name, VeLine)

// import { Button,Table,TableColumn } from "element-ui";
// Vue.use(Button);
// Vue.use(Table);
// Vue.use(TableColumn);
Vue.use(ElementUI)
Vue.config.productionTip = false

Vue.use(VCharts)

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')

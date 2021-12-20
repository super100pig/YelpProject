import Vue from 'vue'
import App from './App.vue'
import 'element-ui/lib/theme-chalk/index.css'
import ElementUI from 'element-ui'
import router from "@/router"
import echarts from 'echarts'
import axios from 'axios'

Vue.config.productionTip = false

Vue.prototype.$echarts = echarts;
Vue.prototype.$axios = axios;

Vue.use(ElementUI);

new Vue({
  el: '#app',
  router,
  render: h => h(App),
}).$mount('#app')

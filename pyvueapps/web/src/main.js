// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import axios from 'axios'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import Antd from 'ant-design-vue';
console.log(Antd);
import App from './App'
import 'ant-design-vue/dist/antd.css';
//import 'ant-design-vue/dist/reset.css';
//import router from './router'
import router from './router/index_demo'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './assets/font-awesome/css/font-awesome.css'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import * as echarts from 'echarts'
import './assets/comm/api.js'


Vue.prototype.$echarts = echarts

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(ElementUI);
Vue.use(Antd);

Vue.config.productionTip = false

router.beforeEach((to, from, next) => {
    console.log(from, '->', to)
    try {
        if (to.path == '/eqAdminIndex') {
            router.replace({
                path: '/eqAdminIndex/game'
            })
        }
        if (to.path == '/eqmo') {
            router.replace({
                path: '/eqmo/live'
            })
        }
    } catch (error) {
        console.log(error)
    }
    next();
})

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    components: { App },
    template: '<App/>'
})
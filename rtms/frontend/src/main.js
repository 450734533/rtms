/* eslint-disable */
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App2'
import router from './router'
import ElementUI from 'element-ui'
import './assets/theme/index.css'
import './assets/common.css'

import axios from './http'

Vue.use(ElementUI)

router.beforeEach((to, from, next) => {
  if (to.path == '/login') {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
  }
  let token = localStorage.getItem('token');
  console.log(token)
  console.log('21211121')
  if (!token && to.path != '/login' && to.path != '/register') {
    next({ path: '/login' })
  } else {
    next()
  }
})


Vue.prototype.$axios = axios;

window.vm = new Vue({
  el: '#app',
  axios,
  router,
  template: '<App/>',
  components: { App }
})

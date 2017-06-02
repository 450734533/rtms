import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)


const router  =new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      component(cb){
        require.ensure([], () => {
          cb(require('../modules/app/pages/Login'))
        })
      }
    },
    {
      path: '/register',
      name: 'register',
      component(cb){
        require.ensure([], () => {
          cb(require('../modules/app/pages/Register'))
        })
      }
    },
    {
      path: '/',
      name: 'dashboard',
      component(cb){
        require.ensure([], () => {
          cb(require('../App'))
        })
      },
      children: [
        ...require('@/modules/app/routes').default
      ]
    }
  ],
})


export default router //关联main.js中的router

/**
 * Created by 80160405 on 2017/4/20.
 */
export default [
  {
    path: '/manifests1',
    name: '新增用例',
    component(cb){
      require.ensure([], () => {
        cb(require('./pages/manifests1'))
      })
    },
    meta: {
      breadcrumb: [

        {
          name: '新建用例'
        }
      ]
    }
  },
  {
    path: '/plan',
    name: '新建计划',
    component(cb){
      require.ensure([], () => {
        cb(require('./pages/plan'))
      })
    },
    meta: {
      breadcrumb: [

        {
          name: '新建计划'
        }
      ]
    }
  },
  {
    path: '/flow',
    name: '新增流程',
    component(cb){
      require.ensure([], () => {
        cb(require('./pages/flow'))
      })
    },
    meta: {
      breadcrumb: [

        {
          name: '新增流程'
        }
      ]
    }
  },
  {
    path: '/auth_s',
    name: '新增鉴权',
    component(cb){
      require.ensure([], () => {
        cb(require('./pages/auths'))
      })
    },
    meta: {
      breadcrumb: [

        {
          name: '新增鉴权'
        }
      ]
    }
  },
  {
      path: '/plan/create',
      name: '计划 新建',
      component(cb){
        require.ensure([], () => {
          cb(require('./pages/plan/create'))
        })
      },
      meta:{
        breadcrumb:[
          {
            name: '计划'
          },
          {
            name: '新建 计划'
          }
        ]
      }
    },
    {
      path: '/plan/list',
      name: '计划 列表',
      component(cb){
        require.ensure([], () => {
          cb(require('./pages/plan/list'))
        })
      },
      meta:{
        breadcrumb:[
          {
            name: '计划'
          },
          {
            name: '计划 列表'
          }
        ]
      }
    },
    {
      path: '/plan/task',
      name: '结果列表',
      component(cb){
        require.ensure([], () => {
          cb(require('./pages/plan/task'))
        })
      },
      meta:{
        breadcrumb:[
          {
            name: '计划'
          },
          {
            name: '结果 列表'
          }
        ]
      }
    }
]


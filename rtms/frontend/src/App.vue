
<template>
  <div id="app" class="h100">
    <div id="header" class="h100">
      <router-link to="/">
        <img class="logo" src="./assets/main/images/oppo_logo.png">
      </router-link>
    </div>
    <el-row class="h100">
      <el-col class="h100" :span="4">
        <el-menu class="h100" :default-active="$route.path" :router="true">
          <el-menu-item index="/">信息流自动化</el-menu-item>
          <el-submenu index="/1">
            <template slot="title">测试</template>
            <el-menu-item index="/manifests1">新增用例</el-menu-item>
            <el-menu-item index="/plan">新建计划</el-menu-item>
            <el-menu-item index="/flow">新增流程</el-menu-item>
            <el-menu-item index="/auth_s">新增鉴权</el-menu-item>
          </el-submenu>
            <el-submenu index="/2">
            <template slot="title">测试计划</template>
            <el-menu-item index="/plan/create">新建计划</el-menu-item>
              <el-menu-item index="/plan/list">计划列表</el-menu-item>
              <el-menu-item index="/plan/task">执行结果</el-menu-item>
            </el-submenu>
        </el-menu>
      </el-col>
      <el-col class="h100" :span="20" id="app-container">
        <div class="content-inner">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item v-for="(item, i) in $route.meta.breadcrumb" :key="i" :to="item.to">
              {{item.name}}
            </el-breadcrumb-item>
          </el-breadcrumb>
          <div style="height: 20px;"></div>
          <router-view></router-view>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import {Loading} from 'element-ui'
  export default {
    name: 'app',
    data() {
      return {
        username: localStorage.username
      }
    },
    methods: {},
    created: function () {
      // this.$loading({fullscreen: true, target: '#app-container', text: '正在加载...'})
    },
    components: {
      'op-badge': require('@/components/badge')
    }
  }
</script>

<style>

  #app {
    padding-top: 60px;
    overflow-x: hidden;
  }

  #header {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    height: 60px;
    background: #32a77e;
    z-index: 9;
  }

  #app-container {
    position: relative;
  }

  .logo {
    margin-top: 20px;
    margin-left: 40px;
  }

  .header-right {
    float: right;
    margin: 0;
    padding: 0;
    font-size: 14px;
  }

  .msg {
    display: inline-block;
    position: relative;
    line-height: 1.64;
  }

  .header-right li {
    display: inline-block;
    vertical-align: middle;
    padding: 0 40px;
    line-height: 60px;
    color: #fff;
  }

  .header-right li a {
    color: inherit;
  }

  .el-dropdown-link {
    color: #fff;
  }

  #nav {
    position: absolute;
    left: 0;
    top: 60px;
    width: 100px;
  }

  #nav .el-menu {
    height: 100%;
  }

  .content-inner {
    padding: 30px 20px;
  }
</style>

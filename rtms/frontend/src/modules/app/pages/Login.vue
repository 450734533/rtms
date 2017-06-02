<template>
  <el-row :gutter="20">
    <el-col :span="4" :offset="10">
      <el-form :model="loginForm" :rules="rules2" ref="loginForm" label-position="left" label-width="0px" class="demo-ruleForm login-container">
      <h3 class="title">ITMS登录</h3>
      <el-form-item prop="account">
        <el-input type="text" v-model="loginForm.account" auto-complete="off" placeholder="账号"></el-input>
      </el-form-item>
      <el-form-item prop="checkPass">
        <el-input type="password" v-model="loginForm.checkPass" auto-complete="off" placeholder="密码"></el-input>
      </el-form-item>
      <el-form-item style="width:100%;">
        <el-button type="primary" @click.native.prevent="login" :loading="logining">登录</el-button>
        <el-button type="primary" @click.native.prevent="register">注册</el-button>
      </el-form-item>
    </el-form>
    </el-col>
  </el-row>
</template>

<script>
  import axios from 'axios';
  export default {
    data() {
      return {
        logining: false,
        loginForm: {
          account: '',
          checkPass: ''
        },
        rules2: {
          account: [
            { required: true, message: '请输入账号', trigger: 'blur' }
          ],
          checkPass: [
            { required: true, message: '请输入密码', trigger: 'blur' }
          ]
        }
      };
    },
    methods: {
      handleReset2() {
        this.$refs.loginForm.resetFields();
      },
      login() {
        this.$refs.loginForm.validate((valid) => {
          if (valid) {
            this.logining = true;
            var loginParams = { username: this.loginForm.account, password: this.loginForm.checkPass };
            var _this = this;
            axios.post("http://172.17.160.36:8000/api-token-auth/", loginParams).then(
              function (response) {
                _this.logining = false;
                var res = response.data;
                if ( !res.status ){
                  _this.$message({
                    message: 'Unable to log in with provided credentials',
                    type: 'error'
                  })
                } else {
                  localStorage.setItem('token', res.token);
                  _this.$router.push({ path: '/' });
                }
              }
            ).catch(function (error) {
              this.$message({
                message: 'error',
                type: 'error'
              })
            })
          }
        })
      },
      register() {
        this.$router.push({ path: '/register' })
      }
    }
  }


</script>

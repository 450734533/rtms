<template>
  <el-row :gutter="20">
    <el-col :span="8" :offset="8">
      <el-form :model="RegisterForm" :rules="rules" ref="RegisterForm" label-width="100px">
      <h3 class="title">RTMS注册</h3>
      <el-form-item label="工号" prop="username">
        <el-input v-model="RegisterForm.username"></el-input>
      </el-form-item>
      <el-form-item label="姓名" prop="first_name">
        <el-input v-model="RegisterForm.first_name"></el-input>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="RegisterForm.email"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="pass">
        <el-input type="password" v-model="RegisterForm.pass"></el-input>
      </el-form-item>
      <el-form-item label="密码确认" prop="checkPass">
        <el-input type="password" v-model="RegisterForm.checkPass"></el-input>
      </el-form-item>
      <el-form-item style="width:100%;">
        <el-button type="primary" @click.native.prevent="register" :loading="logining">注册</el-button>
        <el-button @click="resetForm('RegisterForm')">重置</el-button>
      </el-form-item>
    </el-form>
    </el-col>
  </el-row>
</template>
<script>
//  import { requestLogin } from '../../../api/api';

  import axios from 'axios';
  export default {
    data() {
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (this.RegisterForm.checkPass !== '') {
            this.$refs.RegisterForm.validateField('checkPass');
          }
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.RegisterForm.pass) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
      return {
        logining: false,
        RegisterForm: {
          username: '',
          first_name: '',
          pass: '',
          checkPass: '',
          email: ''
        },
        rules: {
          username: [
            { required: true, message: '请输入账号', trigger: 'blur' }
          ],
          email: [
            { required: true, message: '请输入邮箱', trigger: 'blur' },
            { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur,change' }
          ],
          first_name: [
            { required: true, message: '请输入姓名', trigger: 'blur' }
          ],
          pass: [
            { validator:validatePass , trigger: 'blur' }
          ],
          checkPass: [
            { validator:validatePass2, trigger: 'blur' }
          ],
        }
      };
    },
    mounted: function () {
        window.register = this;
    },
    methods: {
      register () {
        this.$refs.RegisterForm.validate((valid) => {
            if (valid) {
              let _url = 'http://172.17.160.36/users/register/';
              axios.post(_url, this.RegisterForm).then(response=>{
                if (response.status===201) {
                  this.$message({
                      message: '注册成功，请联系管理员添加权限',
                      type: 'success',
                      duration: 5000
                  });
                  this.$router.push({ path: '/login' });
                }
              }).catch(function (error) {
                register.$message({
                  message: '注册失败，已存在该用户',
                  type: 'error'
                })
              });
            }
        })
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      }
    }
  }

</script>

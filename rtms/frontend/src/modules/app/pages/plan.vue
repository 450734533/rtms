<template>
  <el-row>
    <el-col :span="6">
      <el-input placeholder="输入关键字进行过滤" v-model="filterText"></el-input>
      <el-tree
        :filter-node-method="filterNode"
        class="projectTree"
        :data="groups"
        show-checkbox
        node-key="id"
        ref="tree"
        @check-change="handleCheckChange"
        highlight-current
        check-strictly
        :props="defaultProps"
     >
      </el-tree>
    </el-col>
    <el-col :span="18">
      <el-tabs v-model="activeName">
        <el-tab-pane label="鉴权key值" name="key">
          <el-card class="box-card">
            <el-form :model="authForm" :rules="addFormRules" ref="authForm">
              <el-table :data="planList" highlight-current-row
                        style="width: 100%" border v-model="authForm.authCase">
                <el-table-column type="index" width="60">
                </el-table-column>
                <el-table-column prop="name" label="名称">
                </el-table-column>
              </el-table>
              <el-form-item v-for="(auth, index) in authForm.auths" :label="'鉴权' + index">
                <el-col :span="5">
                  <el-input v-model="auth.authKey" placeholder="Key"></el-input>
                </el-col>
                <el-col :span="10" :offset="1">
                  <el-input v-model="auth.authValue" placeholder="Value"></el-input>
                </el-col>
                <el-col :span="2" :offset="1">
                  <el-button type="danger" icon="delete" @click.prevent="removeAuth(auth)"></el-button>
                </el-col>
              </el-form-item>
            </el-form>
            <el-button @click="addAuth">新增</el-button>
            <el-button type="primary" @click.native="editSubmit" :loading="editLoading">保存</el-button>
          </el-card>
        </el-tab-pane>
        <el-tab-pane label="鉴权脚本" name="script">
          <editor v-model="content" @init="editorInit();" lang="python" theme="github" width="100%"
                  height="600"></editor>
          <el-button type="primary" @click.native="editSubmit" :loading="editLoading">保存</el-button>
        </el-tab-pane>
      </el-tabs>
    </el-col>
  </el-row>
</template>

<script>
  export default{
    data(){
      return {
        replace: '',
        planList: [],
        filterText: '',
        groups: [],
        currentId: '', //鼠标选择tree中的节点
        activeName: 'key',
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        addFormRules: {
          auths: [
            {required: true, message: '请输入模块名称', trigger: 'blur'}
          ]
        },
        content: '',
        authForm: {
          auths: [{
            authKey: '',
            authValue: ''
          }],
          authCase: ''
        },
        editLoading: false
      }
    },
    mounted: function () {
      this.treeView();
      window.xxx = this;
    },
    methods: {
      filterNode(value, data) {
        if (!value) return true;
        return data.label.indexOf(value) !== -1;
      },
      treeView: function () {
        this.$axios.get('/api/case/tree/').then(response => {
          var res = response.data;
          if (res) {
            this.groups = res.tree;
          }
        });

      },
      handleDel: function (index, row) {
        let url = '/api/case/' + row.id + '/';
        this.$axios.delete(url).then(response => {
          this.listLoading = false;
          this.$message({
            message: '删除成功',
            type: 'success'
          });
          this.projectView()
        })
        ;
      },
      addAuth() {
        this.authForm.auths.push({
          authKey: '',
          authValue: ''
        });
      },
      removeAuth(item) {
        let index = this.authForm.auths.indexOf(item);
        if (index !== -1) {
          this.authForm.auths.splice(index, 1)
        }
      },
      editSubmit: function () {
        this.$confirm('确认提交吗？', '提示', {}).then(() => {
          this.editLoading = true
          let para = Object.assign({}, this.authForm)
          para.auths = JSON.stringify(para.auths)
          console.log('aaasss')
          console.log(para)
          this.$axios.post('/api/auth/', para).then(response => {
            this.editLoading = false;
            this.$message({
              message: '保存成功',
              type: 'success'
            });
          });
        });
      },
      getID(x) {
        return x.id
      },
      handleCheckChange(data, node, self) {
        let modules = this.$refs.tree.getCheckedNodes(true)
        let moduleIds = modules.map(this.getID)
        let cases = JSON.stringify(moduleIds)
        this.authForm.authCase = cases
        if (moduleIds.length === 0) {
          this.planList = [];
        } else {
          let _this = this;
          let planList = [];
          moduleIds.forEach(function (item) {
            _this.currentId = String(item);
            let url = '/api/case/' + String(item) + '/';
            _this.$axios.get(url).then(response => {
              planList = planList.concat(response.data)
              _this.planList = planList;
            });
          })
        }
      },
      editorInit: function () {
        require('brace/mode/python');
        require('brace/theme/github');
      }
    },
    components: {
      editor: require('vue2-ace-editor'),
    },
  }
</script>
<style>
  .el-input {
    margin-bottom: 22px;
  }
</style>

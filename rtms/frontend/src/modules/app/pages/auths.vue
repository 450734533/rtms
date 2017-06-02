<template>
  <el-row>
    <el-col :span="24" class="toolbar" style="margin-bottom: 3px;padding:3px 10px;background:#f3f9f7">
      <el-form :inline="true" :model="filters">
        <el-form-item>
          <el-input v-model="filters.name"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" v-on:click="projectView" placeholder="请输入内容">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAdd">新增</el-button>
        </el-form-item>
      </el-form>
    </el-col>

    <el-table :data="projectList" highlight-current-row v-loading="listLoading"
              @selection-change="selsChange" style="width: 100%" border>
      <el-table-column type="selection" width="55">
      </el-table-column>
      <el-table-column type="index" width="60">
      </el-table-column>
      <el-table-column prop="name" label="名称">
      </el-table-column>
      <el-table-column prop="auth_jar" label="文件">
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template scope="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!--新增界面-->
    <el-dialog title="新增" v-model="addFormVisible" :close-on-click-modal="false" size="small">
      <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
        <el-form-item label="用例名称" prop="name">
          <el-input v-model="addForm.name" placeholder="请输入用例名称"></el-input>
        </el-form-item>
        <el-upload ref="auth_jar" name="auth_jar" action="" :auto-upload="false" :multiple="false"
                   :file-list="auth_jar">
          <el-button slot="trigger" size="small" type="primary" @click="clearFileList()">选择python文件<i
            class="el-icon-upload el-icon--right"></i></el-button>
          <el-button style="margin-left: 10px;" size="small" type="success" @click.native="editSubmitZip" :loading="editLoading1">上传到服务器</el-button>
        </el-upload>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="addFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
      </div>
    </el-dialog>

    <!--编辑界面-->
    <el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false" size="small">
      <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
        <el-form-item label="用例名称" prop="name">
          <el-input v-model="addForm.name" placeholder="请输入用例名称"></el-input>
        </el-form-item>
        <el-upload ref="auth_jar" name="auth_jar" action="" :auto-upload="false" :multiple="false"
                   :file-list="auth_jar">
          <el-button slot="trigger" size="small" type="primary" @click="clearFileList()">选择python文件<i
            class="el-icon-upload el-icon--right"></i></el-button>
          <el-button style="margin-left: 10px;" size="small" type="success" @click.native="editSubmitZip" :loading="editLoading1">上传到服务器</el-button>
        </el-upload>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="addFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
      </div>
    </el-dialog>
    <!--工具条-->
    <el-col :span="24" class="toolbar">
      <el-button type="danger" @click="batchRemove" :disabled="sels.length===0">批量删除</el-button>
      <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="15" :total="total"
                     style="float:right;">
      </el-pagination>
    </el-col>
  </el-row>
</template>
<script type="text/ecmascript-6">
  export default{
    data(){
      return {
        auth_jar: [],
        del_file: false,
        projectList: [], //每一项是一个Object
        sels: [],//列表选中列
        total: 0,  //总数
        page: 1,    //第几页
        filters: {    //搜索内容
          name: ''
        },
        listLoading: false,  //列表是否在加载中
        addFormVisible: false,  //新增视图是否出来
        editFormVisible: false,  //编辑视图是否出来
        addLoading: false,    //新增视图是否在加载中
        editLoading: false,   //编辑视图是否在加载中
        editLoading1: false,
        executeFormVisible: false,
        addFormRules: {       //效验输入是否合法
          name: [
            {required: true, message: '请输入鉴权名称', trigger: 'blur'}
          ]
        },
        addForm: {       //新增输入内容，只要输入了就会有更新
          name: '',
          auth_jar: ''
        },
        activeNames: ['1', '2', '3', '4', '5'],
        debugResult: {
          'url': '',
          'header': '',
          'args': '',
          'status_code': '',
          'result': '',
          'debug': '',
          'except': '',
          'error': ''
        }

      }
    },
    mounted: function () {
      this.projectView();
      window.xxx = this;
    },
    methods: {
      projectView: function () {
        let para = {
          page: this.page,
          name: this.filters.name
        };
        this.listLoading = true;
        this.$axios.get("/api/auth_s/", {params: para}).then(response => {
          this.total = response.data.count;
          this.projectList = response.data.results;
          this.listLoading = false;
        })
        ;
      },
      handleCurrentChange(val) {
        this.page = val;
        this.projectView();
      },
      addSubmit: function () {
        this.$refs.addForm.validate((valid) => {
            if (valid) {
              this.$confirm('确认提交吗？', '提示', {}).then(() => {
                this.addLoading = true;
                let para = Object.assign({}, this.addForm);
                this.$axios.post('/api/auth_s/', para).then(response => {
                  this.addLoading = false;
                  this.$message({
                    message: '提交成功',
                    type: 'success'
                  });
                  this.addFormVisible = false;
                  this.$refs['addForm'].resetFields()
                  this.projectView();
                })
                ;

              })
              ;
            }
          }
        )
        ;
      },
      editSubmitZip: function () {
        this.$confirm('确认提交吗？', '提示', {}).then(() => {
          this.editLoading1 = true;
          var form = new FormData()
          if (this.$refs.auth_jar.uploadFiles[0]) {
            if (this.$refs.auth_jar.uploadFiles[0].raw) {
              this.auth_jar[0] = this.$refs.auth_jar.uploadFiles[0].raw;
              form.append('auth_jar', this.auth_jar[0]);
            } else {
              this.editLoading1 = false;
              this.$message({
                message: '文件无变化，无需修改',
                type: 'success'
              });
              return
            }
          } else {
            this.del_file = true;
            form.append('del_file', this.del_file);
          }
          let url = '/api/auth_s/';
          this.$axios.post(url, form, {
            method: 'post',
            headers: {'Content-Type': 'multipart/form-data'}
          }).then(response => {
            this.editLoading1 = false;
            this.addForm.auth_jar = response.data.file_path
            this.$message({
              message: '修改成功',
              type: 'success'
            });
          });
        });
      },
      clearFileList() {
        this.$refs.auth_jar.clearFiles();
        this.auth_jar = [];
      },
      handleDel: function (index, row) {
        this.$confirm('确认删除该记录吗?', '提示', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          let url = '/api/auth_s/' + row.id + '/';
          this.$axios.delete(url).then(response => {
            this.listLoading = false;
            this.$message({
              message: '删除成功',
              type: 'success'
            });
            this.projectView()
          })
          ;
        })
      },
      handleAdd: function () {
        this.addFormVisible = true;
        this.addForm = {
          name: '',
          auth_jar: ''
        };
      },
      handleEdit: function (index, row) {
        this.editFormVisible = true;
        this.addForm = Object.assign({}, row);                // 复制Object=row
      },
      editSubmit: function () {
        this.$refs.addForm.validate((valid) => {
            if (valid) {
              this.$confirm('确认提交吗？', '提示', {}).then(() => {
                this.editLoading = true;
                let para = Object.assign({}, this.addForm);
                let url = '/api/auth_s/' + para['id'] + '/';
                this.$axios.put(url, para).then(response => {
                  this.editLoading = false;
                  this.$message({
                    message: '修改成功',
                    type: 'success'
                  });
                  this.editFormVisible = false;
                  this.projectView();
                })
                ;
              })
              ;
            }
          }
        )
        ;
      },
      querySearch(queryString, cb) {
        this.$axios.get('/api/auth_s/').then(response => {
          var results = response.data.results;
          cb(results);
        })
        ;
      },
      selsChange: function (sels) {
        this.sels = sels;
      },
      //批量删除
      batchRemove: function () {
        var ids = this.sels.map(item => item.id
        ).join(',');
        this.$confirm('确认删除选中记录吗？', '危险', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          this.$axios.get('/api/auth_s/batch/?id=' + ids).then(response => {
            this.listLoading = false;
            var status = response.data.status;
            if (status) {
              this.$message({
                message: '批量删除成功',
                type: 'success'
              });
              this.projectView();
            } else {
              var message = response.data.message;
              this.$message({
                message: message,
                type: 'error'
              })
            }
          })
          ;
        }).catch(() => {
          }
        )
        ;
      }
    }
  }

</script>

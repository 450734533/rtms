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
      <el-table-column prop="remark" label="备注">
      </el-table-column>
      <el-table-column prop="retId" label="retId" width="80">
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template scope="scope">
          <el-button type="success" size="small" @click="handleExecute(scope.$index, scope.row)">
            执行
          </el-button>
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
        <el-form-item label="url" prop="url">
          <el-input v-model="addForm.url" placeholder="请输入url"></el-input>
        </el-form-item>
        <el-form-item label="cookies" prop="cookies">
          <el-input v-model="addForm.cookies" placeholder="请输入cookies,非必填"></el-input>
        </el-form-item>
        <el-form-item label="header" prop="header">
          <el-input v-model="addForm.header" placeholder="请输入header" type="textarea"
                    rows=4></el-input>
        </el-form-item>
        <el-form-item label="boby" prop="boby">
          <el-input v-model="addForm.boby" placeholder="请输入boby" type="textarea"
                    rows=10></el-input>
        </el-form-item>
        <el-form-item label="期望值" prop="expect">
          <el-input v-model="addForm.expect" placeholder="请输入expect"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="addForm.remark"></el-input>
        </el-form-item>
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
        <el-form-item label="url" prop="url">
          <el-input v-model="addForm.url" placeholder="请输入url"></el-input>
        </el-form-item>
        <el-form-item label="cookies" prop="cookies">
          <el-input v-model="addForm.cookies" placeholder="请输入cookies,非必填"></el-input>
        </el-form-item>
        <el-form-item label="header" prop="header">
          <el-input v-model="addForm.header" placeholder="请输入header" type="textarea"
                    rows=4></el-input>
        </el-form-item>
        <el-form-item label="boby" prop="boby">
          <el-input v-model="addForm.boby" placeholder="请输入boby" type="textarea"
                    :autosize="{ minRows: 2, maxRows: 25}"></el-input>
        </el-form-item>
        <el-form-item label="期望值" prop="expect">
          <el-input v-model="addForm.expect" placeholder="请输入expect"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="addForm.remark"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="editFormVisible=false">取消</el-button>
        <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
      </div>
    </el-dialog>

    <el-dialog title="调试" v-model="executeFormVisible" :close-on-click-modal="false"
               :custom-class="debugResult.debug">
      <template v-if="debugResult.except === true">
        <el-alert
          title="执行错误"
          type="error"
          :description="debugResult.error"
          show-icon>
        </el-alert>
      </template>
      <template v-else>
        <el-collapse v-model="activeNames">
          <el-collapse-item title="Uri" name="1">
            <div v-text="debugResult.url"></div>
          </el-collapse-item>
          <el-collapse-item title="Request Headers" name="2">
            <div v-text="debugResult.header"></div>
          </el-collapse-item>
          <el-collapse-item title="Request Data" name="3">
            <div v-text="debugResult.args"></div>
          </el-collapse-item>
          <el-collapse-item title="Status Code" name="4">
            <div v-text="debugResult.status_code"></div>
          </el-collapse-item>
          <el-collapse-item title="Response Result" name="5">
            <div v-text="debugResult.result"></div>
          </el-collapse-item>
        </el-collapse>
      </template>
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
        executeFormVisible: false,
        addFormRules: {       //效验输入是否合法
          name: [
            {required: true, message: '请输入项目名称', trigger: 'blur'}
          ]
        },
        addForm: {       //新增输入内容，只要输入了就会有更新
          name: '',
          url: '',
          cookies: '',
          header: '',
          boby: '',
          remark: '',
          expect: ''

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
        this.$axios.get("/api/case/", para).then(response => {
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
      handleDel: function (index, row) {
        this.$confirm('确认删除该记录吗?', '提示', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
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
      })
      },
      handleAdd: function () {
        this.addFormVisible = true;
        this.addForm = {
          name: '',
          url: '',
          cookies: '',
          header: '',
          boby: '',
          remark: '',
          expect: ''
        };
      },
      handleExecute: function (index, row) {
        this.executeFormVisible = true;
        let url = '/api/case/' + row.id + '/execute/';
        console.log('aaa')
        console.log(url)
        this.$axios.get(url).then(response => {
          this.debugResult.except = response.data.except
        if (this.debugResult.except) {
          this.debugResult.error = response.data.error
        } else {
          this.debugResult.url = response.data.url
          this.debugResult.header = response.data.header
          this.debugResult.args = response.data.args
          this.debugResult.status_code = response.data.status_code
          this.debugResult.result = response.data.result
          this.debugResult.debug = response.data.debug
        }
      })
        ;
      },
      handleEdit: function (index, row) {
        this.editFormVisible = true;
        this.addForm = Object.assign({}, row);                // 复制Object=row
      },
      addSubmit: function () {
        this.$refs.addForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.addLoading = true;
            let para = Object.assign({}, this.addForm);
            this.$axios.post('/api/case/', para).then(response => {
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
      editSubmit: function () {
        this.$refs.addForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editLoading = true;
            let para = Object.assign({}, this.addForm);
            let url = '/api/case/' + para['id'] + '/';
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
        this.$axios.get('/api/case/').then(response => {
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
        ).
        join(',');
        this.$confirm('确认删除选中记录吗？', '危险', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
        this.$axios.get('/api/case/batch/?id=' + ids).then(response => {
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
      }).
        catch(() => {}
        )
        ;
      }
    }
  }

</script>

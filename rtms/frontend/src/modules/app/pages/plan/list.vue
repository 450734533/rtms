<template>
  <el-row>
    <el-col :span="24" class="toolbar" style="margin-bottom: 3px;padding:3px 10px;background:#f3f9f7">
      <el-form :inline="true" :model="filters">
        <el-form-item>
          <el-input v-model.trim="filters.search"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" v-on:click="planView" placeholder="请输入内容">查询</el-button>
        </el-form-item>
      </el-form>
    </el-col>

    <!--table-->
    <el-table :data="planList" highlight-current-row v-loading="listLoading" style="width: 100%" >
      <el-table-column type="index" width="60">
      </el-table-column>
      <el-table-column prop="name" label="名称" width="200">
      </el-table-column>
      <el-table-column prop="create_time" label="创建时间" width="200">
      </el-table-column>
      <el-table-column label="执行方式" width="200">
        <template scope="scope">
          <el-tag :type="scope.row.flag|executeType"
                  close-transition>{{ scope.row.flag | executeMode(scope.row.frikcy, scope.row.execute_time) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="cases_id" label="执行用例" width="200">
      </el-table-column>
      <el-table-column prop="switch" label="开关">
        <template scope="scope">
          <el-button size="small" :type="scope.row.switch|enableType">{{ scope.row.switch | enableText }}
          </el-button>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态">
        <template scope="scope">
          <el-tag :type="scope.row.status|statusType"
                  close-transition>{{ scope.row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="id" label="结果">
        <template scope="scope">
          <router-link :to="{ path: '/plan/task', query: { planId: scope.row.id } }">查看结果</router-link>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="280">
        <template scope="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
          <el-button size="small" type="success" @click="handleRun(scope.$index, scope.row)">执行</el-button>
          <el-button type="danger" size="small" @click="handleDelPlan(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!--编辑-->
    <el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
      <el-form :model="editForm" label-width="90px" ref="editForm" :rules="editFormRules">
        <el-form-item label="名称" prop="name">
          <el-col :span="12">
            <el-input v-model="editForm.name"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="开关" prop="switch">
          <el-switch on-text="" off-text="" v-model="editForm.switch"></el-switch>
        </el-form-item>
        <el-form-item label="执行方式" prop="flag">
          <el-select v-model="editForm.flag">
            <el-option label="待命" value="A"></el-option>
            <el-option label="每天执行" value="B"></el-option>
            <el-option label="间隔周期执行" value="C"></el-option>
          </el-select>
        </el-form-item>
        <template v-if="editForm.flag==='B'">
          <el-form-item label="执行时间">
            <el-time-picker
              type="fixed-time"
              format="HH:mm"
              v-model="editForm.execute_time"
              placeholder="选择执行时间">
            </el-time-picker>
          </el-form-item>
        </template>
        <template v-if="editForm.flag==='C'">
          <el-form-item label="执行周期" prop="flag">
            <el-col :span="8">
              <el-input-number v-model="editForm.frikcy" :min=0></el-input-number>
            </el-col>
            <el-col class="line" :span="2">-</el-col>
            <el-col :span="6">
              <el-select v-model="editForm.unit" placeholder="间隔">
                <el-option label="分钟" value="m"></el-option>
                <el-option label="小时" value="h"></el-option>
                <el-option label="天" value="d"></el-option>
              </el-select>
            </el-col>
          </el-form-item>
        </template>

        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span style="line-height: 36px;">已选用例</span>
          </div>
          <el-table :data="chooseCaseData" border tooltip-effect="dark" style="width: 100%">
            <el-table-column type="index" width="60">
            </el-table-column>
            <el-table-column prop="name" label="名称">
            </el-table-column>
            <el-table-column prop="remark" label="备注">
            </el-table-column>
            <el-table-column label="操作" width="80">
              <template scope="scope">
                <el-button type="danger" icon="delete" size="small" @click="handleDelCase(scope.row)"></el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="editFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
      </div>
    </el-dialog>

    <!--工具条-->
    <el-col :span="24" class="toolbar">
      <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="15" :total="total"
                     style="float:right;">
      </el-pagination>
    </el-col>

  </el-row>
</template>

<script>
  export default {
    data () {
      return {
        planList: [],
        total: 0,
        page: 1,
        filters: {
          search: ''
        },
        editFormRules: {
          name: [
            {required: true, message: '请输入计划名称', trigger: 'blur'}
          ]
        },
        editFormVisible: false,
        listLoading: false,
        editLoading: false,
        editForm: {
          name: '',
          flag: '',   //B按天执行，C间隔周期执行
          execute_time: '',
          frikcy: 0,   //执行周期
          unit: '',   //间隔时间,不需要保存在数据库
          switch: true
        },
        chooseCaseData: []
      }
    },
    mounted: function () {
      this.planView();
      window.planList = this;
    },
    methods: {
      planView: function () {
        let para = {
          page: this.page,
          search: this.filters.search
        };
        this.listLoading = true;
        this.$axios.get('/api/plans/', {params: para}).then(response => {
          this.total = response.data.count;
          this.planList = response.data.results;
          this.listLoading = false;
        });
      },
      handleCurrentChange(val) {
        this.page = val;
        this.planView();
      },
      handleDelPlan(index, row) {
        this.$confirm('确认删除该计划吗?', '提示', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          let url = '/api/plans/' + row.id + '/';
          this.$axios.delete(url).then(response => {
            this.listLoading = false;
            this.$message({
              message: '删除成功',
              type: 'success'
            });
            this.editLoading = false
            this.planView()
          });
        })
      },
      handleRun(index, row){
        this.$confirm('立即执行一次本计划?', '提示', {
          type: 'warning'
        }).then(() => {
          let url = '/api/plans/' + row.id + '/execute/';
          this.$axios.get(url).then(response => {
            this.$router.push({path: '/plan/task'});
          })
        })
      },
      handleEdit(index, row){
        console.log(1212343)
        console.log(row)
        this.editForm.name = row.name
        this.editForm.switch = row.switch
        this.editForm.flag = row.flag
        this.editForm.id = row.id
        let frikcy = row.frikcy;
        if (frikcy % 60 === 0) {
          frikcy = frikcy / 60;
          this.editForm.unit = 'h'
        } else {
          this.editForm.unit = 'm'
        }
        this.editForm.frikcy = frikcy
        let now = new Date()
         //execute_time is string need convert to datetime
        if (row.execute_time) {
          this.editForm.execute_time = new Date(2017, 4, 10, row.execute_time.split(':')[0], row.execute_time.split(':')[1])
        } else {
          this.editForm.execute_time = ''
        }
        let url = '/api/plans/' + row.id + '/cases/'
        this.$axios.get(url).then(response => {
          this.chooseCaseData = response.data.cases;
        })
        this.editFormVisible = true;
      },
      handleDelCase: function (row) {
        let index = this.chooseCaseData.indexOf(row);
        this.chooseCaseData.splice(index, 1)
      },

      editSubmit: function () {
        this.$refs.editForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editLoading = true;
              let para = Object.assign({}, this.editForm);
              let executeTime = para.execute_time;
              let unit = para.unit;
              delete para.execute_time;
              delete para.unit;
              if (unit === 'h') {
                para.frikcy = para.frikcy * 60
              } else if (unit === 'd') {
                para.frikcy = para.frikcy * 24 * 60
              }
              para.execute_time = executeTime.getHours() + ':' + executeTime.getMinutes()

              let flows = [];
              this.chooseCaseData.forEach(function (item) {
                flows.push(item.id)
              })
              para.cases_id = JSON.stringify(flows)
              let url = '/api/plans/' + para['id'] + '/';
              this.$axios.put(url, para).then(response => {
                this.editLoading = false;
                this.$message({
                  message: '修改计划成功',
                  type: 'success'
                });
                this.editFormVisible = false;
                this.planView();
              });
            });
          }
        });
      },
    },

    filters: {
      executeMode: function (value, frikcy, execute_time) {
        if (value === 'A') {
          return '待命'
        } else if (value === 'B') {
          return '每天执行(' + execute_time + ')'
        } else if (value === 'C') {
          return '间隔周期执行(' + frikcy + '分钟)'
        }
      },
      executeType: function (value) {
        if (value === 'A') {
          return 'success'
        } else if (value === 'B') {
          return 'warning'
        } else if (value === 'C') {
          return 'primary'
        }
      },
      enableText: function (value) {
        if (value) {
          return '开启'
        } else {
          return '关闭'
        }
      },
      enableType: function (value) {
        if (value) {
          return 'success'
        } else {
          return 'danger'
        }
      },
      statusType: function (value) {
        if (value === 'Ready') {
          return 'success'
        } else if (value === 'Running') {
          return 'danger'
        }
      }
    }
  }
</script>

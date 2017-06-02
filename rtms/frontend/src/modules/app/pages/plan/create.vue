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
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span style="line-height: 36px;">候选用例</span>
          <el-button type="primary" style="float: right;" @click="handleAdd"><i class="el-icon-plus el-icon--left"></i>新建计划
          </el-button>
        </div>
        <el-table
          :data="planList"
          ref="table"
          border
          tooltip-effect="dark"
          style="width: 100%">
          <el-table-column type="index" width="60">
          </el-table-column>
          <el-table-column prop="name" label="名称">
          </el-table-column>
          <el-table-column prop="remark" label="备注">
          </el-table-column>
        </el-table>
      </el-card>
    </el-col>

    <el-dialog title="新建计划" v-model="addFormVisible">
      <el-form :model="addForm" label-width="90px" ref="addForm" :rules="addFormRules">
        <el-form-item label="名称" prop="name">
          <el-col :span="6">
            <el-input v-model="addForm.name"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="执行方式" prop="flag">
          <el-select v-model="addForm.flag">
            <el-option label="每天执行" value="B"></el-option>
            <el-option label="间隔周期执行" value="C"></el-option>
          </el-select>
        </el-form-item>
        <template v-if="addForm.flag==='B'">
          <el-form-item label="执行时间">
            <el-time-picker
              type="fixed-time"
              format="HH:mm"
              v-model="addForm.execute_time"
              placeholder="选择执行时间">
            </el-time-picker>
          </el-form-item>
        </template>
        <template v-if="addForm.flag==='C'">
          <el-form-item label="执行周期" prop="flag">
            <el-col :span="6">
              <el-input-number v-model="addForm.frikcy" :min=0></el-input-number>
            </el-col>
            <el-col class="line" :span="1">-</el-col>
            <el-col :span="6">
              <el-select v-model="addForm.unit" placeholder="间隔">
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
                <el-button type="danger" icon="delete" size="small" @click="handleDel(scope.row)"></el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addFormVisible = false">取 消</el-button>
        <el-button type="primary" @click.native="editSubmit" :loading="editLoading">确 定</el-button>
      </div>
    </el-dialog>
  </el-row>
</template>

<script>
  export default{
    data(){
      return {
        planList: [],  //选中的用例
        filterText: '',
        groups: [],   //用例树
        chooseCaseData: [],   // 新建时选中的用例
        currentId: '', //鼠标选择tree中的节点
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        addFormVisible: false,
        addFormRules: {
          auths: [
            {required: true, message: '请输入模块名称', trigger: 'blur'}
          ]
        },
        addForm: {
          name : '',
          flag: '',   //B按天执行，C间隔周期执行
          create_time:'',
          execute_time: '',
          frikcy: 0,   //执行周期
          unit: '',   //间隔时间,不需要保存在数据库
          cases_id: '',  //执行用例集
          switch: true
        },
        editLoading: false
      }
    },
    mounted: function () {
      this.treeView();
      window.xxx = this;
    },


    methods: {
      handleAdd(){
        this.chooseCaseData = this.planList;
        this.addFormVisible = true;
      },
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
     handleDel: function (row) {
        let index = this.chooseCaseData.indexOf(row);
        this.chooseCaseData.splice(index, 1)
      },
      editSubmit(){
        this.$refs.addForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              let para = Object.assign({}, this.addForm);
              let executeTime = para.execute_time;
              let unit = para.unit;
              delete para.execute_time;
              delete para.unit;
              if (unit === 'h') {
                para.frikcy = para.frikcy * 60
              } else if (unit === 'd') {
                para.frikcy = para.frikcy * 24 * 60
              }
              if (executeTime) {
                para.execute_time = executeTime.getHours() + ':' + executeTime.getMinutes()  //按天执行有执行时间
              } else {
                para.execute_time = ''      //按时间间隔没有执行时间
              }
              let flows = [];
              this.chooseCaseData.forEach(function (item) {
                flows.push(item.id)
              })
              para.cases_id = JSON.stringify(flows)
              this.$axios.post('/api/plans/', para).then(response => {
                this.$message({
                  message: '创建计划成功',
                  type: 'success'
                });
                this.addFormVisible = false;
                this.$router.push({path: '/plan/list'});
              })
            })
          }
        })
      },
      getID(x) {
        return x.id
      },
      handleCheckChange(data, node, self) {
        let modules = this.$refs.tree.getCheckedNodes(true)
        let moduleIds = modules.map(this.getID)
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


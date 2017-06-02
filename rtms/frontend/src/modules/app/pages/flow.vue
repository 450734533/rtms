<template>
  <el-row>
    <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
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

    <!--table-->
    <el-table :data="projectList" highlight-current-row v-loading="listLoading"
              @selection-change="selsChange" style="width: 100%" border>
      <el-table-column type="selection" width="55">
      </el-table-column>
      <el-table-column type="index" width="60">
      </el-table-column>
      <el-table-column prop="name" label="名称">
      </el-table-column>
      <el-table-column prop="flowRemark" label="备注">
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

    <!--工具条-->
    <el-col :span="24" class="toolbar">
      <el-button type="danger" @click="batchRemove" :disabled="sels.length===0">批量删除</el-button>
      <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="15"
                     :total="total" style="float:right;">
      </el-pagination>
    </el-col>

    <!--新增界面-->
    <el-dialog title="新建流程" v-model="addFormVisible" :close-on-click-modal="false" size="small">
      <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
        <el-form-item label="名称" prop="name">
          <el-input v-model="addForm.name" placeholder="请输入用例名称"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="name">
          <el-input v-model="addForm.flowRemark" placeholder="备注，非必填"></el-input>
        </el-form-item>
        <el-form-item label-width="10px">
          <el-button @click="addCard" type="success">新增步骤</el-button>
        </el-form-item>
        <el-card v-for="(card, i) in addForm.cards" class="box-card" :key="card.key">
          <div slot="header" class="clearfix">
            <span v-html="'流程'+ (i+1)" class="span"></span>
            <el-button type="text" class="button" @click.prevent="removeCard(card)">
              删除
            </el-button>
          </div>
          <el-form-item label="用例" :prop="'cards.' + i + '.caseId'">
            <el-select v-model="card.caseId" placeholder="请选择" @change="interface_select()"
                       :disabled="choose_interface.length===0">
              <el-option
                if
                v-for="item in choose_interface"
                :label="item.name"
                :value="item.id"
              >
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="次数" :prop="'cards.' + i + '.cnt'">
            <el-col :span="6">
              <el-input v-model="card.cnt" placeholder="请输入执行次数"></el-input>
            </el-col>
          </el-form-item>
          <i class="el-icon-plus" @click="addDomain(i)">
          </i>

          <el-form-item v-for="(domain, index) in card.domains" :label="'替换' + (index+1)"
                        :key="domain.key"
          >
            <!--{# :prop="'card.domains.' + index + '.replace'+'card.domains.' + index + '.step'"#}-->
            <el-col :span="3" :offset="0">
              <el-input v-model="domain.step" size="small" placeholder="step"></el-input>
            </el-col>
            <el-col :span="6">
              <el-input v-model="domain.replace" size="small"
                        placeholder="field"></el-input>
            </el-col>
            <el-col :span="2" :offset="1">
              <el-button type="danger" size="small" icon="delete"
                         @click.prevent="removeDomain(i,domain)">
              </el-button>
            </el-col>
          </el-form-item>
        </el-card>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="addFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
      </div>
    </el-dialog>

    <!--编辑界面-->
    <el-dialog title="编辑流程" v-model="editFormVisible" :close-on-click-modal="false" size="small">
      <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
        <el-form-item label="名称" prop="name">
          <el-input v-model="addForm.name" placeholder="请输入用例名称"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="name">
          <el-input v-model="addForm.flowRemark" placeholder="备注，非必填"></el-input>
        </el-form-item>
        <el-form-item label-width="10px">
          <el-button @click="addCard" type="success">新增步骤</el-button>
        </el-form-item>
        <el-card v-for="(card, i) in addForm.cards" class="box-card" :key="card.key">
          <div slot="header" class="clearfix">
            <span v-html="'流程'+ (i+1)" class="span"></span>
            <el-button type="text" class="button" @click.prevent="removeCard(card)">
              删除
            </el-button>
          </div>
          <el-form-item label="用例" :prop="'cards.' + i + '.caseId'">
            <el-select v-model="card.caseId" placeholder="请选择" @change="interface_select(i)"
                       :disabled="choose_interface.length===0">
              <el-option
                if
                v-for="item in choose_interface"
                :label="item.name"
                :value="item.id"
              >
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="次数" :prop="'cards.' + i + '.cnt'">
            <el-col :span="6">
              <el-input v-model="card.cnt" placeholder="请输入执行次数"></el-input>
            </el-col>
          </el-form-item>
          <i class="el-icon-plus" @click="addDomain(i)">
          </i>

          <el-form-item v-for="(domain, index) in card.domains" :label="'替换' + (index+1)"
                        :key="domain.key"
          >
            {# :prop="'card.domains.' + index + '.replace'+'card.domains.' + index + '.step'"#}
            <el-col :span="3" :offset="0">
              <el-input v-model="domain.step" size="small" placeholder="step"></el-input>
            </el-col>
            <el-col :span="6">
              <el-input v-model="domain.replace" size="small"
                        placeholder="field"></el-input>
            </el-col>
            <el-col :span="2" :offset="1">
              <el-button type="danger" size="small" icon="delete"
                         @click.prevent="removeDomain(i,domain)">
              </el-button>
            </el-col>
          </el-form-item>
        </el-card>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="editFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
      </div>
    </el-dialog>
  </el-row>
</template>

<script>
  export default{
    data(){
      return {
        current_caseId: 0,
        choose_interface: [],//选择框内的case
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
        executeLoading: false,
        executeFormVisible: false,
        addFormRules: {       //效验输入是否合法
          name: [
            {required: true, message: '请输入项目名称', trigger: 'blur'}
          ]
        },
        addForm: {       //新增输入内容，只要输入了就会有更新
          name: '',
          flowRemark: '',
          cards: [{
            caseId: '',
            cnt: 1,
            domains: [{
              step: '',
              replace: ''
            }],
          }],

        }

      };
    },
    mounted: function () {
      this.projectView();
      window.xxx = this;
    },
    methods: {
      projectView: function () {
        this.$axios.get("/api/case/").then(response => {
          this.choose_interface = response.data.results;
        });
        let para = {
          page: this.page,
          name: this.filters.name
        };
        this.listLoading = true;
        this.$axios.get("/api/flow/", {params: para}).then(response => {
          this.total = response.data.count;
          this.projectList = response.data.results;
          this.listLoading = false;
        });
      },
      handleCurrentChange(val) {
        this.page = val;
        this.projectView();
      },
      interface_select(i){
        console.log('aaaa1111')
        console.log(i)
        // let para = {
        //     current_caseId: item
        // }
        // let url = '/api/flow/item'
        // this.$axios.get(url, {params: para}).then(response=> {
        //     this.addForm.cards[i].caseId = item
        // });
      },
      removeDomain(i, item) {
        var index = this.addForm.cards[i].domains.indexOf(item)
        if (index !== -1) {
          this.addForm.cards[i].domains.splice(index, 1)
        }
      },
      removeCard(item) {
        var index = this.addForm.cards.indexOf(item)
        if (index !== -1) {
          this.addForm.cards.splice(index, 1)

        }
        // this.addForm.cards.$remove(item);
      },
      addDomain(i) {
        this.addForm.cards[i].domains.push({
          step: '',
          replace: '',
          key: Date.now()
        });
      },
      addCard() {
        this.addForm.cards.push({
          caseId: '',
          cnt: 1,
          domains: [{
            step: '',
            replace: ''
          }],
          key: Date.now()
        });
      },
      handleDel: function (index, row) {
        this.$confirm('确认删除该记录吗?', '提示', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          let url = '/api/flow/' + row.id + '/';
          this.$axios.delete(url).then(response => {
            this.listLoading = false;
            this.$message({
              message: '删除成功',
              type: 'success'
            });
            this.projectView()
          });
        })
      },
      handleAdd: function () {
        this.addFormVisible = true;
        this.addForm = {
          name: '',
          flowRemark: '',
          cards: [{
            caseId: '',
            cnt: 1,
            domains: [{
              step: '',
              replace: ''
            }],
          }],
        };
      },
      handleExecute: function (index, row) {
        this.listLoading = true;
        this.executeLoading = true;
        this.executeFormVisible = true;
        let url = '/api/flow/' + row.id + '/execute';
        this.$axios.get(url).then(response => {
          this.listLoading = false;
          this.executeLoading = false;
          this.executeFormVisible = false;
          this.$message({
            message: '执行成功',
            type: 'success'
          });
          this.projectView()
        });
      },
      handleEdit: function (index, row) {
        // let a = JSON.parse(row.cards)  //str转obj
        let para = Object.assign({}, row)
        para.cards = JSON.parse(para.cards)  //str转obj
        this.editFormVisible = true;
        this.addForm = Object.assign({}, para);                // 复制Object=row
      },
      addSubmit: function () {
        this.$refs.addForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.addLoading = true;
              let para = Object.assign({}, this.addForm);
              para.cards = JSON.stringify(para.cards)   //obj转str
              this.$axios.post('/api/flow/', para).then(response => {
                this.addLoading = false;
                this.$message({
                  message: '提交成功',
                  type: 'success'
                });
                this.addFormVisible = false;
                this.$refs['addForm'].resetFields()
                this.projectView();
              });

            });
          }
        });
      },
      editSubmit: function () {
        this.$refs.addForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editLoading = true;
              let para = Object.assign({}, this.addForm);
              para.cards = JSON.stringify(para.cards)
              let url = '/api/flow/' + para['id'] + '/';
              this.$axios.put(url, para).then(response => {
                this.editLoading = false;
                this.$message({
                  message: '修改成功',
                  type: 'success'
                });
                this.editFormVisible = false;
                this.projectView();
              });
            });
          }
        });
      },
      querySearch(queryString, cb) {
        this.$axios.get('/api/flow/').then(response => {
          var results = response.data.results;
          cb(results);
        });
      },
      selsChange: function (sels) {
        this.sels = sels;
      },
      //批量删除
      batchRemove: function () {
        var ids = this.sels.map(item => item.id).join(',');
        this.$confirm('确认删除选中记录吗？', '危险', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          this.$axios.get('/api/flow/batch/?id=' + ids).then(response => {
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
          });
        }).catch(() => {
        });
      }
    }
  }

</script>
    <style>
        .button {
            padding: 0;
            float: right;
            color: #e6091c;
            font-size: large;
        }

        .span {
            font-size: large;
        }
    </style>

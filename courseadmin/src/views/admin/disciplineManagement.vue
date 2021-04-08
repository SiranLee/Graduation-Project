<template>
  <div class="wrapper">
    <el-row :gutter="10">
      <el-col :span="4">
        <el-input v-model="input" placeholder="请输入学科名称" @input="inputChange" />
      </el-col>
      <el-col :span="3">
        <el-button type="primary" @click="disciplineSearch">搜索</el-button>
      </el-col>
    </el-row>
    <div class="tableWrapper">
      <el-table
        :data="tableData"
        style="width: 100%;"
        row-key="id"
        border
        default-expand-all
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      >
        <el-table-column
          prop="sequence"
          align="center"
          label="序号"
          sortable
        />
        <el-table-column
          prop="name"
          align="center"
          label="学科名称"
        />
        <el-table-column
          prop="teachers"
          align="center"
          label="任课人数"
        />
        <el-table-column
          prop="students"
          align="center"
          label="学科人数"
        />
        <el-table-column
          prop="courses"
          align="center"
          label="课程"
        />
        <el-table-column prop="operation" align="center" label="操作">
          <template slot-scope="{ row }">
            <div v-if="row.children">
              <el-button
                type="primary"
                size="mini"
                @click="editDiscipline(row)"
              >
                编辑
              </el-button>
              <el-button
                v-if="row.status != 'deleted'"
                size="mini"
                type="danger"
                @click="deleteDiscipline(row)"
              >
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <div class="bottomBtn">
        <el-button type="success" style="width: 60%;" @click="addDiscipline">添加学科</el-button>
      </div>
    </div>
    <div class="popGizmos">
      <el-dialog title="学科信息" :visible.sync="dialogVisible" width="30%">
        <div class="infoWrapper">
          <el-row :gutter="20" style="margin-bottom: 20px">
            <el-col :span="4" class="disciplineLabel"><span>学科名称</span></el-col>
            <el-col
              :span="15"
            ><el-input
              v-model="currentRow.name"
            /></el-col>
          </el-row>
          <el-row :gutter="20" style="margin-bottom: 20px">
            <el-col :span="4" class="disciplineLabel"><span>任课人数</span></el-col>
            <el-col
              :span="15"
            ><el-input
              :value="currentRow.teachers ? currentRow.teachers : ''"
              disabled
            /></el-col>
          </el-row>
          <el-row :gutter="20" style="margin-bottom: 20px">
            <el-col :span="4" class="disciplineLabel"><span>学科人数</span></el-col>
            <el-col
              :span="15"
            ><el-input
              :value="currentRow.students ? currentRow.students : ''"
              disabled
            /></el-col>
          </el-row>
          <el-row :gutter="20" style="margin-bottom: 20px">
            <el-col :span="4" class="disciplineLabel"><span>课程</span></el-col>
            <el-col
              :span="15"
            ><el-input
              :value="currentRow.courses ? currentRow.courses : ''"
              disabled
            /></el-col>
          </el-row>
          <el-row>
            <el-button type="success" style="width: 100%" @click="submitDisciplineChange">确定</el-button>
          </el-row>
        </div>
      </el-dialog>
      <el-dialog title="添加学科" :visible.sync="addDialogVisible" width="30%">
        <div style="text-align: center;" class="infoWrapper">
          <el-row :gutter="20" style="margin-bottom: 20px">
            <el-col :span="4" class="disciplineLabel"><span>学科名称</span></el-col>
            <el-col
              :span="15"
            ><el-input
              v-model="addDisciplineName"
            /></el-col>
          </el-row>
          <el-button style="width: 100%;" type="success" @click="confirmAddDiscipline">确定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>
<script>
import { routerMap } from '@/router/index'
export default {
  data() {
    return {
      input: '',
      tableData: [],
      dialogVisible: false,
      currentRow: { name: '' },
      lastName: '',
      addDisciplineName: '',
      addDialogVisible: false,
      tempTableData: []
    }
  },
  mounted() {
    this.$store.dispatch('admin/fetchDisciplineTableData')
      .then(res => {
        const $this = this
        const index = 0
        res.data.table.forEach((item) => {
          $this.tableData.push(item)
          $this.tempTableData.push(item)
        })
      })
      .catch(err => {})
  },
  methods: {
    inputChange() {
      const $this = this
      if (this.input.length === 0) {
        this.tableData.splice(0, this.tableData.length)
        this.tempTableData.forEach(item => {
          $this.tableData.push(item)
        })
      }
    },
    // 搜索学科
    disciplineSearch() {
      const targetItem = []
      const $this = this
      this.tableData.forEach(item => {
        if (item.name.indexOf($this.input) != -1) {
          targetItem.push(item)
        }
      })
      this.tableData = targetItem
    },
    // 删除学科信息
    deleteDiscipline(row) {
      this.$confirm('此操作将删除与该学科有关的所有信息, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 发送删除请求
        this.$store.dispatch('admin/delDiscipline', { id: row.key, discipline_name: row.name, discipline_en_name: row.en_name })
          .then(res => {
            console.log(this.tableData.indexOf(row))
            if (res.data.message === 'ok') {
              this.$message({ message: '操作成功', type: 'success' })
              this.tableData.splice(this.tableData.indexOf(row), 1)
            } else {
              this.$message({
                message: res.data.message,
                type: 'danger'
              })
            }
          })
          .catch(err => {})
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    // 编辑学科信息
    editDiscipline(row) {
      this.currentRow = row
      this.dialogVisible = true
    },
    submitDisciplineChange() {
      if (this.currentRow.name === this.lastName) return
      this.$store.dispatch('admin/submitDisciplineChange', { discipline: this.currentRow })
        .then(res => {
          if (res.data.message === 'ok') {
            this.$message({
              message: '操作成功',
              type: 'success'
            })
          }
        })
        .catch(err => {})
    },
    addDiscipline() {
      this.addDialogVisible = true
    },
    confirmAddDiscipline() {
      this.$store.dispatch('admin/addDiscipline', { disciplineName: this.addDisciplineName })
        .then(res => {
          let index = 2
          this.tableData.forEach(item => {
            if (item.children && item.children.length > 0) {
              index += item.children.length
            }
            index++
          })
          res.data.item['id'] = index
          res.data.item['sequence'] = index
          res.data.item['en_name'] = 'addedDiscipline' + res.data.suffix
          this.tableData.push(res.data.item)
          this.$message({ message: '操作成功', type: 'success' })
          return this.addRouteComponent('addedDiscipline' + res.data.suffix)
        })
        .then(res => {
          this.addDisciplineName = ''
        })
        .catch(err => {})
    },
    addRouteComponent(addedDisciplineName) {
      const componentName = addedDisciplineName
      routerMap[componentName] = () => import('@/views/sourcelist/index')
      return this.$store.dispatch('admin/addRouteForDiscipline', { id: this.$store.state.user.id, disciplineName_en: addedDisciplineName, disciplineName_cn: this.addDisciplineName, icon: 'added', path: '@/views/sourcelist/index' })
    }
  }
}
</script>
<style scoped>
.wrapper {
  padding: 20px;
  padding-top: 40px;
}
.upToolSegment {
  width: 20%;
}
.tableWrapper {
  margin-top: 30px;
}
.disciplineLabel{
  height: 100%;
  transform: translateY(60%);
  font-weight: 700;
}
.infoWrapper{
  margin: 0;
}
.bottomBtn{
  padding: 20px;
  text-align: center;
  background-color: #fff;
  border-left: 1px solid #EBEEF5;
  border-right: 1px solid #EBEEF5;
  border-bottom: 1px solid #EBEEF5;
}
</style>

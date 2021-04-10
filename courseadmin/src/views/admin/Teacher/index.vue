<template>
  <div style="padding: 40px;">
    <div class="filter">
      <el-select v-model="majorSelect" placeholder="请选择专业" @change="majorChange">
        <el-option
          v-for="item in majorOptions"
          :key="item.major_id"
          :label="item.title"
          :value="item.major_id"
        />
      </el-select>
      <!-- <el-select placeholder="请选择课程" @change="askForTeachers" v-model="courseSelect">
        <el-option
          v-for="item in courseOptions"
          :key="item.major_id"
          :label="item.title"
          :value="item.course_id"
        />
      </el-select> -->
      <el-input
        :value="keyWord"
        placeholder="请输入教师姓名"
        style="width: 15%;"
        @input="rollBack"
      />
      <el-button type="primary" @click="search">搜索</el-button>
      <el-input
        :value="teaNo"
        placeholder="请输入教师工号"
        style="width: 15%;"
        @input="rollBackForNo"
      />
      <el-button type="primary" @click="searchWithNo">搜索</el-button>
      <upload :is-disable="false" :loading="loading" :emit-file="getFile" />
      <a class="downloadLink" :href="excelTemplate" download>教师表模板</a>
    </div>
    <div class="pagination">
      <pagination
        :total="total"
        :page-size="pageSize"
        @pageChange="pageChange"
      />
    </div>
    <div class="tableView">
      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="id" label="序号" align="center" width="180" />
        <el-table-column
          prop="tea_number"
          label="工号"
          align="center"
          width="170"
        />
        <el-table-column
          prop="tea_name"
          label="姓名"
          align="center"
          width="170"
        />
        <el-table-column
          prop="tea_position"
          label="职称"
          align="center"
          width="170"
        />
        <el-table-column
          prop="tea_major"
          label="所在系部"
          align="center"
          width="180"
        />
        <el-table-column prop="courseStr" align="center" label="课程" />
        <el-table-column prop="operate" align="center" label="操作" width="300">
          <template slot-scope="{ row }">
            <el-button type="primary" size="mini" @click="editTeacher(row)">
              编辑
            </el-button>
            <el-button type="success" size="mini" @click="editPermission(row)">
              编辑权限
            </el-button>
            <el-button
              v-if="row.status != 'deleted'"
              :loading="row.del_wait"
              size="mini"
              type="danger"
              @click="deleteTeacher(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <the-dialog
        :dialog-visible="dialogVisible"
        :item="currentItem"
        @changeInfo="submitChange"
        @changeVisible="dialogVisible = !dialogVisible"
      />
      <el-dialog title="权限编辑" :visible.sync="dialogTableVisible" @close="closeDialog">
        <el-row style="height: 350px" :gutter="20">
          <el-col :span="10" style="height: 100%;">
            <div class="itemZone" style="margin: 0;">
              <span>姓名: </span><el-input v-model="editPermissionRow.tea_name" disabled />
            </div>
            <div class="itemZone">
              <span>职称: </span><el-input v-model="editPermissionRow.tea_position" disabled />
            </div>
            <div class="itemZone">
              <span>课程: </span><el-input v-model="editPermissionRow.courseStr" disabled />
            </div>
            <el-button type="success" style="width:100%; margin-top: 50px" @click="confirmEditPermission" :loading="permissionLoading">确定</el-button>
          </el-col>
          <el-col :span="14" style="height: 100%;">
            <div style="overflow-y: scroll; height: 100%">
              <!-- @check="handleNodeClick" -->
              <el-tree ref="tree" :data="permissionData" :default-expanded-keys="defaultCheckedItems" :default-checked-keys="defaultCheckedItems" node-key="route_id" show-checkbox @check="handleNodeCheck" />
            </div>
          </el-col>
        </el-row>
      </el-dialog>
    </div>
  </div>
</template>
<script>
import theDialog from './components/Dialog'
import pagination from '@/components/SimplePagination'
import upload from '@/components/UploadExcel/uploadExcel'
import * as ladda from 'ladda'
export default {
  components: {
    upload,
    pagination,
    theDialog
  },
  data() {
    return {
      teaNo: "",
      total: 0,
      pageSize: 10,
      currentPage: 1,
      dialogVisible: false,
      currentItem: {},
      courseOptions: [],
      tableData: [],
      majorOptions: [],
      majorSelect: '',
      // courseSelect: "",
      teacherName: '',
      loading: false,
      keyWord: '',
      throttle: false,
      excelTemplate: '',
      dialogTableVisible: false,
      editPermissionRow: {
        tea_number: '',
        tea_name: '',
        tea_position: '',
        courseStr: ''
      },
      permissionLoading: false,
      permissionData: [],
      defaultCheckedItems: [],
      addCheckedItems: [],
      removeCheckedItems: [],
      pivotCheckedItems: []
    }
  },
  computed: {
    isAdmin() {
      return this.$store.state.user.roles.includes('admin')
    }
  },
  async mounted() {
    // 请求专业
    const { data } = await this.$store.dispatch('publicOpen/getAllMajors')
    const result = await this.$store.dispatch('admin/getExcelTemplate')
    if (result.data) { this.excelTemplate = process.env.VUE_APP_BASE_API + result.data.link }
    if (data) this.majorOptions = data.majors
    this.majorSelect = this.majorOptions[0].major_id
    this.askForTeachers()
  },
  methods: {
    //  async askForCourse(){
    //     const { data } = await this.$store.dispatch('teachers/getShortCourse', {major_id: this.majorSelect})
    //     if(data) this.courseOptions = data.courses
    //     if(this.courseOptions.length>0){
    //       this.courseSelect =  this.courseOptions[0].course_id
    //       this.askForTeachers();
    //     }
    //   },
    majorChange() {
      this.askForTeachers()
    },
    async askForTeachers() {
      const { data } = await this.$store.dispatch('admin/getTeachers', {
        major_id: this.majorSelect,
        limit: this.pageSize,
        page: this.currentPage
      })
      if (data) {
        data.teachers.forEach((item, index) => {
          item.id = index + 1
          item.tea_no = item.tea_number
          item.courseStr = item.teacher_course.join(',')
          item.del_wait = false
        })
        this.tableData = data.teachers
        this.total = data.total
      }
    },
    async editTeacher(item) {
      this.dialogVisible = true
      this.currentItem = item
    },
    async editPermission(row) {
      const $this = this
      this.dialogTableVisible = true
      for (const key in this.editPermissionRow) {
        if (Object.hasOwnProperty.call(this.editPermissionRow, key)) {
          this.editPermissionRow[key] = row[key]
        }
      }
      this.permissionData.splice(0, this.permissionData.length)
      this.defaultCheckedItems.splice(0, this.defaultCheckedItems.length)
      this.pivotCheckedItems.splice(0, this.pivotCheckedItems.length)
      this.$store.dispatch('admin/fetchRoutes')
        .then(res => {
          const $this = this
          res.data.routes.forEach(item => {
            if (item.children.length == 1) {
              item.parent_id = item.route_id
              item.route_id = item.children[0].route_id
              item.label = item.children[0].label
              item.children.splice(0, 1)
            }
            $this.permissionData.push(item)
          })
          return this.$store.dispatch('admin/fetchRouteForTeacher', { tea_no: this.editPermissionRow.tea_number })
        })
        .then(res => {
          res.data.routes.forEach((item, index) => {
            $this.defaultCheckedItems.push(item)
            $this.pivotCheckedItems.push(item)
          })
          this.$nextTick(() => {
            console.log('here')
            this.$refs.tree.setCheckedKeys(this.defaultCheckedItems)
          })
        })
        .catch(err => {})
    },
    handleNodeCheck(relatedNode, option) {
      const $this = this
      if (option.checkedNodes.indexOf(relatedNode) != -1) {
        // 说明是选中relatedNode
        const index = this.removeCheckedItems.indexOf(relatedNode.route_id)
        if (index == -1) {
          if (Object.hasOwnProperty.call(relatedNode, 'parent_id')) {
            this.addCheckedItems.push(relatedNode.parent_id)
          }
          this.addCheckedItems.push(relatedNode.route_id)
          if (relatedNode.children && relatedNode.children.length > 0) {
            relatedNode.children.forEach(item => $this.addCheckedItems.push(item.route_id))
          }
        } else {
          this.removeCheckedItems.splice(index, 1)
          if (Object.hasOwnProperty.call(relatedNode, 'parent_id')) {
            this.removeCheckedItems.splice(this.removeCheckedItems.indexOf(relatedNode.parent_id), 1)
          }
          if (relatedNode.children && relatedNode.children.length > 0) {
            relatedNode.children.forEach(val => {
              const child_index = $this.removeCheckedItems.indexOf(val.route_id)
              if (child_index != -1) {
                $this.removeCheckedItems.splice(child_index, 1)
              }
            })
          }
        }
      } else {
        // 说明是退选relateNode
        const index = this.addCheckedItems.indexOf(relatedNode.route_id)
        if (index == -1) {
          // 说明当前node未曾加入过，说明是要删除的权限
          if (Object.hasOwnProperty.call(relatedNode, 'parent_id')) {
            this.removeCheckedItems.push(relatedNode.parent_id)
          }
          this.removeCheckedItems.push(relatedNode.route_id)
          if (relatedNode.children && relatedNode.children.length > 0) {
            relatedNode.children.forEach(val => {
              $this.removeCheckedItems.push(val.route_id)
            })
          }
        } else {
          if (Object.hasOwnProperty.call(relatedNode, 'parent_id')) {
            const parent_index = this.addCheckedItems.indexOf(relatedNode.parent_id)
            this.addCheckedItems.splice(parent_index, 1)
          }
          this.addCheckedItems.splice(this.addCheckedItems.indexOf(relatedNode.route_id), 1)
          if (relatedNode.children && relatedNode.children.length > 0) {
            relatedNode.children.forEach(val => {
              const child_index = $this.addCheckedItems.indexOf(val.route_id)
              if (child_index != -1) {
                $this.addCheckedItems.splice(child_index, 1)
              }
            })
          }
        }
      }
    },
    closeDialog() {
      this.addCheckedItems.splice(0, this.addCheckedItems.length)
      this.removeCheckedItems.splice(0, this.removeCheckedItems.length)
    },
    async confirmEditPermission() {
      this.permissionLoading = true;
      this.$store.dispatch('admin/setPermissionForTeacher', { add_permission: this.addCheckedItems, del_permission: this.removeCheckedItems, id: this.editPermissionRow.tea_number })
        .then(res => {
          if (res.data.message == 'ok') {
            this.$message({
              message: '操作成功',
              type: 'success'
            });
            this.permissionLoading = false;
          }
          this.addCheckedItems.splice(0, this.addCheckedItems.length)
          this.removeCheckedItems.splice(0, this.removeCheckedItems.length)
        })
        .catch(() => {})
    },
    async deleteTeacher(item) {
      this.$confirm('请确认操作', '警告', {
        confirmButtonText: '确定',
        deleteButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        item.del_wait = true;
        const { data } = await this.$store.dispatch('admin/deleteTeacher', {
          id: item.tea_number
        })
        if (data.message === 'ok') {
          this.$message({
            message: '删除成功',
            type: 'success'
          })
          this.tableData = this.tableData.filter(
            tea => tea.tea_number !== item.tea_number
          )
          item.del_wait = false;
        }
      })
    },
    async pageChange(page) {
      const { data } = await this.$store.dispatch('admin/getTeachers', {
        major_id: this.majorSelect,
        limit: this.pageSize,
        page: page
      })
      if (data) {
        data.teachers.forEach((item, index) => {
          item.id = index + 1
          item.courseStr = item.teacher_course.join(',')
        })
        this.tableData = data.teachers
        this.total = data.total
        this.currentPage = page
      }
    },
    async submitChange(item) {
      const { data } = await this.$store.dispatch('admin/submitChange', {
        item,
        admin_id: this.$store.state.user.id
      })
      if (data.message === 'ok') {
        this.$message({
          message: '修改成功',
          type: 'success'
        })
        let target = this.tableData.filter(
          tea => tea.tea_number === item.tea_number
        )
        target = item
        this.dialogVisible = false
      }
    },
    async getFile(file) {
      const formData = new FormData()
      formData.append('excel', file)
      formData.append('major_id', this.majorSelect)
      // formData.append('limit', this.pageSize)
      // formData.append('page', this.currentPage)
      this.loading = true
      this.$store
        .dispatch('admin/uploadTeas', formData)
        .then(res => {
          if (res.data.message === 'ok') {
            this.$message({
              message: '导入成功',
              type: 'success'
            })
            this.askForTeachers()
            this.loading = false
          }
        })
        .catch(err => {})
    },
    async search() {
      const { data } = await this.$store.dispatch('admin/searchTeacher', {
        name: this.keyWord,
        limit: this.pageSize
      })
      if (data) {
        data.teachers.forEach((item, index) => {
          item.id = index + 1
          item.courseStr = item.teacher_course.join(',')
        })
        this.total = data.total
        this.pageSize = data.total
        this.tableData = data.teachers
      }
    },
    async searchWithNo(){
      const { data } = await this.$store.dispatch('admin/searchTeacherWithNo',{ teaNo: this.teaNo})
      if(data){
        data.teachers.forEach((item, index) => {
          item.id = index + 1
          item.courseStr = item.teacher_course.join(',')
        })
        this.total = data.total
        this.pageSize = data.total
        this.tableData = data.teachers
      }
    },
    rollBack(v) {
      this.keyWord = v
      if (v.length === 0) {
        this.pageSize = 10
        this.askForTeachers()
      }
    },
    rollBackForNo(v){
      this.teaNo = v
      if(v.length === 0){
        this.pageSize = 10;
        this.askForTeachers()
      }
    }
  }
}
</script>
<style scoped>
.filter {
  margin-bottom: 20px;
}
.downloadLink {
  display: inline-block;
  background-color: #67c23a;
  padding: 10px;
  border-radius: 5px;
  color: white;
}
.itemZone{
  margin-top: 30px;
}
.itemZone span{
  display: block;
  margin-bottom: 5px;
  font-weight: 700 disabled;
}
</style>

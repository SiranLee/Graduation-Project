<template>
  <div>
    <el-container>
      <el-main>
        <div class="filters">
          <el-row>
            <el-col :span="3"><filter-widget v-model="selmajor" :emit-change="majorchange" hint="请选择专业" :options="optionsMajor" /></el-col>
            <el-col :span="3"><filter-widget v-model="selcourse" :emit-change="courseChange" hint="请选择课程" :options="optionsCourse" /></el-col>

            <el-col :span="3"><el-input v-model="keyWord" placeholder="请输入学生姓名" @input="keyChange" /></el-col>
            <el-col :span="1"><el-button type="primary" @click="search">搜索</el-button></el-col>
            <el-col :span="0.5"><div style="width:10px;height:10px" /></el-col>
            <el-col :span="3"><el-input v-model="stuNo" placeholder="请输入学生学号" @input="keyChange" /></el-col>
            <el-col :span="1"><el-button type="primary" @click="searchWithNo">搜索</el-button></el-col>

            <el-col :span="2"><upload :emit-file="getFile" :loading="upload_loading" /></el-col>
            <el-col :span="2"><el-button type="success"><a :href="templateLink" download>表模板</a></el-button></el-col>
          </el-row>
        </div>
        <div class="tables">
          <table-widget :table-loading="loading" :table-data="tabData" @operation="handleOperate" />
        </div>
      </el-main>
      <el-footer>
        <stu-pagination :current-page="currentPage" :page-sizes="page_sizes" :page-size="page_size" :total="total" @getPage="pageChange" @sizeChange="sizeChange" />
      </el-footer>
    </el-container>
    <tea-dialog :dialog-visible="showDialog" :stu-item="currentRow" @changeStuInfo="changeStuInfo" @changeVisible="showDialog=!showDialog" />
  </div>
</template>
<script>
import FilterWidget from './components/FilterWidget'
import TableWidget from './components/TableWidget'
import StuPagination from './components/Stupagination'
import TeaDialog from './components/TeaDialog'
import upload from '@/components/UploadExcel/uploadExcel'
export default {
  components: {
    FilterWidget,
    TableWidget,
    StuPagination,
    TeaDialog,
    upload
  },
  data() {
    return {
      stuNo: '',
      keyWord: '',
      selcourse: '',
      selmajor: '',
      optionsCourse: [],
      optionsMajor: [],
      tabData: [],
      total: 0,
      page_sizes: [10, 20, 30, 40],
      page_size: 10,
      currentPageSize: 10,
      loading: true,
      importDisable: true,
      currentPage: 1,
      showDialog: false,
      currentRow: {},
      templateLink: '',
      upload_loading: false
    }
  },
  async mounted() {
    const { data } = await this.$store.dispatch('publicOpen/getMajors', { id: this.$store.state.user.id })
    const $this = this
    data.majors.forEach(item => { $this.optionsMajor.push({ label: item.title, value: item.major_id }) })
    this.templateLink = process.env.VUE_APP_BASE_API + data.link
    console.log(this.optionsMajor)
    this.selmajor = this.optionsMajor.find(item => item.label === this.$store.state.user.major).value
    const result = await this.$store.dispatch('teachers/getShortCourse', { id: this.$store.state.user.id, major: this.selmajor })
    result.data.courses.forEach(item => { this.optionsCourse.push({ label: item.title, value: item.course_id }) })
    this.selcourse = this.optionsCourse[0].value
    this.$store.dispatch('teachers/getPageData', { major_id: this.selmajor, course_id: this.selcourse, page: this.currentPage, limit: this.page_size })
      .then(res => {
        res.data.stus.forEach((item, index) => { item.id = index + 1 })
        this.tabData = res.data.stus
        this.total = res.data.total
        this.loading = false
      })
      .catch(() => { return })
  },
  methods: {
    async majorchange(v) {
      this.selmajor = v
      this.optionsCourse.splice(0, this.optionsCourse.length)
      const { data } = await this.$store.dispatch('teachers/getShortCourse', { id: this.$store.state.user.id, major: v })
      data.courses.forEach(item => { this.optionsCourse.push({ label: item.title, value: item.course_id }) })
      this.courseChange(this.optionsCourse[0].value)
    },
    courseChange(v) {
      this.selcourse = v
      this.importDisable = false
      this.$store.dispatch('teachers/getPageData', { major_id: this.selmajor, course_id: this.selcourse, page: this.currentPage, limit: this.page_size })
        .then(res => {
          res.data.stus.forEach((item, index) => { item.id = index + 1 })
          this.tabData = res.data.stus
          this.total = res.data.total
          this.loading = false
        })
        .catch(() => { return })
    },
    async keyChange() {
      if (!this.keyWord) {
        this.$store.dispatch('teachers/getPageData', { major_id: this.selmajor, course_id: this.selcourse, page: this.currentPage, limit: this.page_size })
          .then(res => {
            res.data.stus.forEach((item, index) => { item.id = index + 1 })
            this.tabData = res.data.stus
            this.total = res.data.total
            this.loading = false
          })
          .catch(() => { return })
      }
    },
    async search() {
      if (!this.selcourse || !this.selmajor || !this.keyWord) {
        return this.$message({
          message: '请选择完整搜索字段',
          type: 'warning'
        })
      }
      const { data } = await this.$store.dispatch('teachers/searchStu', { major_id: this.selmajor, course_id: this.selcourse, keyword: this.keyWord, limit: this.page_size, page: this.currentPage })
      this.tabData = data.stus
      this.total = data.total
      this.loading = false
    },
    async searchWithNo() {
      if (!this.selcourse || !this.selmajor || !this.stuNo) {
        return this.$message({
          message: '请先选择下拉菜单的选项',
          type: 'warning'
        })
      }
      const { data } = await this.$store.dispatch('teachers/searchWithNo', { major_id: this.selmajor, course_id: this.selcourse, stuNo: this.stuNo, limit: this.page_size, page: this.currentPage })
      this.tabData = data.stus
      this.total = data.total
      this.loading = false
    },
    async pageChange(payload) {
      this.loading = true
      // 异步请求
      this.$store.dispatch('teachers/getPageData', { major_id: this.selmajor, course_id: this.selcourse, page: payload, limit: this.page_size })
        .then(res => {
          res.data.stus.forEach((item, index) => { item.id = index + 1 })
          this.tabData = res.data.stus
          this.loading = false
          this.currentPage = payload
        })
        .catch(() => { return })
    },
    async sizeChange(size) {
      if (size > this.currentPageSize) {
        this.loading = true
        const { data } = await this.$store.dispatch('teachers/getPageData', { major_id: this.selmajor, course_id: this.selcourse, page: 1, limit: size })
        this.tabData = data.stus.slice(0, Math.min(size, data.stus.length))
      } else {
        this.tabData = this.tabData.slice(0, size)
      }
      this.tabData.forEach((item, index) => item.id = index + 1)
      this.currentPageSize = size
      this.loading = false
    },
    handleOperate(row, type) {
      if (type) {
        this.$confirm('确定删除吗?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            console.log(row)
            this.$store.dispatch('teachers/deleteStu', { id: row.stu_number, course: this.selcourse })
              .then(res => {
                if (res.data.message === 'ok') {
                  this.$message({
                    message: '删除成功',
                    type: 'success'
                  })
                  this.tabData = this.tabData.filter(item => item.stu_number !== row.stu_number)
                }
              })
              .catch(() => { return })
          })
          .catch(() => {})
      } else {
        this.currentRow.newPwd = ''
        this.currentRow = row
        this.showDialog = true
      }
    },
    changeStuInfo(stu, pwd) {
      // this.showDialog = true
      this.$store.dispatch('teachers/modifyPwd', { id: stu.stu_number, pwd: stu.newPwd })
        .then(res => {
          if (res.data && res.data.message === 'ok') {
            this.$message({
              message: '操作成功',
              type: 'success'
            })
            this.showDialog = false
          }
        })
        .catch(() => { return })
    },
    async getFile(file) {
      this.upload_loading = true
      this.loading = true
      const formData = new FormData()
      formData.append('major_id', this.selmajor)
      formData.append('course_id', this.selcourse)
      formData.append('excel', file)
      this.$store.dispatch('teachers/uploadFile', formData)
        .then(async res => {
          this.loading = false
          const item_snos = []
          let stugrade = ''
          res.data.stus.forEach((item, index) => {
            item.id = index % 10 + 1
            item_snos.push(item.stu_number)
            stugrade = item.stu_grade
          })
          this.total = res.data.total
          this.tabData = res.data.stus.splice(0, this.page_size)
          console.log(this.tabData)
          const result = await this.$store.dispatch('teachers/creatClassAndSetRoutes', { course_id: this.selcourse, grade: stugrade, snos: item_snos })
          this.upload_loading = false
          if (result.data.message == 'ok') {
            this.$message({
              message: '写入成功',
              type: 'success'
            })
          } else {
            this.$message({
              message: '网络错误，请稍后重试',
              type: 'danger'
            })
          }
        })
    }
  }
}
</script>
<style scoped>
.filters{
  margin-bottom: 20px;
}
.filters .el-col{
  margin-right: 10px;
}
</style>

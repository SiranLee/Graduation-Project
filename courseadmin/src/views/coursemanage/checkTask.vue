<template>
  <div style="padding: 30px">
    <div class="filter">
      <el-row>
        <el-col
          :span="3"
        ><filter-widget
          :value="selGrade"
          hint="请选择年级"
          :options="optionsGrade"
          :emit-change="Tagchange"
          title="Grade"
        /></el-col>
        <el-col
          :span="3"
        ><filter-widget
          :value="selMajor"
          hint="请选择专业"
          :options="optionsMajor"
          :emit-change="Tagchange"
          title="Major"
        /></el-col>
        <el-col
          :span="3"
        ><filter-widget
          :value="selCourse"
          hint="请选择课程"
          :options="optionsCourse"
          :emit-change="Tagchange"
          title="Course"
        /></el-col>
        <el-col
          :span="3"
        ><filter-widget
          :value="selTask"
          :emit-change="Tagchange"
          hint="请选择任务"
          :options="optionsTask"
          title="Task"
        /></el-col>
        <el-col
          :span="3"
        ><filter-widget
          :value="selStatus"
          hint="作业状态"
          :options="optionsStatus"
          :emit-change="Tagchange"
          title="Status"
        /></el-col>
        <!-- <el-col :span="3">
          <el-input
            :value="keyWord"
            placeholder="请输入学生姓名"
            @input="searchInput"
          />
        </el-col>
        <el-col
          :span="1"
        ><el-button type="primary" @click="search">搜索</el-button></el-col> -->
      </el-row>
    </div>
    <div>
      <pagination
        style="margin-bottom: 10px;"
        :total="listTotal"
        :page-size="limit"
        @pageChange="pageChange"
      />
    </div>
    <div class="tableView">
      <el-table v-loading="tableLoading" :data="tableData" border style="width: 100%">
        <el-table-column prop="index" label="序号" align="center" width="120" />
        <el-table-column
          prop="stu_number"
          label="学号"
          align="center"
          width="160"
        />
        <el-table-column
          prop="stu_grade"
          label="年级"
          align="center"
          width="120"
        />
        <el-table-column
          prop="stu_major"
          label="专业"
          align="center"
          width="140"
        />
        <el-table-column prop="name" align="center" label="姓名" />
        <el-table-column prop="score" align="center" label="成绩" />
        <el-table-column
          prop="task"
          align="center"
          label="任务题目"
          width="120"
        />
        <el-table-column align="center" label="状态">
          <template slot-scope="{ row }">
            <el-tag effect="dark" :type="row.type">
              {{ row.state }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column align="center" label="操作">
          <template slot-scope="{ row }">
            <el-button type="primary" size="mini" @click="check(row)">
              批改
            </el-button>
            <el-button
              v-if="row.status != 'deleted'"
              size="mini"
              type="danger"
              @click="remove(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-dialog
      ref="dialog"
      top="0"
      title="批改"
      :visible.sync="dialogVisible"
      width="50%"
      @opened="dialogOpen"
    >
      <pdf
        ref="pdf"
        :loading="pdfLoading"
        :width="dialogWidth"
        :height="600"
        :web-address="webAddress"
      />
      <span slot="footer" class="dialog-footer">
        <div style="padding-bottom: 15px;">
          <label for="scoreInput" style="padding-right: 20px;">得分</label>
          <el-input-number
            id="scoreInput"
            v-model="currentStu.score"
            :max="100"
            :min="0"
          />
        </div>
        <el-button
          style="width: 30%;"
          type="success"
          @click="submitSingleScore"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import FilterWidget from '../studentmanage/components/FilterWidget'
// import TableWidget from '../studentmanage/components/TableWidget'
import pagination from '@/components/SimplePagination'
import pdf from './components/pdfView'
// import axios from 'axios'
export default {
  components: {
    FilterWidget,
    // TableWidget,
    pagination,
    pdf
  },
  data() {
    return {
      pdfLoading: true,
      dialog: {},
      dialogWidth: 0,
      selGrade: '',
      selCourse: '',
      selTask: '',
      selMajor: '',
      selStatus: '',
      keyWord: '',
      webAddress: {
        link: ''
      },
      dialogVisible: false,
      optionsCourse: [],
      optionsTask: [],
      optionsGrade: [],
      optionsClass: [],
      optionsMajor: [],
      optionsStatus: [],
      limit: 20,
      currentPage: 1,
      currentStu: {},
      tableData: [],
      tableLoading: false,
      listTotal: 0
    }
  },
  async mounted() {
    this.tableLoading = true
    window.addEventListener('resize', () => {
      if (this.dialog) {
        this.dialogWidth = this.dialog.offsetWidth
      }
    })

    // 请求课程
    this.$store.dispatch('teachers/getGrade', { id: this.$store.state.user.id })
      .then(res => {
        this.optionsGrade = this.uniqueArr(res.data.grades)
        this.optionsMajor = res.data.majors
        this.selGrade = this.optionsGrade[0].value
        this.selMajor = this.optionsMajor[0].value
        return this.$store.dispatch('teachers/getShortCourse', { id: this.$store.state.user.id, major: this.selMajor })
      })
      .then(res => {
        this.optionsCourse = res.data.courses
        this.selCourse = this.optionsCourse[0].course_id
        return this.$store.dispatch('teachers/getTasksByCourse', { course_id: this.selCourse })
      })
      .then(res => {
        this.optionsStatus = res.data.status
        this.selStatus = this.optionsStatus[0].value
        this.optionsTask = res.data.tasks
        this.selTask = this.optionsTask[0].value
        return this.$store.dispatch('teachers/getPDF', {
          id: this.$store.state.user.id,
          course_id: this.selCourse,
          grade_id: this.selGrade,
          task_id: this.selTask,
          major_id: this.selMajor,
          page: this.currentPage,
          limit: this.limit,
          status: this.selStatus
        })
      })
      .then(res => {
        res.data.list.forEach((item, index) => {
          item.index = index + 1
        })
        this.tableData = res.data.list
        this.tableLoading = false
      })
      .catch(() => { return })
  },
  methods: {
    uniqueArr(arr){
      let tempArr = []
      let arrSet = new Set([arr[0].label])
      for(let i = 1;i<arr.length;i++){
        arrSet.add(arr[i].label)
      }
      let pureArr = Array.from(arrSet)
      pureArr.forEach(item => {tempArr.push({label: item, value: item})})
      return tempArr
    },
    getData(data) {
      this.$store
        .dispatch('teachers/getPDF', data)
        .then(res => {
          this.listTotal = res.data.listTotal
          res.data.list.forEach((item, index) => {
            item.index = index + 1
          })
          this.tableData = res.data.list
        })
        .catch(() => { return })
    },
    Tagchange(v, suffix) {
      // 这里添加代码
      // console.log('herherher')
      this[`sel${suffix}`] = v
      // console.log(this[`sel${suffix}`])
      this.$store.dispatch('teachers/getShortCourse', { id: this.$store.state.user.id, major: this.selMajor })
      .then(res => {
        this.optionsCourse = res.data.courses
        this.selCourse = this.optionsCourse[0].course_id
        return this.$store.dispatch('teachers/getTasksByCourse', { course_id: this.selCourse })
      })
      .then(res => {
        this.optionsTask = res.data.tasks
        // if(suffix === 'Course')

        // this.selTask = this.optionsTask[0].value
        return this.getData({
          id: this.$store.state.user.id,
          grade_id: this.selGrade,
          course_id: this.selCourse,
          task_id: this.selTask,
          major_id: this.selMajor,
          limit: this.limit,
          page: this.currentPage,
          status: this.selStatus
        })
      }).then(res => {
        res.data.list.forEach((item, index) => {
          item.index = index + 1
        })
        this.tableData = res.data.list
        this.tableLoading = false
      })
        .catch(() => { return })
    },
    searchInput(v) {
      this.keyWord = v
      if (v.length === 0) {
        this.getData({
          id: this.$store.state.user.id,
          grade_id: this.selGrade,
          class_id: this.selClass,
          course_id: this.selCourse,
          task_id: this.selTask,
          major_id: this.selMajor,
          limit: this.limit,
          page: this.currentPage
        })
      }
    },
    search() {
      this.$store
        .dispatch('teachers/getSomeone', {
          major_id: this.selMajor,
          stu_name: this.keyWord
        })
        .then(res => {
          this.tableData = res.data.item
        })
        .catch(() => { return })
    },
    check(row) {
      // 批改作业
      this.dialogVisible = true
      this.currentStu = row
      this.pdfLoading = true
    },
    remove(row) {
      // 移除...
    },
    submitSingleScore() {
      this.$store
        .dispatch('teachers/submitSingleScore', {
          id: this.currentStu.stu_number,
          score: this.currentStu.score,
          course_id: this.selCourse,
          task_id: this.selTask
        })
        .then(res => {
          if (res.data.message === 'ok') {
            this.dialogVisible = false
            res.data.ack.index = this.currentStu.index
            const index = this.tableData.findIndex(item => item.stu_number === this.currentStu.stu_number)
            this.tableData.splice(index, 1, res.data.ack)
          }
        })
        .catch(() => { return })
    },
    pageChange(page) {
      this.$store
        .dispatch('teachers/getTaskByQuery', {
          grade_id: this.selGrade,
          class_id: this.selClass,
          course_id: this.selCourse,
          task_id: this.selTask,
          major_id: this.selMajor,
          limit: this.limit,
          page: page
        })
        .then(res => {
          this.currentPage = page
          this.listTotal = res.data.listTotal
          this.tableData = res.data.list
        })
        .catch(() => { return })
    },
    dialogOpen(row) {
      this.webAddress.link =
        process.env.VUE_APP_BASE_API + this.currentStu.link
      this.dialog = this.$refs['dialog'].$refs['dialog']
      this.dialogWidth = this.dialog.offsetWidth
      this.pdfLoading = false
    }
  }
}
</script>
<style scoped>
.filter {
  margin-bottom: 20px;
}
.filter .el-col {
  margin-right: 10px;
}
</style>

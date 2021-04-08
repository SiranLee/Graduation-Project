<template>
  <div style="padding: 40px;">
    <div class="uploadTask">
      <div class="divider"><span class="innerHint">上传作业</span></div>
      <div class="main">
        <el-row :gutter="20">
          <el-col
            :span="3"
          ><filter-widget
            :value="selGrade"
            hint="请选择年级"
            :options="optionsGrade"
            :emit-change="(v) => {selGrade = v}"
          /></el-col>
          <el-col
            :span="4"
          ><filter-widget
            :value="selMajor"
            hint="请选择专业"
            :options="optionsMajor"
            :emit-change="(v) => {selMajor = v}"
          /></el-col>
          <el-col
            :span="4"
          ><filter-widget
            :value="selCourse"
            hint="请选择课程"
            :options="optionsCourse"
            :emit-change="courseChange"
          /></el-col>
          <el-col
            :span="4"
          ><filter-widget
            :value="selTask"
            hint="请选择作业"
            :options="optionsTask"
            :emit-change="(v) => {selTask = v}"
          /></el-col>
        </el-row>
        <div class="uploader">
          <el-upload
            class="upload"
            action="/"
            :on-remove="fileWillRemove"
            :on-change="fileLIstChange"
            multiple
            :limit="limit"
            :on-exceed="handleExceed"
            :file-list="fileList"
            :auto-upload="false"
            :accept="accept"
          >
            <el-button size="small" type="primary">点击上传</el-button>
            <div slot="tip" class="el-upload__tip">
              只能上传pdf文件，且总大小不超过{{ maxFileSize / 1024 / 1024 }}MB
            </div>
          </el-upload>
          <el-button
            v-loading="loading"
            type="success"
            style="margin-top: 15px; width: 30%"
            @click="stuUpload"
          >上传作业</el-button>
        </div>
      </div>
    </div>
    <div class="uploadHistory">
      <div class="divider"><span class="innerHint">提交记录</span></div>
      <div class="main">
        <el-row style="padding-bottom: 10px;">
          <el-col :span="3">
            <filter-widget
              :value="taskCourse"
              hint="请选择课程"
              :options="optionsCourse"
              :emit-change="Tagchange"
            />
          </el-col>
          <el-col :span="20">
            <pagination :total="total" :page-size="tableLimit" style="float: right;" />
          </el-col>
        </el-row>
        <!-- 序号，专业，课程，作业题目，提交时间 -->
        <el-table :data="tableData" border>
          <el-table-column prop="id" label="序号" align="center" width="180" />
          <el-table-column prop="stu_major" label="专业" align="center" />
          <el-table-column prop="stu_course" label="课程" align="center" />
          <el-table-column prop="stu_taskTitle" label="作业" align="center" />
          <el-table-column
            prop="stu_submitDate"
            label="提交时间"
            align="center"
          />
        </el-table>
      </div>
    </div>
  </div>
</template>
<script>
import FilterWidget from '../studentmanage/components/FilterWidget'
import pagination from '@/components/SimplePagination'
export default {
  components: {
    FilterWidget,
    pagination
  },
  data() {
    return {
      limit: 1,
      selGrade: '',
      selMajor: '',
      selCourse: '',
      selTask: '',
      optionsGrade: [],
      optionsMajor: [],
      optionsCourse: [],
      optionsTask: [],
      fileList: [],
      maxFileSize: 10 * 1024 * 1024,
      accept: 'application/pdf',
      loading: false,
      tableData: [],
      total: 0,
      tableLimit: 5,
      currentPage: 1,
      taskCourse: ''
    }
  },
  computed: {
    conditionComplete() {
      return this.selGrade && this.selMajor && this.selCourse && this.selTask
    }
  },
  mounted() {
    this.$store
      .dispatch('stu/getShortCourse', { id: this.$store.state.user.id })
      .then(res => {
        this.optionsCourse = res.data.courses
        this.selCourse = this.optionsCourse[0].value
        // 请求年级和专业
        return this.$store.dispatch('stu/getGrade', {
          id: this.$store.state.user.id
        })
      })
      .then(res => {
        this.optionsGrade = res.data.grades
        this.optionsMajor = res.data.majors
        this.selGrade = this.optionsGrade[0].value
        this.selMajor = this.optionsMajor[0].value
        // 请求某个课程下的任务名们
        return this.$store.dispatch('stu/getTasksByCourse', {
          course_id: this.selCourse
        })
      })
      .then(res => {
        this.optionsTask = res.data.tasks
        this.selTask = this.optionsTask[0].value
        return this.getPageData()
      })
      .then(res => {
        this.total = res.data.total
        this.tableData = res.data.list
        const $this = this
        this.tableData.forEach((element, index) => {
          element.id = index + 1
          element.stu_major = $this.$store.state.user.major
        })
      })
      .catch(() => { return })
  },
  methods: {
    async getPageData(course) {
      return this.$store.dispatch('stu/getTableData', {
        id: this.$store.state.user.id,
        limit: this.tableLimit,
        page: this.currentPage,
        course_id: this.selCourse,
        course: course || ''
      })
    },
    fileWillRemove(file, fileList) {
      this.fileList = fileList
    },
    courseChange(v) {
      this.selCourse = v
      this.$store.dispatch('stu/getTasksByCourse', {
        course_id: this.selCourse
      }).then((res) => {
        this.optionsTask = res.data.tasks
        this.selTask = this.optionsTask[0].value
      })
    },
    Tagchange(v) {
      this.taskCourse = v
      this.getPageData(v)
        .then(res => {
          this.total = res.data.total
          this.tableData = res.data.list
          const $this = this
          this.tableData.forEach((element, index) => {
            element.id = index + 1
            element.stu_major = $this.$store.state.user.major
          })
        })
        .catch(() => { return })
    },
    handleExceed() {
      this.$message({
        message: `上传的文件数不能超过${this.limit}个`,
        type: 'warning'
      })
    },
    fileLIstChange(file, fileList) {
      if (file.raw.type.indexOf(this.accept) === 0) {
        let newSize = file.size
        fileList.forEach(item => {
          newSize += item.size
        })
        if (newSize > this.maxFileSize) {
          this.$message({
            message: `文件总大小不能超过${this.maxFileSize / 1024 / 1024}MB`,
            type: 'warning'
          })
          fileList.pop()
        } else {
          this.fileList = fileList
        }
      } else {
        this.$message({
          message: '文件类型不匹配',
          type: 'warning'
        })
        fileList.pop()
      }
    },
    stuUpload() {
      if (!this.conditionComplete) {
        return this.$message({
          message: '请填写完整表单',
          type: 'warning'
        })
      }
      if (this.fileList.length <= 0) {
        return this.$message({
          message: '至少上传一个文件',
          type: 'warning'
        })
      }
      const config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      const formData = new FormData()
      // ....
      formData.append('id', this.$store.state.user.id)
      formData.append('grade', this.selGrade)
      formData.append('major', this.selMajor)
      formData.append('course', this.selCourse)
      formData.append('task', this.selTask)
      formData.append('count', this.fileList.length)
      this.fileList.forEach((item, index) => {
        formData.append('file' + index, item.raw)
      })
      this.$store
        .dispatch('stu/uploadTask', { config, formData })
        .then(res => {
          if (res.data.message === 'ok') {
            this.$message({
              message: '提交成功',
              type: 'success'
            })
          }
          // 将新添加的这条记录添加到提交记录中
          res.data.record.id = this.tableData.length + 1
          this.tableData.push(res.data.record)
        })
        .catch(() => { return })
    }
  }
}
</script>
<style scoped>
.divider {
  border-top: 2px solid #999;
  position: relative;
}
.divider .innerHint {
  position: absolute;
  top: -20px;
  left: 40px;
  background-color: #f4f7fc;
  padding: 10px;
  font-size: 18px;
}
.main {
  padding: 30px 0 30px 0;
}
.uploader {
  padding-top: 20px;
  width: 50%;
}
</style>

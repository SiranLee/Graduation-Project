<template>
  <div>
    <el-container>
      <el-main>
        <course-detail-top :info="detailTop" @inputTrigger="handelQuest" />
        <course-detail-bottom
          :types="detailBottom.types"
          :task-types="detailBottom.taskTypes"
          :staging-list="detailBottom.stagingList"
          :source-list="detailBottom.sourceList"
          :task-list="detailBottom.taskList"
          :total="pagination.total"
          :task-total="pagination.taskTotal"
          :staging-total="pagination.stagingTotal"
          @renewList="renewList"
          @renewTasks="refreshTasks"
          @pageChange="pagechange"
          @checkPageChanged="checkPageChange"
          @taskpageChange="taskpageChange"
          @deleteResource="delRes"
          @delTask="delTask"
        />
      </el-main>
    </el-container>
  </div>
</template>
<script>
import courseDetailTop from './components/courseDetailTop'
import courseDetailBottom from './components/courseDetailBottom'
import pageConfig from '@/components/SimplePagination/pagination.config'
export default {
  name: 'Detail',
  components: {
    courseDetailTop,
    courseDetailBottom
  },
  data() {
    return {
      course_id: '',
      pagination: {
        pageSize: 8,
        stagingCurPage: 1,
        currentPage: 1,
        taskCurPage: 1,
        total: 0,
        taskTotal: 0,
        stagingTotal: 0
      },
      detailTop: {
        title: '',
        teacher: '',
        intro: '',
        cover: ''
      },
      detailBottom: {
        types: [],
        taskTypes: [],
        sourceList: [],
        taskList: [],
        stagingList: []
      }
    }
  },
  async mounted() {
    this.course_id = this.$route.params.course_id
    // 请求数据
    const res = await this.$store.dispatch('teachers/getCourseDetail', this.course_id)
    if (res.code === 20000) {
      this.detailTop = res.data
    }
    // 请求资源列表和资源类型
    const res1 = await this.$store.dispatch('teachers/getTypes')
    if (res.code === 20000) {
      this.detailBottom.types = res1.data.types
      this.detailBottom.taskTypes = res1.data.taskTypes
    }
    const res2 = await this.$store.dispatch('teachers/getSourceListType', { course_id: this.course_id, page: this.pagination.currentPage, limit: this.pagination.pageSize })
    if (res2.code === 20000) {
      this.$set(this.pagination, 'total', parseInt(res2.data.listTotal))
      this.detailBottom.sourceList = res2.data.list
      this.pagination.total = res2.data.listTotal
    }
    const res3 = await this.$store.dispatch('teachers/getStagingSources', { course_id: this.course_id, page: this.pagination.stagingCurPage, limit: this.pagination.pageSize })
    if (res3.code === 20000) {
      console.log('here')
      this.$set(this.pagination, 'stagingTotal', parseInt(res3.data.total))
      this.detailBottom.stagingList = res3.data.sources
    }

    const res4 = await this.$store.dispatch('teachers/getReleasedTasks', { course_id: this.course_id, page: this.pagination.taskCurPage, limit: this.pagination.pageSize })
    if (res4.code === 20000) {
      this.$set(this.pagination, 'taskTotal', parseInt(res4.data.listTotal))
      this.detailBottom.taskList = res4.data.list
    }
  },
  methods: {
    async pagechange(page) {
      const res2 = await this.$store.dispatch('teachers/getSourceListType', { course_id: this.course_id, page: page, limit: this.pagination.pageSize })
      if (res2.code === 20000) {
        this.$set(this.pagination, 'total', parseInt(res2.data.listTotal))
        this.detailBottom.types = res2.data.types
        res2.data.list.forEach(item => item.upload_date.substr(0, 10))
        this.detailBottom.sourceList = res2.data.list
        this.pagination.currentPage = page
      }
    },
    async checkPageChange(page) {
      this.pagination.stagingCurPage = page
      const res3 = await this.$store.dispatch('teachers/getStagingSources', { course_id: this.course_id, page: this.pagination.stagingCurPage, limit: this.pagination.pageSize })
      if (res3.code === 20000) {
        this.$set(this.pagination, 'stagingTotal', parseInt(res3.data.total))
        this.detailBottom.stagingList = res3.data.sources
      }
    },
    handelQuest(value) {
      this.$store.dispatch('teachers/setCourseInfo', value)
        .then(res => {
          this.detailTop = res.data.info
          this.detailTop.cover = res.data.filePath
          this.$message({
            message: '修改成功',
            type: 'success'
          })
        })
        .catch(err => {
          this.$message({
            message: '网络错误，请稍后重试',
            type: 'error'
          })
        })
    },
    delRes(id) {
      this.$store.dispatch('teachers/delRes', { source_id: id })
        .then(res => {
          if (res.data.message === 'ok') {
            this.$message({
              message: '删除成功',
              type: 'success'
            })
            this.detailBottom.sourceList = this.detailBottom.sourceList.filter(item => item.upload_id !== id)
          }
        })
        .catch(() => { return })
    },
    async renewList() {
      // 上传之后renew staging list
      const res2 = await this.$store.dispatch('teachers/getStagingSources', { course_id: this.course_id, page: this.pagination.currentPage, limit: this.pagination.pageSize })
      if (res2.code === 20000) {
        this.$set(this.pagination, 'stagingTotal', parseInt(res2.data.total))
        // this.$set(this.detailBottom, 'types', res2.data.types)
        this.detailBottom.stagingList = res2.data.sources
      }
    },
    // 作业相关
    async refreshTasks() {
      const res = await this.$store.dispatch('teachers/getReleasedTasks', { course_id: this.course_id, page: this.pagination.taskCurPage, limit: this.pagination.pageSize })
      if (res.code === 20000) {
        this.$set(this.pagination, 'taskTotal', parseInt(res.data.listTotal))
        this.detailBottom.taskList = res.data.list
      }
    },
    async taskpageChange(page) {
      const res2 = await this.$store.dispatch('teachers/getReleasedTasks', { course_id: this.course_id, page: page, limit: this.pagination.pageSize })
      if (res2.code === 20000) {
        this.$set(this.pagination, 'taskTotal', parseInt(res2.data.listTotal))
        this.detailBottom.taskList = res2.data.list
        this.pagination.currentPage = page
      }
    },
    delTask(id) {
      this.$store.dispatch('teachers/delTask', { task_id: id })
        .then(res => {
          if (res.data.message === 'ok') {
            this.$message({
              message: '删除成功',
              type: 'success'
            })
            this.detailBottom.taskList = this.detailBottom.taskList.filter(item => item.task_id !== id)
          }
        })
        .catch(() => { return })
    }
  }
}
</script>
<style scoped>

</style>

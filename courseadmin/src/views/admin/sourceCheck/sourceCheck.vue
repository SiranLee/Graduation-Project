<template>
  <div style="padding: 20px">
    <source-table
      :is-check="true"
      :table-data="tableData"
      :major-options="majorOptions"
      :course-options="courseOptions"
      :type-options="typeOptions"
      :status-options="statusOptions"
      :major-value="majorValue"
      :course-value="courseValue"
      :type-value="typeValue"
      :status-value="statusValue"
      :current-page="currentPage"
      :page-size="pageSize"
      :source-total="stagingFileTotal"
      @majorValueChange="majorChange"
      @courseValueChange="courseChange"
      @pageSizeChange="pageSizeChanged"
      @currentPageChange="currentPageChanged"
      @typeValueChange="typeValueChanged"
      @statusValueChange="statusValueChanged"
      @clearSelectParams="clearSelectedParams"
    />
  </div>
</template>
<script>
import sourceTable from './souceTable'
export default {
  components: {
    sourceTable
  },
  data() {
    return {
      tableData: null,
      majorOptions: [],
      courseOptions: [],
      typeOptions: [],
      statusOptions: [],
      majorValue: '',
      courseValue: '',
      typeValue: '',
      statusValue: '',
      currentPage: 1,
      pageSize: 10,
      stagingFileTotal: 0
    }
  },
  async mounted() {
    const $this = this
    const data_majors = await this.$store.dispatch('publicOpen/getAllMajors')
    data_majors.data.majors.forEach(item => {
      const dic = { label: item.title, value: item.major_id }
      $this.majorOptions.push(dic)
    })
  },
  methods: {
    // 专业改变
    async majorChange(newMajor) {
      const $this = this
      if (this.statusOptions.length === 0 && this.typeOptions.length === 0) {
        const staging_file_types = await this.$store.dispatch('admin/getStagingTypes')
        staging_file_types.data.staging_types.forEach(item => { $this.statusOptions.push({ label: item.name, value: item.value }) })
        const data_types = await this.$store.dispatch('teachers/getTypes')
        this.typeOptions = data_types.data.types
      }
      this.majorValue = newMajor
      const current_type = this.typeValue.length === 0 ? '-1' : this.typeValue
      const current_status = this.statusValue.length === 0 ? '-1' : this.statusValue
      // 请求该专业下上传的待审核的资源
      const stagingSources = await this.$store.dispatch('admin/getStagingFileUnderMajor', { major_id: this.majorValue, current_type: current_type, current_status: current_status, current_page: this.currentPage, page_size: this.pageSize })
      stagingSources.data.sources.forEach(item => item.previewLoading = false)
      this.tableData = stagingSources.data.sources
      this.stagingFileTotal = stagingSources.data.total
      // 请求该专业下的课程
      const data_courses = await this.$store.dispatch('publicOpen/getCourseInfo', { major_id: this.majorValue })
      data_courses.data.courses.forEach(item => {
        const dic = { label: item.title, value: item.course_id }
        $this.courseOptions.push(dic)
      })
    },
    // 课程改变
    async courseChange(newCourse) {
      this.courseValue = newCourse
      let current_type = this.typeValue.length === 0?'-1':this.typeValue
      let current_status = this.statusValue.length === 0?'-1':this.statusValue
      // 请求该课程下的资源
      let sources = await this.$store.dispatch('admin/getStagingSourcesUnderCourse', {course_id: this.courseValue, current_type: current_type, current_status: current_status, current_page: this.currentPage, page_size: this.pageSize})
      sources.data.sources.forEach(item => item.previewLoading = false)
      this.tableData = sources.data.sources
      this.stagingFileTotal = sources.data.total
    },
    // 页大小改变
    pageSizeChanged(newPageSize) {

    },
    // 页码改变
    currentPageChanged(newPage) {

    },
    // 类型改变
    async typeValueChanged(newType) {
      this.typeValue = newType
      let current_course = this.courseValue.length === 0?'-1':this.courseValue
      let current_status = this.statusValue.length === 0?'-1':this.statusValue
      // 请求该类型下的资源
      let sources = await this.$store.dispatch('admin/getStagingSourceUnderType', {major_id: this.majorValue, course_id: current_course, current_type: this.typeValue, current_status: current_status, current_page: this.currentPage, page_size: this.pageSize})
      sources.data.sources.forEach(item => item.previewLoading = false)
      this.tableData = sources.data.sources
      this.stagingFileTotal = sources.data.total
    },
    // 状态改变
    async statusValueChanged(newStatus) {
      this.statusValue = newStatus
      let current_type = this.typeValue.length === 0?'-1':this.typeValue
      let current_course = this.courseValue.length === 0?'-1':this.courseValue
      // 请求该状态下的资源
      let sources = await this.$store.dispatch('admin/getStagingSourceUnderStatus', {major_id: this.majorValue, course_id: current_course, current_type: current_type, current_status: this.statusValue, current_page: this.currentPage, page_size: this.pageSize})
      sources.data.sources.forEach(item => item.previewLoading = false)
      this.tableData = sources.data.sources
      this.stagingFileTotal = sources.data.total
    },
    // 清理参数
    clearSelectedParams() {
      this.majorValue = ''
      this.courseValue = ''
      this.typeValue = ''
      this.statusValue = ''
      this.typeOptions.splice(0, this.typeOptions.length)
      this.tableData.splice(0, this.tableData.length)
    }
  }
}
</script>
<style scoped>

</style>

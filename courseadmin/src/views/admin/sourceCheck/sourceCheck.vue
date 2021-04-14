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
    sourceTable,
  },
  data(){
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
      stagingFileTotal: 0,
    }
  },
  async mounted(){
    const $this = this
    const data_majors = await this.$store.dispatch('publicOpen/getAllMajors')
    data_majors.data.majors.forEach(item => {
      const dic = { label: item.title, value: item.major_id }
      $this.majorOptions.push(dic)
    })
  },
  methods:{
    // 专业改变
    async majorChange(newMajor){
      const $this = this
      if(this.statusOptions.length === 0 && this.typeOptions.length === 0){
        const staging_file_types = await this.$store.dispatch('admin/getStagingTypes')
        staging_file_types.data.staging_types.forEach(item => {$this.statusOptions.push({label: item.name, value: item.value})})
        const data_types = await this.$store.dispatch('teachers/getTypes')
        this.typeOptions = data_types.data.types
      }
      this.majorValue = newMajor
      let current_type = this.typeValue.length === 0?'-1':this.typeValue
      let current_status = this.statusValue.length === 0?'-1':this.statusValue
      // 请求该专业下上传的待审核的资源
      const data = await this.$store.dispatch('admin/getStagingFileUnderMajor', {major_id: this.majorValue, current_type: current_type, current_status: current_status, current_page: this.currentPage, page_size: this.pageSize})

    },
    // 课程改变
    courseChange(newCourse){

    },
    // 页大小改变
    pageSizeChanged(newPageSize){

    },
    // 页码改变
    currentPageChanged(newPage){
      
    },
    // 类型改变
    typeValueChanged(newType){
      this.typeValue = newType
    },
    // 状态改变
    statusValueChanged(newStatus){
      this.statusValue = newStatus
    },
    // 清理参数
    clearSelectedParams(){

    }
  }
}
</script>
<style scoped>

</style>

<template>
  <div>
    <el-pagination
      layout="prev, pager, next"
      :total="total"
      :page-size="pageSize"
      :current-page="currentPage"
      @current-change="currentChange"
    />
  </div>
</template>
<script>
import pageConfig from './pagination.config'
export default {
  props: {
    total: {
      type: Number,
      default: 0
    },
    pageSize: {
      type: Number,
      default: pageConfig.pageSize
    }
  },
  data() {
    return {
      currentPage: pageConfig.currentPage
    }
  },
  methods: {
    currentChange(page) {
      this.$emit(pageConfig.currentChange, page)
    }
  }
}
</script>
<style scoped></style>

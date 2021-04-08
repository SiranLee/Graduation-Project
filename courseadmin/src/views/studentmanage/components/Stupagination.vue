<template>
  <div>
    <el-pagination
      :current-page="currentPage"
      :page-sizes="pageSizes"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>
<script>
export default {
  props: {
    total: {
      type: Number,
      default: 0
    },
    pageSize: {
      type: Number,
      default: 0
    },
    pageSizes: {
      type: Array,
      default: () => []
    },
    currentPage: {
      type: Number,
      default: 1
    }
  },
  methods: {
    handleCurrentChange(page) {
      this.$emit('getPage', page)
    },
    handleSizeChange(size) {
      this.$emit('sizeChange', size)
    }
  }
}
</script>
<style scoped>

</style>

<template>
  <div class="pagination-container">
    <el-pagination
      background
      layout="prev, pager, next"
      :total="total"
      :page-size="pageSize"
      :pager-count="5"
      :current-page="current"
      @current-change="currentChange"
      @prev-click="prevClick"
      @next-click="nextClick"
    />
  </div>
</template>
<style scoped>
.pagination-container{
  float: right;
}
</style>
<script>
export default {
  props: {
    cols: {
      type: Number,
      default: 4
    },
    rows: {
      type: Number,
      default: 2
    },
    total: {
      type: Number,
      default: 19
    },
    currentChange: {
      type: Function,
      default: null
    },
    prevClick: {
      type: Function,
      default: null
    },
    nextClick: {
      type: Function,
      default: null
    },
    current: {
      type: Number,
      default: 1
    }
  },
  data() {
    return {
    }
  },
  computed: {
    pageSize() {
      return this.cols * this.rows
    }
  },
  methods: {

  }
}
</script>

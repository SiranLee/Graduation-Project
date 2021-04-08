<template>
  <div class="search-container">
    <el-input
      :value="value"
      :placeholder="placeholder"
      prefix-icon="el-icon-search"
      @input="searchInput"
      @keyup.enter.native="searchResult"
    />
  </div>
</template>
<style scoped>
.search-container{
  width: 20%;
  display: inline-block;
}
</style>
<script>
export default {
  props: {
    value: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: '请输入搜索的课程名'
    }
  },
  data() {
    return {
      last: ''
    }
  },
  methods: {
    searchInput(value) {
      this.$emit('update:value', value)
      this.$emit('valueChange', value)
    },
    searchResult() {
      if (!this.value.length) {
        this.$emit('emptyInput')
      }
      if (this.last !== this.value) {
        this.$emit('search', this.value)
        this.last = this.value
      }
    }
  }
}
</script>

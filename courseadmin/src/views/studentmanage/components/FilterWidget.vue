<template>
  <div>
    <el-select :size="size" :value="value" :placeholder="hint" @change="change($event)">
      <el-option
        v-for="item in options"
        :key="item.value||item.course_id"
        :label="item.label||item.title"
        :value="item.value||item.course_id"
      />
    </el-select>
  </div>
</template>
<script>
export default {
  props: {
    value: {
      type: String,
      default: ''
    },
    options: {
      type: Array,
      default: () => {}
    },
    hint: {
      type: String,
      default: ''
    },
    size: {
      type: String,
      default: ''
    },
    emitChange: {
      type: Function,
      default: () => {}
    },
    title: {
      type: String,
      default: ''
    }
  },
  methods: {
    change(value) {
      // this.$emit('input', value)
      this.emitChange(value, this.title)
    }
  }
}
</script>
<style scoped>
.el-select{
  width: 100%;
}
</style>

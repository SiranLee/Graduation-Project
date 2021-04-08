<template>
  <div @click="click">
    <el-tooltip class="item" effect="dark" :content="isFull?'恢复':'全屏'" placement="bottom">
      <svg-icon :icon-class="!isFull?'fullscreen':'shrink'" style="font-size:20px" />
    </el-tooltip>
  </div>
</template>
<script>
import screenfull from 'screenfull'
export default {
  name: 'ScreenFull',
  data() {
    return {
      isFull: false
    }
  },
  methods: {
    click() {
      if (!screenfull.isEnabled) {
        this.$message({
          message: '当前浏览器不支持全屏',
          type: 'warning'
        })
        return false
      }
      this.isFull ? screenfull.exit() : screenfull.request()
      this.isFull = !this.isFull
    }
  }
}
</script>

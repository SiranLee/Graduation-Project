<template>
  <span>
    <input ref="excel-upload-input" class="excel-upload-input" type="file" accept=".xlsx, .xls" @change="handleClick">
    <el-button :disabled="isDisable" :loading="loading" style="margin-left:16px;" type="primary" @click="handleUpload">
      导入
    </el-button>
  </span>
</template>

<script>
export default {
  props: {
    emitFile: Function,
    loading: {
      type: Boolean,
      default: false
    },
    isDisable: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {

      uploadFile: null
    }
  },
  methods: {
    handleUpload() {
      this.$refs['excel-upload-input'].click()
    },
    handleClick(e) {
      const files = e.target.files
      const rawFile = files[0]
      this.uploadFile = rawFile
      if (!rawFile) return
      this.upload(rawFile)
    },
    upload(rawFile) {
      this.$refs['excel-upload-input'].value = null
      if (!this.isExcel(rawFile)) return this.$message({ message: '请上传正确的文件', type: 'warnning' })
      if (this.emitFile) {
        this.emitFile(rawFile)
      }
    },
    isExcel(file) {
      return /\.(xlsx|xls|csv)$/.test(file.name)
    }
  }
}
</script>

<style scoped>
.excel-upload-input{
  display: none;
  z-index: -9999;
}
.drop{
  border: 2px dashed #bbb;
  width: 600px;
  height: 160px;
  line-height: 160px;
  margin: 0 auto;
  font-size: 24px;
  border-radius: 5px;
  text-align: center;
  color: #bbb;
  position: relative;
}
</style>

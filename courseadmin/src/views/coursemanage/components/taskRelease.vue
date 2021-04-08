<template>
  <div>
    <el-form :label-position="labelPosition" label-width="125px" :model="form">
      <el-form-item label="请选择任务类型">
        <el-select v-model="form.selectValue" placeholder="请选择">
          <el-option
            v-for="item in types"
            :key="item.value"
            :label="item.types_label"
            :value="item.types_value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="请填写任务标题">
        <el-input v-model="form.title" style="width: 30%;" />
      </el-form-item>
      <el-form-item label="请填写任务说明">
        <div>
          <editor :content="form.describe" :catch-data="contentChange" />
        </div>
      </el-form-item>
      <el-form-item label="任务附件上传">
        <el-upload
          class="upload-demo"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :before-remove="beforeRemove"
          multiple
          :auto-upload="false"
          :limit="maxFileCount"
          :on-change="change"
          :on-exceed="handleExceed"
          :file-list="form.fileList"
          :accept="accept"
        >
          <el-button size="small" type="primary">点击上传</el-button>
          <span
            slot="tip"
            class="el-upload__tip"
            style="margin-left:10px;"
          >单次只能上传 {{ maxFileCount }} 个文件</span>
        </el-upload>
        <el-dialog title="文件预览" :visible.sync="dialogVisible">
          <img
            style="width:100%"
            :src="previewURL"
            alt="图片预览"
            class="previewImage"
          >
        </el-dialog>
      </el-form-item>
      <el-form-item>
        <el-button
          type="success"
          :loading="submitting"
          :disabled="isDisable"
          style="width:100%;"
          @click="submit"
        >提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import editor from '@/components/Editor/Editor'
// import { format } from 'url'
export default {
  name: 'BottomBaseInfo',
  components: {
    editor
  },
  props: {
    types: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      labelPosition: 'right',
      form: {
        fileList: [],
        describe: '',
        title: '',
        selectValue: ''
      },
      accept: '*',
      dialogVisible: false,
      previewURL: '',
      submitting: false,
      maxFileCount: 5,
      maxFileSize: 1024 * 1024 * 50 // 最大文件长度为50MB
    }
  },
  computed: {
    isDisable() {
      return this.form.selectValue.length <= 0 || this.form.title.length <= 0
    }
  },
  methods: {
    handleRemove(file, fileList) {
      this.form.fileList = fileList
    },
    handlePreview(file) {
      if (file.raw.type.indexOf('image') !== 0) {
        this.$message({
          message: '此格式的文件暂不支持预览',
          type: 'warning'
        })
        return
      }
      const blob = file.raw
      const imgURL = window.URL.createObjectURL(blob)
      this.dialogVisible = true
      this.previewURL = imgURL
    },
    handleExceed(files, fileList) {
      this.$message.warning(
        `当前限制选择 ${this.maxFileCount} 个文件，本次选择了 ${
          files.length
        } 个文件，共选择了 ${files.length + fileList.length} 个文件`
      )
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`)
    },
    change(file, fileList) {
      let currentTotal = 0
      let overflow = false
      fileList.forEach(item => {
        currentTotal += item.size
        if (currentTotal > this.maxFileSize) {
          overflow = true
          return this.$message({
            message: `文件总大小不能超过 ${this.maxFileSize / 1024 / 1024}MB`,
            type: 'error'
          })
        }
      })
      if (overflow) {
        fileList.pop()
      } else {
        this.form.fileList = fileList
      }
    },
    submit() {
      this.submitting = true
      const formData = new FormData()
      // 在把文本域做成formdata就可以啦
      formData.append('describe', this.form.describe)
      formData.append('title', this.form.title)
      formData.append('course_id', this.$route.params.course_id)
      formData.append('count', this.form.fileList.length)
      formData.append('type', this.form.selectValue)
      this.form.fileList.forEach((item, index) => {
        formData.append('file' + index, item.raw)
      })
      const config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      this.$store
        .dispatch('teachers/releaseTask', { config, formData })
        .then(res => {
          this.submitting = false
          this.form.fileList = []
          this.$message({
            message: '发布成功',
            type: 'success'
          })
          this.$emit('releaseTabClick')
        })
        .catch(() => {
          this.$message({
            message: '发布失败, 请稍后重试',
            type: 'error'
          })
          this.form.fileList = []
        })
    },
    contentChange(content) {
      this.form.describe = content
    }
  }
}
</script>
<style scoped></style>

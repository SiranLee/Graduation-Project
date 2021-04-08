<template>
  <div class="outer">
    <el-row :gutter="40">
      <el-col :span="16" :offset="4">
        <el-form
          ref="pwdForm"
          v-model="form"
          status-icon
          class="pwdForm"
          label-position="right"
          label-width="120px"
        >

          <el-form-item label="请选择课程专业">
            <el-select v-model="form.major" type="password" auto-complete="off">
              <el-option
                v-for="item in options"
                :key="item.major_id"
                :label="item.title"
                :value="item.major_id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="请填写课程名称">
            <el-input v-model="form.title" style="width: 30%" auto-complete="off" />
          </el-form-item>
          <el-form-item label="请选择课程封面">
            <input id="cover" type="file" hidden @change="preview">
            <div class="coverContainer">
              <img v-if="previewURL" :src="previewURL" width="100%" height="100%" style="cursor: pointer;" @click="triggerLabel">
              <label id="trigger" for="cover" class="fileTrigger"><span v-if="!previewURL">上传图片</span></label>
            </div>
          </el-form-item>
          <el-form-item label="请填写课程大纲">
            <editor :catch-data="getContent" :content="form.intro" />
          </el-form-item>
          <el-form-item>
            <el-button type="success" style="width:100%" :loading="loading" @click="createCourse">确定</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import editor from '@/components/Editor/Editor'
export default {
  components: {
    editor
  },
  data() {
    return {
      form: {
        major: '',
        title: '',
        cover: '',
        intro: ''
      },
      loading: false,
      options: [],
      previewURL: ''
    }
  },
  mounted() {
    this.$store.dispatch('publicOpen/getAllMajors')
      .then(res => {
        this.options = res.data.majors
      })
      .catch(err => {})
  },
  methods: {
    createCourse() {
      this.loading = true
      const id = this.$store.state.user.id
      const formData = new FormData()
      formData.append('id', id)
      for (const key in this.form) {
        if (this.form.hasOwnProperty(key)) {
          formData.append(key, this.form[key])
        }
      }
      this.$store.dispatch('teachers/createCourse', formData)
        .then(res => {
          if (res.data.message === 'ok') {
            this.$message({
              message: '操作成功',
              type: 'success'
            })
            this.form.title = ''
            this.form.cover = null
            this.form.intro = ''
            this.form.major = ''
          }
        })
        .catch(err => {})
        .finally(() => {
          this.loading = false
        })
    },
    getContent(v) {
      this.form.intro = v
    },
    preview() {
      const file = document.getElementById('cover').files[0]
      if (file.type.indexOf('image') !== 0) {
        return this.$message({ message: '请上传图片文件!', type: 'warning' })
      }
      this.previewURL = URL.createObjectURL(file)
      this.form.cover = file
    },
    triggerLabel() {
      const triggerHandle = document.getElementById('trigger')
      triggerHandle.click()
    }
  }
}
</script>
<style scoped>
.outer{
  padding: 40px
}
.coverContainer{
  height: 270px;
  border: dashed #666;
  width: 440px;
}
.fileTrigger{
  text-align: center;
  display: block;
  height: 100%;
  line-height: 270px;
  width: 100%;
  cursor: pointer;
}
.coverContainer:hover{
  border: dashed #00a4ff;
}
</style>

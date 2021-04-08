<template>
  <div class="top">
    <el-dialog
      title="课程基本信息修改"
      :visible.sync="dialogVisible"
      :before-close="handleBeforClose"
      width="60%"
      top="8vh"
    >
      <form id="form" enctype="multipart/form-data" @submit.prevent="submitForm">
        <el-row :gutter="40">
          <el-col :span="8" :offset="1" class="coverPreview" style="padding: 0">
            <label for="imgUpload" class="mask">
              <img src="../../../assets/upload.png" alt>
            </label>
            <input id="imgUpload" type="file" name="coverImage" style="display:none" @input="previewImage">
            <img :src="cover" width="100%" alt>
          </el-col>
          <el-col :span="14">
            <div class="input_item">
              <label for="title">课程名称</label>
              <div>
                <input id="title" v-model="copyInfo.title" type="text">
              </div>
            </div>
            <div class="input_item">
              <label for="teacher">授课教师</label>
              <div>
                <input id="teacher" v-model="copyInfo.teacher" type="text">
              </div>
            </div>
            <div class="input_item">
              <label for="intro">课程介绍</label>
              <div>
                <editor :id="editor_id" :bars-all="false" :content="copyInfo.intro" :editor-elem="'shortInfo'" :catch-data="contentChange" class="editor" />
              </div>
            </div>
          </el-col>
        </el-row>
        <el-row>
          <button type="submit" class="submitBtn el-button el-button--success">提交</button>
        </el-row>
      </form>
    </el-dialog>
    <el-row :gutter="40">
      <el-col :span="20" :offset="2">
        <el-row class="wrapper">
          <el-col :span="8" class="cover_img">
            <img :src="infoCover">
          </el-col>
          <el-col :span="15" class="course_base_info">
            <div>
              <h2>{{ info.title }}</h2>
              <div class="course_info">
                授课教师:
                <span>{{ info.teacher }}</span>
              </div>
              <div class="course_info">
                课程介绍:
                <el-collapse v-model="collapse.activeNames" @change="handleChange">
                  <el-collapse-item :title="'点击'+collapse.tint" name="1">
                    <p class="course_intro" v-html="info.intro" />
                  </el-collapse-item>
                </el-collapse>
              </div>
            </div>
          </el-col>
        </el-row>
        <span id="edit" @click="edit">
          <svg-icon class="svg" icon-class="edit" />
        </span>
      </el-col>
    </el-row>

  </div>
</template>
<script>
import editor from '@/components/Editor/Editor'
export default {
  name: 'Top',
  components: {
    editor
  },
  props: {
    info: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      editor_id: 'short',
      course_id: this.$route.params.course_id,
      teacher_id: this.$store.state.user.id,
      collapse: {
        activeNames: [],
        status: false, // 展开是true
        tint: '展开'
      },
      dialogVisible: false,
      cover: '',
      copyInfo: {
        title: '',
        teacher: '',
        intro: '',
        cover: ''
      }
    }
  },
  computed: {
    infoCover() {
      return process.env.VUE_APP_BASE_API + this.info.cover
    }
  },
  mounted() {
    // console.log(this.info);
  },
  methods: {
    edit() {
      this.dialogVisible = true
      this.$nextTick(() => {
        document.querySelector(`#${this.editor_id}`).querySelector('.w-e-text-container').style.height = '200px'
      })
      for (const key in this.info) {
        if (this.info.hasOwnProperty(key)) {
          this.copyInfo[key] = this.info[key]
        }
      }
      this.cover = process.env.VUE_APP_BASE_API + this.info.cover
    },
    contentChange(v) {
      this.copyInfo.intro = v
    },
    handleBeforClose(done) {
      done()
    },
    handleChange() {
      this.collapse.tint = this.collapse.status ? '展开' : '收起'
      this.collapse.status = !this.collapse.status
    },
    previewImage() {
      const upload = document.getElementById('imgUpload').files[0]
      this.copyInfo.cover = upload
      this.cover = window.URL.createObjectURL(upload)
    },
    submitForm(event) {
      const headers = { 'Content-Type': 'multipart/form-data' }
      const formData = new FormData()
      formData.append('course_id', this.course_id)
      formData.append('teacher_id', this.teacher_id)
      for (const key in this.copyInfo) {
        if (this.copyInfo.hasOwnProperty(key)) {
          formData.append(key, this.copyInfo[key])
        }
      }
      this.$emit('inputTrigger', { headers, data: formData })
    }
  }
}
</script>
<style scoped>
.el-col {
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 2px 2px 10px #aaa;
  position: relative;
}
.el-col .wrapper {
  padding: 20px 0px 20px 0;
}
.el-col img {
  vertical-align: top;
  height: 300px;
  width: 100%;
}
.el-col.coverPreview {
  position: relative;
}
.el-col.cover_img{
  border: none;
  box-shadow: none;
  border-radius: 0;
}
.el-col.coverPreview .mask {
  position: absolute;
  width: 100%;
  height: 300px;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  text-align: center;
  transition: all ease 0.3s;
  cursor: pointer;
  margin-bottom: 40px;
}
.el-col.coverPreview .mask:hover {
  opacity: 1;
}
.el-col.coverPreview .mask img {
  line-height: 300px;
  width: 40px;
  height: 40px;
  margin-top: 50%;
  transform: translateY(-100%);
}
.el-collapse{
  margin-top: 10px;
}
#form .el-col{
  border: none;
  box-shadow: none;
  border-radius: 0;
}
.input_item{
  margin-left: 20px;
  height: 50px;
  margin-bottom: 20px;
  padding-right: 10px;
  padding-top: 5px;
}
.input_item label{
  float: left;
  font-size: 18px;
  width: 20%;
  text-align: center;
  line-height: 50px;
}
.input_item textarea{
  height: 100%;
}
.input_item div{
  float: right;
  width: 80%;
}
.input_item div input{
  width: 100%;
  height: 40px;
  text-indent: 10px;
  border-radius: 5px;
  outline: none;
  border: 1px solid #ccc;
}
.input_item div input:focus{
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
.input_item .editor{
  float: left;
  width: 100%;
}
.el-col .course_base_info{
  vertical-align: top;
  margin-left: 20px;
  border: none;
  box-shadow: none;
  border-radius: 0;
}
.el-col .course_base_info .course_info {
  font-size: 18px;
  margin-bottom: 20px;
  font-weight: 600;
}
.el-col .course_base_info .course_info span {
  font-size: 20px;
  font-weight: 300;
  letter-spacing: 1px;
}
.el-col .course_base_info h3 {
  font-size: 25px;
  font-weight: normal;
  color: #333;
  margin-top: 0;
}
.el-col .course_base_info.title {
  font-size: 18px;
  margin-left: 0;
}
.el-col .course_base_info .course_info .course_intro {
  margin-top: 5px;
  font-size: 18px;
  font-weight: 400;
}
.submitBtn{
  width: 100%;
  margin-top: 30px;
}

#edit {
  position: absolute;
  width: 50px;
  height: 50px;
  border-radius: 25px;
  background-color: rgba(0, 0, 0, 0.7);
  bottom: 30px;
  right: 25px;
  cursor: pointer;
}
#edit .svg {
  color: #fff;
  font-size: 24px;
  font-weight: 400;
  text-align: center;
  margin: 12px 13px;
}
</style>

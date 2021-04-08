<template>
  <div class="top">
    <el-row :gutter="40">
      <el-col :span="16" :offset="1">
        <el-row class="wrapper">
          <el-col :span="10" class="cover_img">
            <img :src="courseCover">
          </el-col>
          <el-col :span="10" class="course_base_info">
            <div>
              <div class="course_info">
                课程名称:
                <span>{{ info.title }}</span>
              </div>
              <div class="course_info">
                授课教师:
                <span>{{ info.teacher }}</span>
              </div>
            </div>
          </el-col>
        </el-row>
      </el-col>
      <el-col :span="4" class="personCount">
        <div>
          <span class="label">选课总人数</span>
          <span class="quantity">{{ info.stuTotal }}</span>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="21" :offset="1">
        <el-tabs type="border-card">
          <el-tab-pane label="课程大纲">
            <div class="sturcture" v-html="info.intro" />
          </el-tab-pane>
          <el-tab-pane label="资源列表">
            <el-select v-model="selectValue" placeholder="请选择" @change="selectChange">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
            <search :value.sync="searchValue" :placeholder="'请输入搜索的资源标题'" @emptyInput="emptyInput" @search="search" />
            <course-uploaded
              :source-list="sourceList"
              :deletable="false"
              :total="total"
              @delteResource="() => {}"
              @pageChange="pagechange"
            />
          </el-tab-pane>
          <el-tab-pane label="课程任务">
            <releasedTasks :total="taskTotal" :list="taskList" :deletable="false" @taskpageChange="taskpageChange" />
          </el-tab-pane>
        </el-tabs>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import courseUploaded from '../coursemanage/components/courseUpload'
import Search from './components/Search'
import detailConf from './detail.cofig'
import releasedTasks from '../coursemanage/components/releasedTasks'
export default {
  name: 'Top',
  components: {
    Search,
    courseUploaded,
    releasedTasks,
  },
  data() {
    return {
      // temp
      sourceList: [],
      info: {
        title: '',
        teacher: '',
        intro: '',
        cover: '',
        stuTotal: ''
      },

      options: [],
      total: 0,
      currentPage: 1,
      limit: detailConf.limit,

      taskTotal: 0,
      taskList:[],

      selectValue: '',
      searchValue: ''

    }
  },
  computed: {
    courseCover() {
      return process.env.VUE_APP_BASE_API + this.info.cover
    }
  },
  async mounted() {
    const course_id = this.$route.params.courseid
    this.$store.dispatch('publicOpen/getSourceDetailBaseInfo', { course_id: course_id })
      .then(async res => {
        if (res.data) {
          this.total = res.data.source_total
          this.info.stuTotal = res.data.stu_count
          this.info.title = res.data.course_name
          this.info.teacher = res.data.course_teacher
          this.info.cover = res.data.course_cover
          this.info.intro = res.data.course_intro
          const result = await this.$store.dispatch('teachers/getSourceListType', { course_id: course_id, page: this.currentPage, limit: this.limit })
          if (result.data) {
            this.sourceList = result.data.list
            this.total = result.data.listTotal
          }
          const types = await this.$store.dispatch('teachers/getTypes')
          if (types.data) {
            this.options = types.data.types
          }
        }
      
      })
      .catch(err => { console.log(err) })

      const res3 = await this.$store.dispatch('teachers/getReleasedTasks', { course_id: course_id, page: this.currentPage, limit: this.limit })
      if (res3.code === 20000) {
      this.taskTotal = parseInt(res3.data.listTotal)
      this.taskList = res3.data.list
    }
  },
  methods: {
    async taskpageChange(page){
      const res2 = await this.$store.dispatch('teachers/getReleasedTasks', { course_id: this.$route.params.courseid, page: page, limit: this.limit })
      if (res2.code === 20000) {
        this.taskTotal = parseInt(res2.data.listTotal)
        this.currentPage = page;
        this.taskList = res2.data.list
        this.currentPage = page
      }
    },
    pagechange(page) {
      const course_id = this.$route.params.courseid
      this.$store.dispatch('teachers/getSourceListType', { course_id: course_id, page: page, limit: this.limit })
        .then(res => {
          if (res.data) {
            this.sourceList = res.data.list
            this.total = res.data.listTotal
            this.currentPage = page
          }
        })
        .catch(err => { console.log(err) })
    },
    selectChange() {
      const course_id = this.$route.params.courseid
      console.log(this.selectValue)
      this.$store.dispatch('publicOpen/sourceFilterByType', { source_type: this.selectValue, course_id: course_id, page: 1, limit: this.limit })
        .then(res => {
          if (res.data) {
            this.sourceList = res.data.course_resourceList
            this.currentPage = 1
          }
        })
        .catch(err => { console.log(err) })
    },
    async emptyInput() {
      const result = await this.$store.dispatch('teachers/getSourceListType', { course_id: course_id, page: this.currentPage, limit: this.limit })
      if (result.data) {
        this.sourceList = result.data.list
        this.total = result.data.listTotal
      }
    },
    search() {
      console.log(this.searchValue)
      const course_id = this.$route.params.courseid
      this.$store.dispatch('publicOpen/searchSource', { key_word: this.searchValue, course_id: course_id, page: 1, limit: this.limit })
        .then(res => {
          if (res.data) {
            this.sourceList = res.data.course_resourceList
            this.total = res.data.total
            this.currentPage = 1
          }
        })
        .catch(err => { console.log(err) })
    }
  }
}
</script>
<style scoped>
.top {
  width: 100%;
  padding-top: 20px;
}
.el-row {
  margin-bottom: 10px;
}
.el-col {
  position: relative;
}
.el-col .wrapper {
  padding: 20px 20px 20px 20px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 2px 2px 10px #aaa;
}
.el-col img {
  vertical-align: top;
  height: 300px;
  width: 100%;
}
.el-col.coverPreview {
  position: relative;
}
.el-col.cover_img {
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
.el-col .course_base_info {
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
.top .personCount {
  width: 300px;
  height: 340px;
  padding: 20px 20px 20px 20px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 2px 2px 10px #aaa;
  text-align: center;
  font-size: 20px;
}
.top .personCount .label {
  display: block;
  padding-top: 80px;
  line-height: 60px;
}
.top .personCount .quantity {
  display: block;
  font-size: 60px;
  color: #ff4900;
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
.sturcture {
  width: 100%;
  padding: 10px;
  background-color: #eee;
  border-radius: 5px;
}
</style>

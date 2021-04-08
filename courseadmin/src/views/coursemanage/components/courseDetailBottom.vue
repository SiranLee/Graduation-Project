<template>
  <div class="operate">
    <el-row :gutter="40">
      <el-col :span="20" :offset="2" style="padding:0">
        <el-tabs type="border-card">
          <el-tab-pane label="资源上传">
            <course-base-info :types="types" @tabsClick="renewList" />
          </el-tab-pane>
          <el-tab-pane label="已上传的资源">
            <course-uploaded :source-list="sourceList" :total="total" @deleteResource="deleteRes" @pageChange="pagechange" />
          </el-tab-pane>
          <el-tab-pane label="发布任务">
            <taskRelease :types="taskTypes" @releaseTabClick="refreshReleasedTasks" />
          </el-tab-pane>
          <el-tab-pane label="已发布任务">
            <releasedTasks :total="taskTotal" :list="taskList" @deleteTask="delTask" @taskpageChange="taskpageChange" />
          </el-tab-pane>
        </el-tabs>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import courseBaseInfo from '../components/courseBaseInfo'
import courseUploaded from '../components/courseUpload'
import taskRelease from './taskRelease'
import releasedTasks from './releasedTasks'
export default {
  name: 'Bottom',
  components: {
    taskRelease,
    courseUploaded,
    courseBaseInfo,
    releasedTasks
  },
  props: {
    types: {
      type: Array,
      default: () => []
    },
    taskTypes: {
      type: Array,
      default: () => []
    },
    sourceList: {
      type: Array,
      default: () => []
    },
    total: {
      type: Number,
      default: 0
    },
    taskTotal: {
      type: Number,
      default: 0
    },
    taskList: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    deleteRes(item) {
      this.$emit('deleteResource', item)
    },
    pagechange(page) {
      this.$emit('pageChange', page)
    },
    renewList() {
      this.$emit('renewList')
    },
    refreshReleasedTasks() {
      this.$emit('renewTasks')
    },
    taskpageChange(page) {
      this.$emit('taskpageChange', page)
    },
    delTask(item) {
      this.$emit('delTask', item)
    }
  }
}
</script>
<style scoped>
.el-main .operate .el-row {
  margin-top: 20px;
}
.coverPreview {
  height: 400px;
  background-color: red;
}
.infoForm {
  height: 400px;
  background-color: blue;
}
</style>

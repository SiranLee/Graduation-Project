<template>
  <div>
    <el-card :body-style="{ padding: '0px' }">
      <div class="head">
        <span class="cover"><i>{{ item.title }}</i></span>
        <img :src="courseCover" class="image" style="width:100%;height:270px;">
      </div>
      <div style="padding: 14px;">
        <router-link tag="button" :to="'/detail/'+item.course_id" class="el-button el-button--primary">查看详情</router-link>
        <el-button type="danger" class="delete" @click="deleteCourse">删除课程</el-button>
      </div>
    </el-card>
  </div>
</template>
<script>
export default {
  props: {
    item: {
      type: Object,
      default: () => {}
    }
  },
  computed: {
    courseCover() {
      return process.env.VUE_APP_BASE_API + this.item.cover_link
    }
  },
  mounted() {

  },
  methods: {
    deleteCourse() {
      this.$confirm('此操作将会删除该课程,是否继续', '提示', {
        confirmButtonText: '确定',
        candelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          return this.$store.dispatch('teachers/deleteCourse', { course_id: this.item.course_id, id: this.$store.state.user.id })
        })
        .then(res => {
          if (res.data.message === 'ok') {
            this.$message({ message: '删除成功', type: 'success' })
            this.$emit('deleteCourse', this.item.course_id)
          }
        })
        .catch(() => {})
    }
  }
}
</script>
<style scoped>
.el-card{
    border-radius: 5px;
    box-shadow: 0 10px 10px 0 rgba(0,0,0,.1);
}
.el-card .el-card__body img{
    width: 100%;
    vertical-align: top
}
.el-card .el-card__body .el-button{
    display: block;
    width: 100%;
}
.el-card .head {
    position: relative;
}
.el-card .cover {
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 100%;
    background-color: rgba(0,0,0,.5);
}
.el-card span i {
    position: absolute;
    font-style: normal;
    font-size: 25px;
    color: #fff;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%)
}
.el-button.delete{
  margin-left: 0px;
  margin-top: 10px;
}
</style>

<template>
  <div>
    <course-list :items="courses" />
  </div>
</template>
<script>
import courseList from './components/courseList'
export default {
  components: {
    courseList
  },
  data() {
    return {
      courses: []
    }
  },
  mounted() {
    this.$store.dispatch('teachers/getCourse', this.$store.state.user.id).then(res => {
      this.courses = res.data.course
    }).catch(err => {
      this.$message({
        message: '出错啦,' + err.message,
        type: 'error',
        showClose: true
      })
    })
  }
}
</script>
<style scoped>

</style>

<template>
  <div>
    <el-row :gutter="gutter">
      <el-col v-for="item in items" :key="item.course_id" :span="24/cols">
        <course-item :item="item" @deleteCourse="deleteCourse" />
      </el-col>
    </el-row>
  </div>
</template>
<script>
import courseItem from './courseItem'
import pagination from '@/views/sourcelist/components/Pagenation'
export default {
  components: {
    courseItem
  },
  props: {
    items: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      gutter: 40
    }
  },
  computed: {
    cols() {
      return 3
    }
  },
  methods: {
    deleteCourse(id) {
      this.items = this.items.filter(item => item.course_id !== id)
    }
  }
}
</script>
<style scoped>
.el-row{
  padding: 40px 40px 20px ;
}
.el-col{
  margin-bottom: 40px;
}

</style>

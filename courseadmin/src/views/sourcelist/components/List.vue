<template>
  <div>
    <el-row :gutter="gutter">
      <el-col v-for="item in items" :key="item.id" :span="24/cols">
        <list-item :item="item" />
      </el-col>
    </el-row>
  </div>
</template>
<script>
import ListItem from './ListItem'
export default {
  components: {
    ListItem
  },
  props: {
    cols: {
      type: Number,
      default: 0
    },
    rows: {
      type: Number,
      default: 0
    },
    gutter: {
      type: Number,
      default: 20
    },
    items: {
      type: Array,
      default: () => []
    }
  }
}
</script>
<style scoped>

</style>

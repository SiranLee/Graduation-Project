<template>
  <div>
    <el-table
      v-loading="tableLoading"
      :data="tableData"
      border
      style="width: 100%"
    >
      <el-table-column
        prop="id"
        label="序号"
        align="center"
        width="180"
      />
      <el-table-column
        prop="stu_number"
        label="学号"
        align="center"
        width="180"
      />
      <el-table-column
        prop="stu_grade"
        label="年级"
        align="center"
        width="180"
      />
      <el-table-column
        prop="stu_major"
        label="专业"
        align="center"
        width="180"
      />
      <el-table-column
        prop="stu_class"
        label="班级"
        align="center"
        width="180"
      />
      <el-table-column
        prop="name"
        align="center"
        label="姓名"
      />
      <el-table-column
        prop="course"
        align="center"
        label="课程"
      />
      <el-table-column
        prop="operate"
        align="center"
        label="操作"
      >
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="$emit('operation',row,0)">
            编辑
          </el-button>
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="$emit('operation',row,1)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
export default {
  props: {
    tableData: {
      type: Array,
      default: () => []
    },
    tableLoading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
    }
  }
}
</script>
<style scoped>

</style>

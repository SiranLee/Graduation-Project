<template>
  <div>
    <div class="top_choose_bar">
      <el-select :value="majorValue" placeholder="请选择专业" @change="majorValueChange">
        <el-option
          v-for="item in majorOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-select :value="courseValue" placeholder="请选择课程" @change="courseValueChange">
        <el-option
          v-for="item in courseOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-select :value="typeValue" placeholder="请选择资源类型" @change="typeValueChange">
        <el-option
          v-for="item in typeOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-select
        v-if="isCheck"
        :value="statusValue"
        placeholder="请选择资源状态"
        @change="statusValueChange"
      >
        <el-option
          v-for="item in statusOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-button type="warning" @click="clearSelectParams">清空所选参数</el-button>
    </div>
    <div class="paginationContainer">
      <el-pagination
        :current-page="currentPage"
        :page-sizes="[10, 20, 30, 40]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="sourceTotal"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
    <el-table :data="tableData" border style="width: 100%">
      <el-table-column
        prop="up_date"
        label="上传日期"
        align="center"
      />
      <el-table-column
        prop="source_type"
        label="资源类型"
        align="center"
      />
      <el-table-column align="center" prop="source_title" label="资源标题" />
      <el-table-column align="center" prop="source_name" label="资源名称" />
      <el-table-column align="center" prop="source_course" label="资源所在课程" />
      <el-table-column
        v-if="isCheck"
        align="center"
        prop="source_status"
        label="资源状态"
      />
      <el-table-column
        v-if="isBrowse"
        prop="source_download_time"
        label="资源下载次数"
        align="center"
      />
      <el-table-column v-if="isCheck" align="center" label="资源可见性">
        <template slot-scope="scope">
          <span v-if="scope.row.not_available2all">仅该课程学生可见</span>
          <span v-if="!scope.row.not_available2all">任何学生可见</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="资源说明">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="browseSourceDes(scope.row)">查看</el-button>
        </template>
      </el-table-column>
      <el-table-column
        v-if="isCheck"
        align="center"
        label="资源预览"
      >
        <template slot-scope="scope">
          <el-button type="primary" @click="openOrDownload(scope.source_link)">预览</el-button>
        </template>
      </el-table-column>
      <el-table-column
        v-if="isCheck"
        align="center"
        label="操作"
      >
        <template slot-scope="scope">
          <el-button type="danger" @click="failPass(scope.source_id)">打 回</el-button>
          <el-button type="success" @click="sourcePass(scope.source_id)">通 过</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-if="isCheck"
      title="打回原因"
      :visible.sync="dialogVisible"
      width="50%"
    >
      <el-input v-model="reasonForFail" placeholder="请填写打回原因" />
      <span slot="footer" class="dialog-footer">
        <el-button type="success" @click="submitReason">提 交</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="资源说明"
      :visible.sync="sourceDesDialogVisible"
      width="40%"
    >
      <div v-html="sourceDes" />
    </el-dialog>

  </div>
</template>
<script>
export default {

  props: {
    isCheck: {
      type: Boolean,
      default: false
    },
    isBrowse: {
      type: Boolean,
      default: false
    },
    tableData: {
      type: Array,
      default: () => []
    },
    majorOptions: {
      type: Array,
      default: () => []
    },
    courseOptions: {
      type: Array,
      default: () => []
    },
    typeOptions: {
      type: Array,
      default: () => []
    },
    statusOptions: {
      type: Array,
      default: () => []
    },
    majorValue: {
      type: String,
      default: ''
    },
    courseValue: {
      type: String,
      default: ''
    },
    typeValue: {
      type: String,
      default: ''
    },
    statusValue: {
      type: String,
      default: ''
    },
    currentPage: {
      type: Number,
      default: 1
    },
    pageSize: {
      type: Number,
      default: 10
    },
    sourceTotal: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      sourceDesDialogVisible: false,
      dialogVisible: false,
      reasonForFail: '',
      sourceDes: '',
      currentSourceId: ''
    }
  },
  mounted() {
    // 请求数据
  },
  methods: {
    majorValueChange(newMajor) {
      this.$emit('majorValueChange', newMajor)
    },
    courseValueChange(newCourse) {
      this.$emit('courseValueChange', newCourse)
    },
    typeValueChange(newType) {
      this.$emit('typeValueChange', newType)
    },
    statusValueChange(newStatus) {
      this.$emit('statusValueChange', newStatus)
    },
    handleSizeChange(newSize) {
      this.$emit('pageSizeChange', newSize)
    },
    handleCurrentChange(newPage) {
      this.$emit('currentPageChange', newPage)
    },
    clearSelectParams() {
      this.$emit('clearSelectParams')
    },
    openOrDownload(url) {

    },
    failPass(sourceId) {
      this.dialogVisible = false
      this.currentSourceId = sourceId
    },
    submitReason() {
      // 资源未通过提交错误信息
    },
    sourcePass(sourceId) {
      // 资源通过
      this.currentSourceId = sourceId
    },
    browseSourceDes(row) {
      this.sourceDesDialogVisible = true
      this.sourceDes = row.source_des
    }
  }
}
</script>
<style scoped>
.top_choose_bar {
  margin-bottom: 40px;
}
.paginationContainer{
  margin-bottom: 20px;
}
</style>

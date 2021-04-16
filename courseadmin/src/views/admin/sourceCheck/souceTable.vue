<template>
  <div>
    <div class="top_choose_bar">
      <el-select
        :value="majorValue"
        placeholder="请选择专业"
        @change="majorValueChange"
      >
        <el-option
          v-for="item in majorOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-select
        :value="courseValue"
        placeholder="请选择课程"
        @change="courseValueChange"
      >
        <el-option
          v-for="item in courseOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-select
        :value="typeValue"
        placeholder="请选择资源类型"
        @change="typeValueChange"
      >
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
      <el-button
        type="warning"
        @click="clearSelectParams"
      >清空所选参数</el-button>
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
      <el-table-column prop="up_date" label="上传日期" align="center" />
      <el-table-column prop="source_type" label="资源类型" align="center" />
      <el-table-column align="center" prop="source_title" label="资源标题" />
      <el-table-column align="center" prop="source_name" label="资源名称" />
      <el-table-column
        align="center"
        prop="source_course"
        label="资源所在课程"
      />
      <el-table-column
        v-if="isCheck"
        align="center"
        prop="source_status"
        label="资源状态"
      >
        <template slot-scope="scope">
          <el-tag
            v-if="scope.row.source_status == 1"
            type="info"
          >待审核</el-tag>
          <el-tag
            v-if="scope.row.source_status == 2"
            type="success"
          >通过</el-tag>
          <el-tag
            v-if="scope.row.source_status == 3"
            type="danger"
          >未通过</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        v-if="isBrowse"
        prop="source_download_time"
        label="资源下载次数"
        align="center"
      />
      <el-table-column v-if="isCheck" align="center" label="资源可见性">
        <template slot-scope="scope">
          <span
            v-if="scope.row.source_not_available2all"
          >仅该课程学生可见</span>
          <span v-if="!scope.row.source_not_available2all">任何学生可见</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="资源说明">
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="small"
            @click="browseSourceDes(scope.row)"
          >查看</el-button>
        </template>
      </el-table-column>
      <el-table-column v-if="isCheck" align="center" label="资源预览">
        <template slot-scope="scope">
          <el-button
            :disabled="scope.row.source_status === 2"
            type="primary"
            size="small"
            :loading="scope.row.previewLoading"
            @click="openOrDownload(scope.row)"
          >预览</el-button>
        </template>
      </el-table-column>
      <el-table-column v-if="isCheck" align="center" label="操作" width="270">
        <template slot-scope="scope">
          <el-button
            type="danger"
            size="small"
            v-if="scope.row.source_status === 1"
            @click="failPass(scope.row.source_id)"
          >打 回</el-button>
          <el-button
            :disabled="scope.row.source_status===2"
            type="success"
            size="small"
            @click="sourcePass(scope.row.source_id)"
          >通 过</el-button>
          <el-button
            v-if="scope.row.source_status === 2"
            type="danger"
            size="small"
            @click="deletePassStaging(scope.row)"
          >删除此记录</el-button>
          <el-button 
            v-if="scope.row.source_status === 3"
            type="info"
            size="small"
            @click="showFailReason(scope.row)"
          >查 看 原 因</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-if="isCheck"
      title="打回原因"
      :visible.sync="dialogVisible"
      :before-close="handleClose"
      width="50%"
    >
      <el-input :disabled="viewReason" v-model="reasonForFail" placeholder="请填写打回原因" />
      <span slot="footer" class="dialog-footer">
        <el-button type="success" @click="submitReason" :disabled="reasonForFail.length === 0 || viewReason">提 交</el-button>
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
import { registerCoordinateSystem } from 'echarts'
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
      rootLink: '',
      sourceDesDialogVisible: false,
      dialogVisible: false,
      reasonForFail: '',
      sourceDes: '',
      currentSourceId: '',
      viewReason: false,
    }
  },
  mounted() {
    // 请求数据
    this.rootLink = process.env.VUE_APP_BASE_API
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
    openOrDownload(row) {
      const type = row.source_name.substring(row.source_name.lastIndexOf('.'))
      if (row.source_type == '图片' || row.source_type == '视频' || type == '.pdf') {
        window.open(this.rootLink + row.source_link)
        return
      }
      row.previewLoading = true
      this.$store
        .dispatch('admin/previewStagingSource', {
          id: row.source_id,
          link: row.source_link,
          name: row.source_name
        })
        .then((res) => {
          const url = res.data.preview_link
          row.previewLoading = false
          window.open(this.rootLink + url)
        })
        .catch((err) => {
          this.$message({
            message: '出现错误，请刷新后稍后重试',
            type: 'warning'
          })
          row.previewLoading = false
        })
    },
    failPass(sourceId) {
      this.reasonForFail = ''
      this.dialogVisible = true
      this.currentSourceId = sourceId
    },
    submitReason() {
      // 资源未通过提交错误信息
      this.$emit('statusChange', {isFail: true, reasonForFail:this.reasonForFail, staging_id:this.currentSourceId})
    },
    sourcePass(sourceId) {
      // 资源通过
      this.currentSourceId = sourceId
      this.$emit('statusChange', {isFail: false, reasonForFail: this.reasonForFail, staging_id:this.currentSourceId})
    },
    browseSourceDes(row) {
      this.sourceDesDialogVisible = true
      this.sourceDes = row.source_des
    },
    deletePassStaging(row){},
    showFailReason(row){
      this.viewReason = true
      this.reasonForFail = row.source_fail_resaon
      this.dialogVisible = true
    },
    handleClose(done){
      this.viewReason = false
      done()
    }
  }
}
</script>
<style scoped>
.top_choose_bar {
  margin-bottom: 40px;
}
.paginationContainer {
  margin-bottom: 20px;
}
</style>

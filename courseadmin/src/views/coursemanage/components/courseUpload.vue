<template>
  <div>
    <el-row>
      <el-col :span="10" class="pagination">
        <pagination
          :total="total"
          @pageChange="pageChange"
        />
      </el-col>
    </el-row>
    <el-table :data="sourceList" stripe :default-sort="{ prop: 'upload_date', order: 'descending' }" style="width: 100%">
      <el-table-column
        align="center"
        prop="upload_date"
        label="上传日期"
        sortable
      />
      <el-table-column
        align="center"
        prop="upload_type"
        label="资源类型"
      />
      <el-table-column
        align="center"
        prop="upload_title"
        label="资源标题"
      />
      <el-table-column align="center" label="资源文件">
        <template slot-scope="scope">
          <span>{{ scope.row.upload_filename }}</span>
        </template>
      </el-table-column>
      <el-table-column v-if="!notCheck" align="center" label="资源状态" width="150">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.upload_status===1" type="warning">审核中</el-tag>
          <el-tag v-if="scope.row.upload_status===3" type="danger">未通过</el-tag>
          <el-button v-if="scope.row.upload_status===3" size="mini" @click="checkReason(scope.row)">原因</el-button>
        </template>
      </el-table-column>
      <el-table-column v-if="!notCheck" align="center" label="资源可见性">
        <template slot-scope="scope">
          <span v-if="scope.row.not_available2all">仅该课程学生可见</span>
          <span v-if="!scope.row.not_available2all">任何学生可见</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="资源说明">
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="small"
            @click="browseExplain(scope.row)"
          >查看</el-button>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="270">
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="small"
            @click="downloadFile(link + scope.row.upload_filelink)"
          >下载</el-button>
          <el-button
            v-if="deletable"
            type="danger"
            size="small"
            @click="remove(scope.row.upload_id)"
          >删除</el-button>
          <el-popover
            v-if="deletable && notCheck"
            placement="top"
            width="150"
            trigger="click"
          >
            <el-switch v-model="scope.row.read_limit" style="display: block; text-align:center" active-text="是" inactive-text="否" active-color="#13ce66" inactive-color="#ccc" @change="switchValueChanged(scope.row)" />
            <p style="text-align: center; font-weight: bolder; margin-block-end: 0;">仅该课程学生可见</p>
            <el-button slot="reference" size="small">设置可见性</el-button>
          </el-popover>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      title="资源说明"
      :visible.sync="dialogVisible"
      width="30%"
    >
      <div class="sourceIntro" v-html="sourceEx" />
    </el-dialog>
    <el-dialog
      title="未通过原因"
      :visible.sync="reasonDialogVisible"
      width="30%"
    >
    {{ reason }}
    </el-dialog>
  </div>
</template>
<script>
import pagination from '@/components/SimplePagination'
import paginationConfig from '../../../components/SimplePagination/pagination.config'

export default {
  components: {
    pagination
  },
  props: {
    sourceList: {
      type: Array,
      default: () => []
    },
    total: {
      type: Number,
      default: 0
    },
    deletable: {
      type: Boolean,
      default: true
    },
    notCheck: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      dialogVisible: false,
      sourceEx: '',
      reasonDialogVisible: false,
      reason: ''
    }
  },
  computed: {
    link() {
      return process.env.VUE_APP_BASE_API
    }
  },
  methods: {
    pageChange(page) {
      if (this.notCheck) {
        this.$emit('pageChange', page)
      } else {
        this.$emit('checkPageChange', page)
      }
    },
    remove(row) {
      this.$confirm('此操作将会删除数据,是否继续', '警告', {
        confirmButtonText: '继续',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.$emit('deleteResource', row)
        })
        .catch(() => {})
    },
    browseExplain(row) {
      this.dialogVisible = true
      this.sourceEx = row.upload_intro
    },
    downloadFile(url) {
      window.open(url)
    },
    async switchValueChanged(row) {
      const { data } = await this.$store.dispatch('teachers/modifySourceReadLimit', { source_id: row.upload_id, read_limit: row.read_limit })
      if (data.message === 'ok') {
        this.$message({
          message: '设置成功',
          type: 'success'
        })
      }
    },
    checkReason(row){
      this.reason = ''
      this.reasonDialogVisible = true
      this.reason = row.upload_fail_reason
    }
  }
}
</script>
<style scoped>
.sourceIntro{
  padding: 5px;
  background-color: #eee;
  border-radius: 5px;
}
.pagination{
  padding-left: 0%;
}
.downloadLink:hover{
  color: #00a4ff;
  text-decoration: underline;
}
</style>

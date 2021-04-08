<template>
  <div>
    <el-row>
      <el-col :span="10" class="pagination">
        <pagination :total="total" @pageChange="pageChange" />
      </el-col>
    </el-row>
    <el-table
      :data="list"
      stripe
      :default-sort="{ prop: 'upload_date', order: 'descending' }"
      style="width: 100%"
    >
      <el-table-column
        align="center"
        prop="release_time"
        label="发布日期"
        width="220"
        sortable
      />
      <el-table-column
        align="center"
        prop="task_type"
        label="任务类型"
        width="200"
      />
      <el-table-column
        align="center"
        prop="task_title"
        label="任务标题"
        width="200"
      />
      <el-table-column align="center" label="任务文件" width="200">
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="small"
            @click="showFileTale(scope.row)"
          >查看</el-button>
        </template>
      </el-table-column>
      <el-table-column align="center" label="任务说明" width="200">
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="small"
            @click="browseExplain(scope.row)"
          >查看</el-button>
        </template>
      </el-table-column>
      <el-table-column v-if="deletable" align="center" label="操作">
        <template slot-scope="scope">
          <el-button
            type="danger"
            size="small"
            @click="remove(scope.row.task_id)"
            
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog title="任务说明" :visible.sync="dialogVisible" width="30%">
      <div class="sourceIntro" v-html="sourceEx" />
    </el-dialog>
    <el-dialog title="附件列表" :visible.sync="fileDialogVisible" width="40%">
      <el-table :data="sourceList">
        <el-table-column
          align="center"
          prop="id"
          label="序号"
          width="200"
        />
        <el-table-column
          align="center"
          prop="task_title"
          label="任务标题"
          width="200"
        />
        <el-table-column align="center" label="附件链接">
          <template slot-scope="scope">
            <a
              class="downloadLink"
              :href="link + scope.row.task_filelink"
              :download="link + scope.row.task_filename"
            >{{ scope.row.task_filename }}</a>
          </template>
        </el-table-column>
        <el-table-column align="center" label="操作" v-if="deletable">
          <template slot-scope="scope">
            <el-button
              type="danger"
              size="small"
              @click="removeFile(scope.row)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>
<script>
import pagination from '@/components/SimplePagination'
// import paginationConfig from '../../../components/SimplePagination/pagination.config'

export default {
  components: {
    pagination
  },
  props: {
    list: {
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
  },
  data() {
    return {
      fileDialogVisible: false,
      dialogVisible: false,
      sourceEx: '',
      sourceList: [],
      currrentRowId: ''
    }
  },
  computed: {
    link() {
      return process.env.VUE_APP_BASE_API
    }
  },
  methods: {
    pageChange(page) {
      this.$emit('taskpageChange', page)
    },
    remove(row) {
      this.$confirm('此操作将会删除数据,是否继续', '警告', {
        confirmButtonText: '继续',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.$emit('deleteTask', row)
        })
        .catch(() => {})
    },
    browseExplain(row) {
      this.dialogVisible = true
      this.sourceEx = row.task_intro
    },
    showFileTale(row) {
      this.$store
        .dispatch('teachers/getFiles', { task_id: row.task_id })
        .then(res => {
          this.fileDialogVisible = true
          this.sourceList = row.fileList
          this.currrentRowId = row.task_id
          res.data.fileList.forEach((item, index) => { item.id = index + 1 })
          this.sourceList = res.data.fileList
        })
        .catch(() => { return })
    },
    removeFile(row) {
      this.$store.dispatch('teachers/deleteFileByTask', { task_id: this.currrentRowId, file_id: row.file_id })
        .then(res => {
          if (res.data.message === 'ok') {
            this.$message({
              message: '删除成功',
              type: 'success'
            })
            this.sourceList = this.sourceList.filter(item => { item.file_id !== row.file_id })
          }
        })
        .catch(() => { return })
    }
  }
}
</script>
<style>
.sourceIntro {
  padding: 5px;
  background-color: #eee;
  border-radius: 5px;
}
.pagination {
  padding-left: 0%;
}
.downloadLink:hover {
  color: #00a4ff;
  text-decoration: underline;
}
</style>

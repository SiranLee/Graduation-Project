<template>
  <div v-loading="itemsLoading">
    <el-container>
      <el-header style="height: 100%">
        <search :value.sync="keyWord" @search="searchResult" @valueChange="change" />
        <pagination
          v-show="total"
          :total="aboutTotal"
          :current-change="currentChange"
          :prev-click="()=>{}"
          :next-click="()=>{}"
          :current="cur"
        />
      </el-header>
      <keep-alive>
        <el-main>
          <list :cols="cols" :rows="rows" :gutter="gutter" :items="items" />
        </el-main>
      </keep-alive>
    </el-container>
  </div>
</template>
<script>
import Search from './components/Search'
import Pagination from './components/Pagenation'
import List from './components/List'
import detailConf from './detail.cofig'
export default {
  components: {
    Search,
    Pagination,
    List
  },
  data() {
    return {
      gutter: detailConf.listItemGutter,

      keyWord: '',
      major_id: '',

      cols: detailConf.cols,
      rows: detailConf.rows,
      items: [],
      total: 0,
      lastPage: 0,

      itemsLoading: true
    }
  },
  computed: {
    aboutTotal: {
      get: function() {
        return this.total
      },
      set: function(v) {
        this.total = v
      }
    },
    cur: {
      get: function() {
        return this.$router.history.current.meta.currentPage
      },
      set: function(v) {
        this.$router.history.current.meta.currentPage = v
      }
    }
  },
  mounted() {
    this.itemsLoading = true
    this.$store.dispatch('publicOpen/getAllMajors')
      .then(res => {
        this.major_id = res.data.majors.find(item => item.title === this.$route.meta.title).major_id
        if (this.major_id.length > 0) {
          return this.getData(this.major_id, this.cur, this.cols * this.rows)
        }
      })
      .then(res => {
        this.total = res.data.total
        this.items = res.data.courses
      })
      .catch(err => {
      }).finally(() => {
        this.itemsLoading = false
      })
  },
  methods: {
    async getData(start, page, limit) {
      this.itemsLoading = true
      const result = await this.$store.dispatch('publicOpen/getAllCourse', { major_id: start, page: page, limit: limit })
      if (result.data) {
        this.$message({
          message: '请求成功',
          type: 'success'
        })
        return result
      }
      return Promise.reject(result)
    },
    async change(value) {
      if (value.length === 0) {
        const { data } = await this.getData(this.major_id, 1, this.rows * this.cols)
        this.items = data.courses
        this.total = data.total
        this.itemsLoading = false
      }
    },
    currentChange(page) {
      this.itemsLoading = true
      if (this.lastPage === page) {
        this.itemsLoading = false
        return
      }
      this.getData(this.major_id, page, this.cols * this.rows).then(res => {
        this.cur = page
        this.lastPage = page
        this.items = res.data.courses
      }).catch(err => {
        this.cur = page - 1 > 0 ? page - 1 : 1
      }).finally(() => {
        this.itemsLoading = false
      })
    },
    searchResult() {
      this.$store.dispatch('publicOpen/searchByKeyWord', this.keyWord)
        .then(res => {
          this.items = res.data.courses
          this.total = res.data.total
        })
        .catch(err => {})
    }
  }
}
</script>
<style scoped>
.el-header{
  padding: 40px 40px 20px 40px;
  overflow: hidden;
}
.el-main{
  padding: 0 40px;
}
</style>

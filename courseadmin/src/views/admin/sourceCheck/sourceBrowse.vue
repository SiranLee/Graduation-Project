<template>
  <div style="padding: 20px">
    <div style="margin-bottom: 30px">
      <source-table
        :is-browse="true"
        :table-data="tableData"
        :major-options="majorOptions"
        :course-options="courseOptions"
        :type-options="typeOptions"
        :major-value="majorValue"
        :course-value="courseValue"
        :type-value="typeValue"
        :current-page="currentPage"
        :page-size="pageSize"
        :source-total="sourceTotal"
        @majorValueChange="majorChange"
        @courseValueChange="courseChange"
        @pageSizeChange="pageSizeChanged"
        @currentPageChange="currentPageChanged"
        @typeValueChange="typeValueChanged"
        @clearSelectParams="clearSelectedParams"
      />
    </div>
    <div class="chartView">
      <el-row :gutter="30">
        <el-col :span="9"><div id="pie" /></el-col>
        <el-col :span="15"><div id="calender" /></el-col>
      </el-row>
    </div>
  </div>
</template>
<script>
import * as echarts from 'echarts/lib/echarts'
import grid from 'echarts/lib/component/grid'
import * as pie from 'echarts/lib/chart/pie'
import * as visualMap from 'echarts/lib/component/visualMap'
import * as calenderHeatMap from 'echarts/lib/chart/heatmap'
import * as calendar from 'echarts/lib/component/calendar'
import title from 'echarts/lib/component/title'
import legend from 'echarts/lib/component/legend'
import tooltip from 'echarts/lib/component/tooltip'
import toolbox from 'echarts/lib/component/toolbox'
import sourceTable from './souceTable'

export default {
  components: {
    sourceTable
  },
  data() {
    return {
      tableData: null,
      majorOptions: [],
      courseOptions: [],
      typeOptions: [],
      majorValue: '',
      courseValue: '',
      typeValue: '',
      currentPage: 1,
      pageSize: 10,
      sourceTotal: 0,
      pieData: [],
      heatChartData: []
    }
  },
  async mounted() {
    const $this = this
    // 请求专业
    const data_majors = await this.$store.dispatch('publicOpen/getAllMajors')
    data_majors.data.majors.forEach(item => {
      const dic = { label: item.title, value: item.major_id }
      $this.majorOptions.push(dic)
    })
    // const data_courses = await this.$store.dispatch('publicOpen/get_courseinfo',{major_id: })
  },
  methods: {
    // 请求数据 当专业，课程改变后重新画饼图
    drawPie() {
      const option = {
        title: {
          text: '各类型资源占比',
          left: 'center',
          padding: [25, 0, 0, 0]
        },
        toolbox: {
          show: true,
          feature: {
            saveAsImage: {
              // 保存图片
              show: true
            }
          }
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'horizontal',
          left: 'center',
          bottom: '10px'
        },
        series: [
          {
            name: '资源类别',
            type: 'pie',
            radius: '50%',
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 1
            },
            data: this.pieData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      const pieChart = echarts.init(document.getElementById('pie'))
      pieChart.setOption(option)
    },
    // 当课程确定后，画日历热力图
    drawCalenderHeat() {
      const option = {
        title: {
          top: 50,
          left: 'center',
          text: '年度资源提交热力图'
        },
        tooltip: {
          position: 'top',
          formatter: function(p) {
            var format = echarts.format.formatTime('yyyy-MM-dd', p.data[0])
            return format + ': ' + p.data[1] + '次'
          }
        },
        visualMap: {
          min: 0,
          max: 40,
          type: 'piecewise',
          orient: 'horizontal',
          left: 'center',
          bottom: 50,
          inRange: {
            color: ['#C7DBFF', '#1989fc']
          }
        },
        calendar: {
          top: 130,
          left: 40,
          right: 30,
          height: 140,
          cellSize: ['auto', 14],
          range: '2021',
          itemStyle: {
            borderWidth: 0.5
          },
          yearLabel: { show: false },
          splitLine: {
            show: true,
            lineStyle: {
              width: 0.5,
              color: '#888'
            }
          }
        },
        series: {
          type: 'heatmap',
          coordinateSystem: 'calendar',
          data: this.heatChartData
        }
      }
      const heatMapChart = echarts.init(document.getElementById('calender'))
      heatMapChart.setOption(option)
    },
    // 专业改变
    async majorChange(newMajor) {
      const $this = this
      // 请求资源类型
      if (this.typeOptions.length === 0) {
        const data_types = await this.$store.dispatch('teachers/getTypes')
        this.pieData.splice(0, this.pieData.length)
        this.typeOptions = data_types.data.types
        this.typeOptions.forEach(item => $this.pieData.push({ name: item.label, value: 0 }))
      }
      // 清理上一次的记录
      this.pieData.forEach(item => item.value = 0)
      this.heatChartData.splice(0, this.heatChartData.length)
      this.courseOptions.splice(0, this.courseOptions.length)
      this.courseValue = ''
      const currentType = this.typeValue.length == 0 ? '-1' : this.typeValue
      // 赋予新值
      this.majorValue = newMajor
      this.currentPage = 1
      // 请求该专业下上传的资源
      const data_sources = await this.$store.dispatch('admin/getSourceUnderMajor', { major_id: this.majorValue, currentType: currentType, current_page: this.currentPage, page_size: this.pageSize })
      this.wirteTableAndChart(data_sources)
      // 请求课程数据
      const data_courses = await this.$store.dispatch('publicOpen/getCourseInfo', { major_id: this.majorValue })
      data_courses.data.courses.forEach(item => {
        const dic = { label: item.title, value: item.course_id }
        $this.courseOptions.push(dic)
      })
    },
    // 课程改变
    async courseChange(newCourse) {
      // 清理历史
      this.pieData.forEach(item => item.value = 0)
      this.heatChartData.splice(0, this.heatChartData.length)
      // 赋新值
      this.courseValue = newCourse
      this.currentPage = 1
      const currentType = this.typeValue.length === 0 ? '-1' : this.typeValue
      // 请求该课程下上传的资源
      const data = await this.$store.dispatch('admin/getSourceUnderCourse', { course_id: this.courseValue, currentType: currentType, currentPage: this.currentPage, pageSize: this.pageSize })
      this.wirteTableAndChart(data)
    },
    // 资源类型改变
    async typeValueChanged(newType) {
      this.typeValue = newType
      // const $this = this
      let current_course = -1
      if (this.courseValue.length !== 0) {
        current_course = this.courseValue
      }
      const data = await this.$store.dispatch('admin/sourceTypeChange', { major_id: this.majorValue, course_id: current_course, type: this.typeValue, page_size: this.pageSize, current_page: this.currentPage })
      this.tableData = data.data.sources
      this.sourceTotal = data.data.total
    },
    // 页大小改变
    pageSizeChanged(newSize) {
      // const $this = this
      this.pageSize = newSize
      this.paginationDataChanged()
    },
    // 页码改变
    currentPageChanged(newPage) {
      // const $this = this
      this.currentPage = newPage
      this.paginationDataChanged()
    },
    // 分页组件数据改变的请求
    async paginationDataChanged() {
      const currentType = this.typeValue.length === 0 ? '-1' : this.typeValue
      let data_sources = null
      // 判断是哪一个选择框对应的change了
      if (this.majorValue.length > 0 && this.courseValue.length === 0 && this.typeValue.length === 0) {
        // 说明是majorchange了
        data_sources = await this.$store.dispatch('admin/getSourceUnderMajor', { major_id: this.majorValue, currentType: currentType, current_page: this.currentPage, page_size: this.pageSize })
      } else if (this.courseValue.length > 0 && this.typeValue.length === 0) {
        // 说明是coursechange了
        data_sources = await this.$store.dispatch('admin/getSourceUnderCourse', { course_id: this.courseValue, currentType: currentType, currentPage: this.currentPage, pageSize: this.pageSize })
      } else if (this.courseValue.length === 0 && this.typeValue.length > 0) {
        data_sources = await this.$store.dispatch('admin/sourceTypeChange', { major_id: this.majorValue, course_id: '-1', type: currentType, page_size: this.pageSize, current_page: this.currentPage })
      }
      this.tableData = data_sources.data.sources
    },
    // 将请求下来的资源写到页面上
    wirteTableAndChart(data_sources) {
      this.tableData = data_sources.data.sources
      this.sourceTotal = data_sources.data.total
      // 配置图表数据
      this.processChartData(data_sources.data.heat)
      this.drawPie()
      this.drawCalenderHeat()
    },
    // 配置图表数据
    processChartData(heatData) {
      const $this = this
      this.tableData.forEach(item => {
        for (let i = 0; i < $this.pieData.length; i++) {
          if (item.source_type === $this.pieData[i].name) {
            $this.pieData[i].value++
          }
        }
      })

      heatData.forEach(item => {
        $this.heatChartData.push([item.time, item.heat])
      })
    },
    // 清空所选参数
    clearSelectedParams() {
      this.majorValue = ''
      this.courseValue = ''
      this.typeValue = ''
      this.typeOptions.splice(0, this.typeOptions.length)
      this.tableData.splice(0, this.tableData.length)
      this.pieData.splice(0, this.pieData.length)
      this.heatChartData.splice(0, this.heatChartData.length)
    }
  }
}
</script>
<style scoped>
.el-col div {
  height: 400px;
  box-shadow: 2px 0px 10px 0px #ddd;
  border-radius: 10px;
  background-color: #fff;
}
</style>

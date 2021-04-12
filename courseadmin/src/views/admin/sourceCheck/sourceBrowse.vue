<template>
  <div style="padding: 20px">
    <div style="margin-bottom: 30px">
      <source-table
        :is-browse="true"
        :tableData="tableData"
        :majorOptions="majorOptions"
        :courseOptions="courseOptions"
        :typeOptions="typeOptions"
        :statusOptions="statusOptions"
        :majorValue="majorValue"
        :courseValue="courseValue"
        :typeValue="typeValue"
        :currentPage="currentPage"
        :pageSize="pageSize"
        :sourceTotal="sourceTotal"
        @majorValueChange="majorChange"
        @courseValueChange="courseChange"
        @pageSizeChange="pageSizeChanged"
        @currentPageChange="currentPageChanged"
      />
    </div>
    <div class="chartView">
      <el-row :gutter="30">
        <el-col :span="9"><div id="pie"></div></el-col>
        <el-col :span="15"><div id="calender"></div></el-col>
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
  data(){
    return {
      tableData: null,
      majorOptions: [],
      courseOptions: [],
      typeOptions: [],
      statusOptions: [],
      majorValue: '',
      courseValue: '',
      typeValue: '',
      currentPage: 1,
      pageSize: 10,
      sourceTotal: 0,
      pieData: [],
      heatChartData: [],
    }
  },
  async mounted(){
    let $this = this
    // 请求资源类型
    const data_types = await this.$store.dispatch('teachers/getTypes')
    this.typeOptions = data_types.data.types
    this.typeOptions.forEach(item => $this.pieData.push({name: item.label, value: 0}))
    // 请求专业
    const data_majors = await this.$store.dispatch('publicOpen/getAllMajors')
    data_majors.data.majors.forEach(item => {
      let dic = {label: item.title, value: item.major_id}
      $this.majorOptions.push(dic)
    })
    // const data_courses = await this.$store.dispatch('publicOpen/get_courseinfo',{major_id: })
    
    this.drawCalenderHeat()
  },
  methods:{
    // 请求数据 当专业，课程改变后重新画饼图
    drawPie(){
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
    drawCalenderHeat(){
      const option = {
        title: {
          top: 50,
          left: 'center',
          text: '年度资源提交热力图'
        },
        tooltip: {
          position: 'top',
          formatter: function (p) {
            var format = echarts.format.formatTime('yyyy-MM-dd', p.data[0]);
            return format + ': ' + p.data[1] + '次';
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
          },
        },
        calendar: {
            top: 130,
            left: 40,
            right: 30,
            height: 140,
            cellSize: ['auto', 14],
            range: '2017',
            itemStyle: {
              borderWidth: 0.5,
            },
            yearLabel: {show: false},
            splitLine:{
              show: true, 
              lineStyle:{
                width: 0.5,
                color: '#888'
              }
            }
        },
        series: {
          type: 'heatmap',
          coordinateSystem: 'calendar',
          data:  [['2017-01-01', 5], ['2017-01-02', 20], ['2017-01-03', 10]]
        }
      }
      const heatMapChart = echarts.init(document.getElementById('calender'))
      heatMapChart.setOption(option)
    },
    // 专业改变
    async majorChange(newMajor){
      // 清理上一次的记录
      this.pieData.forEach(item => item.value = 0)
      this.courseOptions.splice(0, this.courseOptions.length)
      this.courseValue = ''
      // 赋予新值
      this.majorValue = newMajor
      const $this = this
      // 请求该专业下上传的资源
      const data_sources = await this.$store.dispatch('admin/getSourceUnderMajor', {major_id: this.majorValue, current_page: this.currentPage, page_size: this.pageSize})
      this.tableData = data_sources.data.sources
      this.sourceTotal = data_sources.data.total
      // 配置饼图的数据
      this.tableData.forEach(item => {
        for(let i = 0; i<$this.pieData.length; i++){
          if(item.source_type === $this.pieData[i].name){
            $this.pieData[i].value++
          }
        }
      })
      const data_courses = await this.$store.dispatch('publicOpen/getCourseInfo', {major_id: this.majorValue})
      data_courses.data.courses.forEach(item => {
        let dic = {label: item.title, value: item.course_id}
        $this.courseOptions.push(dic)
      })
      this.drawPie()
    },
    // 课程改变
    async courseChange(newCourse){
      this.courseValue = newCourse
      // 请求该课程下上传的资源
    },
    // 页大小改变
    async pageSizeChanged(newSize){
      const $this = this
      this.pageSize = newSize
      // 重新请求数据
    },
    // 页码改变
    async currentPageChanged(newPage){
      const $this = this
      this.currentPage = newPage
      // 重新请求数据
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

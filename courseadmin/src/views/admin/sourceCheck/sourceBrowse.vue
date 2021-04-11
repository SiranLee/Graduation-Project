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
        :sourceTotal="sourceTotal"
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
      tableData: [],
      majorOptions: [],
      courseOptions: [],
      typeOptions: [],
      statusOptions: [],
      majorValue: '',
      courseValue: '',
      typeValue: '',
      currentPage: 1,
      sourceTotal: 0
    }
  },
  mounted(){
    
    this.drawPie()
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
            data: [{name:'图片', value:20}, {name:'视频', value: 10}, {name:'文件',value:'25'}],
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
            return format + ': ' + p.data[1];
          }
        },
        visualMap: {
          min: 0,
          max: 100,
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
          data:  [['2017-01-01', 90], ['2017-01-02', 87], ['2017-01-03', 69]]
        }
      }
      const heatMapChart = echarts.init(document.getElementById('calender'))
      heatMapChart.setOption(option)
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

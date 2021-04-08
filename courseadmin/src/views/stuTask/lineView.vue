<template>
  <div />
</template>
<script>
import * as echarts from 'echarts'
import * as line from 'echarts/lib/chart/line'
import * as title from 'echarts/lib/component/title'
import * as tooltip from 'echarts/lib/component/tooltip'
export default {
  props: {
    labelData: {
      type: Array,
      default: () => {}
    },
    seriesData: {
      type: Array,
      default: () => {}
    }
  },
  methods: {
    draw() {
      const myChart = echarts.init(document.getElementById('line'))
      const option = {
        title: {
          text: '历次作业成绩'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: this.labelData
        },
        yAxis: {
          type: 'value'
        },
        series: this.seriesData
      }
      myChart.setOption(option)
    }
  }
}
</script>
<style scoped>

</style>

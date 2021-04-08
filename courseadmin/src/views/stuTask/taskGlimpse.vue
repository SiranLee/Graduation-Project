<template>
  <div>
    <div style="padding: 40px;">
      <div class="uploadHistory">
        <div class="divider"><span class="innerHint">统计数据</span></div>
        <div class="main">
          <el-row :gutter="20" style="height: 350px">
            <el-col :span="11" :offset="1" class="graphWrap">
              <div id="radar" class="grid-content" />
            </el-col>
            <el-col id="line" :span="11" class="graphWrap">
              <!-- <div id="line" class="grid-content" style="height: 350px" /> -->
              <line-view ref="child" :series-data="seriesData" :label-data="labels" />
            </el-col>
          </el-row>
        </div>
      </div>
      <div class="uploadHistory">
        <div class="divider"><span class="innerHint">成绩数据</span></div>
        <div class="main">
          <el-row style="padding-bottom: 10px;">
            <el-col :span="3">
              <filter-widget
                :value="taskCourse"
                hint="请选择课程"
                :options="optionsCourse"
                :emit-change="Tagchange"
              />
            </el-col>
            <el-col :span="20">
              <pagination :total="total" :page-size="tableLimit" style="float: right;" />
            </el-col>
          </el-row>
          <!-- 序号，专业，课程，作业题目，提交时间 -->
          <el-table :data="tableData" border>
            <el-table-column prop="id" label="序号" align="center" width="180" />
            <el-table-column prop="stu_major" label="专业" align="center" />
            <el-table-column prop="stu_course" label="课程" align="center" />
            <el-table-column prop="stu_taskTitle" label="作业" align="center" />
            <el-table-column
              prop="stu_score"
              label="得分"
              align="center"
            />
          </el-table>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import * as echarts from 'echarts/lib/echarts'
import * as radar from 'echarts/lib/chart/radar'
import * as line from 'echarts/lib/chart/line'
import * as title from 'echarts/lib/component/title'
import * as legend from 'echarts/lib/component/legend'
import * as tooltip from 'echarts/lib/component/tooltip'
import FilterWidget from '../studentmanage/components/FilterWidget'
import pagination from '@/components/SimplePagination'
import lineView from './lineView'
export default {
  components: {
    FilterWidget,
    pagination,
    lineView
  },
  data() {
    return {
      radarScore: [],
      lineScore: [],
      optionsCourse: [],
      tableData: [],
      completeRealm: [],
      labels: [],
      seriesData: [],
      taskCourse: '',
      total: 0,
      tableLimit: 5,
      currentPage: 1
    }
  },
  async mounted() {
    const res = await this.getData()
    let flap = 1
    const $this = this
    this.radarScore = res.avg_scores
    this.lineScore = res.scores
    this.drawRadar()
    this.makeLineData()
    res.scores.forEach((element, index) => {
      const item = {
        label: element.course,
        value: element.course
      }
      $this.optionsCourse.push(item)
      element.scores.forEach((ele, nindex) => {
        const dic = {
          id: flap,
          stu_major: $this.$store.state.user.major,
          stu_course: element.course,
          stu_taskTitle: element.tasks[nindex],
          stu_score: ele
        }
        $this.tableData.push(dic)
        $this.completeRealm.push(dic)
        flap++
      })
    })
  },
  methods: {
    getData() {
      return this.$store.dispatch('stu/getScoreData', {
        id: this.$store.state.user.id,
        dept: this.$store.state.user.major
      })
    },
    drawRadar() {
      const scores = []
      const indicators = []
      this.radarScore.forEach(element => {
        const dic = {
          name: element.course,
          max: element.max_score
        }
        indicators.push(dic)
        scores.push(element.avg_score)
      })
      const myChart = echarts.init(document.getElementById('radar'))
      const option = {
        title: {
          text: `${this.$store.state.user.name}平均成绩雷达图`
        },
        tooltip: {},
        radar: {
          name: {
            textStyle: {
              color: '#fff',
              backgroundColor: '#999',
              borderRadius: 3,
              padding: [3, 5]
            }
          },
          shape: 'circle',
          indicator: indicators,
          splitArea: {
            areaStyle: {
              color: ['rgba(114, 172, 209, 0.2)',
                'rgba(114, 172, 209, 0.4)', 'rgba(114, 172, 209, 0.6)',
                'rgba(114, 172, 209, 0.8)', 'rgba(114, 172, 209, 1)'],
              shadowColor: 'rgba(0, 0, 0, 0.3)',
              shadowBlur: 10
            }
          }
        },
        series: [{
          type: 'radar',
          data: [
            {
              value: scores,
              name: '学生成绩',
              tooltip: {
                trigger: 'item'
              },
              itemStyle: {
                normal: {
                  color: '#ff5722' // 显示颜色与填充颜色对应
                }
              },
              areaStyle: {
                normal: {
                  color: '#ff5722' // 填充的颜色
                }
              }
            }
          ]
        }]
      }
      myChart.setOption(option)
    },
    makeLineData() {
      let maxTimes = 0
      const $this = this
      this.lineScore.forEach(element => {
        const dic = {
          name: element.course,
          type: 'line',
          data: element.scores
        }
        $this.seriesData.push(dic)
        maxTimes = maxTimes > element.scores.length ? maxTimes : element.scores.length
      })
      for (let index = 0; index < maxTimes; index++) {
        this.labels.push(`第${index + 1}次`)
      }
      this.$refs.child.draw()
    },
    Tagchange(v) {
      this.taskCourse = v
      const temp = []
      this.completeRealm.forEach(element => {
        if (element.stu_course == v) {
          temp.push(element)
        }
      })
      this.tableData = temp
    }
  }
}
</script>
<style scoped>
.divider {
  border-top: 2px solid #999;
  position: relative;
}
.divider .innerHint {
  position: absolute;
  top: -20px;
  left: 40px;
  background-color: #f4f7fc;
  padding: 10px;
  font-size: 18px;
}
.main {
  padding: 30px 0 30px 0;
}
.uploader {
  padding-top: 20px;
  width: 50%;
}
.graphWrap{
  height: 100%;
}
#radar{
  height: 100%;
}
</style>

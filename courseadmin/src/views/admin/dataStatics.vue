<template>
  <div class="mainContainer">
  <div class="btn-no-print" style="margin-bottom: 20px;" ><el-button type="primary" @click="printPage">打印此页</el-button></div>
    <el-row :gutter="20" class="upBannerContainer">
      <el-col v-for="pic in pics" :key="pic.name" :span="6" class="upBanner">
        <div class="grid-content banner">
          <el-row :gutter="10">
            <el-col :span="8" class="leftImage">
              <img :src="pic.pic" :alt="pic.name">
            </el-col>
            <el-col :span="12" class="rightLabel">
              <div class="titleLabel">{{ pic.title }}</div>
              <span class="numLabel">{{
                staticsData[`total_${pic.name}`]
              }}</span>
            </el-col>
          </el-row>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="20" class="middleContainer">
      <el-col :span="16" class="middleBanner">
        <div class="grid-content midbanner">
          <el-select
            v-model="selMajor"
            class="midSelect"
            placeholder="请选择"
            @change="valueChange"
          >
            <el-option
              v-for="item in majorOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
          <div id="stackBar" class="midStackBar" />
        </div>
      </el-col>
      <el-col :span="8" class="middleBanner">
        <div id="pie" class="grid-content midbanner" style="height: 85%" />
        <div class="btnConatiner">
          <el-button
            id="pieBtn"
            type="success"
            plain
            style="width:90%;"
            :loading="pieBtnDownloading"
            @click="downLoadBtnClick"
          >数据导出</el-button>
        </div>
      </el-col>
    </el-row>
    <el-row class="bottomContainer" :gutter="20">
      <el-col :span="8" class="bottomBanner">
        <div class="grid-content bottombanner">
          <el-table
            :data="sourcesListData"
            border
            height="100%"
            style="width: 100%; height: 100%"
            stripe
          >
            <el-table-column prop="course" label="课程" align="center" />
            <el-table-column prop="video" label="视频" align="center" />
            <el-table-column prop="file" label="文件" align="center" />
            <el-table-column prop="image" label="图片" align="center" />
          </el-table>
          <div class="btnConatiner">
            <el-button
              id="tableBtn"
              type="success"
              plain
              style="width:90%;"
              :loading="tableBtnDownloading"
              @click="downLoadBtnClick"
            >数据导出</el-button>
          </div>
        </div>
      </el-col>
      <el-col :span="8" class="bottomBanner">
        <div class="grid-content bottombanner">
          <el-select
            v-model="selCourse"
            style="padding: 10px 0 0 10px;"
            placeholder="请选择"
            @change="stackBarSelectChange"
          >
            <el-option
              v-for="item in courseOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
          <div id="stack" style="padding-top: 20px; height: 85%" />
        </div>

        <div class="btnConatiner">
          <el-button
            id="Btn"
            type="success"

            plain
            style="width:90%;"
            @click="downLoadBtnClick"
          >数据导出</el-button>
        </div>
      </el-col>
      <el-col :span="8" class="bottomBanner">
        <div id="radar" class="grid-content bottombanner" />
        <div class="btnConatiner">
          <el-button
            id="radarBtn"
            type="success"
            :loading="radarBtnDownloading"
            plain
            style="width:90%;"
            @click="downLoadBtnClick"
          >数据导出</el-button>
        </div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import pic1 from '@/assets/static_banner/tea.png'
import pic2 from '@/assets/static_banner/stu.png'
import pic3 from '@/assets/static_banner/source.png'
import pic4 from '@/assets/static_banner/cour.png'
// import vueEasyPrint from "vue-easy-print";
import * as echarts from 'echarts/lib/echarts'
import grid from 'echarts/lib/component/grid'
import * as pie from 'echarts/lib/chart/pie'
import * as bar from 'echarts/lib/chart/bar'
import radar from 'echarts/lib/chart/radar'
import title from 'echarts/lib/component/title'
import legend from 'echarts/lib/component/legend'
import tooltip from 'echarts/lib/component/tooltip'
import toolbox from 'echarts/lib/component/toolbox'
export default {
  // components:{
  //   vueEasyPrint
  // },
  data() {
    return {
      pics: [
        { name: 'teachers', pic: pic1, title: '教师人数' },
        { name: 'stus', pic: pic2, title: '学生人数' },
        { name: 'sources', pic: pic3, title: '资源总数' },
        { name: 'course', pic: pic4, title: '课程总数' }
      ],
      staticsData: {},
      stackBarData: [],

      sourcesListData: [],
      majorOptions: [],
      courseOptions: [],
      labels: [],
      videos: [],
      images: [],
      files: [],
      selMajor: '',
      dep_stus: [],

      task_times: [],
      total_tasks: [],
      checked_tasks: [],
      unchecked_tasks: [],

      selCourse: '',
      pieBtnDownloading: false,
      radarBtnDownloading: false,
      tableBtnDownloading: false
    }
  },
  async mounted() {
    const result = await this.$store.dispatch('admin/getStaticsData')
    this.staticsData = result.data

    const $this = this
    this.drawPie()
    this.drawRadar()

    const majorData = await this.$store.dispatch('publicOpen/getAllMajors')
    majorData.data.majors.forEach(item => {
      $this.majorOptions.push({ label: item.title, value: item.major_id })
    })
    this.selMajor = this.majorOptions[0].value
    this.valueChange()
      .then(async res => {
        const homeworkCheckData = await this.$store.dispatch(
          'admin/getHomeworkData',
          { dep_id: this.selMajor, course_id: this.selCourse }
        )
        homeworkCheckData.data.checked_data.forEach(item => {
          $this.task_times.push(item.times)
          $this.checked_tasks.push(item.status.checked)
          $this.total_tasks.push(item.status.total)
          $this.unchecked_tasks.push(item.status.unchecked)
        })
        this.drawStackBar_2()
      })
      .catch(() => {})
  },
  methods: {
    drawPie() {
      const $this = this
      this.staticsData.dep_stus.forEach(element => {
        $this.dep_stus.push({
          name: element.dep_name,
          value: element.dep_stu_count
        })
      })
      const option = {
        title: {
          text: '各专业人数占比',
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
          left: '20px',
          bottom: '10px'
        },
        series: [
          {
            name: '专业类别',
            type: 'pie',
            radius: '50%',
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 1
            },
            data: this.dep_stus,
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
    drawRadar() {
      const worksData = []
      const worksIndicator = []

      this.staticsData.dep_homeworks.forEach(item => {
        worksData.push(item.count)
        worksIndicator.push({ name: item.dep, max: 12 })
      })
      const option = {
        title: {
          text: '各专业任务数',
          left: 'center',
          top: '20px'
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
        tooltip: {},
        radar: {
          name: {
            textStyle: {
              color: '#aaa',
              borderRadius: 3,
              padding: [3, 5]
            }
          },
          radius: '55%',
          indicator: worksIndicator,
          splitArea: {
            areaStyle: {
              color: [
                'rgba(114, 172, 209, 0.2)',
                'rgba(114, 172, 209, 0.4)',
                'rgba(114, 172, 209, 0.6)',
                'rgba(114, 172, 209, 0.8)',
                'rgba(114, 172, 209, 1)'
              ],
              shadowColor: 'rgba(0, 0, 0, 0.3)',
              shadowBlur: 10
            }
          }
        },
        series: [
          {
            type: 'radar',
            data: [
              {
                value: worksData
              }
            ],
            itemStyle: {
              color: '#795548', // 显示颜色与填充颜色对应
              opacity: 0
            },
            areaStyle: {
              color: 'rgba(254, 67, 101, 1)', // 填充的颜色
              opacity: 1,
              shadowColor: 'rgba(0, 0, 0, 0.3)',
              shadowBlur: 10
            }
          }
        ]
      }
      const radarChart = echarts.init(document.getElementById('radar'))
      radarChart.setOption(option)
    },
    drawStackBar() {
      const stackBarChart = echarts.init(document.getElementById('stackBar'))
      const app = {}
      app.config = {
        rotate: 90,
        align: 'left',
        verticalAlign: 'middle',
        position: 'insideBottom',
        distance: 15
      }

      const labelOption = {
        show: true,
        position: app.config.position,
        distance: app.config.distance,
        align: app.config.align,
        verticalAlign: app.config.verticalAlign,
        rotate: app.config.rotate,
        formatter: '{a}',
        fontSize: 16
      }

      const option = {
        color: ['#fac858', '#42b983', '#ee6666'],
        title: {
          text: `专业下各课程资源数`,
          right: 10
        },
        grid: {
          y2: 40
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['视频', '图片', '文档']
        },
        toolbox: {
          show: true,
          orient: 'vertical',
          left: 'right',
          top: 'center',
          feature: {
            saveAsImage: { show: true }
          }
        },
        xAxis: {
          gridIndex: 0,
          type: 'category',
          data: this.labels
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '视频',
            type: 'bar',
            barGap: 0,
            label: labelOption,
            emphasis: {
              focus: 'series'
            },
            data: this.videos
          },
          {
            name: '图片',
            type: 'bar',
            label: labelOption,
            emphasis: {
              focus: 'series'
            },
            data: this.images
          },
          {
            name: '文档',
            type: 'bar',
            label: labelOption,
            emphasis: {
              focus: 'series'
            },
            data: this.files
          }
        ]
      }

      stackBarChart.setOption(option)
    },
    makeStackBarData() {
      for (let index = 0; index < this.sourcesListData.length; index++) {
        const element = this.sourcesListData[index]
        this.labels.push(element.course)
        this.videos.push(element.video)
        this.images.push(element.image)
        this.files.push(element.file)
      }
    },
    async valueChange(v) {
      const $this = this
      this.courseOptions.splice(0, this.courseOptions.length)
      const stackBarData = await this.$store.dispatch('admin/getStackBarData', {
        dep_id: $this.selMajor
      })
      this.sourcesListData = []
      this.stackBarData = stackBarData.data
      stackBarData.data.stack_bar_data.forEach(element => {
        const dic = {
          course: element.course.name,
          video: element.sources_by_types[0].count,
          file: element.sources_by_types[1].count,
          image: element.sources_by_types[2].count
        }
        $this.sourcesListData.push(dic)
        const cour_dic = {
          label: element.course.name,
          value: element.course.no
        }
        $this.courseOptions.push(cour_dic)
      })
      this.selCourse = this.courseOptions[0].value
      this.labels = []
      this.videos = []
      this.images = []
      this.files = []
      this.makeStackBarData()
      this.drawStackBar()
    },
    stackBarSelectChange(v) {
      const $this = this
      this.task_times.splice(0, this.task_times.length)
      this.checked_tasks.splice(0, this.checked_tasks.length)
      this.unchecked_tasks.splice(0, this.unchecked_tasks.length)
      this.total_tasks.splice(0, this.total_tasks.length)
      // this.drawStackBar_2()
      this.$store.dispatch('admin/getHomeworkData', { dep_id: this.selMajor, course_id: this.selCourse })
        .then(res => {
          console.log(res)
          res.data.checked_data.forEach(item => {
            $this.task_times.push(item.times)
            $this.checked_tasks.push(item.status.checked)
            $this.total_tasks.push(item.status.total)
            $this.unchecked_tasks.push(item.status.unchecked)
          })
          this.drawStackBar_2()
        })
        .catch(() => {})
    },
    // todo
    drawStackBar_2() {
      const stackBar2 = echarts.init(document.getElementById('stack'))

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            // 坐标轴指示器，坐标轴触发有效
            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        legend: {
          data: ['总计', '已批改', '未批改']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            data: this.task_times
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: '总计',
            type: 'bar',
            emphasis: {
              focus: 'series'
            },
            data: this.total_tasks
          },
          {
            name: '已批改',
            type: 'bar',
            // stack: '广告',
            emphasis: {
              focus: 'series'
            },
            data: this.checked_tasks
          },
          {
            name: '未批改',
            type: 'bar',
            // stack: '广告',
            emphasis: {
              focus: 'series'
            },
            data: this.unchecked_tasks
          }
        ]
      }
      stackBar2.setOption(option)
    },
    downLoadBtnClick({ srcElement }) {
      let tHeader = []
      let filterval = []
      let data = []
      let filename = ''
      switch (srcElement.id) {
        case 'pieBtn': {
          let total = 0
          tHeader = ['专业', '人数', '占比']
          this.dep_stus.forEach(item => {
            total += item.value
          })
          filename = '专业人数'
          this.dep_stus.forEach(item => {
            const percent = (item.value / total) * 100 + '%'
            const dic = { dep: item.name, count: item.value, percent: percent }
            data.push(dic)
          })
          filterval = ['dep', 'count', 'percent']
          data = this.formatJson(filterval, data)

          this.pieBtnDownloading = true
          import('@/vendor/Export2Excel').then(excel => {
            excel.export_json_to_excel(tHeader, data, filename)
            this[`${srcElement.id}Downloading`] = false
          })
          break
        }
        case 'radarBtn': {
          this.radarBtnDownloading = true
          tHeader = ['专业', '任务数']
          filename = '专业任务数'
          filterval = ['dep', 'count']
          data = this.formatJson(filterval, this.staticsData.dep_homeworks)
          import('@/vendor/Export2Excel').then(excel => {
            excel.export_json_to_excel(tHeader, data, filename)
            this[`${srcElement.id}Downloading`] = false
          })
          break
        }
        case 'tableBtn': {
          this.tableDownloading = true
          tHeader = ['课程', '视频', '文件', '图片']
          filterval = ['course', 'file', 'image', 'video']
          const $this = this
          this.majorOptions.forEach(element => {
            if (element.value === $this.selMajor) {
              filename = `${element.label}专业各课程资源数`
            }
          })
          data = this.formatJson(filterval, this.sourcesListData)
          import('@/vendor/Export2Excel').then(excel => {
            excel.export_json_to_excel(tHeader, data, filename)
            this[`${srcElement.id}Downloading`] = false
          })
          break
        }
      }
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => v[j]))
    },
    printPage(){
      // this.$print(this.$refs.print)
      window.print()
      // console.log(this.$refs)
      // this.$refs.easyPrint.print()
    }
  }
}
</script>
<style scoped>
@media print{
  .btn-no-print{
    display: none;
  }
  .mainContainer{
    margin: left 0px;
  }
}
div.mainContainer {
  padding: 15px 0 30px 10px;
}
.el-row.upBannerContainer {
  height: 120px;
}
.el-row .el-col.upBanner {
  height: 100%;
}
.el-row .el-col.upBanner .banner {
  height: 100%;
  background-color: white;
  box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.05);
}
.el-row .el-col.upBanner .banner img {
  display: inline-block;
  width: 70%;
  height: 100%;
}
.el-row .el-col.upBanner .banner .leftImage {
  margin: 20px 0 0 15px;
}
.el-row.middleContainer {
  margin-top: 20px;
  height: 450px;
}
.el-row .el-col.upBanner .banner .titleLabel {
  text-align: right;
  padding-top: 30px;
  color: rgba(0, 0, 0, 0.45);
  font-size: 16px;
  font-weight: 700;
}
.el-row .el-col.upBanner .banner .numLabel {
  display: block;
  text-align: right;
  margin-top: 15px;
  font-size: 20px;
  color: #666;
  font-weight: 700;
}
.el-row.middleContainer .el-col.middleBanner {
  height: 100%;
}
.el-row.middleContainer .el-col.middleBanner .midbanner {
  height: 100%;
  background-color: white;
  box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);
  padding: 15px 15px 0 15px;
}
.el-row.middleContainer .btnConatiner{
  display: flex;
  align-items: center;
  justify-content: center;
  height: 15%;
  border-top-width: 2px;
  border-top-color: #aaa;
  border-top-style: dashed;
  background-color: white;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
}
.el-row.bottomContainer {
  margin-top: 20px;
  height: 500px;
}
.el-col.bottomBanner {
  height: 85%;
}
.el-row.bottomContainer .btnConatiner {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 20%;
  border-top-width: 2px;
  border-top-color: #aaa;
  border-top-style: dashed;
  background-color: white;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
}
.el-row.bottomContainer .el-col.bottomBanner .bottombanner {
  height: 100%;
  background-color: white;
  box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);
}
.el-row.middleContainer .el-col.middleBanner .midbanner .midStackBar {
  height: 90%;
}
</style>

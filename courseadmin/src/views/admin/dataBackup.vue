<template>
  <div>
    <div class="singleSheet">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>单表备份</span>
        </div>
        <div style="height: 100%">
          <el-row :gutter="20" style="height: 100%">
            <el-col :span="9" class="settingsGroup">
              <el-select v-model="selSheet" placeholder="请选择" style="width: 100%" @change="tagChange">
                <el-option
                  v-for="item in singleSheetOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
              <el-transfer v-model="singleSelectItems" class="transfer" :data="transferData" />
              <el-button type="primary" style="width: 100%;margin-top: 50px" plain :loading="singleTableLoading" :disabled="selSheet.length===0" @click="singleSheetBackup">备份该表</el-button>
            </el-col>
            <el-col :span="15" class="tableView">
              <el-table style="width: 100%" height="90%" :data="tableData" border>
                <el-table-column v-for="item in tableViewHeader" :key="item.value" :prop="item.value" :label="item.name" />
              </el-table>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </div>
    <div class="multiSheets">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>多表备份</span>
        </div>
        <div style="height: 100%; margin-bottom: 30px;">
          <el-steps :active="active" finish-status="success" align-center="">
            <el-step title="步骤 1" description="选择待导出的表" />
            <el-step title="步骤 2" description="选择待导出的字段" />
            <el-step title="步骤 3" description="点击备份即可开始备份" />
          </el-steps>
        </div>
        <div class="alivePanel">
          <div v-if="active===0" class="selectSheets">
            <el-transfer v-model="multiSelectSheets" class="transfer" :data="multiTransferData" />
          </div>
          <div v-if="active===1" class="selectItems">
            <el-row>
              <el-col :span="5" :offset="5">
                <el-table style="width: 70%; hover: cursor" highlight-current-row height="90%" :data="selectedSheets" border @current-change="handleRowSelect">
                  <el-table-column type="index" label=" " />
                  <el-table-column prop="name" label="已选择的表" />
                </el-table>
              </el-col>
              <el-col :span="9">
                <el-transfer v-model="multiSelectItems" class="transfer" :data="multiTransferItems" @change="multiTransferChange" />
              </el-col>
            </el-row>
          </div>
        </div>
        <div class="btnGroup">
          <el-button type="primary" :disabled="isLastDisable" @click="lastStep">上一步</el-button>
          <el-button type="primary" :disabled="isNextDisable" @click="nextStep">{{ btnStr }}</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      singleSheetOptions: [],
      selSheet: '',
      transferData: [],
      singleSelectItems: [],
      tableViewHeader: [],
      tableData: [],
      active: 0,
      btnStr: '下一步',
      isLastDisable: true,
      singleTableLoading: false,

      // 待选择备份的表
      multiTransferData: [],
      // 已经选中的要备份的表
      multiSelectSheets: [],
      // 当前选中的表
      currentSheet: '',
      // 待选择的表的字段
      multiTransferItems: [],
      // 最后选中的字段的集合
      multiSelectItems: [],
      eachSheetItems: []
    }
  },
  computed: {
    isNextDisable() {
      return this.multiSelectSheets.length === 0
    },
    selectedSheets() {
      const selectSheets = []
      this.multiSelectSheets.forEach(item => {
        const sheet = this.multiTransferData.find(element => item === element.key)
        selectSheets.push({ name: sheet.label, value: sheet.key })
      })
      return selectSheets
    }
  },
  async mounted() {
    // 首先得到所有表名
    const namesData = await this.$store.dispatch('admin/fetchAllSheetNames')
    this.singleSheetOptions = namesData.data.result
    const $this = this
    namesData.data.result.forEach(item => {
      $this.multiTransferData.push({ key: item.value, label: item.label, disabled: false })
    })
  },
  methods: {
    async tagChange(v) {
      const $this = this
      // 请求所有字段
      const result = await this.$store.dispatch('admin/getFiledsForSheet', { 'sheet': v })
      this.transferData.splice(0, this.transferData.length)
      this.singleSelectItems.splice(0, this.singleSelectItems.length)
      result.data.fileds.forEach(element => {
        const flag = (element === 'password')
        $this.transferData.push({ key: element, label: element, disabled: flag })
      })

      // 请求整张表
      this.tableViewHeader.splice(0, this.tableViewHeader.length)
      const wholeSheet = await this.$store.dispatch('admin/getWholeSheet', { 'sheet': v })
      const keys = Object.keys(wholeSheet.data.table[0])
      keys.forEach(item => {
        $this.tableViewHeader.push({ name: item, value: item })
      })
      this.tableData = wholeSheet.data.table
    },
    // 备份单个文件
    async singleSheetBackup() {
      this.singleTableLoading = true
      const $this = this
      const tempData = []
      const filename = this.selSheet
      let tHeader = []
      if (this.singleSelectItems.length == 0) {
        this.transferData.forEach(item => {
          $this.singleSelectItems.push(item.label)
          tHeader.push(item.label)
        })
      } else {
        tHeader = this.singleSelectItems
      }
      this.tableData.forEach(item => {
        const dic = {}
        $this.singleSelectItems.forEach(element => {
          dic[element] = item[element]
        })
        tempData.push(dic)
      })
      const fixedData = this.formatJson(this.singleSelectItems, tempData)
      import('@/vendor/Export2Excel').then(excel => {
        excel.export_json_to_excel(tHeader, fixedData, filename)
        $this.singleTableLoading = false
        $this.singleSelectItems.splice(0, $this.singleSelectItems.length)
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => v[j]))
    },
    // 表格的行被选中
    async handleRowSelect(item) {
      const $this = this
      this.currentSheet = item.value
      const result = await this.$store.dispatch('admin/getFiledsForSheet', { 'sheet': item.value })
      this.multiTransferItems.splice(0, this.multiTransferItems.length)
      this.multiSelectItems.splice(0, this.multiSelectItems.length)
      result.data.fileds.forEach(element => {
        const flag = (element === 'password')
        $this.multiTransferItems.push({ key: element, label: element, disabled: flag })
      })
      const target = this.eachSheetItems.find(item => item['sheetName'] == this.currentSheet)
      if (target) {
        target['selectFields'].forEach(item => $this.multiSelectItems.push(item))
      }
    },
    multiTransferChange(current, direction, changedKeys) {
      const $this = this
      let target = this.eachSheetItems.find(item => item['sheetName'] === $this.currentSheet)
      if (target) { // 有这个元素，直接更新其数据
        target['selectFields'] = current
      } else { // 没有这个元素
        target = {}
        target['sheetName'] = this.currentSheet
        target['selectFields'] = []
        current.forEach(item => target['selectFields'].push(item))
        this.eachSheetItems.push(target)
      }
    },
    // 下一步按钮被点击了
    nextStep() {
      this.active++
      this.isLastDisable = false
      if (this.active === 2) {
        this.btnStr = '备份'
      } else if (this.active === 3) {
        // 真实备份数据
        this.multiSheetsBackup()
      }
    },
    multiSheetsBackup() {
      // 首先检查有没有漏掉的表
      const $this = this
      this.multiSelectSheets.forEach(item => {
        if (!$this.eachSheetItems.find(e => e['sheetName'] === item)) {
          $this.$store.dispatch('admin/getFiledsForSheet', { 'sheet': item })
            .then(result => {
              const target = {}
              target['sheetName'] = item
              target['selectFields'] = []
              result.data.fileds.forEach(ele => target['selectFields'].push(ele))
              $this.eachSheetItems.push(target)
              if ($this.eachSheetItems.length === $this.multiSelectSheets.length) {
                this.multibackup()
              }
            })
        } else {
          this.multibackup()
        }
      })
    },
    multibackup() {
      const $this = this
      this.$store.dispatch('admin/multiBackup', { 'settings': JSON.stringify(this.eachSheetItems) })
        .then(res => {
          const data = res.data.result
          const tHeaders = []
          const filenames = []
          const fixedDatas = []
          data.forEach(item => {
            const targetHeader = (this.eachSheetItems.find(element => item.sheetName === element.sheetName))['selectFields']
            tHeaders.push(targetHeader)
            filenames.push(item.sheetName)
            fixedDatas.push($this.formatJson(targetHeader, item.sheetData))
          })
        import('@/vendor/Export2Excel').then(excel => {
          excel.export_jsons_to_excel(tHeaders, fixedDatas, filenames)
          $this.active = 0
          $this.eachSheetItems.splice(0, $this.eachSheetItems.length)
          $this.multiSelectSheets.splice(0, $this.multiSelectSheets.length)
          $this.multiTransferItems.splice(0, $this.multiTransferItems.length)
          $this.multiSelectItems.splice(0, $this.multiSelectItems.length)
          $this.currentSheet = ''
          $this.btnStr = '下一步'
        })
        })
    },
    // 上一步按钮被点击了
    lastStep() {
      this.active--
      if (this.active === 0) {
        this.isLastDisable = true
        return
      }
      if (this.active === 1) {
        this.btnStr = '下一步'
      }
    }
  }
}
</script>
<style>
.singleSheet {
  padding: 30px;
  height: 700px;
}
.singleSheet .box-card{
  height: 100%;
}
.singleSheet .box-card .el-card__header{
    border-bottom: 3px dashed #EBEEF5
}
.singleSheet .box-card .el-card__body{
    height: 100%;
}
.singleSheet .box-card .clearfix span{
  color: #989797;
}
.singleSheet .el-row .el-col.settingsGroup {
  height: 100%;
}
.singleSheet .el-row .el-col.settingsGroup .transfer{
  margin-top: 50px;
}
.transfer .el-transfer-panel{
    border: 2px solid #EBEEF5;
}
.transfer .el-transfer-panel .el-transfer-panel__header{
  border-bottom: 2px solid #EBEEF5;
}
.singleSheet .el-row .el-col.tableView{
    height: 100%;
}
.multiSheets {
  margin-bottom: 20px;
  padding: 30px;
  padding-top: 0;
}
.multiSheets .box-card .el-card__header{
  border-bottom: 3px dashed #EBEEF5
}
.multiSheets .box-card .clearfix span{
  color: #989797;
}
.multiSheets .btnGroup{
    text-align: center;
    margin-top: 40px;
}
.multiSheets .alivePanel .selectSheets{
  width: 40%;
  margin: 0 auto;
}
</style>

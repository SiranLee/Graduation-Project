<template>
  <div>
    <el-dialog
      title="教师信息"
      :visible="dialogVisible"
      width="30%"
      :show-close="false"
    >
      <el-form ref="teaForm" :label-position="labelPosition" label-width="80px" :rules="rules" :model="item">
        <el-form-item label="工号">
          <el-input v-model="item.tea_number" disabled />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="item.tea_name" disabled />
        </el-form-item>
        <el-form-item label="职称">
          <el-input v-model="item.tea_position" disabled />
        </el-form-item>
        <el-form-item label="所属系部">
          <el-input v-model="item.tea_major" disabled />
        </el-form-item>
        <el-form-item label="所授课程">
          <el-input v-model="item.courseStr" disabled />
        </el-form-item>
        <el-form-item label="密码重置" prop="newPwd">
          <el-input v-model="item.newPwd" type="password" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="$emit('changeVisible')">取 消</el-button>
        <el-button type="primary" @click="modify">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
export default {
  props: {
    dialogVisible: {
      type: Boolean,
      default: false
    },
    item: {
      type: Object,
      default: () => {}
    },
    isAdmin: {
      type: Boolean,
      default: false
    }
  },
  data() {
    const validatePasswordLength = (rule, value, callback) => {
      if (value.length <= 0) {
        callback(new Error('请输入密码'))
      } else if (value.length < 6) {
        callback(new Error('密码长度不低于6位'))
      } else {
        callback()
      }
    }
    return {
      labelPosition: 'right',
      rules: {
        newPwd: [{ validator: validatePasswordLength, trigger: 'blur' }]
      }
    }
  },
  computed: {
    stu() {
      return this.item ? this.item : {}
    }
  },
  methods: {
    modify() {
      this.$refs['teaForm'].validate(valid => {
        if (valid) {
          this.$emit('changeInfo', this.item)
        }
      })
    }
  }
}
</script>
<style scoped>

</style>

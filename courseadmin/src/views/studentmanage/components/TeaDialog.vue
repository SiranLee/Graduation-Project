<template>
  <div>
    <el-dialog
      title="编辑学生信息"
      :visible="dialogVisible"
      width="30%"
      :show-close="false"
    >
      <el-form ref="pwdForm" :label-position="labelPosition" label-width="80px" :rules="rules" :model="stuItem">
        <el-form-item label="学号">
          <el-input v-model="stuItem.stu_number" disabled />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="stuItem.name" disabled />
        </el-form-item>
        <el-form-item label="班级">
          <el-input v-model="stuItem.stu_class" disabled />
        </el-form-item>
        <el-form-item label="专业">
          <el-input v-model="stuItem.stu_major" disabled />
        </el-form-item>
        <el-form-item label="密码重置" prop="newPwd">
          <el-input v-model="stuItem.newPwd" type="password" />
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
    stuItem: {
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
      if (!value || value.length <= 0) {
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
      return this.stuItem ? this.stuItem : {}
    }
  },
  methods: {
    modify() {
      this.$refs['pwdForm'].validate(valid => {
        if (valid) {
          this.$emit('changeStuInfo', this.stuItem)
        }
      })
    }
  }
}
</script>
<style scoped>

</style>

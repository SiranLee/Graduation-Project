<template>
  <div>
    <div class="modifyContainer">
      <el-tabs tab-position="left" type="border-card" style="height: 550px">
        <el-tab-pane label="基本信息修改">
          <el-form :label-position="labelPosition" label-width="80px" :model="form">
            <el-form-item class="avatarItem">
              <label for="avatarUpload" class="avatarLabel">
                <span class="mask">上传头像</span>
                <img :src="form.userAvatar" alt="头像">
              </label>
              <input
                id="avatarUpload"
                type="file"
                accept="image/png, image/jpg, image/jpeg, image/gif"
                style="display: none;"
                @change="avatarChange"
              >
            </el-form-item>
            <el-form-item label="姓名">
              <el-input v-model="form.userName" disabled />
            </el-form-item>
            <el-form-item v-if="isTeacher&&!isAdmin" label="所在系部">
              <el-input v-model="form.userMajor" disabled />
            </el-form-item>
            <el-form-item v-if="!isTeacher&&!isAdmin" label="年级">
              <el-input :value="form.userGrade" disabled="" />
            </el-form-item>
            <el-form-item v-if="!isTeacher&&!isAdmin" label="班级">
              <el-input :value="form.userClass" disabled />
            </el-form-item>
            <el-form-item v-if="!isTeacher&&!isAdmin" label="专业">
              <el-input :value="form.userMajor" disabled />
            </el-form-item>
            <el-form-item>
              <el-button type="success" style="width:100%" @click="changeBaseInfo">提交</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="密码修改">
          <el-form
            ref="pwdForm"
            status-icon
            class="pwdForm"
            :label-position="labelPosition"
            label-width="120px"
            :model="pwd"
            :rules="rules"
          >
            <el-form-item v-if="!isOrgPwdRight" label="请输入原始密码" prop="originPwd">
              <el-input v-model="pwd.originPwd" type="password" auto-complete="off" />
            </el-form-item>
            <div v-if="isOrgPwdRight">
              <el-form-item label="请输入新密码" prop="firstPwd">
                <el-input v-model="pwd.firstPwd" type="password" auto-complete="off" />
              </el-form-item>
              <el-form-item label="请确认密码" prop="confirmPwd">
                <el-input v-model="pwd.confirmPwd" type="password" auto-complete="off" />
              </el-form-item>
            </div>
            <el-form-item>
              <el-button type="success" style="width:100%" @click="changePassword">确定</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    form: {
      type: Object,
      default: () => {}
    },
    isTeacher: {
      type: Boolean,
      default: false
    },
    isAdmin: {
      type: Boolean,
      default: false
    },
    password: {
      type: String,
      default: ''
    },
    classOptions: {
      type: Array,
      default: () => []
    },
    gradeOptions: {
      type: Array,
      default: () => [
        { label: '2019', value: 0 },
        { label: '2018', value: 1 },
        { label: '2017', value: 2 },
        { label: '2016', value: 3 }
      ]
    },
    majorOptions: {
      type: Array,
      default: () => [
        { label: '计算机', value: 0 },
        { label: '公共事业管理', value: 1 },
        { label: '市场营销', value: 2 },
        { label: '信息技术管理', value: 3 }
      ]
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
    const validateFirstPassword = (rule, value, callback) => {
      if (value.length <= 0) {
        callback(new Error('请输入密码'))
      } else if (value.length < 6) {
        callback(new Error('密码长度不低于6位'))
      } else {
        if (this.pwd.confirmPwd !== '') {
          this.$refs['pwdForm'].validateField('confirmPwd')
        }
        callback()
      }
    }
    const validateSecondPassword = (rule, value, callback) => {
      if (value.length <= 0) {
        callback(new Error('请输入密码'))
      } else if (value.length < 6) {
        callback(new Error('密码长度不低于6位'))
      } else {
        if (value !== this.pwd.firstPwd) {
          callback(new Error('两次密码不一致'))
        } else {
          callback()
        }
      }
    }
    return {
      labelPosition: 'right',
      avatarFile: null,

      // 密码相关
      isOrgPwdRight: false,
      pwd: {
        originPwd: '',
        firstPwd: '',
        confirmPwd: ''
      },
      rules: {
        originPwd: [{ required: true, validator: validatePasswordLength, trigger: 'blur' }],
        firstPwd: [{ required: true, validator: validateFirstPassword, trigger: 'blur' }],
        confirmPwd: [{ required: true, validator: validateSecondPassword, trigger: 'blur' }]
      }
    }
  },
  methods: {

    avatarChange() {
      this.avatarFile = document.querySelector('#avatarUpload').files[0]
      if (this.avatarFile.type.indexOf('image') !== 0) { return this.$message({ message: '请上传图片文件', type: 'warning' }) }
      this.form.userAvatar = URL.createObjectURL(this.avatarFile)
    },
    changeBaseInfo() {
      this.form.avatar = this.avatarFile
      this.form.role = this.$store.state.user.roles[0].substr(0, 1)
      this.$emit('baseInfoSubmit', this.form)
    },
    async changePassword() {
      if (!this.isOrgPwdRight) {
        // 说明是说如原始密码阶段 发送校验原始密码请求
        const result = await this.$store.dispatch('publicOpen/compareOriginPwd', { id: this.form.userId, pwd: this.pwd.originPwd, role: this.$store.state.user.roles[0].substr(0, 1) })
        if (result) {
          if (result.data.message === 'ok') {
            this.isOrgPwdRight = true
            this.pwd.originPwd = ''
          } else {
            this.$message({
              message: '密码错误',
              type: 'error'
            })
          }
        }
      } else {
        this.$refs['pwdForm'].validate(async(valid) => {
          if (valid) {
            // 发送修改密码的请求
            const result = await this.$store.dispatch('publicOpen/modifyPwdSelf', { id: this.form.userId, pwd: this.pwd.confirmPwd, role: this.$store.state.user.roles[0].substr(0, 1) })
            if (result && result.data.message === 'ok') {
              this.$message({
                message: '密码修改成功',
                type: 'success'
              })
              for (const key in this.pwd) {
                if (this.pwd.hasOwnProperty(key)) {
                  this.pwd[key] = ''
                }
              }
              this.isOrgPwdRight = false
            }
          } else {
            return false
          }
        })
      }
    }
  }
}
</script>
<style scoped>
.modifyContainer {
  padding: 20px;
  width: 60%;
  margin: 0 auto;
  padding-top: 60px;
}
.avatarItem {
  text-align: center;
  margin-left: 0;
}
.avatarItem .avatarLabel {
  position: relative;
  display: block;
  width: 100px;
  height: 100px;
  border-radius: 50px;
  left: 50%;
  margin-left: -50px;
}
.avatarItem .mask {
  position: absolute;
  top: 0;
  width: 100px;
  height: 100px;
  border-radius: 50px;
  background-color: rgba(0, 0, 0, 0.3);
  text-align: center;
  line-height: 100px;
  color: #fff;
  opacity: 0;
  transition: all ease 0.3s;
  cursor: pointer;
}
.avatarItem .mask:hover {
  opacity: 1;
}
.avatarLabel img {
  cursor: pointer;
  width: 100px;
  height: 100px;
  border-radius: 50px;
  vertical-align: bottom;
}
.el-form {
  padding-top: 30px;
}
.el-form-item {
  width: 60%;
  margin: 0 auto;
  margin-bottom: 20px;
}
.el-form-item .el-select {
  width: 100%;
}
.pwdForm {
  padding-top: 150px;
}
</style>

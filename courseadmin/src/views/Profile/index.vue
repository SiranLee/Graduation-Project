<template>
  <div>
    <profile :form="form" :is-admin="isAdmin" :is-teacher="isTeacher" :password="password" @baseInfoSubmit="baseInfoDischarge" />
  </div>
</template>
<script>
import { mapGetters, mapMutations } from 'vuex'
import profile from './components/profile'
export default {
  components: {
    profile
  },
  data() {
    return {
      password: '',
      form: {
        // this.$store.state.user.avatar
        userAvatar: process.env.VUE_APP_BASE_API + this.$store.state.user.avatar,
        userName: this.$store.state.user.name,
        userId: this.$store.state.user.id,
        userMajor: this.$store.state.user.major,
        userGrade: '',
        userClass: ''
      }
    }
  },
  computed: {
    ...mapGetters(['avatar', 'name', 'roles', 'userid']),
    isTeacher() {
      return this.roles.indexOf('teacher') === 0
    },
    isAdmin() {
      return this.$store.state.user.roles.includes('admin')
    }
  },
  mounted() {
    // 发送请求，请求额外信息
    if (this.isTeacher || this.isAdmin) return
    this.$store.dispatch('publicOpen/getRestInfo', { id: this.form.userId })
      .then(res => {
        this.form.userGrade = res.data.stu_grade
        this.form.userClass = res.data.stu_class
      })
      .catch(err => {
        console.log(err)
      })
  },
  methods: {
    ...mapMutations({
      modifyName: 'user/SET_NAME',
      modifyAvatar: 'user/SET_AVATAR'
    }),
    baseInfoDischarge(info) {
      const formData = new FormData()
      const config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      formData.append('avatar', info.avatar)
      formData.append('userId', info.userId)
      formData.append('role', info.role)
      // for (const key in info) {
      //   if (info.hasOwnProperty(key)) {
      //     if (key !== 'userAvatar') {
      //       formData.append(key, info[key])
      //     }
      //   }
      // }
      // console.log(info)
      this.$store.dispatch('publicOpen/modifyUserBaseInfo', { config, formData })
        .then(res => {
          if (res.data.message === 'ok') {
            // 设置头像，为返回的url
            this.modifyAvatar(res.data.avatar)
            this.$message({
              message: '设置成功',
              type: 'success'
            })
          }
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>
<style scoped>
</style>

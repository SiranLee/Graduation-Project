import Vue from 'vue'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/zh-CN' // lang i18n

import '@/styles/index.scss' // global css

import App from './App'
import store from './store'
// import Print from './utils/print'
import router, { constantRoutes } from './router'

import '@/icons' // icon
import '@/permission' // permission control

/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online! ! !
 */
// import { mockXHR } from '../mock'
// if (process.env.NODE_ENV === 'production') {
//   mockXHR()
// }

// set ElementUI lang to EN
Vue.use(ElementUI, { locale })
// Vue.use(Print)

Vue.config.productionTip = false

var before_unload_sudden = 0
var gap_time = 0

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})

window.addEventListener('unload', async(e) => {
  gap_time = new Date().getTime() - before_unload_sudden
  if (gap_time <= 5) {
    const xhr = new XMLHttpRequest()
    const formData = new FormData()
    formData.append('token', store.state.user.token)
    xhr.onreadystatechange = function() {
      store.dispatch('user/resetTokenSync')
    }
    xhr.open('POST', `${process.env.VUE_APP_BASE_API}/test/`, false)
    xhr.send(formData)
  } else {
    store.dispatch('teachers/getTypes')
      .then(res => {
        console.log(res.data)
      })
      .catch(err => {})
  }
})
window.addEventListener('beforeunload', (e) => {
  before_unload_sudden = new Date().getTime()
  // store.dispatch('teachers/getTypes')
  // .then(res => {

  // })
  // .catch(err=>{})
})

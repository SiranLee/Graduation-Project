import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import app from './modules/app'
import settings from './modules/settings'
import user from './modules/user'
import tagsView from './modules/tagsView'
import permission from './modules/permission'
import publicOpen from './modules/public'
import teachers from './modules/teachers'
import admin from './modules/admin'
import stu from './modules/stu'
Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    app,
    settings,
    user,
    tagsView,
    permission,
    publicOpen,
    teachers,
    admin,
    stu
  },
  getters
})

export default store

import {
  getAllCourse,
  getMajors,
  getSourceInCourse,
  getSourceDetailBaseInfo,
  sourceFilterByType,
  searchSource,
  getRestInfo,
  modifyUserBaseInfo,
  compareOriginPwd,
  modifyPwdSelf,
  searchByKeyWord,
  getAllMajors } from '@/api/public'

const actions = {
  async getAllCourse({ commit }, data) {
    const result = await getAllCourse(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getMajors({ commit }, data) {
    const result = await getMajors(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getAllMajors({ commit }) {
    const result = await getAllMajors()
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getSourceInCourse({ commit }, data) {
    const result = await getSourceInCourse(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getSourceDetailBaseInfo({ commit }, data) {
    const result = await getSourceDetailBaseInfo(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async sourceFilterByType({ commit }, data) {
    const result = await sourceFilterByType(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async searchSource({ commit }, data) {
    const result = await searchSource(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getRestInfo({ commit }, data) {
    const result = await getRestInfo(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async modifyUserBaseInfo({ commit }, data) {
    const result = await modifyUserBaseInfo(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async compareOriginPwd({ commit }, data) {
    const result = await compareOriginPwd(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async modifyPwdSelf({ commit }, data) {
    const result = await modifyPwdSelf(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async searchByKeyWord({ commit }, data) {
    const result = await searchByKeyWord(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  }
}

export default {
  namespaced: true,
  actions
}

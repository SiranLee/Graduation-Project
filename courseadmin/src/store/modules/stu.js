import { uploadTask, getGrade, getShortCourse, getTasksByCourse, getTableData, getScoreData } from '@/api/stu'

const actions = {
  async uploadTask({ commit }, data) {
    const result = await uploadTask(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getGrade({ commit }, data) {
    const result = await getGrade(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getShortCourse({ commit }, data) {
    const res = await getShortCourse(data)
    if (res) {
      return res
    }
    return Promise.reject(res)
  },
  async getTasksByCourse({ commit }, data) {
    const result = await getTasksByCourse(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getTableData({ commit }, data) {
    const result = await getTableData(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getScoreData({ commit }, data) {
    const result = await getScoreData(data)
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

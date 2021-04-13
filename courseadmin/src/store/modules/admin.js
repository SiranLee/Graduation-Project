import {
  getTeachers,
  deleteTeacher,
  submitChange,
  uploadTeas,
  searchTeacher,
  getExcelTemplate,
  getStaticsData,
  getStackBarData,
  getHomeworkData,
  fetchAllSheetNames,
  getFiledsForSheet,
  getWholeSheet,
  getSheetBackUp,
  multiBackup,
  fetchRoutes,
  fetchRouteForTeacher,
  setPermissionForTeacher,
  fetchDisciplineTableData,
  submitDisciplineChange,
  addDiscipline,
  addRouteForDiscipline,
  delDiscipline,
  searchTeacherWithNo,
  getSourceUnderMajor,
  getSourceUnderCourse,
  sourceTypeChange } from '@/api/admin'

const actions = {
  async getTeachers({ commit }, data) {
    const result = await getTeachers(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async deleteTeacher({ commit }, data) {
    const result = await deleteTeacher(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async submitChange({ commit }, data) {
    const result = await submitChange(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async uploadTeas({ commit }, data) {
    const result = await uploadTeas(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async searchTeacher({ commit }, data) {
    const result = await searchTeacher(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getExcelTemplate({ commit }) {
    const result = await getExcelTemplate()
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getStaticsData({ commit }, data) {
    const result = await getStaticsData()
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getStackBarData({ commit }, data) {
    const result = await getStackBarData(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getHomeworkData({ commit }, data) {
    const result = await getHomeworkData(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async fetchAllSheetNames({ commit }, data) {
    const result = await fetchAllSheetNames(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getFiledsForSheet({ commit }, data) {
    const result = await getFiledsForSheet(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getWholeSheet({ commit }, data) {
    const result = await getWholeSheet(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getSheetBackUp({ commit }, data) {
    const result = await getSheetBackUp(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async multiBackup({ commit }, data) {
    const result = await multiBackup(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async fetchRoutes({ commit }, data) {
    const result = await fetchRoutes(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async fetchRouteForTeacher({ commit }, data) {
    const result = await fetchRouteForTeacher(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async setPermissionForTeacher({ commit }, data) {
    const result = await setPermissionForTeacher(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async fetchDisciplineTableData({ commit }, data) {
    const reuslt = await fetchDisciplineTableData(data)
    if (reuslt) {
      return reuslt
    }
    return Promise.reject(reuslt)
  },
  async submitDisciplineChange({ commit }, data) {
    const result = await submitDisciplineChange(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async addDiscipline({ commit }, data) {
    const result = await addDiscipline(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async addRouteForDiscipline({ commit }, data) {
    const result = await addRouteForDiscipline(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async delDiscipline({ commit }, data) {
    const result = await delDiscipline(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async searchTeacherWithNo({ commit }, data) {
    const result = await searchTeacherWithNo(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getSourceUnderMajor({ commit }, data) {
    const result = await getSourceUnderMajor(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getSourceUnderCourse({ commit }, data){
    const result = await getSourceUnderCourse(data)
    if(result){
      return result
    }
    return Promise.reject(result)
  },
  async sourceTypeChange({commit}, data){
    const result = await sourceTypeChange(data)
    if(result){
      return result
    }
    return Promise.reject(reuslt)
  }
}

export default {
  namespaced: true,
  actions
}

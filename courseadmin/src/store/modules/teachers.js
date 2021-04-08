import {
  getTeaCourse,
  getClasses,
  getStudentsAtCategories,
  getDataAtPage,
  getDetail,
  setCourseDetail,
  uploadSource,
  getSourceListType,
  getTypes,
  delRes,
  getShortCourse,
  uploadFile,
  modifyPwd,
  createCourse,
  deleteCourse,
  deleteStu,
  releaseTask,
  getReleasedTasks,
  delTask,
  getFiles,
  deleteFileByTask,
  getSomeone,
  getTaskByQuery,
  getGrade,
  getPDF,
  getTasksByCourse,
  submitSingleScore,
  creatClassAndSetRoutes } from '@/api/teacher'

const actions = {
// 获取教师教授的课程
  async getCourse({ commit }, teacherName) {
    const data = await getTeaCourse(teacherName)
    if (data) {
      return data
    }
    return Promise.reject(data)
  },
  async getTeachingClass({ commit }) {
    const data = await getClasses()
    if (data) {
      return data
    }
    return Promise.reject(data)
  },
  async searchStu({ commit }, conditions) {
    const data = await getStudentsAtCategories(conditions)
    if (data) {
      return data
    }
    return Promise.reject(data)
  },
  async getPageData({ commit }, config) {
    const data = await getDataAtPage(config)
    if (data) {
      return data
    }
    return Promise.reject(data)
  },
  async getCourseDetail({ commit }, course) {
    const data = await getDetail(course)
    if (data) {
      return data
    }
    return Promise.reject(data)
  },
  async setCourseInfo({ commit }, data) {
    const res = await setCourseDetail(data)
    if (res) {
      return res
    }
    return Promise.reject(res)
  },
  async uploadSource({ commit }, data) {
    const res = await uploadSource(data)
    if (res) {
      return res
    }
    return Promise.reject(res)
  },
  async getSourceListType({ commit }, data) {
    const res = await getSourceListType(data)
    if (res) {
      return res
    }
    return Promise.reject(res)
  },
  async getTypes({ commit }) {
    const res = await getTypes()
    if (res) {
      return res
    }
    return Promise.reject(res)
  },
  async delRes({ commit }, id) {
    const res = await delRes(id)
    if (res) {
      return res
    }
    return Promise.reject(res)
  },
  async getShortCourse({ commit }, data) {
    const res = await getShortCourse(data)
    if (res) {
      return res
    }
    return Promise.reject(res)
  },
  async uploadFile({ commit }, data) {
    const result = await uploadFile(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async modifyPwd({ commit }, data) {
    const result = await modifyPwd(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async createCourse({ commit }, data) {
    const result = await createCourse(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async deleteCourse({ commit }, data) {
    const result = await deleteCourse(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async deleteStu({ commit }, data) {
    const result = await deleteStu(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  // 作业相关
  async releaseTask({ commit }, data) {
    const result = await releaseTask(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async delTask({ commit }, data) {
    const result = await delTask(data)
    if (result) {
      return result
    }
    return Promise.reject(data)
  },
  async getReleasedTasks({ commit }, data) {
    const result = await getReleasedTasks(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  // 获取某个任务下的附件列表
  async getFiles({ commit }, data) {
    const result = await getFiles(data)
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
  // 删除某个任务下的某个附件
  async deleteFileByTask({ commit }, data) {
    const result = await deleteFileByTask(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getSomeone({ commit }, data) {
    const result = await getSomeone(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getTaskByQuery({ commit }, data) {
    const result = await getTaskByQuery(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getPDF({ commit }, data) {
    const result = await getPDF(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async getTasksByCourse({ commit }, data) {
    const result = await getTasksByCourse(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async submitSingleScore({ commit }, data) {
    const result = await submitSingleScore(data)
    if (result) {
      return result
    }
    return Promise.reject(result)
  },
  async creatClassAndSetRoutes({commit}, data){
    console.log(data)
    const result = await creatClassAndSetRoutes(data)
    if(result){
      return result
    }
    return Promise.reject(result)
  }
}

export default {
  namespaced: true,
  actions
}

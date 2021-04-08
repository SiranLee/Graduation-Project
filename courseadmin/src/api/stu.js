import request from '@/utils/request'

export function uploadTask(data) {
  const { config, formData } = data
  return request({
    url: '/student_upfile_homework/',
    method: 'post',
    headers: config.headers,
    data: formData
  })
}

export function getTasksByCourse(data) {
  return request({
    url: '/gettaskbycourse/',
    method: 'get',
    params: data
  })
}

export function getGrade(data) {
  return request({
    url: '/studentget_garden/',
    method: 'get',
    params: data
  })
}

export function getShortCourse(id) {
  return request({
    url: '/studentget_course/',
    method: 'get',
    params: id
  })
}

export function getTableData(data) {
  return request({
    url: '/getTableData/',
    method: 'get',
    params: data
  })
}

export function getScoreData(data) {
  return request({
    url: '/stu_getscore/',
    method: 'get',
    params: data
  })
}

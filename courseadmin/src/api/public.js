import request from '@/utils/request'

export function getAllCourse(data) {
  const { major_id, page, limit } = data
  return request({
    url: '/get_dallcourse/',
    method: 'get',
    params: { major_id, page, limit }
  })
}

export function getMajors(data) {
  return request({
    url: '/get_department/',
    method: 'get',
    params: data
  })
}

export function getSourceInCourse(data) {
  return request({
    url: '/public/getSourceInCourse',
    method: 'get',
    params: data
  })
}

export function getSourceDetailBaseInfo(data) {
  return request({
    url: '/course_info/',
    method: 'get',
    params: data
  })
}

export function sourceFilterByType(data) {
  return request({
    url: '/get_sourcebytype/',
    method: 'get',
    params: data
  })
}

export function searchSource(data) {
  return request({
    url: '/tsearch_source/',
    method: 'get',
    params: data
  })
}

export function getRestInfo(data) {
  return request({
    url: '/get_studentinfo/',
    method: 'get',
    params: data
  })
}

export function modifyUserBaseInfo(data) {
  const { config, formData } = data
  return request({
    url: '/updata_icon/',
    method: 'post',
    headers: config.headers,
    data: formData
  })
}

export function compareOriginPwd(data) {
  return request({
    url: '/check_password/',
    method: 'post',
    data
  })
}

export function modifyPwdSelf(data) {
  return request({
    url: '/reset_passwordall/',
    method: 'post',
    data
  })
}

export function searchByKeyWord(data) {
  return request({
    url: '/search_course/',
    method: 'get',
    params: { course_name: data }
  })
}

export function getAllMajors() {
  return request({
    url: '/get_all_majors/',
    method: 'get'
  })
}

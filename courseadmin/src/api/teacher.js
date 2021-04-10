import request from '@/utils/request'

export function getTeaCourse(teacherName) {
  return request({
    url: '/teacher_getcourse/',
    method: 'get',
    params: { teacher_id: teacherName }
  })
}

export function getClasses() {
  return request({
    url: '/teacher/getClasses',
    method: 'get'
  })
}

export function getStudentsAtCategories(params) {
  return request({
    url: '/search_student/',
    method: 'get',
    params: params
  })
}

export function getDataAtPage(config) {
  return request({
    url: '/get_student/',
    method: 'get',
    params: config
  })
}
// 获取课程的详细信息
export function getDetail(course) {
  return request({
    url: '/get_course/',
    method: 'get',
    params: { course_id: course }
  })
}

export function setCourseDetail(info) {
  const { headers, data } = info
  return request({
    url: '/update_info/',
    method: 'post',
    headers: headers,
    data
  })
}
// 上传资源
export function uploadSource(info) {
  const { config, formData } = info
  return request({
    url: '/up_source/',
    method: 'post',
    headers: config.headers,
    data: formData
  })
}
// 获取上传的资源列表和文件类型们
export function getSourceListType(data) {
  const { course_id, page, limit } = data
  return request({
    url: '/get_source/',
    method: 'get',
    params: { course_id, page, limit }
  })
}

export function getTypes() {
  return request({
    url: '/get_sourcetype/',
    method: 'get'
  })
}

export function delRes(id) {
  return request({
    url: '/del_source/',
    method: 'get',
    params: id
  })
}

export function getShortCourse(id) {
  return request({
    url: '/teacherget_course/',
    method: 'get',
    params: id
  })
}

export function uploadFile(data) {
  return request({
    url: '/load_studentinfo/',
    method: 'post',
    data
  })
}

export function modifyPwd(data) {
  return request({
    url: '/reset_password/',
    method: 'post',
    data
  })
}

export function createCourse(data) {
  return request({
    url: '/create_course/',
    method: 'post',
    data
  })
}

export function deleteCourse(data) {
  return request({
    url: '/delete_course/',
    method: 'get',
    params: data
  })
}

export function deleteStu(data) {
  return request({
    url: '/delete_student/',
    method: 'post',
    data
  })
}

// 发布作业
export function releaseTask(data) {
  const { config, formData } = data
  return request({
    url: '/publish_task/',
    method: 'post',
    headers: config.headers,
    data: formData
  })
}

export function getReleasedTasks(data) {
  return request({
    url: '/get_homework/',
    method: 'get',
    params: data
  })
}

export function delTask(data) {
  return request({
    url: '/del_homework/',
    method: 'get',
    params: data
  })
}

export function getFiles(data) {
  return request({
    url: '/get_work/',
    method: 'get',
    params: data
  })
}

export function deleteFileByTask(data) {
  return request({
    url: '/del_work/',
    method: 'get',
    params: data
  })
}

export function getSomeone(data) {
  return request({
    url: '',
    method: 'get',
    params: data
  })
}

export function getTaskByQuery(data) {
  return request({
    url: '/getTasksByQuery/',
    method: 'get',
    params: data
  })
}

export function getGrade(data) {
  return request({
    url: '/teacherget_garden/',
    method: 'get',
    params: data
  })
}

export function getPDF(data) {
  return request({
    url: '/get_upfilework_info/',
    method: 'get',
    params: data
  })
}

export function getTasksByCourse(data) {
  return request({
    url: '/gettaskbycourse/',
    method: 'get',
    params: data
  })
}

export function submitSingleScore(data) {
  return request({
    url: '/submit_score/',
    method: 'post',
    data
  })
}

export function creatClassAndSetRoutes(data){
  return request({
    url: '/create_class_set_routes/',
    method: 'post',
    data
  })
}

export function searchWithNo(data){
  return request({
    url: '/search_with_no/',
    method: 'get',
    params: data
  })
}

export function modifySourceReadLimit(data){
  return request({
    url: '/modify_read_limit/',
    method: 'post',
    params: data
  })
}
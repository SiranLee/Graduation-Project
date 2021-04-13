import request from '@/utils/request'

export function getTeachers(data) {
  return request({
    url: '/admin_getteacherinfo/',
    method: 'get',
    params: data
  })
}

export function deleteTeacher(data) {
  return request({
    url: '/admin_delteacher/',
    method: 'get',
    params: data
  })
}

export function submitChange(data) {
  return request({
    url: '/admin_setpassword/',
    method: 'post',
    data
  })
}

export function uploadTeas(data) {
  return request({
    url: '/load_teacherinfo/',
    method: 'post',
    data
  })
}

export function searchTeacher(data) {
  return request({
    url: '/search_teacher/',
    method: 'get',
    params: data
  })
}

export function getExcelTemplate() {
  return request({
    url: '/get_teachertemplate/',
    method: 'get'
  })
}

export function getStaticsData() {
  return request({
    url: '/get_statics_data/',
    method: 'get'
  })
}

export function getStackBarData(data) {
  return request({
    url: '/get_stackbar_data/',
    method: 'get',
    params: data
  })
}

export function getHomeworkData(data) {
  return request({
    url: '/get_homework_data/',
    method: 'get',
    params: data
  })
}

export function fetchAllSheetNames(data) {
  return request({
    url: '/fetch_all_sheet_names/',
    method: 'get'
  })
}

export function getFiledsForSheet(data) {
  return request({
    url: '/get_fileds_for_sheet/',
    method: 'get',
    params: data
  })
}

export function getWholeSheet(data) {
  return request({
    url: '/get_whole_sheet/',
    method: 'get',
    params: data
  })
}

export function getSheetBackUp(data) {
  return request({
    url: '/get_sheet_back_up/',
    method: 'get',
    params: data
  })
}

export function multiBackup(data) {
  return request({
    url: '/multi_backup/',
    method: 'get',
    params: data
  })
}

export function fetchRoutes(data) {
  return request({
    url: '/fetch_routes/',
    method: 'get'
  })
}

export function fetchRouteForTeacher(data) {
  return request({
    url: '/fetch_route_for_teacher/',
    method: 'get',
    params: data
  })
}

export function setPermissionForTeacher(data) {
  return request({
    url: '/set_permission_for_teacher/',
    method: 'post',
    data
  })
}

export function fetchDisciplineTableData(data) {
  return request({
    url: '/fetch_discipline_tabledata/',
    method: 'get'
  })
}

export function submitDisciplineChange(data) {
  return request({
    url: '/submit_discipline_change/',
    method: 'post',
    data
  })
}

export function addDiscipline(data) {
  return request({
    url: '/add_discipline/',
    method: 'post',
    data
  })
}

export function addRouteForDiscipline(data) {
  return request({
    url: '/add_route_for_discipline/',
    method: 'post',
    data
  })
}

export function delDiscipline(data) {
  return request({
    url: '/del_displine/',
    method: 'post',
    data
  })
}

export function searchTeacherWithNo(data) {
  return request({
    url: '/search_teacher_with_no/',
    method: 'get',
    params: data
  })
}

export function getSourceUnderMajor(data) {
  return request({
    url: '/get_course_under_major/',
    method: 'get',
    params: data
  })
}

export function getSourceUnderCourse(data){
  return request({
    url: '/get_source_under_course/',
    method: 'get',
    params: data
  })
}

export function sourceTypeChange(data){
  return request({
    url: '/source_type_change/',
    method:'get',
    params: data
  })
}
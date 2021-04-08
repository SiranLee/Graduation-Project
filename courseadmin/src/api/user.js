import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/login/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/check/',
    method: 'get',
    params: { token }
  })
}

export function logout(token) {
  return request({
    url: '/logout/',
    method: 'post',
    data: { token: token }
  })
}

export function test(token) {
  return request({
    url: '/test/',
    method: 'post',
    data: { token: token }
  })
}

export function fetchUserRoutes(roles, id) {
  return request({
    url: '/fetch_user_routes/',
    method: 'post',
    data: { roles: roles, id: id }
  })
}

export function fetchRouteComponentMap() {
  return request({
    url: '/fetch_route_component_map/',
    method: 'get'
  })
}

import { asyncRoutes, constantRoutes, routerMap } from '@/router'
import { fetchUserRoutes, fetchRouteComponentMap } from '@/api/user'
/**
 * Use meta.role to determine if the current user has permission
 * @param roles
 * @param route
 */
function hasPermission(roles, route) {
  if (route.meta && route.meta.roles) {
    return roles.some(role => route.meta.roles.includes(role))
  } else {
    return true
  }
}

function str2ComponentMapper(rawResult) {
  rawResult.forEach(function(item, index) {
    item.component = routerMap[item.component]
    if (item.children && item.children.length > 0) {
      str2ComponentMapper(item.children)
    }
  })
  return rawResult
}

/**
 * Filter asynchronous routing tables by recursion
 * @param routes asyncRoutes
 * @param roles
 */
export function filterAsyncRoutes(routes, roles) {
  const res = []

  routes.forEach(route => {
    const tmp = { ...route }
    if (hasPermission(roles, tmp)) {
      if (tmp.children) {
        tmp.children = filterAsyncRoutes(tmp.children, roles)
      }
      res.push(tmp)
    }
  })

  return res
}

const state = {
  routes: [],
  addRoutes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.addRoutes = routes
    state.routes = constantRoutes.concat(routes)
  }
}

const actions = {
  generateRoutes({ commit }, roles) {
    return new Promise(resolve => {
      let accessedRoutes
      accessedRoutes = filterAsyncRoutes(asyncRoutes, roles)
      commit('SET_ROUTES', accessedRoutes)
      resolve(accessedRoutes)
    })
  },
  generateRoutesAsync({ commit }, { roles, id }) {
    return new Promise(async resolve => {
      const result = await fetchUserRoutes(roles, id)
      const { data } = await fetchRouteComponentMap()
      data.map.forEach(item => {
        if (!routerMap[item.component_key]) {
          routerMap[item.component_key] = () => import('@/views/sourcelist/index')
        }
      })
      // 完成从字符串到组件的映射
      const accessRoutes = str2ComponentMapper(result.data.routes)
      commit('SET_ROUTES', accessRoutes)
      resolve(accessRoutes)
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

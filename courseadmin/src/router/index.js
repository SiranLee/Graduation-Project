import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/profile',
    component: Layout,
    redirect: '/profile/self',
    children: [
      {
        path: 'self',
        name: 'Self',
        component: () => import('@/views/Profile/index'),
        meta: { title: '个人信息修改', icon: 'self', affix: true }
      }
    ]
  },
  // {
  //   path: '/sourceCheck',
  //   component: Layout,
  //   redirect: '/sourceCheck/sourceBrowse',
  //   meta: { title: '资源相关', icon: 'relation', roles: ['admin'] },
  //   children: [
  //     {
  //       path: 'sourceBrowse',
  //       name: 'SourceBrowse',
  //       component: () => import('@/views/admin/sourceCheck/sourceBrowse'),
  //       meta: { title: '资源总览', icon: 'browse', roles: ['admin'] }
  //     },
  //     {
  //       path: 'sourceCheck',
  //       name: 'SourceCheck',
  //       component: () => import('@/views/admin/sourceCheck/sourceCheck'),
  //       meta: { title: '资源审核', icon: 'sourceCheck', roles: ['admin'] }
  //     }
  //   ]
  // },
]
export const routerMap = {
  Layout: Layout,
  computer: () => import('@/views/sourcelist/index'),
  infomanage: () => import('@/views/sourcelist/index'),
  market: () => import('@/views/sourcelist/index'),
  publicmanage: () => import('@/views/sourcelist/index'),
  SourceDetail: () => import('@/views/sourcelist/sourceDetail'),
  UploadTask: () => import('@/views/stuTask/uploadTask'),
  TaskGlimpse: () => import('@/views/stuTask/taskGlimpse'),
  CourseManage: () => import('@/views/coursemanage/index'),
  Detail: () => import('@/views/coursemanage/coursedetail'),
  Create: () => import('@/views/coursemanage/createcourse'),
  CheckTask: () => import('@/views/coursemanage/checkTask'),
  StudensManage: () => import('@/views/studentmanage/index'),
  Teachers: () => import('@/views/admin/Teacher/index'),
  DataStatics: () => import('@/views/admin/dataStatics'),
  dataBackup: () => import('@/views/admin/dataBackup'),
  DisciplineManagement: () => import('@/views/admin/disciplineManagement'),
  SourceBrowse: () => import('@/views/admin/sourceCheck/sourceBrowse'),
  SourceCheck: () => import('@/views/admin/sourceCheck/sourceCheck')
}
// export const asyncRoutes = [
//   {
//     path: '/source',
//     component: Layout,
//     redirect: '/source/computer',
//     meta: { title: '学习资源', icon: 'resource', roles: ['teacher', 'student','admin'] },
//     children: [
//       {
//         path: 'computer',
//         name: 'computer',
//         component: () => import('@/views/sourcelist/index'),
//         meta: { title: '计算机科学与技术', icon: 'computer', currentPage: 1, roles: ['teacher', 'student','admin'] }
//       },
//       {
//         path: 'infomanage',
//         name: 'infomanage',
//         component: () => import('@/views/sourcelist/index'),
//         meta: { title: '信息技术管理', icon: 'info', currentPage: 1, roles: ['teacher', 'student','admin'] }
//       },
//       {
//         path: 'market',
//         name: 'market',
//         component: () => import('@/views/sourcelist/index'),
//         meta: { title: '市场营销', icon: 'market', currentPage: 1, roles: ['teacher', 'student','admin'] }
//       },
//       {
//         path: 'publicmanage',
//         name: 'publicmanage',
//         component: () => import('@/views/sourcelist/index'),
//         meta: { title: '公共事业管理', icon: 'public', currentPage: 1, roles: ['teacher', 'student','admin'] }
//       },
//       {
//         path: '/source/:coursename/:courseid',
//         name: 'SourceDetail',
//         hidden: true,
//         props: true,
//         component: () => import('@/views/sourcelist/sourceDetail'),
//         meta: { title: '课程资源详情', roles: ['teacher', 'student','admin'] }
//       }
//     ]
//   },
//   {
//     path: '/task',
//     component: Layout,
//     redirect: '/task/uploadTask',
//     meta: { title: '作业管理', icon: 'resource', roles: ['student'] },
//     children: [
//       {
//         path: 'uploadTask',
//         name: 'UploadTask',
//         component: () => import('@/views/stuTask/uploadTask'),
//         meta: { title: '上传作业', icon: 'upload', roles: ['student'] }
//       },
//       {
//         path: 'taskGlimpse',
//         name: 'TaskGlimpse',
//         component: () => import('@/views/stuTask/taskGlimpse'),
//         meta: { title: '作业成绩', icon: 'glimpse', roles: ['student'] }
//       }
//     ]
//   },
//   {
//     path: '/courseManage',
//     component: Layout,
//     meta: { title: '课程管理', icon: 'coursemanage', roles: ['teacher'] },
//     props: true,
//     children: [
//       {
//         path: '/courseManage/index',
//         name: 'CourseManage',
//         component: () => import('@/views/coursemanage/index'),
//         meta: { title: '课程管理', icon: 'coursemanage', roles: ['teacher'] }
//       },
//       {
//         path: '/detail/:course_id',
//         name: 'Detail',
//         hidden: true,
//         props: true,
//         component: () => import('@/views/coursemanage/coursedetail'),
//         meta: { title: '课程明细', roles: ['teacher'] }
//       },
//       {
//         path: '/create',
//         name: 'Create',
//         component: () => import('@/views/coursemanage/createcourse'),
//         meta: { title: '创建课程', icon: 'add', roles: ['teacher'] }
//       },
//       {
//         path: '/checkTask',
//         name: 'CheckTask',
//         component: () => import('@/views/coursemanage/checkTask'),
//         meta: { title: '批改作业', icon: 'check', roles: ['teacher'] }
//       }
//     ],

//   },
//   {
//     path: '/studensManage',
//     component: Layout,
//     meta: {title:'学生管理',icon: 'students', roles: ['teacher'] },
//     children: [
//       {
//         path: '/studensManage/index',
//         name: 'StudensManage',
//         component: () => import('@/views/studentmanage/index'),
//         meta: { title: '学生管理', icon: 'students', roles: ['teacher'] }
//       }
//     ]
//   },
//   // admin
//   {
//     path: '/teachers',
//     component: Layout,
//     meta: { title: '教师管理',icon:'students',  roles: ['admin'] },
//     children: [
//       {
//         path: 'index',
//         name: 'Teachers',
//         component: () => import('@/views/admin/Teacher/index'),
//         meta: { title: '教师管理', icon: 'students', roles: ['admin'] }
//       }
//     ]
//   },
//   {
//     path: '/dataStatics',
//     component: Layout,
//     redirect: '/dataStatics/index',
//     meta: { title: '数据统计',icon: 'statics',  roles: ['admin'] },
//     children: [
//       {
//         path: 'index',
//         name: 'DataStatics',
//         component: () => import('@/views/admin/dataStatics'),
//         meta: { title: '数据统计', icon: 'statics', roles: ['admin'] }
//       }
//     ]
//   },
//   {
//     path: '/dataBackup',
//     component: Layout,
//     meta: { title: '数据备份',icon: 'backup', roles: ['admin'] },
//     children: [
//       {
//         path: 'index',
//         name: 'dataBackup',
//         component: () => import('@/views/admin/dataBackup'),
//         meta: { title: '数据备份', icon: 'backup', roles: ['admin'] }
//       }
//     ]
//   },
//   // { path: '*', redirect: '/404', hidden: true }
// ]

export const asyncRoutes = []

const createRouter = () => new Router({
  mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router

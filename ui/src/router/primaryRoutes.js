export default [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/projects',
    name: 'projects',
    component: () => import('@/pages/projects/ProjectsHome.vue'),
  },
  {
    path: '/project',
    name: 'project',
    component: () => import('@/pages/project/ProjectHome.vue'),
  },
  {
    path: '/task',
    name: 'task-home',
    component: () => import('@/pages/task/TaskHome.vue'),
  },
  {
    path: '/profile',
    name: 'user-profile',
    component: () => import('@/pages/user/UserProfile.vue'),
  },
]

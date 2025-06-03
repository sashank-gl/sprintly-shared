import { createRouter, createWebHistory } from 'vue-router'

import primaryRoutes from './primaryRoutes'

const routes = [...primaryRoutes]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((x) => x.meta.requiresAuth)
  const requiresGuest = to.matched.some((x) => x.meta.requiresGuest)
  const isLoggedIn = store.getters["UserModule/isLoggedIn"]

  if (requiresAuth && !isLoggedIn) {
    next("/")
  } else if (requiresGuest && isLoggedIn) {
    next("/account")
  } else {
    next()
  }
})

export default router

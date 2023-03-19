// Sets up the Vue Router for the application
import { createRouter, createWebHistory } from 'vue-router'
import Authenticate from '../views/Authenticate.vue'
import Home from '../views/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Authenticate',
      component: Authenticate
    },
    {
      path: '/home',
      name: 'Home',
      component: Home
    }
  ]
})

export default router

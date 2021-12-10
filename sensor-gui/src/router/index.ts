import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Messungen from '../views/Messungen.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
  },
  {
    path: '/sensors',
    name: 'Sensoren',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "sensors" */ '../views/Sensoren.vue')
  },
  {
    path: '/messungen',
    name: 'Messungen',
    component: Messungen,
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

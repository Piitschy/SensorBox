import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      description: {
        text: 'Hallo, ich bin Jans Messtool. \nIch kann dir helfen Smaps automatisiert zu bearbeiten. \nBedenke, dass ich noch ein Prototyp bin...'
      }
    }
  },
  {
    path: '/sensors',
    name: 'Sensoren',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "sensors" */ '@/views/Sensoren.vue'),
    meta: {
      description: {
        text: 'Hallo, ich bin Jans Messtool. \nIch kann dir helfen Smaps automatisiert zu bearbeiten. \nBedenke, dass ich noch ein Prototyp bin...'
      }
    }
  },
  {
    path: '/messungen',
    name: 'Messungen',
    component: () => import(/* webpackChunkName: "measurements" */ '@/views/Messungen.vue'),
    meta: {
      headline: 'Messungen',
      description: {
        text: 'Hallo, ich bin Jans Messtool. \nIch kann dir helfen Smaps automatisiert zu bearbeiten. \nBedenke, dass ich noch ein Prototyp bin...'
      }
    },
    children: [
      {
        path: 'schedule',
        name: 'NewMessung',
        meta: {
          headline: 'Messungen'
        },
        component: () => import(/* webpackChunkName: "newMeasurement" */ '@/views/subviews/NewMessung.vue')
      },
      {
        path: 'schedule/start',
        name: 'StartMessung',
        meta: {
          headline: 'Messungen'
        },
        component: () => import(/* webpackChunkName: "startMeasurement" */ '@/views/subviews/StartMessung.vue')
      },
      {
        path: ':id',
        name: 'Messung',
        meta: {
          headline: 'Messungen'
        },
        component: () => import(/* webpackChunkName: "measurement" */ '@/views/subviews/Messung.vue')
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

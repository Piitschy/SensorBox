import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    notification: {
      namespaced: true,
      state: {
        init: {
          massage: null,
          icon: null,
          color: null,
          timeout: 3000
        },
        trigger: false,
        payload: {}
      },
      mutations: {
        reset (state) {
          state.trigger = false
          state.payload = state.init
        },
        assignPayload (state, payload) {
          state.payload = Object.assign(state.payload, payload)
        },
        trigger (state) {
          state.trigger = true
        }
      },
      actions: {
        set (context, payload) {
          context.commit('reset')
          context.commit('assignPayload', payload)
          context.commit('trigger')
          setTimeout(() => { context.commit('reset') }, context.state.payload.timeout)
        }
      }
    }
  }
})

import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    baseUrl: 'http://192.168.182.176:8080/',
    apiUrl: 'http://192.168.182.176:5000/',
    loading: false,
    headers: [
      {text: 'Name', value: 'name', type: 'sting'},
      {text: 'Sensor', value: 'sensor', type: 'sting'},
      {text: 'Dauer [s]', value: 'duration', type: 'number'},
      {text: 'Rate [Hz]', value: 'rate', type: 'number'},
      {text: 'Datum', value: 'start_date', type: 'sting'},
      {text: 'Zeit', value: 'start_time', type: 'sting'}
    ],
    sensors: [
      {name: 'RF603'}
    ]
  },
  mutations: {
    startLoading(state) {
      state.loading = true
    },
    stopLoading(state) {
      state.loading = false
    },
  },
  actions: {
    async getData(context, route) {
      context.commit('startLoading')
      const response = await fetch(this.state.apiUrl+route)
      const json = await response.json()
      //const result = Object.keys(json.data).map(id => Object.assign({id:id},json.data[id]))
      context.commit('stopLoading')
      return json.data
    },
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

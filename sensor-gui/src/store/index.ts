import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    baseUrl: 'http://192.168.178.200:8081/',
    apiUrl: 'http://192.168.178.200:5000/',
    loading: false,
    headers: [
      {text: 'Name', value: 'name', type: 'text'},
      {text: 'Sensor', value: 'sensor', type: 'text'},
      {text: 'Dauer [s]', value: 'duration', type: 'number'},
      {text: 'Rate [Hz]', value: 'rate', type: 'number'},
      {text: 'Datum', value: 'start_date', type: 'text'},
      {text: 'Zeit', value: 'start_time', type: 'text'}
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
      const response = await fetch(this.state.apiUrl+route,{
        method: 'GET', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        //headers: {
        //  'Content-Type': 'application/json'
          // 'Content-Type': 'application/x-www-form-urlencoded',
        //},
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        //body: JSON.stringify(data) // body data type must match "Content-Type" header
      })
      const json = await response.json()
      //const result = Object.keys(json.data).map(id => Object.assign({id:id},json.data[id]))
      context.commit('stopLoading')
      !json.message || context.dispatch('notification/set', {message: json.message})
      return json.data
    },
    async putData(context, data) {
      const route = data.route
      const body = data.body
      context.commit('startLoading')
      const response = await fetch(this.state.apiUrl+route, {
        method: 'PUT', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
          'Content-Type': 'application/json'
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(body) // body data type must match "Content-Type" header
      })
      const json = await response.json()
      //const result = Object.keys(json.data).map(id => Object.assign({id:id},json.data[id]))
      context.commit('stopLoading')
      !json.message || context.dispatch('notification/set', {message: json.message})
      return json.data
    }

  },
  modules: {
    notification: {
      namespaced: true,
      state: {
        init: {
          message: null,
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

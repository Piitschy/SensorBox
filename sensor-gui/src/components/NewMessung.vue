<template>
  <v-card
    :loading="loading"
  >
    <v-toolbar>
      <v-spacer></v-spacer>
        <v-toolbar-title>
          Neue Messung
        </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
      <v-card-text class="pa-4">
        <v-text-field
            v-for="e in headersExcept" :key="e.value"
            :label="e.text"
            outlined
          ></v-text-field>
      </v-card-text>
    <v-card-actions class="justify-end">
      <v-btn
        text
        @click="$router.go(-1)"
      >Schließen</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script >
  import Vue from 'vue'
  import { mapState } from 'vuex'

  export default Vue.extend({
    name: 'Messung',
    data: () =>{ 
      return {
        apiRouteBase: 'measurements',
        item: {},
        except: [
          'start_date',
          'start_time'
        ]
    }},
    computed: {
      ...mapState(['loading','headers']),
      headersExcept() {
        var newHeaders = []
        for (var i in this.headers) {
          console.log(this.headers[i])
          if (this.except.includes(this.headers[i].value)) continue
          newHeaders.push(this.headers[i])
        }
        return newHeaders
      }
    },
    methods: {
      getText(key) {
        try {
          return this.headers.find(e => e.value === key).text
        } catch (e) {
          return key
        }
      }
    },
  })
</script>

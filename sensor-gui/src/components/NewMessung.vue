<template>
  <v-card
    :loading="loading"
  >
    <v-toolbar>
      <v-spacer></v-spacer>
        <v-toolbar-title>
          Neue Messung planen
        </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
      <v-card-text class="pa-4">
        <v-text-field
          v-for="h in usedHeaders" :key="h.value"
          :label="h.text"
          outlined
        />
        <v-checkbox
          label="Demo"
          :v-model="request.demo"
        />
        {{request}}
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
        apiRoute: 'measurements/schedule',
        request: {},
        hide: [
          'start_date',
          'start_time'
        ]
    }},
    computed: {
      ...mapState(['loading','headers','sensors']),
      usedHeaders() {
        var usedHeaders = []
        for (let e of this.headers) {
          if (this.hide.includes(e.value)) continue
          usedHeaders.push(e)
        }
        return usedHeaders
      },
      sensorNames() {
        return this.sensors.map(e => e.name)
      }
    }
  })
</script>
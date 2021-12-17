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
    <div v-show="loaded">
      {{itemExcept}}
      <v-card-text class="pa-4">
        <v-text-field
            v-for="value,key in itemExcept" :key="key"
            :label="getText(key)"
            :value="value"
            outlined
          ></v-text-field>
      </v-card-text>
    <v-card-actions class="justify-end">
      <v-btn
        text
        @click="$router.go(-1)"
      >Schließen</v-btn>
    </v-card-actions>
  </div>
  <v-skeleton-loader
    v-if="!loaded"
    class="my-4"
    type="list-item@6, actions"
  />
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
        loaded: true,
        item: {},
        except: [
          'data',
          'start',
          'start_date',
          'start_time'
        ]
    }},
    computed: {
      ...mapState(['loading','headers']),
      itemExcept() {
        var newItem = {}
        for (var e in this.item) {
          if (this.except.indexOf(e) >= 0) continue
          newItem[e] = this.item[e]
        }
        return newItem
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

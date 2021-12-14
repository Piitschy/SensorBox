<template>
  <v-card
    :loading="loading"
  >
    <v-toolbar>
        {{item.name}}
    </v-toolbar>
    <v-expand-transition>
      <v-card-text class="pa-4" v-show="loaded">
        <v-list-item v-for="value,key in item" :key="key">
          <v-list-item-content>
            <v-list-item-title>{{value}}</v-list-item-title>
            <v-list-item-subtitle>{{getText(key)}}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-card-text>
    </v-expand-transition>
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
  import { mapState, mapActions } from 'vuex'

  export default Vue.extend({
    name: 'Messung',
    data: () =>{ 
      return {
        loaded: false,
        item: {},
        except: [
          'data',
          'start'
        ]
    }},
    computed: {
      ...mapState(['loading','headers']),
      itemExcept() {
        return null // Hier weitermachen 
      }
    },
    methods: {
      ...mapActions(['getData']),
      getText(key) {
        try {
          return this.headers.find(e => e.value === key).text
        } catch (e) {
          return key
        }
      }
    },
    async mounted() {
      this.loaded=false
      this.item = await this.getData('measurements/'+String(this.$route.params.id))
      this.loaded=true
    }
  })
</script>

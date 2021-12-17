<template>
  <v-card
    :loading="loading"
  >
    <v-toolbar>
      <v-spacer></v-spacer>
        <v-toolbar-title>
          {{item.name}}
        </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <div v-show="loaded">
      <v-card-text class="pa-4">
        <v-text-field
            v-for="value,key in itemExcept" :key="key"
            :label="getText(key)"
            :value="value"
            :disabled="value === null"
            readonly
            outlined
          ></v-text-field>
      </v-card-text>
    <v-card-actions class="justify-end">
       <v-btn
        text
        :href="gotoApi()"
        target="_blank"
      >API call</v-btn>
      <v-btn
        text
        @click="$router.go(-1)"
      >Schließen</v-btn>
    </v-card-actions>
  </div>
  <v-skeleton-loader
    v-if="!loaded"
    class="my-4"
    type="list-item@8, actions"
  />
  </v-card>
</template>

<script >
  import Vue from 'vue'
  import { mapState, mapActions } from 'vuex'

  export default Vue.extend({
    name: 'Messung',
    data: () =>{ 
      return {
        apiRouteBase: 'measurements',
        loaded: false,
        item: {},
        except: [
          'data',
          'start'
        ]
    }},
    computed: {
      ...mapState(['loading','headers']),
      apiRoute() {
        return this.apiRouteBase+'/'+String(this.$route.params.id)
      },
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
      ...mapActions(['getData']),
      getText(key) {
        try {
          return this.headers.find(e => e.value === key).text
        } catch (e) {
          return key
        }
      },
      gotoApi() {
        const ref = this.$store.state.apiUrl+this.apiRoute
        console.log(ref)
        return ref
      }
    },
    async mounted() {
      this.loaded=false
      this.item = await this.getData(this.apiRoute)
      this.loaded=true
    }
  })
</script>

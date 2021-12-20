<template>
  <SubView :loading="loading" :title="item.name">
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
    <v-card-actions class="justify-space-between">
      <v-btn
        text large fab
        color="red"
        @click="deleteData(apiRoute);$router.go(-1)"
      ><v-icon>mdi-delete</v-icon>
      </v-btn>
      <v-btn
        text large fab
        :href="gotoApi()"
        target="_blank"
      ><v-icon>mdi-cloud-braces</v-icon>
      </v-btn>
    </v-card-actions>
  </div>
  <v-skeleton-loader
    v-if="!loaded"
    class="my-4"
    type="list-item@8, actions"
  />
  </SubView>
</template>

<script >
  import Vue from 'vue'
  import SubView from '@/components/SubView'
  import { mapState, mapActions } from 'vuex'

  export default Vue.extend({
    name: 'Messung',
    components: {
      SubView
    },
    data: () =>{ 
      return {
        apiRouteBase: 'measurements',
        loaded: false,
        item: {},
        hide: [
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
          if (this.hide.indexOf(e) >= 0) continue
          newItem[e] = this.item[e]
        }
        return newItem
      }
    },
    methods: {
      ...mapActions(['getData','deleteData']),
      getText(key) {
        try {
          return this.headers.find(e => e.value === key).text
        } catch (e) {
          return key
        }
      },
      gotoApi() {
        const ref = this.$store.state.apiUrl+this.apiRoute
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

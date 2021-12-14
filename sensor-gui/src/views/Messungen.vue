<template>
  <div>
    <v-dialog
        max-width="600"
        :value="dialog"
        v-if="dialog"
        persistent
      >
        <router-view></router-view>
      </v-dialog>
    <v-card>
      <v-card-title>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Suche nach Messdaten"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="measurements"
        :items-per-page="15"
        :search="search"
        :loading="loading"
        class="elevation-1"
        @click:row="click_on_row"
      ></v-data-table>
      <!--<Messung />-->
    </v-card>
  </div>
</template>

<script>
  import Vue from 'vue'
  import { mapState, mapActions } from 'vuex'
  //import Messung from '../components/Messung.vue'

  export default Vue.extend({
    //name: 'Messungen',

    components: {
      //Messung,
    },
    data: () => {
      return {
        search: '',
        selectedItem: {
          name: ''
        },
        measurements: [],
      }
    },

    computed: {
      ...mapState(['loading','headers']),
      dialog() {
        return this.$route.name != 'Messungen'
      }
    },

    methods: {
      ...mapActions(['getData']),
      click_on_row(item) {
        this.selectedItem = item
        this.$router.push({ name: 'Messung', params: { id: item.id }})
      },
      async get_and_transform_data(route) {
        const data = await this.getData(route)
        return Object.keys(data).map(id => Object.assign({id:id},data[id]))
      }
    },

    async mounted() {
      this. measurements = await this.get_and_transform_data('measurements')
    }
  })
</script>

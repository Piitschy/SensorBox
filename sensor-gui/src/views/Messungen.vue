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
          hide-details
        ></v-text-field>

        <v-btn 
          class="ml-4"
          color="primary"
          @click="reload"
        >
          <v-icon>mdi-refresh</v-icon>
        </v-btn>

        <v-btn 
          class="ml-4"
          color="primary"
          @click="$router.push({ name: 'NewMessung'})"
        >
          <v-icon>mdi-playlist-plus</v-icon>
        </v-btn>
        
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="measurements"
        :items-per-page="15"
        :search="search"
        :loading="loadingAnimation"
        loading-text="Lade..."
        class="elevation-1"
        @click:row="click_on_row"
      ></v-data-table>
    </v-card>
  </div>
</template>

<script>
  import Vue from 'vue'
  import { mapState, mapActions } from 'vuex'

  export default Vue.extend({
    name: 'Messungen',
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
      },
      loadingAnimation() {
        return this.loading && this.measurements.length === 0
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
        const measurements = Object.keys(data).map(id => Object.assign({id:id},data[id]))
        this.measurements = measurements
        return measurements
      },
      reload() {
        this.get_and_transform_data('measurements')
      }
    },
    created() {
      this.reload()
    }
  })
</script>
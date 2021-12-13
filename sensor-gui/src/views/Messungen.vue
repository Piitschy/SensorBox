<template>
<div>
  <v-card>
    {{measurements}}
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
  //import Messung from '../components/Messung.vue'

  export default Vue.extend({
    //name: 'Messungen',

    components: {
      //Messung,
    },
    data: () => {
      return {
        search: '',
        loading: false,
        clickedItem: 'nix',
        headers: [
          {text: 'Namen', value: 'name'},
          {text: 'Sensor', value: 'sensor'},
          {text: 'Dauer [s]', value: 'duration'},
          {text: 'Rate [Hz]', value: 'rate'},
          {text: 'Datum', value: 'start_date'},
          {text: 'Zeit', value: 'start_time'},
        ],
        measurements: [],
      }
    },

    computed: {

    },

    methods: {
      async getData() {
        this.loading = true
        const response = await fetch('http://192.168.1.104:5000/measurements')
        const json = await response.json()
        const result = Object.keys(json.data).map(id => Object.assign({id:id},json.data[id]))
        this.loading = false
        return result
      },
      click_on_row(item) {
        this.clickedItem = item.name
      }
    },

    async mounted() {
      this. measurements = await this.getData()
    }

  })
</script>

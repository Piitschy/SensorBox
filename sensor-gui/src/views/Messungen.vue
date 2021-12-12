<template>
<div>
  {{measurements}}
  <v-data-table
    :headers="headers"
    :items="desserts"
    :items-per-page="15"
    class="elevation-1"
  ></v-data-table>
  <!--<Messung />-->
</div>
</template>

<script lang="ts">
  import Vue from 'vue'
  //import Messung from '../components/Messung.vue'

  export default Vue.extend({
    //name: 'Messungen',

    components: {
      //Messung,
    },
    data: () => {
      return {
        headers: [
          {text: 'Namen', value: 'name'},
          {text: 'Kalorien', value: 'calories'}
        ],
        measurements: [],
        desserts: [
          {
            name: 'Frozen Yogurt',
            calories: 159,
          },
          {
            name: 'Ice cream sandwich',
            calories: 237,
          }
        ],
      }
    },

    computed: {

    },

    methods: {
      async getData() {
        const response = await fetch('http://192.168.1.104:5000/measurements')
        this.measurements = response.json()
      }
    },

    async mounted() {
      await this.getData()
    }

  })
</script>

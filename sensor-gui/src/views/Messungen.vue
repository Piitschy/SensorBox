<template>
  <v-data-table
    :headers="headers"
    :items="desserts"
    :items-per-page="15"
    class="elevation-1"
  ></v-data-table>
  <!--<Messung />-->
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

    }

  })
</script>

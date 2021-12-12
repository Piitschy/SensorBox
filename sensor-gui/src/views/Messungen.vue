<template>
    <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">
            Name
          </th>
          <th class="text-left">
            Calories
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="item in desserts"
          :key="item.name"
        >
          <td>{{ item.name }}</td>
          <td>{{ item.calories }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
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

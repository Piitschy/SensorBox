<template>
  <v-container>
    <v-row class="text-center">
      Messung
      <!-- -->
    </v-row>
  </v-container>
</template>

<script lang="ts">
  import Vue from 'vue'

  export default Vue.extend({
    name: 'Messung',
    props: {
      name: {
        type: String,
        default: "Messung"
      },
      data: {
      }
    }
  })
</script>

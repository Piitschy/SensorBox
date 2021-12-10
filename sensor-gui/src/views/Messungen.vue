<template>
  <Messung />
</template>

<script lang="ts">
  import Vue from 'vue'
  import Messung from '../components/Messung.vue'

  export default Vue.extend({
    name: 'Messungen',

    components: {
      Messung,
    },
  })
</script>

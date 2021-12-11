<template>
  <div>
    <v-snackbar
        v-model="trigger"
        :timeout="payload.timeout+10"
        top
        :color="payload.color"
        class="mt-3"
      >
      <center>
        <v-icon left v-if="payload.icon">
          {{payload.icon}}
        </v-icon>
        {{payload.massage}}
      </center>
      <template v-slot:action="{ attrs }">
        <v-btn
          icon
          v-bind="attrs"
          @click="$store.commit('notification/reset')"
        >
          <v-icon small>
              mdi-close
            </v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'Notification',
  computed: mapState('notification', ['trigger', 'payload'])
}
</script>

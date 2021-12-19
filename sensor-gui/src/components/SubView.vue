<template>
  <v-card
    :loading="loading"
  >
    <v-toolbar>
      <v-spacer/>
        <v-toolbar-title>
          {{title}}
        </v-toolbar-title>
      <v-spacer/>
      <v-btn
        text
        fab
        @click="$router.go(-1)"
        absolute
      ><v-icon>mdi-window-close</v-icon>
      </v-btn>
    </v-toolbar>
    <div>
      <slot />
    </div>
  </v-card>
</template>

<script>
export default {
  name: 'SubView',
  props: {
    loading: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: null
    }
  }
}
</script>
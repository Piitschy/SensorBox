<template>
  <v-app>
    <Notification v-if="false" />
        <v-navigation-drawer
          v-model="drawer"
          app
          color="grey darken-2"
          dark
        >
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="title">
              {{ $route.meta.headline }}
            </v-list-item-title>
            <v-list-item-subtitle>
              Bitte auswählen
            </v-list-item-subtitle>
          </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list
        dense
        nav
      >
        <v-list-item v-for="route in routes" :key="route.path" :to="route">
          <v-list-item-icon>
            <v-icon>{{ route.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ route.name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="grey darken-4" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-spacer />
      <v-toolbar-title v-if="!drawer">{{ $route.meta.headline }}</v-toolbar-title>
      <v-spacer />
      <span v-if="pwa">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn  v-bind="attrs" v-on="on" icon @click="install"><v-icon>mdi-download</v-icon></v-btn>
          </template>
          <span>installieren</span>
        </v-tooltip>
      </span>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on" @click="infoSheet = true">
            <v-icon>mdi-information</v-icon>
          </v-btn>
        </template>
        <span>Info</span>
      </v-tooltip>
    </v-app-bar>

    <v-main>
      <div class="px-8 py-4">
        <router-view></router-view>
      </div>
    </v-main>

    <v-bottom-sheet v-model="infoSheet">
      <v-sheet
        class="text-center"
      >
        <div class="py-4">
          <div class="py-4" v-if="pwa">
            <v-btn @click="install" color="info"><v-icon>mdi-download</v-icon> installieren</v-btn>
          </div>
          <!--{{$route.meta.description.text}}-->
        </div>
      </v-sheet>
    </v-bottom-sheet>
    <!--
    <v-footer app>
    </v-footer>
    -->
  </v-app>
</template>

<script>
import Notification from '@/components/Notification.vue'

export default {
  name: 'App',
  components: {
    Notification
  },
  data: () => ({
    drawer: false,
    infoSheet: false,
    pwa: null
  }),
  computed: {
    routes () {
      return this.$router.options.routes.filter(route => !route.meta || !route.meta.hidden)
    }
  },
  methods: {
    async install () {
      this.pwa.prompt()
    }
  },
  created () {
    // PWA INSTALL
    window.addEventListener('beforeinstallprompt', e => {
      e.preventDefault()
      // Stash the event so it can be triggered later.
      this.pwa = e
    })
    window.addEventListener('appinstalled', () => {
      this.pwa = null
    })
    // iOS
    // Detects if device is on iOS
    const isIos = () => {
      const userAgent = window.navigator.userAgent.toLowerCase()
      return /iphone|ipad|ipod/.test(userAgent)
    }
    // Detects if device is in standalone mode
    const isInStandaloneMode = () => ('standalone' in window.navigator) && (window.navigator.standalone)

    // Checks if should display install popup notification:
    if (isIos() && !isInStandaloneMode()) {
      this.setState({ showInstallMessage: true })
    }
  }
}
</script>

<style>
/* Hide scrollbar for Chrome, Safari and Opera */
.scrollbar-hidden::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge add Firefox */
.scrollbar-hidden {
  -ms-overflow-style: none;
  scrollbar-width: none; /* Firefox */
}
</style>
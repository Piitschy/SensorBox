<template>
  <v-app>
    <Notification />
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
.icon {
  /*background: url('assets/logo.png');*/
  height: 20px;
  width: 20px;
  display: block;
  /* Other styles here */
}

.ribbon-wrapper-green {
  width: 85px;
  height: 88px;
  overflow: hidden;
  position: fixed;
  top: 56px;
  right: -1px;
  z-index: 1;
}

.ribbon-green {
  font: bold 15px Sans-Serif;
  color: #333;
  text-align: center;
  text-shadow: rgba(255,255,255,0.5) 0px 1px 0px;
    -webkit-transform: rotate(45deg);
    -moz-transform:    rotate(45deg);
    -ms-transform:     rotate(45deg);
    -o-transform:      rotate(45deg);
  position: relative;
  padding: 7px 0;
  left: -5px;
  top: 15px;
  width: 120px;
  background-color: #BFDC7A;
  background-image: -webkit-gradient(linear, left top, left bottom, from(#BFDC7A), to(#8EBF45));
  background-image: -webkit-linear-gradient(top, #BFDC7A, #8EBF45);
  background-image:    -moz-linear-gradient(top, #BFDC7A, #8EBF45);
  background-image:     -ms-linear-gradient(top, #BFDC7A, #8EBF45);
  background-image:      -o-linear-gradient(top, #BFDC7A, #8EBF45);
  color: #6a6340;
  -webkit-box-shadow: 0px 0px 3px rgba(0,0,0,0.3);
  -moz-box-shadow:    0px 0px 3px rgba(0,0,0,0.3);
  box-shadow:         0px 0px 3px rgba(0,0,0,0.3);
}

.ribbon-green:before, .ribbon-green:after {
  content: "";
  border-top:   3px solid #6e8900;
  border-left:  3px solid transparent;
  border-right: 3px solid transparent;
  position:absolute;
  bottom: -3px;
}

.ribbon-green:before {
  left: 0;
}
.ribbon-green:after {
  right: 0;
}
</style>
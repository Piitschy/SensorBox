<template>
  <SubView :loading="loading" title="Messung starten" arrow>
    <div class="pa-12">
      <div class="d-flex justify-center">
      <v-expand-transition>
      <v-card v-if="!started" class="mb-8 d-inline-flex pa-2" color="grey darken-3">
        <v-card-text class="d-flex justify-space-between">
          Geschätzte Dauer:&nbsp;<b>{{longestDuration}}&nbsp;s</b>
        </v-card-text>
      </v-card>
      </v-expand-transition>
      </div>
      <div class="d-flex justify-center">
      <v-btn
        :disabled="!ready"
        :class="ready ? 'pulse' : null"
        @click="start"
        x-large
        fab
        color="red"
        >{{ started && loading ? countDown : 'START' }}
      </v-btn>
      </div>
      <v-progress-linear
        :active="(started && loading) || finished"
        class="mt-10"
        v-model="progress"
      ></v-progress-linear>
    </div>
  </SubView>
</template>


<script >
import Vue from "vue";
import SubView from "@/components/SubView";
import { mapState, mapActions } from "vuex";
import { gsap } from "gsap";

export default Vue.extend({
  name: "StartMessung",
  components: {
    SubView,
  },
  data: () => {
    return {
      apiRoute: "measurements/schedule/start",
      ready: false,
      started: false,
      finished: false,
      scheduled: [],
      progress: 0,
      countDown: 0
    };
  },
  computed: {
    ...mapState(["loading"]),
    longestDuration() {
      var dur = 0
      if (this.scheduled.length > 0) {
        for (const e of this.scheduled) {
          const newDur = e.duration
          dur = newDur > dur ? newDur : dur
        }
      }
      return dur
    }
  },
  methods: {
    ...mapActions(["getData"]),
    start() {
      this.countDown = this.longestDuration
      this.started = true
      this. finished = false
      this.getData(this.apiRoute);
      this.countDownTimer()
      gsap.fromTo(
        this,
        { progress: 0 },
        { duration: this.longestDuration, progress: 100 }
      );
    },
    countDownTimer() {
      if (this.countDown > 0) {
        setTimeout(() => {
          this.countDown -= 1;
          this.countDownTimer();
        }, 1000);
      } else {
        this.started = false
        this.finished = true
        this.$store.commit('addRefresh')
      }
    },
    async refreshScheduled() {
      var scheduled = await this.getData("measurements/schedule");
      this.scheduled = scheduled
      this.ready = scheduled.length > 0;
    },
  },
  async mounted() {
    await this.refreshScheduled();
  },
});
</script>

<style scoped>
.pulse {
  display: block;
  cursor: pointer;
  animation: pulse 1s infinite;
}
.pulse:hover {
  animation: none;
}

@-webkit-keyframes pulse {
  0% {
    -webkit-box-shadow: 0 0 0 0 rgba(204, 44, 44, 0.4);
  }
  70% {
    -webkit-box-shadow: 0 0 0 20px rgba(204, 44, 44, 0);
  }
  100% {
    -webkit-box-shadow: 0 0 0 0 rgba(204, 44, 44, 0);
  }
}
@keyframes pulse {
  0% {
    -moz-box-shadow: 0 0 0 0 rgba(204, 44, 44, 0.4);
    box-shadow: 0 0 0 0 rgba(204, 44, 44, 0.4);
  }
  70% {
    -moz-box-shadow: 0 0 0 20px rgba(204, 44, 44, 0);
    box-shadow: 0 0 0 20px rgba(204, 44, 44, 0);
  }
  100% {
    -moz-box-shadow: 0 0 0 0 rgba(204, 44, 44, 0);
    box-shadow: 0 0 0 0 rgba(204, 44, 44, 0);
  }
}
</style>
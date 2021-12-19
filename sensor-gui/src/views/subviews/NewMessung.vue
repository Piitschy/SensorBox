<template>
  <SubView :loading="loading" title="Neue Messung planen">
    <v-expand-transition>
      <v-data-table
        v-if="ready"
        dense
        :headers="usedHeaders"
        :items="scheduled"
        item-key="sensor"
        hide-default-footer
        class="ma-5 elevation-2"
      ></v-data-table>
    </v-expand-transition>
    <v-card-text class="pa-4">
      <v-text-field
        v-for="h in usedHeaders"
        :key="h.value"
        v-model="body[h.value]"
        :label="h.text"
        :type="h.type"
        outlined
        clearable
        @input="cleanBody(h.value, h.type)"
      />
      <v-checkbox label="Demo" v-model="body.demo"></v-checkbox>
    </v-card-text>
    <v-fab-transition>
        <v-btn v-if="ready" class="mb-10 ml-1 pt-1 pl-1" color="red" fab left bottom dark absolute>
          <v-icon>mdi-playlist-play</v-icon>
        </v-btn>
      </v-fab-transition>
    <v-card-actions class="justify-end">
      <v-btn text large fab :disabled="!ready" @click="clearRequest"><v-icon>mdi-playlist-remove</v-icon></v-btn>
      <v-btn text large fab :disabled="!body.name" @click="putRequest"><v-icon>mdi-playlist-check</v-icon></v-btn>
    </v-card-actions>
    
  </SubView>
</template>

<script >
import Vue from "vue";
import SubView from '@/components/SubView'
import { mapState, mapActions } from "vuex";

export default Vue.extend({
  name: "Messung",
  components: {
      SubView
    },
  data: () => {
    return {
      apiRoute: "measurements/schedule",
      body: { demo: true },
      scheduled: [],
      hide: ["start_date", "start_time"],
    };
  },
  computed: {
    ...mapState(["loading", "headers", "sensors"]),
    usedHeaders() {
      var usedHeaders = [];
      for (const e of this.headers) {
        if (this.hide.includes(e.value)) continue;
        usedHeaders.push(e);
      }
      return usedHeaders;
    },
    sensorNames() {
      return this.sensors.map((e) => e.name);
    },
    ready() {
      return this.scheduled.length > 0;
    },
  },
  methods: {
    ...mapActions(["getData", "postData", "deleteData"]),
    async putRequest() {
      const data = {
        route: this.apiRoute,
        body: this.body,
      };
      await this.postData(data)
      await this.refreshScheduled()
    },
    async clearRequest() {
      await this.deleteData(this.apiRoute)
      await this.refreshScheduled()
    },
    cleanBody(k, type) {
      this.body[k] ?? delete this.body[k];
      if (type === "number") this.body[k] = Number(this.body[k]);
    },
    async refreshScheduled() {
      this.scheduled = await this.getData(this.apiRoute);
    },
  },
  async mounted() {
    this.refreshScheduled();
  },
});
</script>
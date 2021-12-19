<template>
  <v-card :loading="loading">
    <v-toolbar class="elevation-3">
      <v-spacer></v-spacer>
      <v-toolbar-title> Neue Messung planen </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-fab-transition>
        <v-btn v-if="ready" color="red" fab dark left bottom absolute>
          <v-icon large>mdi-record-rec</v-icon>
        </v-btn>
      </v-fab-transition>
    </v-toolbar>
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
    <v-card-actions class="justify-end">
      <v-btn text @click="putRequest">Planen</v-btn>
      <v-btn text @click="$router.go(-1)">Schließen</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script >
import Vue from "vue";
import { mapState, mapActions } from "vuex";

export default Vue.extend({
  name: "Messung",
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
    ...mapActions(["getData", "putData"]),
    async putRequest() {
      const data = {
        route: this.apiRoute,
        body: this.body,
      };
      await this.putData(data);
      await this.refreshScheduled();
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
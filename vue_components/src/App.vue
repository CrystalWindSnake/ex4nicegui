<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import ECharts from "./components/ECharts/ECharts.vue";


const data = {
  "xAxis": {
    "type": "category",
    "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  },
  "yAxis": { "type": "value" },
  "series": [{ "data": [120, 200, 150, 80, 70, 110, 130], "type": "bar" }],
}




</script>

<template>
  <div class="box">

    <div style="background-color: antiquewhite; grid-area: a;">xxx</div>

    <div style="grid-area: b;background: #8dd165;"></div>

    <ECharts :options="data" style="grid-area: c; border: 1px solid #000;"></ECharts>

    <div style="grid-area: d;background: #d16565;"></div>
    <div style=" grid-area: b;">

      <ECharts :options="data" style="height: 100%;width: 100%; border: 1px solid #000;"></ECharts>
    </div>
  </div>
</template>

<style scoped>
.box {
  min-width: 100vw;
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
<<<<<<< HEAD
  grid-template-rows: 1fr 1fr 1fr;
=======
>>>>>>> 004836b6f4002cc503d7a5eb09cdb101a440bbf7
  grid-template-areas:
    "a a"
    "b c"
    "d e";
}
</style>
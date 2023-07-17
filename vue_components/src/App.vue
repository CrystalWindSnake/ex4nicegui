<script setup lang="ts">
import DragZone from "./components/DragZone/DragZone.vue";

const draggableElementIds = [
  '1',
  '2',
  '3'
]


function onDrop(data) {
  console.log('onDrop', data);

}

</script>

<template>
  <input type="text" id="1">
  <input type="text" id="4" draggable="true">

  <div class="box" id="dragZone"></div>

  <DragZone dropZoneId="dragZone" :draggableElementIds="draggableElementIds" @dropUpdate="onDrop"></DragZone>
</template>

<style scoped>
.box {
  width: 20rem;
  height: 20rem;
  background: burlywood;
}

input {
  user-select: none;
}
</style>

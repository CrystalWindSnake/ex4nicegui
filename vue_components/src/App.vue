<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import DropZone from "./components/DropZone/DropZone.vue";


const dropZoneRef = ref(null)

onMounted(() => {

  dropZoneRef.value.apply('item1', 'aqua')
  dropZoneRef.value.apply('item2', 'red')

})

const keys = ref([] as string[])

function onDraggableKeysUpdated(e: { keys: string[] }) {
  console.log(e.keys);
  keys.value = e.keys
}

function close(key: string) {
  console.log('close');

  dropZoneRef.value.removeKey(key)
}

</script>

<template>
  <div class="box" id="dragZone">

    <div v-for="k in keys" :key="k" :style="{ 'width': '4rem', 'height': '4rem', 'background-color': k }"
      draggable="true"></div>

  </div>

  <DropZone dropZoneId="dragZone" ref="dropZoneRef" @onDraggableKeysUpdated="onDraggableKeysUpdated"></DropZone>


  <div id="item1" style="width: 4rem; height: 4rem; background-color: aqua;"></div>
  <div id="item2" style="width: 4rem; height: 4rem; background-color: red;"></div>
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
./components/DropZone/DragZone.vue
<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits(['change', 'mychange'])

defineProps<{ title: string }>()



const value = ref(0)


function handle_click() {
  value.value += 1
  emit('change', value.value)
  console.log('init mychange');
}

function handle_click_other() {
  emit('mychange', 'xx')
  console.log('init mychange');

}

function reset() {
  value.value = 0
  console.log('reset runned');

}

console.log('init counter');


defineExpose({
  reset
})

</script>

<template>
  <div>
    <button @click="handle_click">
      <strong>{{ title }}: {{ value }} * xxx 10</strong>
    </button>

    <button @click="handle_click_other">
      other
    </button>

  </div>
</template>

<style scoped></style>

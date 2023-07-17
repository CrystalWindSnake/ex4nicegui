<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useMouse, UseMouseOptions, UseMouseSourceType } from '@vueuse/core'

const props = defineProps<{ options?: UseMouseOptions }>()

const emits = defineEmits<{
    (event: 'update', params: { x: number, y: number, sourceType: UseMouseSourceType }): void
}>()

onMounted(() => {
    const { x, y, sourceType } = useMouse(props.options)

    watch([x, y, sourceType], ([x, y, sourceType]) => {
        emits('update', { x, y, sourceType })
    })
})


</script>

<template></template>


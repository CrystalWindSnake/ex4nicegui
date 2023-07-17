<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useDraggable, UseDraggableOptions } from '@vueuse/core'


const props = defineProps<{ elementId: string, options?: UseDraggableOptions }>()

const emits = defineEmits<{
    (event: 'update', params: { x: number, y: number, style: string }): void
    (event: 'isDraggingUpdate', params: { isDragging: boolean }): void
}>()


onMounted(() => {

    const el = document.getElementById(`c${props.elementId}`)

    // `style` will be a helper computed for `left: ?px; top: ?px;`
    const { x, y, style, isDragging } = useDraggable(el, props.options)


    watch([x, y, style], ([x, y, style]) => {
        emits('update', { x, y, style })
    })

    watch(isDragging, v => {
        emits('isDraggingUpdate', { isDragging: v })
    })

    // const rect = el!.getBoundingClientRect()
    // x.value = rect.x
    // y.value = rect.y
})


</script>

<template></template>


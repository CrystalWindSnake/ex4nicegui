<script setup lang="ts">
import { onMounted, ref, reactive, watch } from 'vue'
import { useEventListener } from "@vueuse/core";

const props = defineProps<{ dropZoneId: string, draggableElementIds?: string[] }>()
let draggedId: string | null = null



const emits = defineEmits<{
    (event: 'dropUpdate', params: { data: any[] }): void
}>()

const inBoxElementIds = reactive(new Set<string>())

watch(inBoxElementIds, (data) => {
    emits('dropUpdate', { data: Array.from(data) })
})

const draggableElementIds = reactive(new Set<string>())


watch(draggableElementIds, data => {
    data.forEach(id => {
        const source = document.getElementById(id)

        if (source) {
            source.setAttribute('draggable', 'true')

            useEventListener(source, 'dragstart', event => {
                draggedId = (event.target as HTMLElement).id;

            })

            useEventListener(source, 'dragend', _ => {
                draggedId = null
            })

        }
    })
})


function setDraggableElementId(id: string) {
    draggableElementIds.add(id)
}

defineExpose({
    setDraggableElementId
})

onMounted(() => {


    props.draggableElementIds?.forEach(id => {
        draggableElementIds.add(id)
    })

    const box = document.getElementById(props.dropZoneId)!


    useEventListener(box, 'dragover', (event) => {
        event.preventDefault();

        if (draggedId && props.draggableElementIds.includes(draggedId)) {
            event.preventDefault();

            return
        }

    });


    useEventListener(box, 'drop', (event) => {
        event.preventDefault();

        if (draggedId) {
            inBoxElementIds.add(draggedId)
        }
    });



})


</script>

<template></template>


<script setup lang="ts">
import { onMounted } from 'vue'
import { useEventListener } from "@vueuse/core";

const DATA_DRAG_ZONE_ATTR = 'data-drag-zone-id'
const DATA_DRAGGABLE_ATTR = 'data-draggable-key'


const props = defineProps<{ dropZoneId: string }>()

const emits = defineEmits<{
    (event: 'onDraggableKeysUpdated', params: { keys: string[] }): void
}>()

let currentDraggableItem = null as HTMLElement | null
const draggableElementIds = new Set<string>()
const inBoxKeys = new Set<string>()

function apply(draggableItemId: string, keyStr: string) {
    console.log('apply:', draggableItemId, keyStr);

    if (draggableElementIds.has(draggableItemId)) {
        return
    }


    const draggable = document.getElementById(draggableItemId)
    if (!draggable) {
        throw new Error(`not found draggable item[id = ${draggableItemId}]`);
    }

    draggable.setAttribute('draggable', 'true')
    draggable.setAttribute(DATA_DRAG_ZONE_ATTR, props.dropZoneId)
    draggable.setAttribute(DATA_DRAGGABLE_ATTR, keyStr)

    useEventListener(draggable, 'dragstart', _ => {
        currentDraggableItem = draggable
    })

    useEventListener(draggable, 'dragend', _ => {
        currentDraggableItem = null
    })


    draggableElementIds.add(draggableItemId)

}

function emitKeys() {
    emits('onDraggableKeysUpdated', { keys: Array.from(inBoxKeys.values()) })
}

function removeKey(key: string) {
    if (inBoxKeys.has(key)) {
        inBoxKeys.delete(key)
        emitKeys()
    }
}

defineExpose({
    apply,
    removeKey
})



onMounted(() => {


    const box = document.getElementById(props.dropZoneId)
    if (!box) {
        throw new Error(`not found drop zone[id = ${props.dropZoneId}]`);
    }


    useEventListener(box, 'dragover', (event) => {
        if (!currentDraggableItem) {
            return
        }

        if (props.dropZoneId !== currentDraggableItem.getAttribute(DATA_DRAG_ZONE_ATTR)) {
            return
        }

        if (!currentDraggableItem.hasAttribute(DATA_DRAGGABLE_ATTR)) {
            return
        }

        const keyStr = currentDraggableItem.getAttribute(DATA_DRAGGABLE_ATTR)!

        if (inBoxKeys.has(keyStr)) {
            return
        }

        event.preventDefault();



    });


    useEventListener(box, 'drop', (event) => {
        if (!currentDraggableItem) {
            return
        }

        event.preventDefault();

        const keyStr = currentDraggableItem.getAttribute(DATA_DRAGGABLE_ATTR)!
        if (!inBoxKeys.has(keyStr)) {
            inBoxKeys.add(keyStr)
            emitKeys()
        }
    });


})


</script>

<template></template>


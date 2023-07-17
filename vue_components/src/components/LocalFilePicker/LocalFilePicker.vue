<script setup lang="ts">
import { ref } from 'vue'


type TPath = {
    name: string
    modifyDate: string
    type: string
    size: string
}

const props = defineProps<{ title: string, currentPath: string, paths: TPath[] }>()

const emit = defineEmits(['selectPath'])

const currentPath = ref(props.currentPath)


</script>

<template>
    <div class="box">

        <div class="current-path">
            <input type="text" v-model.lazy="currentPath">
        </div>

        <div class="path-list">

            <div class="row" v-for="path in props.paths">

                <div class="name">{{ path.name }}</div>
                <div class="modify-date">{{ path.modifyDate }}</div>
                <div class="type">{{ path.type }}</div>
                <div class="size">{{ path.size }}</div>
            </div>

        </div>
    </div>
</template>

<style scoped lang="less">
.box {
    display: flex;
    flex-direction: column;
    gap: 0.5em;
    border: 1px solid #000;
    padding: 0.3em 0.5em;

    .current-path {
        width: 100%;
        padding: 0.3em 0.5em;

        input {
            width: 100%;
        }
    }

    .path-list {

        .row {
            display: flex;
            gap: 0.5em;
        }
    }
}
</style>

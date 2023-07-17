<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useEventListener, useResizeObserver } from "@vueuse/core";
import * as echarts from "echarts";



const emits = defineEmits(['chartClick'])

const props = defineProps<{
    options: {},
    theme?: string | object | undefined
}>()

const chartDiv = ref(null as unknown as HTMLDivElement)
onUnmounted(() => {
    echarts.dispose(chartDiv.value)
})

let chartIns: echarts.ECharts | null = null

onMounted(() => {
    chartIns = echarts.init(chartDiv.value, props.theme)
    chartIns.setOption(props.options)

    watch(() => props.options, opts => {
        chartIns?.setOption(opts)
    })

    chartIns.on('click', 'series', params => {
        emits('chartClick', params)
    })

    useEventListener('resize', () => {
        chartIns?.resize()
    })

    useResizeObserver(chartDiv, () => {
        chartIns?.resize()
    })


})

function updateOptions(option: {}, opts?: echarts.SetOptionOpts) {
    chartIns?.setOption(option, opts)
}

defineExpose({
    updateOptions
})



</script>

<template>
    <div class="echart-container relative w-full h-full">
        <div class="echart  w-full h-full" style="min-height: 30vh;min-width: 50rem;" ref="chartDiv">
        </div>
    </div>
</template>

<style scoped lang="less"></style>

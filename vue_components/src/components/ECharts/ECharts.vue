<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch, toRaw } from 'vue'
import { useEventListener, useResizeObserver } from "@vueuse/core";
import * as echarts from "echarts";



const emits = defineEmits(['chartClick', 'chartClickBlank'])

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

    chartIns.on('click', params => {
        emits('chartClick', params)
    })

    chartIns.getZr().on('click', function (event) {
        // 没有 target 意味着鼠标/指针不在任何一个图形元素上，它是从“空白处”触发的。
        if (!event.target) {
            emits('chartClickBlank')
        }
    });


    function chartResize() {
        chartIns?.resize()
    }

    useEventListener('resize', () => {
        chartResize()
    })

    useResizeObserver(chartDiv, () => {
        chartResize()
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
    <div class="echart-container relative">
        <div class="echart  w-full h-full" ref="chartDiv">
        </div>
    </div>
</template>

<style scoped lang="less"></style>

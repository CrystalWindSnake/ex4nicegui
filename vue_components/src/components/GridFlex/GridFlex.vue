<script setup lang="ts">
import { computed, effect, reactive, ref, watch, toRaw } from 'vue'
import { useBreakpoints, breakpointsQuasar } from '@vueuse/core'


type TProps = {
    normalStyles: Record<string, any>
    breakpointStyleMap: Record<any, any>
}

const props = defineProps<TProps>()


const breakpointStyleMap = computed(() => {

    return new Map(
        Object.entries(props.breakpointStyleMap)
    )
})


function useStylesWithBreakpoints() {
    const breakpoints = useBreakpoints({
        sm: 600,
        md: 1024,
        lg: 1440,
        xl: 1920
    })
    const xs = breakpoints.smaller('sm')
    const sm = breakpoints.between('sm', 'md')
    const md = breakpoints.between('md', 'lg')
    const lg = breakpoints.between('lg', 'xl')
    const xl = breakpoints.greaterOrEqual('xl')

    const lt_sm = breakpoints.smaller('sm')
    const lt_md = breakpoints.smaller('md')
    const lt_lg = breakpoints.smaller('lg')
    const lt_xl = breakpoints.smaller('xl')

    const gt_xs = breakpoints.greaterOrEqual('sm')
    const gt_sm = breakpoints.greaterOrEqual('md')
    const gt_md = breakpoints.greaterOrEqual('lg')
    const gt_lg = breakpoints.greaterOrEqual('xl')



    const kws = {
        'xs': xs,
        'sm': sm,
        'md': md,
        'lg': lg,
        'xl': xl,

        'lt-sm': lt_sm,
        'lt-md': lt_md,
        'lt-lg': lt_lg,
        'lt-xl': lt_xl,

        'gt-xs': gt_xs,
        'gt-sm': gt_sm,
        'gt-md': gt_md,
        'gt-lg': gt_lg,
    }

    const style = computed(() => {
        if (breakpointStyleMap.value.size === 0) {
            return props.normalStyles
        }

        for (const [breakpoint, refObj] of Object.entries(kws)) {
            if (refObj.value) {
                if (breakpointStyleMap.value.has(breakpoint)) {
                    return breakpointStyleMap.value.get(breakpoint)!
                }
            }
        }

        return props.normalStyles
    })

    return style
}

const currentStyle = useStylesWithBreakpoints()

// effect(() => {
//     console.log('style:', currentStyle.value);

// })

</script>

<template>
    <div class="grid" :style="currentStyle">
        <slot></slot>
    </div>
</template>


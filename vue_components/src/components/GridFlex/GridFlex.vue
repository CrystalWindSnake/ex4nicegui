<script setup lang="ts">
import { computed, effect, reactive, ref, watch, toRaw } from 'vue'
import { useBreakpoints, breakpointsTailwind } from '@vueuse/core'


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
    const breakpoints = useBreakpoints(breakpointsTailwind)
    const xs = breakpoints.smaller('sm')
    const sm = breakpoints.smaller('md')
    const md = breakpoints.smaller('lg')
    const lg = breakpoints.smaller('xl')
    const xl = breakpoints.smaller('2xl')
    const xxl = breakpoints['2xl']

    const kws = {
        'xs': xs,
        'sm': sm,
        'md': md,
        'lg': lg,
        'xl': xl,
        'xxl': xxl,
    }

    const style = computed(() => {
        console.log('breakpointStyleMap', breakpointStyleMap.value);
        if (breakpointStyleMap.value.size === 0) {
            return props.normalStyles
        }


        for (const [breakpoint, refObj] of Object.entries(kws)) {
            if (refObj.value) {
                console.log('bp targging', breakpoint, refObj.value);

                if (breakpointStyleMap.value.has(breakpoint)) {
                    console.log('trigg done:', breakpointStyleMap.value.get(breakpoint));

                    return breakpointStyleMap.value.get(breakpoint)!
                }
            }
        }

        return props.normalStyles
    })

    return style
}

const currentStyle = useStylesWithBreakpoints()

effect(() => {
    console.log('style:', currentStyle.value);

})

</script>

<template>
    <div class="grid" :style="currentStyle">
        <slot></slot>
    </div>
</template>


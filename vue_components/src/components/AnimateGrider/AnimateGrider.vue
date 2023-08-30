<script setup lang="ts">
import { computed, nextTick, ref } from 'vue'
import { gsap } from "gsap";
import { Flip } from "gsap/Flip";


type TAnimateOption = {
    duration: number
    ease: string
}

type TAnimationFinishParams = {
    id: number
    style: string
    resultProps: {
        opacity: number
    }
}


gsap.registerPlugin(Flip)

const emits = defineEmits<{
    (event: 'onAnimationFinish', params: TAnimationFinishParams): void
}>()

const props = withDefaults(defineProps<{
    columnsTemplate?: string,
    rowsTemplate?: string,
}>(), {
    columnsTemplate: 'repeat(10,1fr)',
    rowsTemplate: 'repeat(10,1fr)',
})

const boxStyles = computed(() => {
    return {
        'grid-template-columns': props.columnsTemplate,
        'grid-template-rows': props.rowsTemplate
    }
})

const boxRef = ref(null as HTMLElement | null)


function changePosition(id: number, elementType: string, gridTemplateStyle: string, opacity: number, animateOption: TAnimateOption,) {
    if (boxRef.value === null) {
        return
    }
    let target = null as HTMLElement | null

    const rid = `c${id}`

    if (elementType === 'Input') {
        const inputTag = boxRef.value.querySelector<HTMLElement>(`[list="${rid}-datalist"]`)
        target = inputTag?.closest(`[for="${inputTag.id}"]`)!
    } else {
        target = boxRef.value.querySelector<HTMLElement>(`#${rid}`)
    }

    if (target) {
        const state = Flip.getState(target, { props: 'opacity' })
        target.style.gridArea = gridTemplateStyle
        target.style.opacity = opacity.toString()

        nextTick(() => {
            Flip.from(state, {
                duration: animateOption.duration,
                ease: animateOption.ease,
                // fade: true,
                // absolute: true,
                onComplete: _ => {

                    emits('onAnimationFinish', {
                        id,
                        style: `grid-area:${gridTemplateStyle};opacity:${opacity}`,
                        resultProps: {
                            opacity
                        }
                    })
                }
            });
        })



    }
}

defineExpose({
    changePosition
})


</script>

<template>
    <div class="grid w-full" ref="boxRef" :style="boxStyles">
        <slot></slot>
    </div>
</template>

<style scoped></style>

<script setup lang="ts">
import { ref, watch } from "vue";
import { useDraggable, UseDraggableOptions } from "@vueuse/core";

const props = defineProps<{
  elementId: string | null;
  options?: UseDraggableOptions;
}>();

const emits = defineEmits<{
  (
    event: "update",
    params: {
      x: number;
      y: number;
      style: string;
      isFirst: boolean;
      isFinal: boolean;
    }
  ): void;
  (event: "isDraggingUpdate", params: { isDragging: boolean }): void;
}>();

const targetId = ref(props.elementId);

watch(targetId, (id) => {
  if (id) {
    apply(id);
  }
});

defineExpose({
  applyTargetId: (id: string) => {
    targetId.value = id;
  },
});

function apply(targetId: string) {
  const el = document.getElementById(`c${targetId}`);

  // `style` will be a helper computed for `left: ?px; top: ?px;`

  function onStart() {
    emits("update", {
      x: x.value,
      y: y.value,
      style: style.value,
      isFirst: true,
      isFinal: false,
    });
  }

  function onEnd() {
    emits("update", {
      x: x.value,
      y: y.value,
      style: style.value,
      isFirst: false,
      isFinal: true,
    });
  }

  const { x, y, style, isDragging } = useDraggable(el, {
    onStart,
    onEnd,
    ...props.options,
  });

  watch([x, y, style], ([x, y, style]) => {
    emits("update", { x, y, style, isFirst: false, isFinal: false });
  });

  watch(isDragging, (v) => {
    emits("isDraggingUpdate", { isDragging: v });
  });
}
</script>

<template></template>

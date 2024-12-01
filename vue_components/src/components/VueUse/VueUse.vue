<script setup lang="ts">
import { getMethod } from "./methodMap";
import * as types from "./types";
const props = defineProps<{ method: string; args: any[] }>();

const emit = defineEmits<{
  change: (args: types.emitArgs) => void;
}>();

const method = getMethod(props.method, props.args, emit);

defineExpose(method.getAllMethods());
</script>

<template></template>

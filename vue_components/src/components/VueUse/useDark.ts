import { watch } from "vue";
import { useDark, useToggle, UseDarkOptions } from "@vueuse/core";
import { MethodInfo } from "./methodMap";
import * as types from "./types";

export function initUseDark(
  options: UseDarkOptions,
  initValue: boolean,
  emit: types.emit
) {
  const isDark = useDark(options);
  isDark.value = initValue;

  const toggleDark = useToggle(isDark);
  const methodInfo = new MethodInfo();

  methodInfo.addMethod("toggleDark", (value?: boolean) => {
    if (isDark.value === value) {
      return;
    }

    if (value === null) {
      toggleDark();
      return;
    }

    toggleDark(value);
  });

  watch(isDark, (value) => {
    emit("change", {
      eventName: "isDark",
      value,
    });
  });

  return methodInfo;
}

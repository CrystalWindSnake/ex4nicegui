import { watch } from "vue";
import { useBreakpoints } from "@vueuse/core";
import { MethodInfo } from "./methodMap";
import * as types from "./types";
import { onSocketConnect } from "./utils";

export function initBreakpoints(
  points: Record<string, number>,
  emit: types.emit
) {
  const breakpoints = useBreakpoints(points);
  const active = breakpoints.active();

  const emitActiveWithMounted = () => {
    emit("change", {
      eventName: "activeWithMounted",
      value: active.value,
    });
  };

  const methodInfo = new MethodInfo();

  methodInfo.addMethod("active", () => active.value);
  methodInfo.addMethod(
    "between",
    (a: any, b: any) => breakpoints.between(a, b).value
  );

  methodInfo.addMethod(
    "betweenReactively",
    (a: string, b: string, eventName: string) => {
      const isBetween = breakpoints.between(a, b);

      watch(isBetween, (value) => {
        emit("change", {
          eventName,
          value,
        });
      });
    }
  );

  onSocketConnect(emitActiveWithMounted);

  watch(active, (value) => {
    emit("change", {
      eventName: "active",
      value,
    });

    emitActiveWithMounted();
  });
  return methodInfo;
}

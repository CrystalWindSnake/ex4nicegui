import { nextTick, ref, watch } from "vue";
import { useQRCode } from "@vueuse/integrations/useQRCode";
import { MethodInfo } from "./methodMap";
import * as types from "./types";
import { onSocketConnect } from "./utils";

export function initUseQRCode(text: string, emit: types.emit) {
  const content = ref(text);
  const qrcode = useQRCode(content);

  const methodInfo = new MethodInfo();
  methodInfo.addMethod("updateText", (text: string) => {
    content.value = text;
  });
  methodInfo.addMethod("getQRCode", () => qrcode.value);

  onSocketConnect(() => {
    emit("change", {
      eventName: "qrcode",
      value: qrcode.value,
    });
  });

  watch(qrcode, (code) => {
    emit("change", {
      eventName: "qrcode",
      value: code,
    });
  });

  return methodInfo;
}

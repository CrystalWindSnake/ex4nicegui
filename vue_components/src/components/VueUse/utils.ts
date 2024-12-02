import { nextTick } from "vue";

export function onSocketConnect(fn: () => void) {
  nextTick(() => {
    const socket = (window as any).socket;
    socket.on("connect", fn);
  });
}

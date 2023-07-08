const T = Vue.getCurrentScope
const H = Vue.onScopeDispose
const M = Vue.unref
const h = Vue.ref
const w = Vue.watch
const W = Vue.defineComponent
const X = Vue.onMounted
function Y(e) {
  return T() ? (H(e), !0) : !1;
}
function E(e) {
  return typeof e == "function" ? e() : M(e);
}
const C = typeof window < "u", L = () => {
};
function S(e) {
  var t;
  const n = E(e);
  return (t = n == null ? void 0 : n.$el) != null ? t : n;
}
const _ = C ? window : void 0;
function y(...e) {
  let t, n, s, r;
  if (typeof e[0] == "string" || Array.isArray(e[0]) ? ([n, s, r] = e, t = _) : [t, n, s, r] = e, !t)
    return L;
  Array.isArray(n) || (n = [n]), Array.isArray(s) || (s = [s]);
  const l = [], u = () => {
    l.forEach((c) => c()), l.length = 0;
  }, i = (c, f, m, d) => (c.addEventListener(f, m, d), () => c.removeEventListener(f, m, d)), a = w(
    () => [S(t), E(r)],
    ([c, f]) => {
      u(), c && l.push(
        ...n.flatMap((m) => s.map((d) => i(c, m, d, f)))
      );
    },
    { immediate: !0, flush: "post" }
  ), p = () => {
    a(), u();
  };
  return Y(p), p;
}
const D = {
  page: (e) => [e.pageX, e.pageY],
  client: (e) => [e.clientX, e.clientY],
  screen: (e) => [e.screenX, e.screenY],
  movement: (e) => e instanceof Touch ? null : [e.movementX, e.movementY]
};
function O(e = {}) {
  const {
    type: t = "page",
    touch: n = !0,
    resetOnTouchEnds: s = !1,
    initialValue: r = { x: 0, y: 0 },
    window: l = _,
    target: u = l,
    eventFilter: i
  } = e, a = h(r.x), p = h(r.y), c = h(null), f = typeof t == "function" ? t : D[t], m = (o) => {
    const v = f(o);
    v && ([a.value, p.value] = v, c.value = "mouse");
  }, d = (o) => {
    if (o.touches.length > 0) {
      const v = f(o.touches[0]);
      v && ([a.value, p.value] = v, c.value = "touch");
    }
  }, A = () => {
    a.value = r.x, p.value = r.y;
  }, x = i ? (o) => i(() => m(o), {}) : (o) => m(o), g = i ? (o) => i(() => d(o), {}) : (o) => d(o);
  return u && (y(u, "mousemove", x, { passive: !0 }), y(u, "dragover", x, { passive: !0 }), n && t !== "movement" && (y(u, "touchstart", g, { passive: !0 }), y(u, "touchmove", g, { passive: !0 }), s && y(u, "touchend", A, { passive: !0 }))), {
    x: a,
    y: p,
    sourceType: c
  };
}
const B = /* @__PURE__ */ W({
  __name: "UseMouse",
  props: {
    options: null
  },
  emits: ["update"],
  setup(e, { emit: t }) {
    const n = e;
    return X(() => {
      const { x: s, y: r, sourceType: l } = O(n.options);
      w([s, r, l], ([u, i, a]) => {
        t("update", { x: u, y: i, sourceType: a });
      });
    }), (s, r) => null;
  }
});
export {
  B as default
};
const U = Vue.unref
const B = Vue.isRef
const N = Vue.toRefs
const T = Vue.customRef
const W = Vue.getCurrentScope
const X = Vue.onScopeDispose
const x = Vue.ref
const D = Vue.computed
const h = Vue.watch
const Y = Vue.defineComponent
const H = Vue.onMounted
function q(e) {
  return W() ? (X(e), !0) : !1;
}
function f(e) {
  return typeof e == "function" ? e() : U(e);
}
const I = typeof window < "u", z = () => {
};
var G = Object.defineProperty, J = Object.defineProperties, K = Object.getOwnPropertyDescriptors, E = Object.getOwnPropertySymbols, Q = Object.prototype.hasOwnProperty, Z = Object.prototype.propertyIsEnumerable, A = (e, t, r) => t in e ? G(e, t, { enumerable: !0, configurable: !0, writable: !0, value: r }) : e[t] = r, j = (e, t) => {
  for (var r in t || (t = {}))
    Q.call(t, r) && A(e, r, t[r]);
  if (E)
    for (var r of E(t))
      Z.call(t, r) && A(e, r, t[r]);
  return e;
}, k = (e, t) => J(e, K(t));
function R(e) {
  if (!B(e))
    return N(e);
  const t = Array.isArray(e.value) ? new Array(e.value.length) : {};
  for (const r in e.value)
    t[r] = T(() => ({
      get() {
        return e.value[r];
      },
      set(o) {
        if (Array.isArray(e.value)) {
          const a = [...e.value];
          a[r] = o, e.value = a;
        } else {
          const a = k(j({}, e.value), { [r]: o });
          Object.setPrototypeOf(a, e.value), e.value = a;
        }
      }
    }));
  return t;
}
function ee(e) {
  var t;
  const r = f(e);
  return (t = r == null ? void 0 : r.$el) != null ? t : r;
}
const F = I ? window : void 0;
function $(...e) {
  let t, r, o, a;
  if (typeof e[0] == "string" || Array.isArray(e[0]) ? ([r, o, a] = e, t = F) : [t, r, o, a] = e, !t)
    return z;
  Array.isArray(r) || (r = [r]), Array.isArray(o) || (o = [o]);
  const v = [], l = () => {
    v.forEach((i) => i()), v.length = 0;
  }, d = (i, p, s, g) => (i.addEventListener(p, s, g), () => i.removeEventListener(p, s, g)), u = h(
    () => [ee(t), f(a)],
    ([i, p]) => {
      l(), i && v.push(
        ...r.flatMap((s) => o.map((g) => d(i, s, g, p)))
      );
    },
    { immediate: !0, flush: "post" }
  ), y = () => {
    u(), l();
  };
  return q(y), y;
}
var te = Object.defineProperty, re = Object.defineProperties, ne = Object.getOwnPropertyDescriptors, S = Object.getOwnPropertySymbols, oe = Object.prototype.hasOwnProperty, ae = Object.prototype.propertyIsEnumerable, b = (e, t, r) => t in e ? te(e, t, { enumerable: !0, configurable: !0, writable: !0, value: r }) : e[t] = r, ie = (e, t) => {
  for (var r in t || (t = {}))
    oe.call(t, r) && b(e, r, t[r]);
  if (S)
    for (var r of S(t))
      ae.call(t, r) && b(e, r, t[r]);
  return e;
}, se = (e, t) => re(e, ne(t));
function le(e, t = {}) {
  var r, o;
  const {
    pointerTypes: a,
    preventDefault: v,
    stopPropagation: l,
    exact: d,
    onMove: u,
    onEnd: y,
    onStart: i,
    initialValue: p,
    axis: s = "both",
    draggingElement: g = F,
    handle: C = e
  } = t, c = x(
    (r = f(p)) != null ? r : { x: 0, y: 0 }
  ), _ = x(), P = (n) => a ? a.includes(n.pointerType) : !0, w = (n) => {
    f(v) && n.preventDefault(), f(l) && n.stopPropagation();
  }, V = (n) => {
    if (!P(n) || f(d) && n.target !== f(e))
      return;
    const m = f(e).getBoundingClientRect(), O = {
      x: n.clientX - m.left,
      y: n.clientY - m.top
    };
    (i == null ? void 0 : i(O, n)) !== !1 && (_.value = O, w(n));
  }, L = (n) => {
    if (!P(n) || !_.value)
      return;
    let { x: m, y: O } = c.value;
    (s === "x" || s === "both") && (m = n.clientX - _.value.x), (s === "y" || s === "both") && (O = n.clientY - _.value.y), c.value = {
      x: m,
      y: O
    }, u == null || u(c.value, n), w(n);
  }, M = (n) => {
    P(n) && _.value && (_.value = void 0, y == null || y(c.value, n), w(n));
  };
  if (I) {
    const n = { capture: (o = t.capture) != null ? o : !0 };
    $(C, "pointerdown", V, n), $(g, "pointermove", L, n), $(g, "pointerup", M, n);
  }
  return se(ie({}, R(c)), {
    position: c,
    isDragging: D(() => !!_.value),
    style: D(
      () => `left:${c.value.x}px;top:${c.value.y}px;`
    )
  });
}
const pe = /* @__PURE__ */ Y({
  __name: "UseDraggable",
  props: {
    elementId: null,
    options: null
  },
  emits: ["update", "isDraggingUpdate"],
  setup(e, { emit: t }) {
    const r = e;
    return H(() => {
      const o = document.getElementById(`c${r.elementId}`);
      function a() {
        t("update", { x: l.value, y: d.value, style: u.value, isFirst: !0, isFinal: !1 });
      }
      function v() {
        t("update", {
          x: l.value,
          y: d.value,
          style: u.value,
          isFirst: !1,
          isFinal: !0
        });
      }
      const { x: l, y: d, style: u, isDragging: y } = le(o, { onStart: a, onEnd: v, ...r.options });
      h([l, d, u], ([i, p, s]) => {
        t("update", { x: i, y: p, style: s, isFirst: !1, isFinal: !1 });
      }), h(y, (i) => {
        t("isDraggingUpdate", { isDragging: i });
      });
    }), (o, a) => null;
  }
});
export {
  pe as default
};
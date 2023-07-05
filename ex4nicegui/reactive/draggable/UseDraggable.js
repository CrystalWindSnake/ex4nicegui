const B = Vue.unref
const N = Vue.isRef
const T = Vue.toRefs
const W = Vue.customRef
const X = Vue.getCurrentScope
const Y = Vue.onScopeDispose
const D = Vue.ref
const x = Vue.computed
const h = Vue.watch
const H = Vue.defineComponent
const q = Vue.onMounted
function z(e) {
  return X() ? (Y(e), !0) : !1;
}
function p(e) {
  return typeof e == "function" ? e() : B(e);
}
const I = typeof window < "u", F = () => {
};
var G = Object.defineProperty, J = Object.defineProperties, K = Object.getOwnPropertyDescriptors, E = Object.getOwnPropertySymbols, Q = Object.prototype.hasOwnProperty, Z = Object.prototype.propertyIsEnumerable, A = (e, r, t) => r in e ? G(e, r, { enumerable: !0, configurable: !0, writable: !0, value: t }) : e[r] = t, j = (e, r) => {
  for (var t in r || (r = {}))
    Q.call(r, t) && A(e, t, r[t]);
  if (E)
    for (var t of E(r))
      Z.call(r, t) && A(e, t, r[t]);
  return e;
}, k = (e, r) => J(e, K(r));
function R(e) {
  if (!N(e))
    return T(e);
  const r = Array.isArray(e.value) ? new Array(e.value.length) : {};
  for (const t in e.value)
    r[t] = W(() => ({
      get() {
        return e.value[t];
      },
      set(o) {
        if (Array.isArray(e.value)) {
          const a = [...e.value];
          a[t] = o, e.value = a;
        } else {
          const a = k(j({}, e.value), { [t]: o });
          Object.setPrototypeOf(a, e.value), e.value = a;
        }
      }
    }));
  return r;
}
function ee(e) {
  var r;
  const t = p(e);
  return (r = t == null ? void 0 : t.$el) != null ? r : t;
}
const C = I ? window : void 0;
function $(...e) {
  let r, t, o, a;
  if (typeof e[0] == "string" || Array.isArray(e[0]) ? ([t, o, a] = e, r = C) : [r, t, o, a] = e, !r)
    return F;
  Array.isArray(t) || (t = [t]), Array.isArray(o) || (o = [o]);
  const c = [], g = () => {
    c.forEach((i) => i()), c.length = 0;
  }, _ = (i, y, s, v) => (i.addEventListener(y, s, v), () => i.removeEventListener(y, s, v)), l = h(
    () => [ee(r), p(a)],
    ([i, y]) => {
      g(), i && c.push(
        ...t.flatMap((s) => o.map((v) => _(i, s, v, y)))
      );
    },
    { immediate: !0, flush: "post" }
  ), f = () => {
    l(), g();
  };
  return z(f), f;
}
var re = Object.defineProperty, te = Object.defineProperties, ne = Object.getOwnPropertyDescriptors, b = Object.getOwnPropertySymbols, oe = Object.prototype.hasOwnProperty, ae = Object.prototype.propertyIsEnumerable, S = (e, r, t) => r in e ? re(e, r, { enumerable: !0, configurable: !0, writable: !0, value: t }) : e[r] = t, ie = (e, r) => {
  for (var t in r || (r = {}))
    oe.call(r, t) && S(e, t, r[t]);
  if (b)
    for (var t of b(r))
      ae.call(r, t) && S(e, t, r[t]);
  return e;
}, se = (e, r) => te(e, ne(r));
function le(e, r = {}) {
  var t, o;
  const {
    pointerTypes: a,
    preventDefault: c,
    stopPropagation: g,
    exact: _,
    onMove: l,
    onEnd: f,
    onStart: i,
    initialValue: y,
    axis: s = "both",
    draggingElement: v = C,
    handle: V = e
  } = r, u = D(
    (t = p(y)) != null ? t : { x: 0, y: 0 }
  ), d = D(), P = (n) => a ? a.includes(n.pointerType) : !0, w = (n) => {
    p(c) && n.preventDefault(), p(g) && n.stopPropagation();
  }, L = (n) => {
    if (!P(n) || p(_) && n.target !== p(e))
      return;
    const m = p(e).getBoundingClientRect(), O = {
      x: n.clientX - m.left,
      y: n.clientY - m.top
    };
    (i == null ? void 0 : i(O, n)) !== !1 && (d.value = O, w(n));
  }, M = (n) => {
    if (!P(n) || !d.value)
      return;
    let { x: m, y: O } = u.value;
    (s === "x" || s === "both") && (m = n.clientX - d.value.x), (s === "y" || s === "both") && (O = n.clientY - d.value.y), u.value = {
      x: m,
      y: O
    }, l == null || l(u.value, n), w(n);
  }, U = (n) => {
    P(n) && d.value && (d.value = void 0, f == null || f(u.value, n), w(n));
  };
  if (I) {
    const n = { capture: (o = r.capture) != null ? o : !0 };
    $(V, "pointerdown", L, n), $(v, "pointermove", M, n), $(v, "pointerup", U, n);
  }
  return se(ie({}, R(u)), {
    position: u,
    isDragging: x(() => !!d.value),
    style: x(
      () => `left:${u.value.x}px;top:${u.value.y}px;`
    )
  });
}
const pe = /* @__PURE__ */ H({
  __name: "UseDraggable",
  props: {
    elementId: null,
    options: null
  },
  emits: ["update", "isDraggingUpdate"],
  setup(e, { emit: r }) {
    const t = e;
    return q(() => {
      const o = document.getElementById(t.elementId), { x: a, y: c, style: g, isDragging: _ } = le(o, t.options);
      h([a, c, g], ([l, f, i]) => {
        r("update", { x: l, y: f, style: i });
      }), h(_, (l) => {
        r("isDraggingUpdate", { isDragging: l });
      });
    }), (o, a) => null;
  }
});
export {
  pe as default
};
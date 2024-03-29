const T = Vue.unref
const U = Vue.isRef
const B = Vue.toRefs
const N = Vue.customRef
const W = Vue.getCurrentScope
const X = Vue.onScopeDispose
const D = Vue.ref
const E = Vue.computed
const x = Vue.watch
const Y = Vue.defineComponent
const H = Vue.onMounted
function q(e) {
  return W() ? (X(e), !0) : !1;
}
function v(e) {
  return typeof e == "function" ? e() : T(e);
}
const F = typeof window < "u", z = () => {
};
var G = Object.defineProperty, J = Object.defineProperties, K = Object.getOwnPropertyDescriptors, A = Object.getOwnPropertySymbols, Q = Object.prototype.hasOwnProperty, Z = Object.prototype.propertyIsEnumerable, I = (e, r, t) => r in e ? G(e, r, { enumerable: !0, configurable: !0, writable: !0, value: t }) : e[r] = t, j = (e, r) => {
  for (var t in r || (r = {}))
    Q.call(r, t) && I(e, t, r[t]);
  if (A)
    for (var t of A(r))
      Z.call(r, t) && I(e, t, r[t]);
  return e;
}, k = (e, r) => J(e, K(r));
function R(e) {
  if (!U(e))
    return B(e);
  const r = Array.isArray(e.value) ? new Array(e.value.length) : {};
  for (const t in e.value)
    r[t] = N(() => ({
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
  const t = v(e);
  return (r = t == null ? void 0 : t.$el) != null ? r : t;
}
const C = F ? window : void 0;
function h(...e) {
  let r, t, o, a;
  if (typeof e[0] == "string" || Array.isArray(e[0]) ? ([t, o, a] = e, r = C) : [r, t, o, a] = e, !r)
    return z;
  Array.isArray(t) || (t = [t]), Array.isArray(o) || (o = [o]);
  const u = [], d = () => {
    u.forEach((i) => i()), u.length = 0;
  }, _ = (i, p, s, l) => (i.addEventListener(p, s, l), () => i.removeEventListener(p, s, l)), g = x(
    () => [ee(r), v(a)],
    ([i, p]) => {
      d(), i && u.push(
        ...t.flatMap((s) => o.map((l) => _(i, s, l, p)))
      );
    },
    { immediate: !0, flush: "post" }
  ), f = () => {
    g(), d();
  };
  return q(f), f;
}
var te = Object.defineProperty, re = Object.defineProperties, ne = Object.getOwnPropertyDescriptors, S = Object.getOwnPropertySymbols, oe = Object.prototype.hasOwnProperty, ae = Object.prototype.propertyIsEnumerable, b = (e, r, t) => r in e ? te(e, r, { enumerable: !0, configurable: !0, writable: !0, value: t }) : e[r] = t, ie = (e, r) => {
  for (var t in r || (r = {}))
    oe.call(r, t) && b(e, t, r[t]);
  if (S)
    for (var t of S(r))
      ae.call(r, t) && b(e, t, r[t]);
  return e;
}, se = (e, r) => re(e, ne(r));
function le(e, r = {}) {
  var t, o;
  const {
    pointerTypes: a,
    preventDefault: u,
    stopPropagation: d,
    exact: _,
    onMove: g,
    onEnd: f,
    onStart: i,
    initialValue: p,
    axis: s = "both",
    draggingElement: l = C,
    handle: P = e
  } = r, c = D(
    (t = v(p)) != null ? t : { x: 0, y: 0 }
  ), y = D(), w = (n) => a ? a.includes(n.pointerType) : !0, $ = (n) => {
    v(u) && n.preventDefault(), v(d) && n.stopPropagation();
  }, V = (n) => {
    if (!w(n) || v(_) && n.target !== v(e))
      return;
    const m = v(e).getBoundingClientRect(), O = {
      x: n.clientX - m.left,
      y: n.clientY - m.top
    };
    (i == null ? void 0 : i(O, n)) !== !1 && (y.value = O, $(n));
  }, L = (n) => {
    if (!w(n) || !y.value)
      return;
    let { x: m, y: O } = c.value;
    (s === "x" || s === "both") && (m = n.clientX - y.value.x), (s === "y" || s === "both") && (O = n.clientY - y.value.y), c.value = {
      x: m,
      y: O
    }, g == null || g(c.value, n), $(n);
  }, M = (n) => {
    w(n) && y.value && (y.value = void 0, f == null || f(c.value, n), $(n));
  };
  if (F) {
    const n = { capture: (o = r.capture) != null ? o : !0 };
    h(P, "pointerdown", V, n), h(l, "pointermove", L, n), h(l, "pointerup", M, n);
  }
  return se(ie({}, R(c)), {
    position: c,
    isDragging: E(() => !!y.value),
    style: E(
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
  setup(e, { expose: r, emit: t }) {
    const o = e;
    r({
      applyTargetId: (u) => {
        a(u);
      }
    });
    function a(u) {
      const d = document.getElementById(`c${u}`);
      function _() {
        t("update", {
          x: f.value,
          y: i.value,
          style: p.value,
          isFirst: !0,
          isFinal: !1
        });
      }
      function g() {
        t("update", {
          x: f.value,
          y: i.value,
          style: p.value,
          isFirst: !1,
          isFinal: !0
        });
      }
      const { x: f, y: i, style: p, isDragging: s } = le(d, {
        onStart: _,
        onEnd: g,
        ...o.options
      });
      x([f, i, p], ([l, P, c]) => {
        t("update", { x: l, y: P, style: c, isFirst: !1, isFinal: !1 });
      }), x(s, (l) => {
        t("isDraggingUpdate", { isDragging: l });
      });
    }
    return H(() => {
      o.elementId && a(o.elementId);
    }), (u, d) => null;
  }
});
export {
  pe as default
};
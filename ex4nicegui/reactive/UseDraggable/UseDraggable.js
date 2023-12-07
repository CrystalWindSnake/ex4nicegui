const U = Vue.unref
const B = Vue.isRef
const M = Vue.toRefs
const N = Vue.customRef
const W = Vue.getCurrentScope
const X = Vue.onScopeDispose
const D = Vue.ref
const E = Vue.computed
const w = Vue.watch
const Y = Vue.defineComponent
function H(e) {
  return W() ? (X(e), !0) : !1;
}
function v(e) {
  return typeof e == "function" ? e() : U(e);
}
const F = typeof window < "u", q = () => {
};
var z = Object.defineProperty, G = Object.defineProperties, J = Object.getOwnPropertyDescriptors, A = Object.getOwnPropertySymbols, K = Object.prototype.hasOwnProperty, Q = Object.prototype.propertyIsEnumerable, I = (e, r, t) => r in e ? z(e, r, { enumerable: !0, configurable: !0, writable: !0, value: t }) : e[r] = t, Z = (e, r) => {
  for (var t in r || (r = {}))
    K.call(r, t) && I(e, t, r[t]);
  if (A)
    for (var t of A(r))
      Q.call(r, t) && I(e, t, r[t]);
  return e;
}, j = (e, r) => G(e, J(r));
function k(e) {
  if (!B(e))
    return M(e);
  const r = Array.isArray(e.value) ? new Array(e.value.length) : {};
  for (const t in e.value)
    r[t] = N(() => ({
      get() {
        return e.value[t];
      },
      set(a) {
        if (Array.isArray(e.value)) {
          const o = [...e.value];
          o[t] = a, e.value = o;
        } else {
          const o = j(Z({}, e.value), { [t]: a });
          Object.setPrototypeOf(o, e.value), e.value = o;
        }
      }
    }));
  return r;
}
function R(e) {
  var r;
  const t = v(e);
  return (r = t == null ? void 0 : t.$el) != null ? r : t;
}
const C = F ? window : void 0;
function x(...e) {
  let r, t, a, o;
  if (typeof e[0] == "string" || Array.isArray(e[0]) ? ([t, a, o] = e, r = C) : [r, t, a, o] = e, !r)
    return q;
  Array.isArray(t) || (t = [t]), Array.isArray(a) || (a = [a]);
  const d = [], l = () => {
    d.forEach((i) => i()), d.length = 0;
  }, g = (i, u, s, c) => (i.addEventListener(u, s, c), () => i.removeEventListener(u, s, c)), _ = w(
    () => [R(r), v(o)],
    ([i, u]) => {
      l(), i && d.push(
        ...t.flatMap((s) => a.map((c) => g(i, s, c, u)))
      );
    },
    { immediate: !0, flush: "post" }
  ), y = () => {
    _(), l();
  };
  return H(y), y;
}
var ee = Object.defineProperty, te = Object.defineProperties, re = Object.getOwnPropertyDescriptors, S = Object.getOwnPropertySymbols, ne = Object.prototype.hasOwnProperty, ae = Object.prototype.propertyIsEnumerable, b = (e, r, t) => r in e ? ee(e, r, { enumerable: !0, configurable: !0, writable: !0, value: t }) : e[r] = t, oe = (e, r) => {
  for (var t in r || (r = {}))
    ne.call(r, t) && b(e, t, r[t]);
  if (S)
    for (var t of S(r))
      ae.call(r, t) && b(e, t, r[t]);
  return e;
}, ie = (e, r) => te(e, re(r));
function se(e, r = {}) {
  var t, a;
  const {
    pointerTypes: o,
    preventDefault: d,
    stopPropagation: l,
    exact: g,
    onMove: _,
    onEnd: y,
    onStart: i,
    initialValue: u,
    axis: s = "both",
    draggingElement: c = C,
    handle: m = e
  } = r, p = D(
    (t = v(u)) != null ? t : { x: 0, y: 0 }
  ), f = D(), $ = (n) => o ? o.includes(n.pointerType) : !0, h = (n) => {
    v(d) && n.preventDefault(), v(l) && n.stopPropagation();
  }, V = (n) => {
    if (!$(n) || v(g) && n.target !== v(e))
      return;
    const O = v(e).getBoundingClientRect(), P = {
      x: n.clientX - O.left,
      y: n.clientY - O.top
    };
    (i == null ? void 0 : i(P, n)) !== !1 && (f.value = P, h(n));
  }, L = (n) => {
    if (!$(n) || !f.value)
      return;
    let { x: O, y: P } = p.value;
    (s === "x" || s === "both") && (O = n.clientX - f.value.x), (s === "y" || s === "both") && (P = n.clientY - f.value.y), p.value = {
      x: O,
      y: P
    }, _ == null || _(p.value, n), h(n);
  }, T = (n) => {
    $(n) && f.value && (f.value = void 0, y == null || y(p.value, n), h(n));
  };
  if (F) {
    const n = { capture: (a = r.capture) != null ? a : !0 };
    x(m, "pointerdown", V, n), x(c, "pointermove", L, n), x(c, "pointerup", T, n);
  }
  return ie(oe({}, k(p)), {
    position: p,
    isDragging: E(() => !!f.value),
    style: E(
      () => `left:${p.value.x}px;top:${p.value.y}px;`
    )
  });
}
const ue = /* @__PURE__ */ Y({
  __name: "UseDraggable",
  props: {
    elementId: null,
    options: null
  },
  emits: ["update", "isDraggingUpdate"],
  setup(e, { expose: r, emit: t }) {
    const a = e, o = D(a.elementId);
    w(o, (l) => {
      l && d(l);
    }), r({
      applyTargetId: (l) => {
        o.value = l;
      }
    });
    function d(l) {
      const g = document.getElementById(`c${l}`);
      function _() {
        t("update", {
          x: i.value,
          y: u.value,
          style: s.value,
          isFirst: !0,
          isFinal: !1
        });
      }
      function y() {
        t("update", {
          x: i.value,
          y: u.value,
          style: s.value,
          isFirst: !1,
          isFinal: !0
        });
      }
      const { x: i, y: u, style: s, isDragging: c } = se(g, {
        onStart: _,
        onEnd: y,
        ...a.options
      });
      w([i, u, s], ([m, p, f]) => {
        t("update", { x: m, y: p, style: f, isFirst: !1, isFinal: !1 });
      }), w(c, (m) => {
        t("isDraggingUpdate", { isDragging: m });
      });
    }
    return (l, g) => null;
  }
});
export {
  ue as default
};